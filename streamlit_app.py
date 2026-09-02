import base64
import json
import mimetypes
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LG ROBO CARE | 로보킹 키우기",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stDecoration"],
      [data-testid="stSidebar"] {display:none!important;}
      #MainMenu, footer {visibility:hidden!important;}
      .stApp{
        background:
          radial-gradient(circle at 18% 10%,#fff9ec 0,transparent 30%),
          radial-gradient(circle at 88% 88%,#ead2a8 0,transparent 28%),
          #eee5d8;
      }
      .block-container{max-width:100%;padding:8px 4px 18px;}
      iframe{border:0!important;border-radius:28px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 맞춤 배터리 준비 결과 기록 연결부
# GitHub에는 아래 구조로 기록을 올리면 됩니다.
# data/home_model_predictions.csv
# data/zone_model_predictions.csv
#
# 사진첩 / 분실물 이미지 연결부 (시연용)
# assets/photos/        → 4번째 탭 "사진첩"에 표시되는 반려동물 사진 (png/jpg/jpeg/gif/webp)
# assets/lost_items/    → 4번째 탭 "오늘의 발견"의 분실물 사진 (없으면 이모지로 표시)
# 각 폴더에 선택적으로 captions.json 을 두면 파일명별 제목/장소/시간/설명을 지정할 수 있습니다.
#   { "cat1.jpg": {"title": "낮잠 자는 콩이", "place": "거실 소파", "time": "오늘 오후 1:20", "note": "햇살 아래에서 낮잠 중"} }
# captions.json 이 없으면 파일명(확장자 제외)이 제목으로 사용됩니다.
# 사진은 한 장당 1MB 이하로 줄여두면 로딩이 빠릅니다.
# ============================================================

BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"
HOME_PRED_PATH = DATA_DIR / "home_model_predictions.csv"
ZONE_PRED_PATH = DATA_DIR / "zone_model_predictions.csv"
ASSET_DIR = BASE_DIR / "assets"
PHOTO_DIR = ASSET_DIR / "photos"
LOST_DIR = ASSET_DIR / "lost_items"

# 데모용 현재 배터리. 실제 제품에서는 로봇/앱에서 받은 현재 배터리로 교체하면 됩니다.
CURRENT_SOC = 80

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def _folder_signature(folder: Path):
    """폴더 안 파일이 바뀌면 캐시가 자동으로 갱신되도록 시그니처를 만듭니다."""
    if not folder.exists():
        return "missing"
    parts = []
    for p in sorted(folder.iterdir()):
        try:
            parts.append(f"{p.name}:{p.stat().st_mtime_ns}:{p.stat().st_size}")
        except Exception:
            parts.append(p.name)
    return "|".join(parts)


@st.cache_data
def load_image_folder(folder_str: str, signature: str):
    folder = Path(folder_str)
    items = []
    if not folder.exists() or not folder.is_dir():
        return items
    captions = {}
    cap_path = folder / "captions.json"
    if cap_path.exists():
        try:
            captions = json.loads(cap_path.read_text(encoding="utf-8")) or {}
        except Exception:
            captions = {}
    for p in sorted(folder.iterdir()):
        if p.suffix.lower() not in IMAGE_EXTS:
            continue
        try:
            raw = p.read_bytes()
        except Exception:
            continue
        mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
        data = base64.b64encode(raw).decode("ascii")
        meta = captions.get(p.name) or captions.get(p.stem) or {}
        if not isinstance(meta, dict):
            meta = {"title": str(meta)}
        items.append({
            "name": p.name,
            "src": f"data:{mime};base64,{data}",
            "title": str(meta.get("title") or p.stem),
            "place": str(meta.get("place") or ""),
            "time": str(meta.get("time") or ""),
            "note": str(meta.get("note") or ""),
        })
    return items


def _is_valid(value):
    return value is not None and not pd.isna(value)


def _safe_text(row, candidates, default=""):
    if row is None:
        return default
    for col in candidates:
        if col in row.index and _is_valid(row[col]):
            return str(row[col])
    return default


def _safe_float(row, candidates, default=0.0):
    if row is None:
        return float(default)
    for col in candidates:
        if col in row.index and _is_valid(row[col]):
            try:
                return float(row[col])
            except Exception:
                pass
    return float(default)


def _soc_target(required_soc):
    return int(round(max(15, min(float(required_soc) + 15, 90))))


def _infer_mop(row, prefix=""):
    """cleaning_type 또는 cleaning_type_code 기반으로 물걸레 여부를 추정합니다."""
    text_candidates = [
        f"{prefix}cleaning_type" if prefix else "cleaning_type",
        "cleaning_type_first",
        "cleaning_type",
    ]
    code_candidates = [
        f"{prefix}cleaning_type_code" if prefix else "cleaning_type_code",
        "cleaning_type_code_first",
        "cleaning_type_code",
    ]

    txt = _safe_text(row, text_candidates, "").lower()
    if any(k in txt for k in ["물", "걸레", "mop", "wet"]):
        return True
    if any(k in txt for k in ["건식", "dry"]):
        return False

    code = _safe_float(row, code_candidates, 0)
    return int(round(code)) == 1


@st.cache_data
def load_prediction_csv(path: str):
    p = Path(path)
    if not p.exists():
        return None
    df = pd.read_csv(p)
    if "global_run_id" in df.columns:
        df["global_run_id"] = df["global_run_id"].astype(str)
    return df


def _make_demo_runs():
    runs = []
    for area in [18, 24, 33, 40, 48, 54, 60, 72]:
        for mop_enabled in [False, True]:
            base = area * 0.75 + (7 if mop_enabled else 0)
            zones = []
            floor_types = ["마루/타일", "저파일 러그", "장판/PVC", "현관매트", "고파일 카펫"]
            dirt_levels = ["낮음", "중간", "낮음", "높음", "중간"]
            weights = [0.18, 0.21, 0.17, 0.24, 0.20]
            for i, w in enumerate(weights, start=1):
                required = max(1.2, base * w)
                zones.append({
                    "scope": "zone",
                    "zone": i,
                    "label": f"{i}구역",
                    "globalRunId": f"demo_{area}_{'mop' if mop_enabled else 'dry'}",
                    "areaPyung": area,
                    "cleaningAreaM2": round(area * 3.3058 * 0.82 * w, 1),
                    "requiredSoc": round(required, 1),
                    "targetSoc": _soc_target(required),
                    "modelName": "RandomForest",
                    "cleaningType": "물걸레" if mop_enabled else "건식",
                    "cleaningTypeCode": 1 if mop_enabled else 0,
                    "mopEnabled": mop_enabled,
                    "obstacleLevel": "중간",
                    "obstacleLevelCode": 2,
                    "floorType": floor_types[i-1],
                    "dirtLevel": dirt_levels[i-1],
                    "dirtCode": 3 if dirt_levels[i-1] == "높음" else (2 if dirt_levels[i-1] == "중간" else 1),
                    "suctionMode": "자동",
                    "suctionCode": 2,
                })
            home_required = round(sum(z["requiredSoc"] for z in zones), 1)
            home = {
                "scope": "home",
                "label": "집 전체",
                "globalRunId": f"demo_{area}_{'mop' if mop_enabled else 'dry'}",
                "areaPyung": area,
                "cleaningAreaM2": int(round(area * 3.3058 * 0.82)),
                "requiredSoc": home_required,
                "targetSoc": _soc_target(home_required),
                "modelName": "XGBoost",
                "cleaningType": "물걸레" if mop_enabled else "건식",
                "cleaningTypeCode": 1 if mop_enabled else 0,
                "mopEnabled": mop_enabled,
                "obstacleLevel": "중간",
                "obstacleLevelCode": 2,
                "floorType": "혼합",
                "dirtLevel": "평균",
                "dirtCode": 2,
                "dirtMaxCode": 3,
                "suctionMode": "자동",
                "suctionCode": 2,
                "suctionMaxCode": 3,
            }
            runs.append({
                "globalRunId": home["globalRunId"],
                "areaPyung": area,
                "mopEnabled": mop_enabled,
                "cleaningType": home["cleaningType"],
                "home": home,
                "zones": zones,
            })
    return runs


def _build_home_scenario(home_row):
    required = _safe_float(
        home_row,
        ["best_pred_required_soc_pct", "pred_XGBoost", "pred_RandomForest", "home_required_soc_pct"],
        25,
    )
    target = _safe_float(
        home_row,
        ["best_pred_target_soc_pct", "home_target_soc_pct"],
        _soc_target(required),
    )
    mop_enabled = _infer_mop(home_row)
    cleaning_type = _safe_text(home_row, ["cleaning_type_first", "cleaning_type"], "물걸레" if mop_enabled else "건식")
    cleaning_type_code = int(round(_safe_float(home_row, ["cleaning_type_code_first", "cleaning_type_code"], 1 if mop_enabled else 0)))
    obstacle_code = _safe_float(home_row, ["obstacle_level_code_first", "obstacle_level_code"], 0)
    dirt_mean_code = _safe_float(home_row, ["dirt_level_code_mean", "dirt_level_code"], 0)
    dirt_max_code = _safe_float(home_row, ["dirt_level_code_max", "dirt_level_code"], dirt_mean_code)
    suction_mean_code = _safe_float(home_row, ["suction_mode_code_mean", "suction_mode_code"], 0)
    suction_max_code = _safe_float(home_row, ["suction_mode_code_max", "suction_mode_code"], suction_mean_code)
    return {
        "scope": "home",
        "label": "집 전체",
        "globalRunId": _safe_text(home_row, ["global_run_id"], ""),
        "areaPyung": int(round(_safe_float(home_row, ["area_pyung_first", "area_pyung"], 0))),
        "cleaningAreaM2": int(round(_safe_float(home_row, ["zone_area_m2_sum", "cleaning_area_m2"], 0))),
        "requiredSoc": round(float(required), 1),
        "targetSoc": int(round(max(15, min(float(target), 90)))),
        "modelName": _safe_text(home_row, ["best_model"], "XGBoost"),
        "cleaningType": cleaning_type,
        "cleaningTypeCode": cleaning_type_code,
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(home_row, ["obstacle_level_first", "obstacle_level"], ""),
        "obstacleLevelCode": round(float(obstacle_code), 3),
        "floorType": "혼합",
        "dirtLevel": "평균",
        "dirtCode": round(float(dirt_mean_code), 3),
        "dirtMaxCode": round(float(dirt_max_code), 3),
        "suctionMode": "자동",
        "suctionCode": round(float(suction_mean_code), 3),
        "suctionMaxCode": round(float(suction_max_code), 3),
    }


def _build_zone_scenario(zrow, idx, home):
    zone_no = int(round(_safe_float(zrow, ["zone"], idx)))
    required = _safe_float(
        zrow,
        ["best_pred_required_soc_pct", "pred_RandomForest", "pred_XGBoost", "zone_required_soc_pct"],
        max(home["requiredSoc"] / 5, 1),
    )
    mop_enabled = _infer_mop(zrow)
    cleaning_type = _safe_text(zrow, ["cleaning_type"], home.get("cleaningType", ""))
    cleaning_type_code = int(round(_safe_float(zrow, ["cleaning_type_code"], 1 if mop_enabled else 0)))
    obstacle_code = _safe_float(zrow, ["obstacle_level_code"], home.get("obstacleLevelCode", 0))
    dirt_code = _safe_float(zrow, ["dirt_level_code"], 0)
    suction_code = _safe_float(zrow, ["suction_mode_code"], 0)
    return {
        "scope": "zone",
        "zone": zone_no,
        "label": f"{zone_no}구역",
        "globalRunId": _safe_text(zrow, ["global_run_id"], home["globalRunId"]),
        "areaPyung": int(round(_safe_float(zrow, ["area_pyung", "area_pyung_first"], home["areaPyung"]))),
        "cleaningAreaM2": round(_safe_float(zrow, ["zone_area_m2"], 0), 1),
        "requiredSoc": round(float(required), 1),
        "targetSoc": _soc_target(required),
        "modelName": _safe_text(zrow, ["best_model"], "RandomForest"),
        "cleaningType": cleaning_type,
        "cleaningTypeCode": cleaning_type_code,
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(zrow, ["obstacle_level"], home.get("obstacleLevel", "")),
        "obstacleLevelCode": round(float(obstacle_code), 3),
        "floorType": _safe_text(zrow, ["floor_type"], ""),
        "dirtLevel": _safe_text(zrow, ["dirt_level"], ""),
        "dirtCode": round(float(dirt_code), 3),
        "suctionMode": _safe_text(zrow, ["effective_suction_mode"], ""),
        "suctionCode": round(float(suction_code), 3),
    }


def make_prediction_payload(home_df, zone_df):
    runs = []

    if home_df is not None and len(home_df) > 0:
        for _, hrow in home_df.iterrows():
            home = _build_home_scenario(hrow)
            gid = home["globalRunId"]
            zones = []

            if zone_df is not None and "global_run_id" in zone_df.columns and gid:
                zdf = zone_df[zone_df["global_run_id"].astype(str) == str(gid)].copy()
                if "zone" in zdf.columns:
                    zdf = zdf.sort_values("zone")
                for idx, (_, zrow) in enumerate(zdf.iterrows(), start=1):
                    zone = _build_zone_scenario(zrow, idx, home)
                    # home의 청소방식과 일관되게 표시
                    zone["cleaningType"] = home["cleaningType"]
                    zone["mopEnabled"] = home["mopEnabled"]
                    zones.append(zone)

            if len(zones) >= 1:
                runs.append({
                    "globalRunId": gid,
                    "areaPyung": home["areaPyung"],
                    "mopEnabled": home["mopEnabled"],
                    "cleaningType": home["cleaningType"],
                    "home": home,
                    "zones": zones,
                })

    # home 기록이 없고 zone 기록만 있을 때도 최소 동작하도록 처리
    if not runs and zone_df is not None and len(zone_df) > 0 and "global_run_id" in zone_df.columns:
        for gid, zdf in zone_df.groupby("global_run_id"):
            if len(zdf) < 1:
                continue
            if "zone" in zdf.columns:
                zdf = zdf.sort_values("zone")
            first = zdf.iloc[0]
            area = int(round(_safe_float(first, ["area_pyung"], 18)))
            mop_enabled = _infer_mop(first)
            dummy_required = 0
            dummy_home = {
                "scope": "home", "label": "집 전체", "globalRunId": str(gid), "areaPyung": area,
                "cleaningAreaM2": int(round(zdf["zone_area_m2"].sum())) if "zone_area_m2" in zdf.columns else 0,
                "requiredSoc": 0, "targetSoc": 15, "modelName": "XGBoost",
                "cleaningType": "물걸레" if mop_enabled else "건식", "cleaningTypeCode": 1 if mop_enabled else 0, "mopEnabled": mop_enabled,
                "obstacleLevel": _safe_text(first, ["obstacle_level"], ""), "obstacleLevelCode": _safe_float(first, ["obstacle_level_code"], 0), "floorType": "혼합",
                "dirtLevel": "평균", "dirtCode": 0, "dirtMaxCode": 0, "suctionMode": "자동", "suctionCode": 0, "suctionMaxCode": 0
            }
            zones = []
            for idx, (_, zrow) in enumerate(zdf.iterrows(), start=1):
                zone = _build_zone_scenario(zrow, idx, dummy_home)
                dummy_required += zone["requiredSoc"]
                zones.append(zone)
            dummy_home["requiredSoc"] = round(dummy_required, 1)
            dummy_home["targetSoc"] = _soc_target(dummy_required)
            runs.append({
                "globalRunId": str(gid), "areaPyung": area, "mopEnabled": mop_enabled,
                "cleaningType": dummy_home["cleaningType"], "home": dummy_home, "zones": zones
            })

    data_status = "csv" if runs else "demo"
    if not runs:
        runs = _make_demo_runs()

    area_options = sorted({r["areaPyung"] for r in runs if r.get("areaPyung")})
    mop_values = sorted({bool(r["mopEnabled"]) for r in runs})
    default_run = runs[0]

    return {
        "currentSoc": int(CURRENT_SOC),
        "runs": runs,
        "areaOptions": area_options,
        "mopOptions": mop_values,
        "defaultAreaPyung": default_run["areaPyung"],
        "defaultMopEnabled": bool(default_run["mopEnabled"]),
        "dataStatus": data_status,
    }


home_pred_df = load_prediction_csv(str(HOME_PRED_PATH))
zone_pred_df = load_prediction_csv(str(ZONE_PRED_PATH))
ui_prediction_data = make_prediction_payload(home_pred_df, zone_pred_df)
UI_PREDICTION_JSON = json.dumps(ui_prediction_data, ensure_ascii=False)

ui_media_data = {
    "photos": load_image_folder(str(PHOTO_DIR), _folder_signature(PHOTO_DIR)),
    "lostItems": load_image_folder(str(LOST_DIR), _folder_signature(LOST_DIR)),
}
UI_MEDIA_JSON = json.dumps(ui_media_data, ensure_ascii=False)

APP_HTML = r"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
  --brown:#4b3324;--brown2:#735139;--cream:#fff8e8;--green:#62aa49;
  --green2:#2f8b3a;--orange:#ff9535;--red:#ef4e45;--yellow:#ffd44f;
  --shadow:0 8px 18px rgba(72,44,20,.15)
}
html,body{margin:0;min-height:100%;font-family:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif;color:var(--brown);background:transparent}
body{display:flex;justify-content:center;align-items:flex-start;padding:8px}
button,input{font-family:inherit} button{cursor:pointer}
.phone{position:relative;width:min(100%,420px);height:960px;overflow:hidden;border:8px solid #242321;border-radius:40px;background:#dfb46b;box-shadow:0 30px 80px rgba(50,33,18,.28),0 8px 20px rgba(50,33,18,.16)}
.notch{position:absolute;z-index:100;top:0;left:50%;width:126px;height:25px;transform:translateX(-50%);border-radius:0 0 18px 18px;background:#242321}
.screen{position:relative;width:100%;height:100%;overflow:hidden;background:linear-gradient(180deg,#d2ab7b 0%,#e8c793 44%,#e1b36c 100%)}

/* Header */
.header{position:relative;z-index:50;height:128px;padding:23px 14px 8px;color:#fff;background:linear-gradient(120deg,#2d2722,#5b3f2d);box-shadow:0 7px 16px rgba(48,31,19,.22)}
.header-top{display:flex;justify-content:space-between;align-items:center}
.brand{font-size:9px;font-weight:900;letter-spacing:1.4px}
.app-title{margin-top:3px;font-size:23px;font-weight:900}
.coin-pill{display:flex;align-items:center;gap:5px;padding:8px 12px;border:1px solid rgba(255,255,255,.17);border-radius:18px;background:rgba(255,255,255,.13);font-size:12px;font-weight:900}
.nav{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:12px}
.nav-btn{padding:8px 3px;border:0;border-radius:14px;background:transparent;color:rgba(255,255,255,.72);font-size:10px;font-weight:900;transition:.2s}
.nav-btn.active{background:#4d291c;color:#fff;box-shadow:0 4px 9px rgba(0,0,0,.18)}
.nav-btn:active{transform:scale(.95)}

/* Pages */
.pages{position:relative;height:calc(100% - 128px);overflow:hidden}
.page{position:absolute;inset:0;display:none;overflow-y:auto;padding:12px 10px 24px;animation:pageIn .25s ease-out}
.page.active{display:block}.page::-webkit-scrollbar{width:0}
@keyframes pageIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:none}}
.section-kicker{color:#76533b;font-size:9px;font-weight:900;letter-spacing:1.3px}
.section-title{margin:2px 0 11px;font-size:22px;font-weight:900}
.panel{border:1px solid rgba(136,87,40,.14);border-radius:17px;background:rgba(255,248,231,.96);box-shadow:var(--shadow)}

/* Home */
#homePage{padding:0;background:linear-gradient(180deg,#cfaa7d 0%,#e0c39a 39%,#d29c58 40%,#d09850 100%)}
.room{position:relative;height:355px;overflow:hidden}
.wall-light{position:absolute;top:-80px;left:50%;width:420px;height:280px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(circle,rgba(255,248,226,.88),rgba(255,240,205,.18) 60%,transparent 74%)}
.floor{position:absolute;left:0;right:0;bottom:0;height:170px;background:repeating-linear-gradient(90deg,rgba(106,63,26,.1) 0,rgba(106,63,26,.1) 2px,transparent 2px,transparent 66px),repeating-linear-gradient(0deg,transparent 0,transparent 38px,rgba(106,63,26,.09) 39px,rgba(106,63,26,.09) 41px),linear-gradient(180deg,#d9b174,#c78e48)}
.plant{position:absolute;z-index:3;left:14px;top:70px;font-size:74px;filter:drop-shadow(0 7px 5px rgba(68,41,21,.18))}
.house{position:absolute;z-index:3;left:88px;top:128px;width:68px;height:58px;border-radius:29px 29px 7px 7px;background:linear-gradient(145deg,#a38b71,#74614d);box-shadow:0 6px 11px rgba(54,36,23,.22)}
.house:before{content:"";position:absolute;left:19px;bottom:0;width:31px;height:32px;border-radius:16px 16px 0 0;background:#403b35}
.house:after{content:"HOME";position:absolute;top:11px;left:16px;color:rgba(255,255,255,.56);font-size:7px;font-weight:900}
.sofa{position:absolute;z-index:2;right:-8px;top:72px;width:139px;height:105px;border-radius:28px 0 8px 8px;background:linear-gradient(145deg,#71847f,#354e4a);box-shadow:0 10px 14px rgba(54,37,23,.27)}
.sofa:before{content:"";position:absolute;top:-18px;left:10px;width:80px;height:48px;border-radius:17px 17px 7px 7px;background:#74867f}
.speech{position:absolute;z-index:20;top:17px;left:50%;width:177px;min-height:74px;padding:14px 12px;transform:translateX(-50%);border-radius:14px;background:rgba(255,255,255,.98);box-shadow:0 7px 16px rgba(58,37,21,.18);text-align:center;font-size:12px;line-height:1.55;font-weight:800}
.speech strong{color:var(--green);font-size:14px}
.speech:after{content:"";position:absolute;left:52%;bottom:-15px;border-width:16px 10px 0 4px;border-style:solid;border-color:white transparent transparent transparent}
.mode-chip{position:absolute;z-index:18;top:106px;left:50%;padding:7px 13px;transform:translateX(-50%);border-radius:18px;background:rgba(255,248,229,.95);box-shadow:0 4px 10px rgba(72,46,23,.16);font-size:9px;font-weight:900}
.rug{position:absolute;z-index:4;left:50%;bottom:12px;width:255px;height:92px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(ellipse,rgba(241,224,197,.91),rgba(191,151,103,.79));box-shadow:inset 0 0 18px rgba(103,70,43,.14)}
.clean-path{position:absolute;z-index:5;left:50%;bottom:41px;width:292px;height:78px;transform:translateX(-50%);overflow:hidden;border:2px dashed rgba(255,255,255,.36);border-radius:50%;opacity:0}
.clean-fill{width:0;height:100%;border-radius:inherit;background:linear-gradient(90deg,rgba(95,177,105,.08),rgba(102,200,115,.51));transition:width .3s}
.charge-ring{position:absolute;z-index:7;left:50%;bottom:19px;width:216px;height:132px;transform:translateX(-50%);border:5px solid transparent;border-top-color:#ffd345;border-right-color:#ff9931;border-radius:50%;opacity:0}
.dust{position:absolute;z-index:8;left:50%;bottom:55px;width:267px;height:75px;transform:translateX(-50%);pointer-events:none}
.dust span{position:absolute;bottom:0;width:7px;height:7px;border-radius:50%;background:rgba(116,78,42,.5);opacity:0}
.dust span:nth-child(1){left:8%}.dust span:nth-child(2){left:21%;animation-delay:.32s}.dust span:nth-child(3){left:37%;animation-delay:.68s}.dust span:nth-child(4){right:8%;animation-delay:.18s}.dust span:nth-child(5){right:23%;animation-delay:.52s}.dust span:nth-child(6){right:39%;animation-delay:.88s}
.robot{position:absolute;z-index:10;left:50%;bottom:31px;width:181px;height:99px;transform:translateX(-50%);transform-origin:center bottom;border:2px solid #a29b92;border-radius:62% 62% 40% 40%;background:linear-gradient(180deg,#fffefb 0%,#e7e8e3 70%,#bbbdb7 100%);box-shadow:0 13px 19px rgba(55,37,21,.32),inset 0 -8px 12px rgba(83,83,79,.12);cursor:pointer;animation:robotIdle 2.8s ease-in-out infinite}
.robot-top{position:absolute;left:50%;top:-5px;width:126px;height:58px;transform:translateX(-50%);border-top:2px solid rgba(119,119,114,.42);border-radius:50%;background:radial-gradient(ellipse at center,#fbfbf8 0%,#d5d6d2 74%,#b8b9b3 100%)}
.face{position:absolute;z-index:3;left:50%;bottom:8px;width:128px;height:54px;transform:translateX(-50%);border-radius:26px 26px 30px 30px;background:linear-gradient(180deg,#2a2c2d,#101213 76%);box-shadow:inset 0 4px 5px rgba(255,255,255,.13)}
.eye{position:absolute;top:14px;width:22px;height:22px;border:2px solid #f2f0dc;border-radius:50%;background:#111;transform-origin:center;animation:blink 4.8s infinite}
.eye:after{content:"";position:absolute;top:4px;left:5px;width:7px;height:7px;border-radius:50%;background:#fff;transition:transform .25s}
.eye.left{left:20px}.eye.right{right:20px}.robot.look-left .eye:after{transform:translateX(-4px)}.robot.look-right .eye:after{transform:translateX(4px)}
.cheek{position:absolute;bottom:8px;width:13px;height:6px;border-radius:50%;background:#ff8d8d;opacity:.75}.cheek.left{left:8px}.cheek.right{right:8px}
.mouth{position:absolute;left:50%;bottom:8px;width:20px;height:11px;transform:translateX(-50%);border:2px solid #f3d6c9;border-top:0;border-radius:0 0 12px 12px}
.crown{position:absolute;z-index:12;left:50%;top:-40px;transform:translateX(-50%);font-size:46px;filter:drop-shadow(0 4px 3px rgba(81,52,17,.25))}
.spark{position:absolute;z-index:11;right:-16px;top:-9px;font-size:28px;animation:sparkle 1.3s ease-in-out infinite}
.slot{position:absolute;left:50%;bottom:-2px;width:43px;height:5px;transform:translateX(-50%);border-radius:10px;background:#484a48}
.effect-layer{position:absolute;z-index:25;inset:0;overflow:hidden;pointer-events:none}.effect{position:absolute;left:50%;top:68%;font-size:20px;animation:effectFly 1.2s ease-out forwards}
.room.cleaning .mode-chip{color:#fff;background:rgba(57,143,82,.93)}.room.cleaning .clean-path{opacity:1}.room.cleaning .dust span{animation:dustRise 1.35s ease-out infinite}.room.cleaning .robot{animation:robotPatrol 2.4s ease-in-out infinite}
.room.charging .mode-chip{color:#fff;background:rgba(242,145,35,.94)}.room.charging .charge-ring{opacity:.92;animation:ringSpin 1.05s linear infinite}.room.charging .robot{animation:robotCharge .85s ease-in-out infinite}
.room.low .robot{animation:robotLow .48s linear infinite}.room.celebrate .robot{animation:robotCelebrate .72s ease-in-out 3}.robot.tap{animation:robotTap .62s ease-out!important}
.mission{position:absolute;z-index:16;left:8px;bottom:14px;width:90px;padding:9px 7px;border-radius:14px;background:rgba(255,248,230,.97);box-shadow:0 4px 10px rgba(61,39,20,.22)}
.mission-title{font-size:10px;font-weight:900}.mission-text{margin-top:5px;font-size:9px;line-height:1.4;font-weight:800}.mission-progress{display:flex;align-items:center;gap:4px;margin-top:8px}.mission-track{flex:1;height:7px;overflow:hidden;border-radius:10px;background:#c9b794}.mission-fill{width:0;height:100%;border-radius:inherit;background:linear-gradient(90deg,#ff8e33,#ffca43);transition:width .3s}.reward-small{color:#8d5814;font-size:9px;font-weight:900}
.quick{position:absolute;z-index:17;right:7px;top:89px;display:flex;flex-direction:column;gap:8px}.quick-btn{width:52px;min-height:51px;padding:4px 2px;border:0;border-radius:15px;background:rgba(255,248,231,.97);box-shadow:0 4px 10px rgba(61,39,20,.22);color:var(--brown);font-size:8px;font-weight:900}.quick-btn .icon{display:block;margin-bottom:3px;font-size:21px}
.home-dashboard{padding:9px 8px 15px;background:linear-gradient(180deg,rgba(239,205,151,.99),rgba(227,181,110,.99))}
.actions{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-bottom:8px;padding:8px 5px;border:1px solid rgba(138,91,40,.18);border-radius:14px;background:rgba(255,247,224,.94);box-shadow:0 4px 9px rgba(87,54,25,.15)}
.action-btn{min-width:0;padding:3px 0;border:0;background:transparent;color:var(--brown);font-size:8px;font-weight:900}.action-icon{display:block;margin-bottom:4px;font-size:23px}
.home-cards{display:grid;grid-template-columns:1.16fr 1fr .78fr;gap:6px}.mini-card{min-height:186px;padding:11px 9px;border:1px solid rgba(139,92,39,.17);border-radius:14px;background:rgba(255,248,230,.97);box-shadow:0 4px 10px rgba(79,48,21,.12)}
.mini-title{margin-bottom:8px;font-size:10px;font-weight:900}.battery-info{font-size:9px;line-height:1.55;font-weight:800}.battery-face{margin:7px 0 5px;text-align:center;font-size:31px}
.scale{position:relative;height:7px;margin:18px 7px 14px;border-radius:10px;background:linear-gradient(90deg,#f15b44 0%,#ffd25c 44%,#76ad51 100%)}.pointer{position:absolute;top:-7px;left:81%;width:14px;height:14px;transform:translateX(-50%);border:3px solid #fff;border-radius:50%;background:#e64c39;box-shadow:0 2px 5px rgba(0,0,0,.23);transition:left .3s}
.scale-labels{display:flex;justify-content:space-between;font-size:7px;font-weight:900}.battery-message{margin-top:10px;padding:7px;border-radius:9px;background:#f1e4c6;font-size:8px;line-height:1.45;font-weight:800}
.time-card{text-align:center}.time-icon{margin-top:10px;font-size:31px;animation:float 2s ease-in-out infinite}.time-number{color:#ef573f;font-size:32px;line-height:1;font-weight:900}.time-number small{font-size:12px}.time-sub{margin-top:4px;font-size:8px;font-weight:800}.time-tip{margin-top:15px;padding:7px 5px;border-radius:9px;background:#fff0ca;color:#745431;font-size:8px;line-height:1.45;font-weight:800}
.food-card{display:flex;flex-direction:column;align-items:center;justify-content:space-between}.food-title{width:100%;font-size:10px;font-weight:900}.food-bowl{position:relative;width:64px;height:42px;margin:26px auto 10px;border-radius:6px 6px 25px 25px;background:linear-gradient(180deg,#d84849,#ad2e36);box-shadow:0 7px 8px rgba(81,37,25,.2),inset 0 -7px 8px rgba(83,12,22,.14)}
.food-bowl:before{content:"";position:absolute;left:4px;top:-9px;width:56px;height:19px;border:4px solid #d54749;border-radius:50%;background:radial-gradient(circle at 30% 35%,#f1ab36 0 4px,transparent 5px),radial-gradient(circle at 60% 45%,#d57d24 0 5px,transparent 6px),radial-gradient(circle at 78% 30%,#f3c248 0 4px,transparent 5px),#944827}.food-bowl:after{content:"⚡";position:absolute;left:50%;top:10px;transform:translateX(-50%);color:#ffd542;font-size:20px;font-weight:900}.food-count{font-size:9px;font-weight:900}


/* 맞춤 배터리 Plan Selector */
.plan-panel{margin-bottom:8px;padding:11px 10px;background:rgba(255,248,231,.98)}
.plan-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.plan-title{font-size:11px;font-weight:900}.plan-model{padding:4px 7px;border-radius:11px;background:#eaf4df;color:#367b36;font-size:8px;font-weight:900}
.scope-buttons{display:grid;grid-template-columns:1.05fr repeat(5,1fr);gap:5px;margin-bottom:8px}
.scope-btn{min-height:37px;padding:5px 2px;border:1px solid rgba(124,83,43,.16);border-radius:12px;background:#f3e2be;color:#5a412e;font-size:8px;font-weight:900;line-height:1.2;box-shadow:0 3px 7px rgba(69,43,20,.09)}
.scope-btn.active{background:linear-gradient(180deg,#65ae4b,#368e3d);color:#fff;border-color:transparent;box-shadow:0 5px 12px rgba(47,139,58,.25)}
.learn-panel{position:relative;z-index:40;margin-bottom:8px;padding:9px;border-radius:13px;background:linear-gradient(145deg,#fff8df,#f3dfb2);border:1px solid rgba(124,83,43,.13)}.learn-top{display:flex;justify-content:space-between;align-items:center;gap:8px}.learn-title{font-size:10px;font-weight:900}.learn-pill{padding:4px 7px;border-radius:11px;background:#fff;color:#8b6139;font-size:8px;font-weight:900}.learn-desc{margin-top:5px;color:#6f4f38;font-size:8px;line-height:1.45;font-weight:800}.learn-progress{height:8px;margin-top:7px;overflow:hidden;border-radius:12px;background:#dcc79f}.learn-fill{width:0;height:100%;border-radius:inherit;background:linear-gradient(90deg,#62aa49,#ffd44f);transition:width .25s}.learn-status{margin-top:6px;font-size:8px;line-height:1.45;font-weight:900;color:#4b3324}.learn-steps{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-top:7px}.learn-step{padding:5px 4px;border-radius:9px;background:rgba(255,255,255,.58);color:#806047;font-size:7px;font-weight:900;text-align:center}.learn-step.done{background:#e7f4d9;color:#2f8b3a}.learn-step.active{background:#fff;color:#ef8c32;box-shadow:0 2px 6px rgba(89,56,26,.12)}.learn-btn{position:relative;z-index:80;pointer-events:auto!important;width:100%;min-height:34px;margin-top:7px;border:0;border-radius:11px;background:linear-gradient(90deg,#ef8c32,#ffb24b);color:#fff;font-size:10px;font-weight:900;box-shadow:0 5px 10px rgba(239,140,50,.22)}.learn-btn.ready{background:linear-gradient(90deg,#4a9b42,#75b84e)}.locked-area{opacity:.45;filter:grayscale(.15)}.condition-panel{margin-bottom:8px;padding:8px;border-radius:13px;background:#fff2cf;border:1px solid rgba(124,83,43,.12)}
.condition-title{margin-bottom:7px;font-size:10px;font-weight:900;color:#6f4f38;line-height:1.4}
.condition-row{display:grid;grid-template-columns:.7fr 1fr .7fr 1fr;gap:6px;align-items:center}.condition-row label{font-size:9px;font-weight:900;color:#6c4a2f}.condition-select{width:100%;min-height:34px;border:1px solid rgba(124,83,43,.22);border-radius:10px;background:#fffaf0;color:#4b3324;font-size:10px;font-weight:900;padding:0 7px}.predict-condition-grid{display:grid;grid-template-columns:.72fr 1fr .72fr 1fr;gap:6px;align-items:center;margin-top:8px}.predict-condition-grid label{font-size:9px;font-weight:900;color:#6c4a2f;white-space:nowrap}.condition-help{font-size:9px;line-height:1.5;color:#8a6a45;margin:7px 0 0;font-weight:800}.first-learn-note{padding:8px 9px;border-radius:11px;background:rgba(255,255,255,.58);font-size:10px;line-height:1.55;color:#6f4f38}.predict-btn{width:100%;min-height:36px;margin-top:8px;border:0;border-radius:11px;background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;font-size:11px;font-weight:900;box-shadow:0 5px 10px rgba(47,139,58,.2)}.predict-loading{margin-top:6px;min-height:18px;font-size:9px;line-height:1.45;color:#745431;font-weight:800}.predict-loading.active{color:#2f8b3a}
.selected-plan{display:grid;grid-template-columns:1fr .9fr;gap:7px;align-items:stretch}.plan-summary{padding:9px;border-radius:12px;background:#fff4d5;font-size:9px;line-height:1.55;font-weight:800}.plan-summary strong{color:#2f8b3a}.plan-soc{padding:9px;border-radius:12px;background:#f0e0be;text-align:center;font-weight:900}.plan-soc-label{font-size:8px;color:#79583e}.plan-soc-value{margin-top:2px;color:#ef573f;font-size:22px;line-height:1}.plan-soc-sub{margin-top:4px;font-size:8px;color:#76553e;line-height:1.35}.start-clean-primary{width:100%;min-height:46px;margin-top:9px;border:0;border-radius:14px;background:linear-gradient(90deg,#ef8c32,#f2a84d);color:#fff;font-size:13px;font-weight:950;letter-spacing:-.2px;box-shadow:0 7px 15px rgba(239,140,50,.26)}.start-clean-primary:disabled{opacity:.55;filter:grayscale(.12);box-shadow:none}.start-clean-primary small{display:block;margin-top:2px;font-size:9px;font-weight:800;color:rgba(255,255,255,.88)}

/* 공용 패널 헤더/기록 목록 (부품 케어 페이지에서 사용) */
.panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.panel-title{font-size:13px;font-weight:900}.badge{padding:5px 8px;border-radius:12px;background:#fff0ce;color:#805c35;font-size:8px;font-weight:900}
.events{margin-top:9px;padding:15px 14px}.event-item{display:grid;grid-template-columns:43px 1fr;gap:8px;padding:11px 0;border-bottom:1px solid rgba(122,87,51,.12)}.event-item:last-child{border-bottom:0}.event-time{color:#946c43;font-size:9px;font-weight:900}.event-content strong{display:block;margin-bottom:3px;font-size:10px}.event-content span{color:#785a43;font-size:9px;line-height:1.4;font-weight:700}

/* Reward */
.level-panel{padding:17px 15px;text-align:center;background:linear-gradient(145deg,#fff3cc,#ffd98a)}.level-robot{font-size:72px;animation:float 2s ease-in-out infinite}.level-number{margin-top:5px;font-size:25px;font-weight:900}.level-track{height:11px;margin:12px 10px 5px;overflow:hidden;border-radius:10px;background:rgba(126,85,39,.18)}.level-fill{width:55%;height:100%;border-radius:inherit;background:linear-gradient(90deg,#ff7f35,#ffd244)}.level-caption{font-size:9px;font-weight:900}
.reward-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}.reward-card{min-height:125px;padding:14px;border:1px solid rgba(136,87,40,.14);border-radius:16px;background:rgba(255,248,231,.97);box-shadow:var(--shadow);text-align:center}.reward-icon{font-size:38px}.reward-title{margin-top:7px;font-size:11px;font-weight:900}.reward-desc{margin-top:4px;color:#775943;font-size:8px;line-height:1.4;font-weight:800}.reward-btn{width:100%;margin-top:9px;padding:8px;border:0;border-radius:10px;background:#f0dfbc;color:#5c422f;font-size:9px;font-weight:900}

/* Modal */
.modal{position:absolute;z-index:200;inset:0;display:none;align-items:center;justify-content:center;padding:30px;background:rgba(45,33,23,.62);backdrop-filter:blur(4px)}.modal.show{display:flex}.modal-card{width:100%;padding:19px;border-radius:20px;background:#fff8e8;box-shadow:0 18px 45px rgba(28,19,12,.38);animation:popup .18s ease-out}.modal-title{font-size:18px;font-weight:900}.modal-body{margin:13px 0 17px;color:#6c513c;font-size:12px;line-height:1.65;font-weight:700}.modal-actions{display:grid;grid-template-columns:1fr 1fr;gap:9px}.modal-btn{width:100%;padding:11px;border:0;border-radius:12px;font-weight:900}.modal-secondary{background:#efe1c8;color:#5c422f}.modal-primary{background:#ef8c32;color:#fff}.modal-actions.single{grid-template-columns:1fr}.modal-actions.single .modal-secondary{display:none}
.toast{position:absolute;z-index:220;left:50%;bottom:25px;width:max-content;max-width:84%;padding:11px 17px;transform:translateX(-50%) translateY(30px);border-radius:18px;background:rgba(44,37,31,.95);color:#fff;font-size:11px;font-weight:800;opacity:0;pointer-events:none;transition:.25s}.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* Animations */
@keyframes robotIdle{0%,100%{transform:translateX(-50%) translateY(0) rotate(-1deg)}50%{transform:translateX(-50%) translateY(-7px) rotate(1deg)}}
@keyframes robotPatrol{0%{transform:translateX(calc(-50% - 67px)) rotate(-4deg)}50%{transform:translateX(calc(-50% + 67px)) rotate(4deg)}100%{transform:translateX(calc(-50% - 67px)) rotate(-4deg)}}
@keyframes robotCharge{0%,100%{transform:translateX(-50%) scale(1)}50%{transform:translateX(-50%) translateY(-4px) scale(1.04)}}
@keyframes robotLow{0%{transform:translateX(-50%) translateX(-2px)}50%{transform:translateX(-50%) translateX(2px)}100%{transform:translateX(-50%) translateX(-2px)}}
@keyframes robotCelebrate{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(-35px) rotate(-5deg)}75%{transform:translateX(-50%) translateY(-7px) rotate(5deg)}}
@keyframes robotTap{0%,100%{transform:translateX(-50%) scale(1)}45%{transform:translateX(-50%) scale(.92,1.08)}70%{transform:translateX(-50%) scale(1.08,.94)}}
@keyframes blink{0%,45%,49%,100%{transform:scaleY(1)}47%{transform:scaleY(.08)}}
@keyframes sparkle{0%,100%{transform:scale(.85) rotate(-10deg);opacity:.55}50%{transform:scale(1.18) rotate(8deg);opacity:1}}
@keyframes ringSpin{from{transform:translateX(-50%) rotate(0)}to{transform:translateX(-50%) rotate(360deg)}}
@keyframes dustRise{0%{transform:translateY(0) scale(.6);opacity:0}25%{opacity:.65}100%{transform:translateY(-45px) translateX(15px) scale(1.25);opacity:0}}
@keyframes effectFly{0%{transform:translate(0,0) scale(.7);opacity:0}20%{opacity:1}100%{transform:translate(var(--move-x),-125px) scale(1.35) rotate(var(--rotate));opacity:0}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes popup{from{opacity:0;transform:scale(.88)}to{opacity:1;transform:scale(1)}}
@media(max-width:440px){body{padding:0}.phone{width:100%;height:100vh;border:0;border-radius:0}.notch{display:none}}


/* ===== Sticky robot room: only the lower control panel scrolls ===== */
#homePage.page{
  display:none;
  height:100%;
  padding:0;
  overflow:hidden;
  background:linear-gradient(180deg,#cfaa7d 0%,#e0c39a 39%,#d29c58 40%,#d09850 100%);
}
#homePage.page.active{
  display:flex;
  flex-direction:column;
}
#homePage .room{
  flex:0 0 355px;
  height:355px;
  min-height:355px;
  position:relative;
  z-index:12;
  overflow:hidden;
  box-shadow:0 8px 18px rgba(87,54,25,.14);
}
#homePage .home-dashboard{
  flex:1 1 auto;
  min-height:0;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
  padding:10px 8px 24px;
  background:linear-gradient(180deg,rgba(239,205,151,.99),rgba(227,181,110,.99));
  border-top:2px solid rgba(120,76,38,.10);
}
#homePage .home-dashboard::-webkit-scrollbar{width:0;height:0}
#homePage .home-dashboard{scrollbar-width:none;}
@media(max-height:820px){
  #homePage .room{flex-basis:330px;height:330px;min-height:330px;}
}


/* ===== Balanced readable mode: keep original phone shape, enlarge text without stretching layout ===== */
.phone{
  width:min(100%,420px)!important;
  height:960px!important;
  border:8px solid #242321!important;
  border-radius:40px!important;
  overflow:hidden!important;
}
.notch{display:block!important;}
.header{
  height:136px!important;
  padding:24px 14px 8px!important;
}
.pages{height:calc(100% - 136px)!important;}
body{
  padding:8px!important;
  align-items:flex-start!important;
}
body,button,input,select{
  font-size:13px!important;
  word-break:keep-all;
}
.brand{font-size:11px!important;letter-spacing:1.2px!important;}
.app-title{font-size:29px!important;line-height:1.08!important;}
.coin-pill{font-size:14px!important;padding:9px 13px!important;}
.nav{margin-top:11px!important;gap:6px!important;}
.nav-btn{font-size:11px!important;min-height:36px!important;padding:8px 2px!important;border-radius:16px!important;}
.section-kicker{font-size:11px!important;}
.section-title{font-size:24px!important;}
#homePage .room{
  flex:0 0 330px!important;
  height:330px!important;
  min-height:330px!important;
}
#homePage .home-dashboard{
  padding:10px 8px 24px!important;
}
.speech{width:218px!important;min-height:86px!important;font-size:14px!important;line-height:1.55!important;padding:15px 14px!important;}
.speech strong{font-size:17px!important;}
.mode-chip{font-size:11px!important;padding:8px 14px!important;top:111px!important;}
.mission{width:98px!important;padding:9px 8px!important;}
.mission-title{font-size:12px!important;}
.mission-text{font-size:11px!important;line-height:1.45!important;}
.reward-small{font-size:11px!important;}
.quick{right:7px!important;top:86px!important;gap:7px!important;}
.quick-btn{width:54px!important;min-height:53px!important;font-size:10px!important;line-height:1.2!important;}
.quick-btn .icon{font-size:22px!important;}
.actions{gap:4px!important;padding:8px 5px!important;}
.action-btn{font-size:10px!important;line-height:1.15!important;}
.action-icon{font-size:23px!important;}
.plan-panel{padding:12px 10px!important;border-radius:16px!important;}
.plan-head{margin-bottom:8px!important;gap:8px!important;}
.plan-title{font-size:14px!important;line-height:1.25!important;}
.plan-model{font-size:11px!important;padding:5px 8px!important;white-space:nowrap!important;flex:0 0 auto!important;}
.learn-panel{padding:12px 10px!important;border-radius:15px!important;}
.learn-top{align-items:flex-start!important;gap:8px!important;}
.learn-title{font-size:14px!important;line-height:1.3!important;flex:1 1 auto!important;min-width:0!important;}
.learn-pill{
  font-size:11px!important;
  line-height:1.15!important;
  padding:6px 8px!important;
  white-space:nowrap!important;
  word-break:keep-all!important;
  flex:0 0 auto!important;
  min-width:58px!important;
  text-align:center!important;
}
.learn-desc{font-size:12px!important;line-height:1.55!important;}
.learn-status{font-size:12px!important;line-height:1.5!important;}
.learn-step{font-size:11px!important;line-height:1.25!important;padding:7px 5px!important;word-break:keep-all!important;}
.learn-btn{font-size:14px!important;min-height:45px!important;border-radius:13px!important;}
.condition-panel{padding:12px 10px!important;border-radius:15px!important;}
.condition-title{font-size:13px!important;line-height:1.45!important;margin-bottom:9px!important;}
.condition-row,.predict-condition-grid{
  grid-template-columns:76px 1fr 76px 1fr!important;
  gap:8px!important;
  align-items:center!important;
}
.condition-row label,.predict-condition-grid label{
  font-size:12px!important;
  white-space:nowrap!important;
  line-height:1.2!important;
}
.condition-select{font-size:13px!important;min-height:42px!important;padding:0 9px!important;border-radius:11px!important;}
.condition-help{font-size:12px!important;line-height:1.5!important;margin:8px 0 0!important;}
.profile-chip{display:inline-block;background:#edf8df;color:#2f8b3a;border:1px solid #d5ecc3;border-radius:999px;padding:5px 8px!important;font-size:11px!important;font-weight:900;margin-left:4px;white-space:nowrap!important;}
.first-learn-note{font-size:12px!important;line-height:1.55!important;padding:9px 10px!important;}
.predict-btn{font-size:14px!important;min-height:44px!important;border-radius:13px!important;}
.predict-loading{font-size:12px!important;line-height:1.5!important;min-height:24px!important;border-radius:10px;padding:6px 8px;background:rgba(255,255,255,.35);}
.predict-loading.active{background:#eaf4df;color:#2f8b3a;}
.scope-buttons{grid-template-columns:1.05fr repeat(5,1fr)!important;gap:5px!important;}
.scope-btn{font-size:10.5px!important;min-height:42px!important;padding:6px 3px!important;line-height:1.2!important;}
.selected-plan{grid-template-columns:1fr .82fr!important;gap:8px!important;}
.plan-summary{font-size:12px!important;line-height:1.35!important;padding:11px!important;}
.plan-soc{padding:11px 8px!important;}
.plan-soc-label{font-size:11px!important;}
.plan-soc-value{font-size:30px!important;}
.plan-soc-sub{font-size:11px!important;line-height:1.45!important;white-space:normal!important;}
.start-clean-primary{font-size:15px!important;min-height:54px!important;border-radius:15px!important;}
.start-clean-primary small{font-size:11px!important;}
.home-cards{grid-template-columns:1.1fr 1fr .78fr!important;gap:7px!important;}
.mini-card{padding:11px 9px!important;}
.mini-title{font-size:13px!important;}
.battery-info{font-size:11.5px!important;line-height:1.55!important;}
.battery-message{font-size:11px!important;line-height:1.45!important;}
.time-number{font-size:35px!important;}
.time-number small{font-size:14px!important;}
.time-sub{font-size:10.5px!important;}
.time-tip{font-size:11px!important;line-height:1.45!important;}
.food-title,.food-count{font-size:11.5px!important;}
.panel-title{font-size:16px!important;}
.badge{font-size:11px!important;}
.event-content strong{font-size:12.5px!important;}
.event-content span{font-size:11.5px!important;line-height:1.5!important;}
.event-time{font-size:11.5px!important;}
.reward-title{font-size:13px!important;}
.reward-desc{font-size:11.5px!important;line-height:1.5!important;}
.reward-btn{font-size:12px!important;}
.level-number{font-size:30px!important;}
.level-caption{font-size:11px!important;}
.modal{align-items:flex-end!important;justify-content:center!important;padding:0 16px 18px!important;background:rgba(45,33,23,.32)!important;backdrop-filter:blur(2px)!important;}
.modal-card{max-width:392px!important;padding:22px!important;border-radius:24px 24px 20px 20px!important;animation:sheetUp .22s ease-out!important;}
@keyframes sheetUp{from{opacity:0;transform:translateY(46px)}to{opacity:1;transform:translateY(0)}}
.modal-title{font-size:22px!important;}
.modal-body{font-size:15px!important;line-height:1.7!important;}
.modal-btn{font-size:15px!important;padding:13px!important;}
.toast{font-size:13px!important;line-height:1.5!important;min-width:260px;text-align:center;}
@media(max-width:440px){
  body{padding:8px!important;}
  .phone{
    width:min(calc(100% - 16px),420px)!important;
    height:960px!important;
    border:8px solid #242321!important;
    border-radius:40px!important;
  }
  .notch{display:block!important;}
  .header{height:136px!important;}
  .pages{height:calc(100% - 136px)!important;}
  .condition-row,.predict-condition-grid{grid-template-columns:72px 1fr 72px 1fr!important;gap:7px!important;}
  .condition-row label,.predict-condition-grid label{font-size:11.5px!important;}
  .condition-select{font-size:12.5px!important;padding:0 7px!important;}
}
@media(max-height:820px){
  #homePage .room{flex-basis:315px!important;height:315px!important;min-height:315px!important;}
  .speech{top:12px!important;}
}

/* CTA click safety: keep the first-learning button above decorative layers */
#learnPanel{position:relative!important;z-index:60!important;}
#learnBtn{position:relative!important;z-index:9999!important;pointer-events:auto!important;touch-action:manipulation!important;isolation:isolate!important;}
.learn-panel,.plan-panel,.home-dashboard{position:relative!important;}
.learn-panel{z-index:80!important;}
.condition-panel{position:relative!important;z-index:10!important;}

/* ===== Compact learning/profile summary cards ===== */
.compact-note{padding:9px 10px!important;line-height:1.35!important;}
.note-title{font-size:12px;font-weight:950;color:#6f4f38;margin-bottom:7px;}
.profile-mini-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:4px 0 7px;}
.profile-mini-grid span{display:flex;align-items:center;justify-content:center;min-height:28px;border-radius:9px;background:rgba(255,255,255,.72);font-size:11px;font-weight:950;color:#6f4f38;white-space:nowrap;}
.note-caption{font-size:11px;font-weight:850;color:#8a6a45;line-height:1.35;}
.summary-card{display:flex;flex-direction:column;gap:6px;}
.summary-title{font-size:12px;font-weight:950;color:#2f8b3a;margin-bottom:1px;}
.summary-row{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:5px 0;border-bottom:1px dashed rgba(124,83,43,.16);}
.summary-row:last-child{border-bottom:0;}
.summary-key{color:#7c5c3d;font-size:11px;font-weight:900;white-space:nowrap;}
.summary-val{color:#4b3324;font-size:11px;font-weight:950;text-align:right;line-height:1.25;}
.summary-val.em{color:#ef573f;font-size:15px;}
.summary-val.green{color:#2f8b3a;}

/* ===== User guidance banner: persistent next-step explanation ===== */
.flow-guide{
  margin:9px 0 8px;
  padding:10px 11px;
  border:1px solid rgba(78,139,58,.20);
  border-left:5px solid #62aa49;
  border-radius:13px;
  background:linear-gradient(145deg,#f3fbeb,#fff7dc);
  box-shadow:0 4px 10px rgba(79,48,21,.08);
  color:#4b3324;
  font-size:12px;
  line-height:1.5;
  font-weight:850;
}
.flow-guide b{font-weight:1000;color:#2f8b3a;}
.flow-guide .guide-step{display:block;margin-bottom:3px;color:#7a5a3c;font-size:11px;font-weight:1000;}
.flow-guide.warning{border-left-color:#ef8c32;background:linear-gradient(145deg,#fff5dc,#fff0cb);}
.flow-guide.warning b{color:#ef8c32;}
.flow-guide.danger{border-left-color:#ef4e45;background:linear-gradient(145deg,#fff0e9,#fff7dc);}
.flow-guide.danger b{color:#ef4e45;}
.flow-guide.done{border-left-color:#2f8b3a;background:linear-gradient(145deg,#eff9e8,#fff7dc);}
.flow-guide.charging{border-left-color:#f2a84d;background:linear-gradient(145deg,#fff2d2,#fff8e8);}

/* ===== Reward closet: equipped items stay on Roboking ===== */
.robot-accessory{
  position:absolute;
  z-index:34;
  left:50%;
  transform:translateX(-50%);
  pointer-events:none;
  display:none;
  filter:drop-shadow(0 4px 4px rgba(64,38,18,.22));
}
.robot.has-custom-head .crown{display:none!important;}
.robot-head-deco{
  top:-38px;
  min-width:104px;
  height:62px;
  display:none;
  align-items:center;
  justify-content:center;
  text-align:center;
  font-size:43px;
  line-height:1;
}
.robot-head-deco.show{display:flex;animation:decoPop .34s ease-out;}
.robot-head-deco.ribbon{top:-35px;font-size:48px;}
/* 모자는 로보킹 머리 위에 실제로 얹힌 느낌이 나도록 낮게 배치 */
.robot-head-deco.hat{
  top:-38px;
  font-size:66px;
  height:58px;
  transform:translateX(-58%) rotate(-10deg);
  filter:drop-shadow(0 4px 4px rgba(64,38,18,.18));
}
/* 토끼/고양이는 동물 이모지가 아니라 로보킹 자체에 귀가 붙는 장착형 레이어 */
.robot-head-deco.ears{top:-42px;width:138px;height:78px;min-width:138px;}
.robot-head-deco.ears.show{display:block;animation:decoPop .34s ease-out;}
.robo-ear{position:absolute;z-index:2;bottom:4px;filter:drop-shadow(0 3px 3px rgba(64,38,18,.16));}
.robot-head-deco.bunny .robo-ear{
  width:22px;height:62px;border:3px solid #fff;border-radius:16px 16px 12px 12px;
  background:linear-gradient(180deg,#fff 0%,#f1edf8 100%);
}
.robot-head-deco.bunny .robo-ear:after{
  content:"";position:absolute;left:50%;top:8px;width:9px;height:43px;transform:translateX(-50%);
  border-radius:12px;background:linear-gradient(180deg,#ffb5ce,#ffd7e5);
}
.robot-head-deco.bunny .robo-ear.left{left:36px;transform:rotate(-8deg);transform-origin:bottom center;}
.robot-head-deco.bunny .robo-ear.right{right:36px;transform:rotate(8deg);transform-origin:bottom center;}
.robot-head-deco.cat .robo-ear{
  width:36px;
  height:34px;
  bottom:6px;
  background:linear-gradient(180deg,#ffbd4a 0%,#ff922e 82%,#f07725 100%);
  clip-path:polygon(50% 0,4% 100%,96% 100%);
  border-radius:8px;
  filter:drop-shadow(0 3px 3px rgba(64,38,18,.22));
}
.robot-head-deco.cat .robo-ear:after{
  content:"";
  position:absolute;
  left:50%;
  bottom:6px;
  width:16px;
  height:16px;
  transform:translateX(-50%);
  background:linear-gradient(180deg,#ffd6a7,#ff8f80);
  clip-path:polygon(50% 0,8% 100%,92% 100%);
}
.robot-head-deco.cat .robo-ear.left{left:20px;transform:rotate(-16deg);transform-origin:bottom center;}
.robot-head-deco.cat .robo-ear.right{right:20px;transform:rotate(16deg);transform-origin:bottom center;}
.robot-aura-deco{
  position:absolute;
  z-index:5;
  inset:-42px -46px -22px -46px;
  pointer-events:none;
  display:none;
}
.robot-aura-deco.show{display:block;}
.robot-aura-deco span{
  position:absolute;
  font-size:22px;
  filter:drop-shadow(0 3px 3px rgba(64,38,18,.18));
  animation:decoTwinkle 1.6s ease-in-out infinite;
}
.robot-aura-deco span:nth-child(1){left:7px;top:35px;animation-delay:.1s;}
.robot-aura-deco span:nth-child(2){right:2px;top:22px;animation-delay:.45s;}
.robot-aura-deco span:nth-child(3){right:18px;bottom:22px;animation-delay:.8s;}
.robot-aura-deco span:nth-child(4){left:22px;bottom:10px;animation-delay:1.05s;}
.level-robot-preview{position:relative;display:inline-grid;place-items:center;min-width:112px;min-height:94px;margin:0 auto;}
.level-robot-preview .preview-base{font-size:72px;line-height:1;animation:float 2s ease-in-out infinite;}
.preview-head,.preview-aura{position:absolute;pointer-events:none;}
.preview-head{top:-4px;left:50%;transform:translateX(-50%);font-size:35px;filter:drop-shadow(0 3px 3px rgba(64,38,18,.18));}
.preview-head.hat{top:-9px;transform:translateX(-56%) rotate(-10deg);font-size:48px;}
.preview-head.ears{top:-13px;width:92px;height:48px;}
.preview-head.ears .p-ear{position:absolute;bottom:0;filter:drop-shadow(0 2px 2px rgba(64,38,18,.14));}
.preview-head.bunny .p-ear{width:13px;height:42px;border:2px solid #fff;border-radius:12px;background:#f5f1fb;}
.preview-head.bunny .p-ear:after{content:"";position:absolute;left:50%;top:6px;width:5px;height:29px;transform:translateX(-50%);border-radius:8px;background:#ffc2d7;}
.preview-head.bunny .p-ear.left{left:24px;transform:rotate(-8deg)}.preview-head.bunny .p-ear.right{right:24px;transform:rotate(8deg)}
.preview-head.cat .p-ear{width:24px;height:22px;background:linear-gradient(180deg,#ffbd4a,#ff922e 85%);clip-path:polygon(50% 0,4% 100%,96% 100%);}
.preview-head.cat .p-ear:after{content:"";position:absolute;left:50%;bottom:3px;width:10px;height:10px;transform:translateX(-50%);background:linear-gradient(180deg,#ffd6a7,#ff8f80);clip-path:polygon(50% 0,8% 100%,92% 100%);}
.preview-head.cat .p-ear.left{left:13px;transform:rotate(-15deg)}.preview-head.cat .p-ear.right{right:13px;transform:rotate(15deg)}
.preview-aura{inset:0;font-size:18px;animation:decoTwinkle 1.5s ease-in-out infinite;}
.preview-aura .a1{position:absolute;left:2px;top:15px}.preview-aura .a2{position:absolute;right:0;top:28px}.preview-aura .a3{position:absolute;right:12px;bottom:12px}
.reward-btn.equipped{background:linear-gradient(90deg,#4a9b42,#75b84e)!important;color:#fff!important;}
.reward-btn.owned{background:#fff2cf!important;color:#5c422f!important;border:1px solid rgba(124,83,43,.18)!important;}
.reward-card.owned{background:rgba(255,253,240,.98)!important;border-color:rgba(75,155,66,.22)!important;}
.reward-card.equipped{box-shadow:0 0 0 2px rgba(75,155,66,.2), var(--shadow)!important;}
.reward-status{margin-top:5px;color:#4a9b42;font-size:10px;font-weight:950;min-height:13px;}

.reward-folder-tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 9px;}
.reward-folder-btn{min-height:43px;border:1px solid rgba(124,83,43,.18);border-radius:14px;background:rgba(255,248,231,.9);color:#6f4f38;font-size:13px;font-weight:950;box-shadow:0 4px 10px rgba(79,48,21,.1);}
.reward-folder-btn.active{background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;border-color:transparent;}
.reward-panel{display:block;}
.reward-panel.hidden{display:none;}
.coupon-card{min-height:178px;text-align:left;display:flex;flex-direction:column;align-items:stretch;}
.coupon-card .reward-icon{text-align:center;font-size:34px;line-height:1.05;}
.coupon-card .reward-title{text-align:center;line-height:1.25;min-height:32px;display:flex;align-items:center;justify-content:center;}
.coupon-card .reward-desc{font-size:10.5px;line-height:1.5;text-align:left;min-height:58px;}
.coupon-benefit{margin-top:7px;padding:7px 8px;border-radius:10px;background:#fff2cf;color:#6f4f38;font-size:10px;font-weight:900;line-height:1.35;text-align:left;min-height:42px;display:flex;align-items:center;}
.coupon-card .reward-status{min-height:15px;text-align:center;}
.coupon-card .reward-btn{margin-top:auto;min-height:42px;display:flex;align-items:center;justify-content:center;text-align:center;}
.coupon-card.owned{border-color:rgba(75,155,66,.24);background:rgba(255,253,240,.98);}
.reward-btn.need-coins{background:#efe0bc!important;color:#6f4f38!important;}
.reward-btn.need-coins:after{content:"";}

@keyframes decoPop{from{opacity:0;transform:translateX(-50%) translateY(8px) scale(.7)}to{opacity:1;transform:translateX(-50%) translateY(0) scale(1)}}
@keyframes decoTwinkle{0%,100%{opacity:.45;transform:scale(.88) rotate(-8deg)}50%{opacity:1;transform:scale(1.12) rotate(8deg)}}

/* ===== Room status cleanup: avoid speech overlap + show current robot 배터리 ===== */
#homePage .room .mode-chip{
  top:125px!important;
  left:12px!important;
  right:auto!important;
  bottom:auto!important;
  transform:none!important;
  width:142px!important;
  max-width:142px!important;
  min-height:34px!important;
  padding:7px 9px!important;
  border-radius:15px!important;
  background:rgba(255,248,229,.96)!important;
  box-shadow:0 5px 12px rgba(72,46,23,.18)!important;
  color:#5b3f2d!important;
  font-size:10.5px!important;
  line-height:1.25!important;
  font-weight:950!important;
  text-align:center!important;
  white-space:normal!important;
  word-break:keep-all!important;
}
#homePage .room.cleaning .mode-chip{color:#fff!important;background:rgba(57,143,82,.94)!important;}
#homePage .room.charging .mode-chip{color:#fff!important;background:rgba(242,145,35,.94)!important;}
.robot-soc-badge{
  position:absolute;
  z-index:24;
  right:64px;
  bottom:114px;
  width:98px;
  min-height:44px;
  padding:7px 8px 6px;
  border:2px solid rgba(255,255,255,.82);
  border-radius:16px;
  background:rgba(255,255,255,.95);
  box-shadow:0 7px 16px rgba(60,38,20,.22);
  text-align:center;
  pointer-events:none;
}
.robot-soc-badge span{
  display:block;
  color:#7a5a3c;
  font-size:9.5px;
  line-height:1.05;
  font-weight:950;
  white-space:nowrap;
}
.robot-soc-badge b{
  display:block;
  margin-top:2px;
  color:#2f8b3a;
  font-size:19px;
  line-height:1;
  font-weight:1000;
  letter-spacing:-.5px;
}
.robot-soc-badge.need b{color:#ef8c32;}
.robot-soc-badge.low b{color:#ef4e45;}
.robot-soc-badge.ok b{color:#2f8b3a;}
.robot-soc-badge:after{
  content:"";
  position:absolute;
  left:50%;
  bottom:-8px;
  transform:translateX(-50%);
  border-width:8px 6px 0;
  border-style:solid;
  border-color:rgba(255,255,255,.95) transparent transparent;
}
@media(max-height:820px){
  #homePage .room .mode-chip{top:118px!important;}
  .robot-soc-badge{right:60px;bottom:105px;}
}

/* ===== SVG learned home map card ===== */
.learn-steps.map-ready,
#learnSteps.map-ready{
  display:block!important;
  grid-template-columns:1fr!important;
  gap:0!important;
  width:100%!important;
}
#learnSteps.map-ready .home-map-card{
  width:100%!important;
  max-width:none!important;
}
.home-map-card{
  width:100%;
  padding:6px;
  margin-top:8px;
  border-radius:16px;
  background:rgba(255,255,255,.72);
  border:1px solid rgba(124,83,43,.14);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.48);
}
.home-map-head{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  gap:8px;
  margin-bottom:5px;
}
.home-map-title{display:none;}
.home-map-badge{
  flex:0 0 auto;
  padding:4px 8px;
  border-radius:999px;
  background:#e8f5dc;
  color:#2f8b3a;
  font-size:10px;
  line-height:1;
  font-weight:950;
  white-space:nowrap;
}
.home-map-img-wrap{
  position:relative;
  overflow:hidden;
  width:100%;
  min-height:210px;
  border-radius:14px;
  background:linear-gradient(145deg,#f6e3ba,#fff7e4);
  border:1px solid rgba(124,83,43,.12);
}
.home-map-svg{display:block;width:100%;height:220px;}
.home-map-caption{display:none;}
.map-room{stroke:#fffdf4;stroke-width:4;filter:drop-shadow(0 3px 4px rgba(67,42,20,.13));}
.map-room.dashed{stroke-dasharray:8 5;stroke:#fffdf4;}
.map-room-label{fill:#64472f;font-size:13px;font-weight:950;text-anchor:middle;dominant-baseline:middle;}
.map-room-sub{fill:#8a6744;font-size:9.4px;font-weight:850;text-anchor:middle;dominant-baseline:middle;}
.map-route{fill:none;stroke:rgba(255,255,255,.82);stroke-width:3;stroke-linecap:round;stroke-dasharray:5 6;}
.map-room-group{cursor:pointer;}
.map-room-group .map-room{transition:opacity .18s ease, filter .18s ease;}
.map-room-group.no-go .map-room{opacity:.42;filter:grayscale(.35);}
.map-no-go-shade{fill:rgba(255,255,255,.48);}
.map-no-go-line{stroke:#8b6f57;stroke-width:4;stroke-linecap:round;opacity:.72;}
.map-action-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:8px;}
.map-action-btn{
  min-height:38px;
  border:0;
  border-radius:13px;
  background:#fff4d8;
  color:#68472d;
  font-size:11.5px;
  font-weight:950;
  box-shadow:inset 0 0 0 1px rgba(135,88,43,.16);
  cursor:pointer;
}
.map-action-btn.active{color:#fff;background:linear-gradient(135deg,#50ae48,#77c75b);box-shadow:0 7px 12px rgba(67,126,56,.20);}
.map-action-btn.danger.active{background:linear-gradient(135deg,#f07a54,#f7a13e);box-shadow:0 7px 12px rgba(190,93,45,.20);}
.map-action-hint{
  margin-top:7px;
  padding:7px 9px;
  border-radius:12px;
  background:rgba(255,250,235,.92);
  border:1px solid rgba(124,83,43,.10);
  color:#6f4f36;
  font-size:11px;
  line-height:1.38;
  font-weight:850;
  text-align:center;
}
.map-action-hint b{color:#2f8b3a;}
.map-legend{
  display:flex;
  align-items:center;
  justify-content:center;
  flex-wrap:wrap;
  gap:7px 10px;
  margin-top:8px;
  padding:8px 8px;
  border-radius:14px;
  background:rgba(255,250,235,.92);
  border:1px solid rgba(124,83,43,.13);
  color:#68472d;
  font-size:12px;
  line-height:1.15;
  font-weight:950;
}
.map-legend-title{color:#4b3324;font-weight:1000;margin-right:2px;}
.map-legend-item{display:inline-flex;align-items:center;gap:5px;}
.map-dot{display:inline-block;width:12px;height:12px;border-radius:999px;border:1px solid rgba(80,50,28,.16);box-shadow:0 1px 2px rgba(72,43,19,.12);}
.dot-clean{background:#cfeec0;}
.dot-normal{background:#ffe08a;}
.dot-dusty{background:#ffb169;}
.dot-focus{background:#ff7d68;}

/* ===== Main map CTA row ===== */
.learn-actions{display:grid;grid-template-columns:1fr;gap:8px;margin-top:8px;}
.learn-actions.ready{grid-template-columns:1fr 1fr;}
.clean-execute-btn{
  position:relative;
  z-index:9999;
  width:100%;
  min-height:45px;
  border:0;
  border-radius:13px;
  background:linear-gradient(90deg,#41a346,#79c75a);
  color:#fff;
  font-size:14px;
  font-weight:950;
  box-shadow:0 7px 12px rgba(67,126,56,.22);
  cursor:pointer;
  pointer-events:auto!important;
  touch-action:manipulation!important;
}
.clean-execute-btn:disabled{opacity:.55;cursor:not-allowed;filter:grayscale(.12);}
.condition-panel.manual-mode{margin-top:9px!important;background:linear-gradient(145deg,#fff8e6,#f3dfb2)!important;}
.condition-panel.manual-mode .condition-title:before{content:"✍️ ";}

/* ===== Home simplification: one main clean-prep button, no extra lower cards ===== */
.scope-buttons,
.selected-plan,
.start-clean-primary,
.actions,
.home-cards{display:none!important;}
.condition-panel{margin-bottom:0!important;}
.predict-btn{position:relative;z-index:30;}
#flowGuide{margin-top:9px;}

.manual-action-row{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:8px;
  margin-top:10px;
}
.manual-clean-btn{
  position:relative;
  z-index:31;
  width:100%;
  min-height:43px;
  border:0;
  border-radius:13px;
  color:#fff;
  background:linear-gradient(90deg,#f69028,#f9b047);
  font-size:12.5px;
  font-weight:950;
  box-shadow:0 7px 12px rgba(210,117,35,.18);
  cursor:pointer;
}
.manual-clean-btn.ready{
  background:linear-gradient(90deg,#41a346,#79c75a);
  box-shadow:0 7px 12px rgba(67,126,56,.20);
}
.manual-clean-btn:disabled{
  opacity:.55;
  cursor:not-allowed;
  filter:grayscale(.12);
}
.manual-action-row .predict-btn{
  margin-top:0!important;
}
.manual-combo-btn{
  width:100%;
  min-height:46px!important;
  margin-top:10px!important;
  border-radius:14px!important;
  font-size:13px!important;
  font-weight:950!important;
  background:linear-gradient(90deg,#41a346,#79c75a)!important;
  color:#fff!important;
  box-shadow:0 7px 12px rgba(67,126,56,.22)!important;
}
.manual-combo-btn.running{
  background:linear-gra
