import json
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
    
/* ===== Readability upgrade: larger text for mobile demo ===== */
.phone{height:960px;}
.header{height:136px;padding:26px 16px 10px;}
.pages{height:calc(100% - 136px);}
.brand{font-size:10px;}
.app-title{font-size:26px;}
.coin-pill{font-size:13px;padding:9px 13px;}
.nav-btn{font-size:11px;padding:9px 4px;}
.speech{width:206px;min-height:84px;font-size:14px;line-height:1.55;padding:15px 14px;}
.speech strong{font-size:16px;}
.mode-chip{font-size:10px;padding:8px 14px;}
.mission{width:102px;padding:10px 8px;}
.mission-title{font-size:11px;}
.mission-text{font-size:10px;line-height:1.45;}
.reward-small{font-size:10px;}
.quick-btn{width:56px;min-height:55px;font-size:9px;}
.quick-btn .icon{font-size:23px;}
.action-btn{font-size:9px;}
.action-icon{font-size:25px;}
.mini-title{font-size:12px;}
.battery-info{font-size:10.5px;line-height:1.55;}
.battery-message{font-size:10px;line-height:1.5;padding:8px;}
.time-sub{font-size:9.5px;}
.time-tip{font-size:10px;line-height:1.5;padding:8px 6px;}
.food-title,.food-count{font-size:11px;}
.plan-panel{padding:12px;}
.plan-title{font-size:13px;}
.plan-model{font-size:9.5px;padding:5px 8px;}
.learn-panel{padding:12px;border-radius:15px;}
.learn-title{font-size:12px;}
.learn-pill{font-size:9.5px;padding:5px 8px;}
.learn-desc{font-size:10px;line-height:1.55;}
.learn-status{font-size:10px;line-height:1.5;}
.learn-steps{gap:6px;}
.learn-steps.map-ready{
  display:block!important;
  grid-template-columns:1fr!important;
  width:100%!important;
}

.learn-step{font-size:9.5px;padding:6px 5px;}
.learn-btn{font-size:12px;min-height:39px;}
.condition-panel{padding:11px;border-radius:15px;}
.condition-title{font-size:11px;line-height:1.45;margin-bottom:8px;}
.condition-row{grid-template-columns:.55fr 1fr .55fr 1fr;gap:7px;}
.condition-row label{font-size:10px;}
.condition-select{font-size:11px;min-height:38px;padding:0 9px;}

.predict-condition-grid{display:grid;grid-template-columns:.7fr 1fr .7fr 1fr;gap:8px;align-items:center;margin-top:8px;}
.predict-condition-grid label{font-size:10.5px;font-weight:900;color:#6c4a2f;white-space:nowrap;}
.condition-help{font-size:10.3px;line-height:1.55;color:#8a6a45;margin:8px 0 0;}
.profile-chip{display:inline-block;background:#edf8df;color:#2f8b3a;border:1px solid #d5ecc3;border-radius:999px;padding:5px 9px;font-size:9.5px;font-weight:900;margin-left:4px;}
@media(max-width:440px){.predict-condition-grid{grid-template-columns:.8fr 1fr;gap:7px}.predict-condition-grid label{font-size:10px}}
.predict-btn{font-size:12px;min-height:40px;}
.predict-loading{font-size:10px;line-height:1.5;min-height:22px;}
.scope-btn{font-size:10px;min-height:42px;padding:6px 3px;}
.selected-plan{gap:8px;}
.plan-summary{font-size:10.5px;line-height:1.6;padding:11px;}
.plan-soc{padding:11px;}
.plan-soc-label{font-size:10px;}
.plan-soc-value{font-size:26px;}
.plan-soc-sub{font-size:10px;line-height:1.45;}
.gauge-label{font-size:11px;}
.gauge-desc{font-size:10px;}
.control-head{font-size:12px;}
.control-caption{font-size:9.5px;}
.panel-title{font-size:14px;}
.badge{font-size:9.5px;}
.legend{font-size:10px;}
.insight-row{font-size:11px;line-height:1.6;}
.record-label,.event-time{font-size:10px;}
.event-content strong{font-size:11px;}
.event-content span{font-size:10px;line-height:1.45;}
.reward-title{font-size:12px;}
.reward-desc{font-size:10px;line-height:1.45;}
.reward-btn{font-size:10px;}
.modal-card{padding:22px;border-radius:22px;}
.modal-title{font-size:20px;}
.modal-body{font-size:14px;line-height:1.7;}
.modal-btn{font-size:13px;padding:13px;}
.toast{font-size:12px;}
@media(max-width:440px){.phone{height:100vh;}.pages{height:calc(100% - 136px);}}



/* ===== Final UX: use bottom sheet only for decisions; routine updates use cards/toasts/speech ===== */
.modal{align-items:flex-end!important;justify-content:center!important;padding:0 16px 18px!important;background:rgba(45,33,23,.32)!important;backdrop-filter:blur(2px)!important;}
.modal-card{max-width:392px!important;border-radius:24px 24px 20px 20px!important;animation:sheetUp .22s ease-out!important;}
@keyframes sheetUp{from{opacity:0;transform:translateY(46px)}to{opacity:1;transform:translateY(0)}}
.predict-loading{border-radius:10px;padding:6px 8px;background:rgba(255,255,255,.35);}
.predict-loading.active{background:#eaf4df;color:#2f8b3a;}

</style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 맞춤 배터리 준비 결과 기록 연결부
# GitHub에는 아래 구조로 기록를 올리면 됩니다.
# data/home_model_predictions.csv
# data/zone_model_predictions.csv
# ============================================================

BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"
HOME_PRED_PATH = DATA_DIR / "home_model_predictions.csv"
ZONE_PRED_PATH = DATA_DIR / "zone_model_predictions.csv"

# 데모용 현재 배터리. 실제 제품에서는 로봇/앱에서 받은 현재 배터리로 교체하면 됩니다.
CURRENT_SOC = 80


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

    # home 기록가 없고 zone 기록만 있을 때도 최소 동작하도록 처리
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

/* Battery */
.gauge-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.gauge-card{padding:14px 10px;text-align:center}
.gauge{--value:81;--color:#49a646;position:relative;width:118px;height:118px;margin:0 auto 8px;display:grid;place-items:center;border-radius:50%;background:conic-gradient(var(--color) calc(var(--value)*1%),#ead9b9 0)}
.gauge:before{content:"";position:absolute;width:82px;height:82px;border-radius:50%;background:#fff4d8}.gauge-content{position:relative;z-index:2;font-weight:900}.gauge-label{font-size:10px}.gauge-value{margin-top:2px;font-size:24px}.gauge-desc{font-size:9px;line-height:1.5;font-weight:800}
.control{margin-top:9px;padding:15px 14px}.control-row{margin-bottom:17px}.control-row:last-child{margin-bottom:0}.control-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:11px;font-weight:900}.control-value{color:var(--green2)}input[type=range]{width:100%;accent-color:var(--green2)}.control-caption{display:flex;justify-content:space-between;margin-top:4px;color:#806047;font-size:8px;font-weight:800}
.primary-btn{width:100%;margin-top:12px;padding:12px;border:0;border-radius:13px;background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;font-size:12px;font-weight:900;box-shadow:0 5px 12px rgba(63,132,57,.23)}
.chart-panel{margin-top:9px;padding:15px 14px}.panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.panel-title{font-size:13px;font-weight:900}.badge{padding:5px 8px;border-radius:12px;background:#fff0ce;color:#805c35;font-size:8px;font-weight:900}.soc-chart{width:100%;height:167px;overflow:visible}.grid-line{stroke:#d7c6a8;stroke-width:1;stroke-dasharray:4 5}.line-red{fill:none;stroke:#eb6650;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}.line-green{fill:none;stroke:#4c9a43;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}.chart-text{fill:#856347;font-size:9px;font-weight:800}.legend{display:flex;gap:13px;font-size:9px;font-weight:900}.dot{display:inline-block;width:9px;height:9px;margin-right:4px;border-radius:50%}.insight{margin-top:9px;padding:14px}.insight-row{display:flex;gap:9px;font-size:10px;line-height:1.6;font-weight:800}.insight-icon{font-size:20px}

/* Record */
.weekly{padding:15px 14px}.bar-chart{height:190px;display:flex;align-items:flex-end;justify-content:space-between;gap:8px;padding:17px 5px 0}.bar-item{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}.bar{width:100%;max-width:32px;border-radius:12px 12px 5px 5px;background:linear-gradient(180deg,#66b449,#138b35);transform-origin:bottom;animation:barGrow .65s ease-out}.bar-value{margin-bottom:4px;color:#426d32;font-size:8px;font-weight:900}.bar-label{margin-top:5px;font-size:9px;font-weight:900}
.record-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}.record-card{min-height:90px;padding:14px;border:1px solid rgba(136,87,40,.14);border-radius:16px;background:rgba(255,248,231,.96);box-shadow:var(--shadow)}.record-label{color:#6e503a;font-size:9px;font-weight:900}.record-value{margin-top:7px;color:#31241b;font-size:23px;font-weight:900}
.events{margin-top:9px;padding:15px 14px}.event-item{display:grid;grid-template-columns:43px 1fr;gap:8px;padding:11px 0;border-bottom:1px solid rgba(122,87,51,.12)}.event-item:last-child{border-bottom:0}.event-time{color:#946c43;font-size:9px;font-weight:900}.event-content strong{display:block;margin-bottom:3px;font-size:10px}.event-content span{color:#785a43;font-size:9px;line-height:1.4;font-weight:700}


/* Event page placeholder */
.event-hero{padding:16px 14px;margin-bottom:9px;background:linear-gradient(145deg,#fff8e8,#f5dfa9)}
.event-hero-title{font-size:18px;font-weight:950;color:#4b3324;margin-bottom:8px}
.event-hero-desc{font-size:12px;line-height:1.55;font-weight:800;color:#76533b}
.event-placeholder-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}
.event-placeholder-card{min-height:112px;padding:14px;border-radius:16px;background:rgba(255,248,231,.96);box-shadow:var(--shadow);border:1px solid rgba(136,87,40,.14)}
.event-placeholder-icon{font-size:30px;margin-bottom:8px}
.event-placeholder-title{font-size:13px;font-weight:950;color:#4b3324}
.event-placeholder-text{margin-top:5px;font-size:11px;line-height:1.45;font-weight:800;color:#7b5a3e}

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
@keyframes barGrow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
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


/* ===== Large text mode: all readable UI text increased by 30%+ ===== */
.phone{height:1040px!important;}
.header{height:154px!important;padding:29px 16px 10px!important;}
.pages{height:calc(100% - 154px)!important;}
body,button,input,select{font-size:15px!important;}
.brand{font-size:13px!important;}
.app-title{font-size:32px!important;}
.coin-pill{font-size:17px!important;padding:10px 14px!important;}
.nav{gap:6px!important;margin-top:14px!important;}
.nav-btn{font-size:14px!important;min-height:42px!important;padding:9px 4px!important;}
.section-kicker{font-size:12px!important;}
.section-title{font-size:30px!important;}
.speech{width:238px!important;min-height:98px!important;font-size:16px!important;line-height:1.62!important;padding:17px 15px!important;}
.speech strong{font-size:19px!important;}
.mode-chip{font-size:13px!important;padding:9px 15px!important;}
.mission-title{font-size:14px!important;}
.mission-text{font-size:13px!important;line-height:1.55!important;}
.reward-small{font-size:13px!important;}
.quick-btn{font-size:12px!important;min-height:58px!important;}
.action-btn{font-size:12px!important;}
.mini-title{font-size:15px!important;}
.battery-info{font-size:13px!important;line-height:1.6!important;}
.battery-message{font-size:13px!important;line-height:1.55!important;padding:9px!important;}
.time-number{font-size:39px!important;}
.time-number small{font-size:16px!important;}
.time-sub{font-size:12px!important;}
.time-tip{font-size:13px!important;line-height:1.55!important;padding:9px 7px!important;}
.food-title,.food-count{font-size:13px!important;}
.plan-panel{padding:14px 12px!important;}
.plan-title{font-size:15px!important;}
.plan-model{font-size:12px!important;padding:6px 9px!important;}
.learn-panel{padding:14px 12px!important;border-radius:16px!important;}
.learn-title{font-size:15px!important;}
.learn-pill{font-size:12px!important;padding:6px 9px!important;}
.learn-desc{font-size:13px!important;line-height:1.6!important;}
.learn-status{font-size:13px!important;line-height:1.55!important;}
.learn-step{font-size:12px!important;line-height:1.35!important;padding:8px 6px!important;}
.learn-btn{font-size:16px!important;min-height:48px!important;}
.condition-panel{padding:14px 12px!important;border-radius:16px!important;}
.condition-title{font-size:15px!important;line-height:1.5!important;margin-bottom:10px!important;}
.condition-row{grid-template-columns:92px 1fr!important;gap:9px 10px!important;align-items:center!important;}
.condition-row label{font-size:13px!important;}
.condition-select{font-size:15px!important;min-height:48px!important;padding:0 12px!important;border-radius:12px!important;}
.predict-condition-grid{grid-template-columns:92px 1fr!important;gap:9px 10px!important;align-items:center!important;}
.predict-condition-grid label{font-size:13px!important;white-space:normal!important;}
.condition-help{font-size:13px!important;line-height:1.6!important;margin:10px 0 0!important;}
.profile-chip{font-size:12px!important;padding:6px 10px!important;}
.first-learn-note{font-size:13px!important;line-height:1.6!important;padding:10px 11px!important;}
.predict-btn{font-size:16px!important;min-height:50px!important;border-radius:13px!important;}
.predict-loading{font-size:13px!important;line-height:1.55!important;min-height:26px!important;}
.scope-buttons{grid-template-columns:repeat(2,1fr)!important;gap:8px!important;}
.scope-btn{font-size:13px!important;min-height:50px!important;padding:8px 6px!important;}
.selected-plan{grid-template-columns:1fr!important;gap:10px!important;}
.plan-summary{font-size:14px!important;line-height:1.65!important;padding:13px!important;}
.plan-soc{padding:13px!important;}
.plan-soc-label{font-size:13px!important;}
.plan-soc-value{font-size:35px!important;}
.plan-soc-sub{font-size:13px!important;line-height:1.5!important;}
.start-clean-primary{font-size:18px!important;min-height:64px!important;border-radius:16px!important;}
.start-clean-primary small{font-size:12px!important;}
.gauge-label{font-size:13px!important;}
.gauge-value{font-size:32px!important;}
.gauge-desc{font-size:13px!important;line-height:1.55!important;}
.control-head{font-size:15px!important;}
.control-caption{font-size:12px!important;}
.primary-btn{font-size:16px!important;min-height:48px!important;}
.panel-title{font-size:18px!important;}
.panel-head > div:last-child{font-size:14px!important;}
.badge{font-size:12px!important;}
.chart-text{font-size:12px!important;}
.legend{font-size:13px!important;}
.insight-row{font-size:14px!important;line-height:1.65!important;}
.record-label,.event-time{font-size:13px!important;}
.record-value{font-size:31px!important;}
.event-content strong{font-size:14px!important;}
.event-content span{font-size:13px!important;line-height:1.55!important;}
.bar-value{font-size:12px!important;}
.bar-label{font-size:12px!important;}
.level-number{font-size:34px!important;}
.level-caption{font-size:12px!important;}
.reward-title{font-size:15px!important;}
.reward-desc{font-size:13px!important;line-height:1.55!important;}
.reward-btn{font-size:13px!important;min-height:40px!important;}
.modal-title{font-size:25px!important;}
.modal-body{font-size:17px!important;line-height:1.75!important;}
.modal-btn{font-size:17px!important;padding:14px!important;}
.toast{font-size:15px!important;line-height:1.55!important;}
#homePage .home-dashboard{padding:14px 10px 34px!important;}
@media(max-width:440px){
  .phone{height:100vh!important;}
  .header{height:154px!important;}
  .pages{height:calc(100% - 154px)!important;}
  .condition-row,.predict-condition-grid{grid-template-columns:88px 1fr!important;gap:9px 9px!important;}
  .scope-buttons{grid-template-columns:repeat(2,1fr)!important;}
}
@media(max-height:820px){
  #homePage .room{flex-basis:318px!important;height:318px!important;min-height:318px!important;}
  .speech{top:12px!important;}
  .mode-chip{top:114px!important;}
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
.profile-chip{font-size:11px!important;padding:5px 8px!important;white-space:nowrap!important;}
.first-learn-note{font-size:12px!important;line-height:1.55!important;padding:9px 10px!important;}
.predict-btn{font-size:14px!important;min-height:44px!important;border-radius:13px!important;}
.predict-loading{font-size:12px!important;line-height:1.5!important;min-height:24px!important;}
.scope-buttons{grid-template-columns:1.05fr repeat(5,1fr)!important;gap:5px!important;}
.scope-btn{font-size:10.5px!important;min-height:42px!important;padding:6px 3px!important;line-height:1.2!important;}
.selected-plan{grid-template-columns:1fr .82fr!important;gap:8px!important;}
.plan-summary{font-size:12px!important;line-height:1.55!important;padding:11px!important;}
.plan-soc{padding:11px 8px!important;}
.plan-soc-label{font-size:11px!important;}
.plan-soc-value{font-size:30px!important;}
.plan-soc-sub{font-size:11px!important;line-height:1.45!important;}
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
.gauge-label{font-size:12px!important;}
.gauge-value{font-size:28px!important;}
.gauge-desc{font-size:12px!important;line-height:1.5!important;}
.control-head{font-size:13px!important;}
.control-caption{font-size:11px!important;}
.primary-btn{font-size:14px!important;min-height:45px!important;}
.panel-title{font-size:16px!important;}
.badge{font-size:11px!important;}
.legend{font-size:12px!important;}
.insight-row{font-size:12.5px!important;line-height:1.6!important;}
.record-label,.event-time{font-size:11.5px!important;}
.record-value{font-size:27px!important;}
.event-content strong{font-size:12.5px!important;}
.event-content span{font-size:11.5px!important;line-height:1.5!important;}
.reward-title{font-size:13px!important;}
.reward-desc{font-size:11.5px!important;line-height:1.5!important;}
.reward-btn{font-size:12px!important;}
.modal-title{font-size:22px!important;}
.modal-body{font-size:15px!important;line-height:1.7!important;}
.modal-btn{font-size:15px!important;padding:13px!important;}
.toast{font-size:13px!important;line-height:1.5!important;}
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
.plan-summary{line-height:1.35!important;}
.plan-soc-sub{white-space:normal!important;}




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
.toast{min-width:260px;text-align:center;line-height:1.45;}

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
.home-map-title{
  display:none;
}
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
.home-map-svg{
  display:block;
  width:100%;
  height:220px;
}
.home-map-caption{
  display:none;
}
.map-room{
  stroke:#fffdf4;
  stroke-width:4;
  filter:drop-shadow(0 3px 4px rgba(67,42,20,.13));
}
.map-room.dashed{
  stroke-dasharray:8 5;
  stroke:#fffdf4;
}
.map-room-label{
  fill:#64472f;
  font-size:13px;
  font-weight:950;
  text-anchor:middle;
  dominant-baseline:middle;
}
.map-room-sub{
  fill:#8a6744;
  font-size:9.4px;
  font-weight:850;
  text-anchor:middle;
  dominant-baseline:middle;
}
.map-route{
  fill:none;
  stroke:rgba(255,255,255,.82);
  stroke-width:3;
  stroke-linecap:round;
  stroke-dasharray:5 6;
}
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
.map-legend-title{
  color:#4b3324;
  font-weight:1000;
  margin-right:2px;
}
.map-legend-item{
  display:inline-flex;
  align-items:center;
  gap:5px;
}
.map-dot{
  display:inline-block;
  width:12px;
  height:12px;
  border-radius:999px;
  border:1px solid rgba(80,50,28,.16);
  box-shadow:0 1px 2px rgba(72,43,19,.12);
}
.dot-clean{background:#cfeec0;}
.dot-normal{background:#ffe08a;}
.dot-dusty{background:#ffb169;}
.dot-focus{background:#ff7d68;}


/* ===== Home simplification: one main clean-prep button, no extra lower cards ===== */
.scope-buttons,
.selected-plan,
.start-clean-primary,
.actions,
.home-cards{display:none!important;}
.condition-panel{margin-bottom:0!important;}
.predict-btn{position:relative;z-index:30;}
#flowGuide{margin-top:9px;}

</style>
</head>

<body>
<div class="phone">
  <div class="notch"></div>
  <div class="screen">

    <header class="header">
      <div class="header-top">
        <div>
          <div class="brand">LG ROBO CARE</div>
          <div class="app-title">로보킹 키우기</div>
        </div>
        <div class="coin-pill">🪙 <span id="coinText">050</span></div>
      </div>
      <nav class="nav">
        <button class="nav-btn active" data-page="homePage">홈</button>
        <button class="nav-btn" data-page="batteryPage">배터리</button>
        <button class="nav-btn" data-page="recordPage">기록</button>
        <button class="nav-btn" data-page="eventPage">이벤트</button>
        <button class="nav-btn" data-page="rewardPage">리워드</button>
      </nav>
    </header>

    <main class="pages">

      <section class="page active" id="homePage">
        <div class="room" id="room">
          <div class="wall-light"></div><div class="floor"></div>
          <div class="plant">🪴</div><div class="house"></div><div class="sofa"></div>
          <div class="speech" id="speech"><strong>배가 든든해요!</strong><br>청소를 준비할게요!</div>
          <div class="mode-chip" id="modeChip">✨ 로보킹 맞춤 준비</div>
          <div class="rug"></div>
          <div class="clean-path"><div class="clean-fill" id="cleanFill"></div></div>
          <div class="charge-ring"></div>
          <div class="dust"><span></span><span></span><span></span><span></span><span></span><span></span></div>

          <div class="robot" id="robot" data-action="pet">
            <div class="robot-aura-deco" id="robotAuraDeco"><span>✨</span><span>✨</span><span>✨</span><span>✨</span></div>
            <div class="crown">👑</div>
            <div class="robot-accessory robot-head-deco" id="robotHeadDeco"></div>
            <div class="spark" id="spark">✨</div><div class="robot-top"></div>
            <div class="face">
              <div class="eye left"></div><div class="eye right"></div>
              <div class="cheek left"></div><div class="cheek right"></div><div class="mouth"></div>
            </div>
            <div class="robot-accessory robot-body-deco" id="robotBodyDeco"></div>
            <div class="slot"></div>
          </div>
          <div class="robot-soc-badge" id="robotSocBadge"><span>🔋 현재 배터리</span><b>20%</b></div>

          <div class="mission">
            <div class="mission-title">오늘의 미션</div>
            <div class="mission-text">거실 청소 1회 완료하기</div>
            <div class="mission-progress">
              <div class="mission-track"><div class="mission-fill" id="missionFill"></div></div>
              <span class="reward-small">+50</span>
            </div>
          </div>

          <div class="quick">
            <button class="quick-btn" data-action="status"><span class="icon">💖</span>상태보기</button>
            <button class="quick-btn" data-action="charge"><span class="icon">🔋</span>배터리 관리</button>
            <button class="quick-btn" data-action="record"><span class="icon">📋</span>청소 기록</button>
            <button class="quick-btn" data-action="decorate"><span class="icon">🎩</span>꾸미기</button>
          </div>
          <div class="effect-layer" id="effectLayer"></div>
        </div>

        <div class="home-dashboard">

          <div class="panel plan-panel">
            <div class="plan-head">
              <div class="plan-title">우리 집 맞춤 청소 준비</div>
              <div class="plan-model" id="planModel">1회차 학습 전</div>
            </div>
            <div class="learn-panel" id="learnPanel">
              <div class="learn-top">
                <div class="learn-title">처음 사용할 때는 로보킹이 집을 먼저 배워요</div>
                <div class="learn-pill" id="learnPill">초기 학습</div>
              </div>
              <div class="learn-desc">처음 한 번만 집 구조와 바닥 상태를 배워요.</div>
              <div class="learn-progress"><div class="learn-fill" id="learnFill"></div></div>
              <div class="learn-status" id="learnStatus">1회차 학습 청소를 시작하면 로보킹이 집 구조와 구역 정보를 자동으로 기록해요.</div>
              <div class="learn-steps" id="learnSteps"></div>
              <button type="button" class="learn-btn" id="learnBtn" data-action="startFirstMapping" onpointerdown="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);" onmousedown="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);" ontouchstart="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);" onclick="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);">🏠 1회차 학습 청소 시작</button>
            </div>
            <div class="condition-panel" id="conditionPanel">
              <div class="condition-title" id="conditionTitle">1회차 학습 청소로 우리 집 정보를 먼저 만들어요</div>

              <div id="firstLearnInputs">
                <div class="condition-help first-learn-note compact-note">
                  <div class="note-title">저장 항목</div>
                  <div class="profile-mini-grid">
                    <span>집 크기</span><span>청소 영역</span><span>면적</span>
                    <span>바닥 타입</span><span>오염도</span><span>배터리 사용</span>
                  </div>
                  <div class="note-caption">처음 청소하며 우리 집 환경을 저장해요.</div>
                </div>
              </div>

              <div id="predictionInputs" style="display:none;">
                <div class="condition-help">오늘 상태만 고르면 필요한 만큼 알아서 준비해요.</div>
                <div class="predict-condition-grid">
                  <label for="scopeSelect">청소 범위</label>
                  <select class="condition-select" id="scopeSelect">
                    <option value="home">집 전체</option>
                    <option value="1">1구역</option>
                    <option value="2">2구역</option>
                    <option value="3">3구역</option>
                    <option value="4">4구역</option>
                    <option value="5">5구역</option>
                  </select>
                  <label for="cleanModeSelect">청소 방식</label>
                  <select class="condition-select" id="cleanModeSelect">
                    <option value="dry">건식</option>
                    <option value="mop">물걸레</option>
                    <option value="both">건식+물걸레</option>
                  </select>
                  <label for="intensitySelect">청소 강도</label>
                  <select class="condition-select" id="intensitySelect">
                    <option value="fast">빠른</option>
                    <option value="standard" selected>표준</option>
                    <option value="careful">꼼꼼</option>
                  </select>
                  <label for="todayStateSelect">오늘 상태</label>
                  <select class="condition-select" id="todayStateSelect">
                    <option value="normal">평소와 같음</option>
                    <option value="dust">먼지 많음</option>
                    <option value="pet">반려동물 털 많음</option>
                    <option value="obstacle">바닥 물건 많음</option>
                  </select>
                </div>
              </div>

              <button class="predict-btn" id="predictBtn" data-action="predictSoc">🤖 오늘 청소 준비하기</button>
              <div class="predict-loading" id="predictLoading">1회차 학습 청소가 끝나면 오늘 청소 준비를 할 수 있어요.</div>
              <div class="flow-guide" id="flowGuide"><span class="guide-step">현재 단계</span>1회차 학습 청소로 집 정보를 먼저 저장해 주세요.</div>
            </div>
            <div class="scope-buttons">
              <button class="scope-btn active" id="scopeHome" data-action="selectHome">집 전체</button>
              <button class="scope-btn" id="scopeZone1" data-action="selectZone1">1구역</button>
              <button class="scope-btn" id="scopeZone2" data-action="selectZone2">2구역</button>
              <button class="scope-btn" id="scopeZone3" data-action="selectZone3">3구역</button>
              <button class="scope-btn" id="scopeZone4" data-action="selectZone4">4구역</button>
              <button class="scope-btn" id="scopeZone5" data-action="selectZone5">5구역</button>
            </div>
            <div class="selected-plan">
              <div class="plan-summary" id="planSummary">집 전체 청소 조건을 분석 중입니다.</div>
              <div class="plan-soc">
                <div class="plan-soc-label">충전 준비</div>
                <div class="plan-soc-value"><span id="planTargetSoc">81</span>%</div>
                <div class="plan-soc-sub" id="planSocSub">필요한 만큼만 충전</div>
              </div>
            </div>
            <button class="start-clean-primary" id="startCleanPrimary" data-action="clean" disabled>
              🧹 청소 미션 수행하기
              <small id="startCleanHint">준비가 끝나면 바로 시작할 수 있어요</small>
            </button>
          </div>

          <div class="actions">
            <button class="action-btn" data-action="feed"><span class="action-icon">🥣</span>먹여주기</button>
            <button class="action-btn" data-action="play"><span class="action-icon">🏐</span>놀아주기</button>
            <button class="action-btn" data-action="train"><span class="action-icon">🏋️</span>훈련하기</button>
            <button class="action-btn" data-action="photo"><span class="action-icon">📷</span>사진첩</button>
            <button class="action-btn" data-action="clean"><span class="action-icon">🏆</span>미션</button>
            <button class="action-btn" data-action="shop"><span class="action-icon">🛒</span>상점</button>
          </div>

          <div class="home-cards">
            <section class="mini-card">
              <div class="mini-title">배터리 컨디션</div>
              <div class="battery-info">너무 배부르거나<br>너무 배고프지 않게<br>로보킹이 알아서 관리해요!</div>
              <div class="battery-face" id="batteryFace">😊</div>
              <div class="scale"><div class="pointer" id="pointer"></div></div>
              <div class="scale-labels"><span>0%</span><span>15%</span><span>90%</span><span>100%</span></div>
              <div class="battery-message" id="batteryMessage">배터리 컨디션이 좋아요.</div>
            </section>

            <section class="mini-card time-card">
              <div class="mini-title">필요 청소 가능 시간</div>
              <div class="time-icon">🤖</div>
              <div class="time-number"><span id="cleanTime">45</span><small> 분</small></div>
              <div class="time-sub">현재 배터리 기준</div>
              <div class="time-tip" id="timeTip">현재 배터리로 청소가 가능합니다.</div>
            </section>

            <section class="mini-card food-card">
              <div class="food-title">오늘의 음식</div><div class="food-bowl"></div>
              <div class="food-count">보유량: <span id="foodText">1</span>개</div>
            </section>
          </div>
        </div>
      </section>

      <section class="page" id="batteryPage">
        <div class="section-kicker">BATTERY HEALTH</div>
        <div class="section-title">배터리 건강 돌보기</div>

        <div class="gauge-grid">
          <div class="panel gauge-card">
            <div class="gauge" id="socGauge" style="--value:81;--color:#49a646">
              <div class="gauge-content"><div class="gauge-label">배터리</div><div class="gauge-value" id="socGaugeText">81%</div></div>
            </div>
            <div class="gauge-desc">건강하게 쓰는<br>배터리 구간</div>
          </div>

          <div class="panel gauge-card">
            <div class="gauge" id="tempGauge" style="--value:40;--color:#ff7c22">
              <div class="gauge-content"><div class="gauge-label">온도</div><div class="gauge-value" id="tempGaugeText">29℃</div></div>
            </div>
            <div class="gauge-desc">안정 온도 구간<br>15℃~50℃</div>
          </div>
        </div>

        <div class="panel control">
          <div class="control-row">
            <div class="control-head"><span>맞춤 충전 조절</span><span class="control-value" id="targetLabel">81%</span></div>
            <input id="targetSlider" type="range" min="15" max="90" value="81">
            <div class="control-caption"><span>15%</span><span>오래 쓰기 추천</span><span>90%</span></div>
          </div>
          <div class="control-row">
            <div class="control-head"><span>온도 시뮬레이션</span><span class="control-value" id="tempLabel">29℃</span></div>
            <input id="tempSlider" type="range" min="15" max="50" value="29">
            <div class="control-caption"><span>15℃</span><span>현재 배터리 온도</span><span>50℃</span></div>
          </div>
          <button class="primary-btn" data-action="chargeFromBattery">로보킹 맞춤 충전하기</button>
        </div>

        <div class="panel chart-panel">
          <div class="panel-head"><div class="panel-title">오늘 배터리 변화</div><div class="badge">과충전 방지</div></div>
          <svg class="soc-chart" viewBox="0 0 340 165">
            <line class="grid-line" x1="30" y1="28" x2="330" y2="28"></line>
            <line class="grid-line" x1="30" y1="132" x2="330" y2="132"></line>
            <text class="chart-text" x="3" y="32">90%</text><text class="chart-text" x="5" y="136">15%</text>
            <polyline class="line-red" points="30,128 80,102 128,54 180,35 235,31 285,29 328,28"></polyline>
            <polyline class="line-green" id="aiLine" points="30,128 80,103 128,82 180,74 235,74 285,74 328,74"></polyline>
          </svg>
          <div class="legend">
            <span><span class="dot" style="background:#eb6650"></span>기존 완충 방식</span>
            <span><span class="dot" style="background:#4c9a43"></span>맞춤 충전</span>
          </div>
        </div>

        <div class="panel insight"><div class="insight-row"><div class="insight-icon">💡</div><div id="insightText">최근 청소 패턴을 분석한 결과, 오늘은 배터리 81%까지만 충전해도 필요 청소를 완료할 수 있습니다.</div></div></div>
      </section>

      <section class="page" id="recordPage">
        <div class="section-kicker">ACTIVITY LOG</div>
        <div class="section-title">청소 활동 기록</div>

        <div class="panel weekly">
          <div class="panel-head"><div class="panel-title">주간 청소 시간</div><div style="font-size:10px;font-weight:900">평균 <span id="avgText">38</span>분</div></div>
          <div class="bar-chart">
            <div class="bar-item"><div class="bar-value">25</div><div class="bar" style="height:42%"></div><div class="bar-label">월</div></div>
            <div class="bar-item"><div class="bar-value">41</div><div class="bar" style="height:68%"></div><div class="bar-label">화</div></div>
            <div class="bar-item"><div class="bar-value">34</div><div class="bar" style="height:56%"></div><div class="bar-label">수</div></div>
            <div class="bar-item"><div class="bar-value">49</div><div class="bar" style="height:81%"></div><div class="bar-label">목</div></div>
            <div class="bar-item"><div class="bar-value">40</div><div class="bar" style="height:66%"></div><div class="bar-label">금</div></div>
            <div class="bar-item"><div class="bar-value">57</div><div class="bar" style="height:94%"></div><div class="bar-label">토</div></div>
            <div class="bar-item"><div class="bar-value" id="sunValue">34</div><div class="bar" id="sunBar" style="height:56%"></div><div class="bar-label">일</div></div>
          </div>
        </div>

        <div class="record-grid">
          <div class="record-card"><div class="record-label">이번 주 청소 면적</div><div class="record-value"><span id="areaText">72</span>㎡</div></div>
          <div class="record-card"><div class="record-label">평균 청소 시간</div><div class="record-value"><span id="recordAvgText">38</span>분</div></div>
          <div class="record-card"><div class="record-label">고온 복귀</div><div class="record-value">0회</div></div>
          <div class="record-card"><div class="record-label">맞춤 충전 수락</div><div class="record-value"><span id="acceptText">4</span>회</div></div>
        </div>

        <div class="panel events">
          <div class="panel-title">이벤트 기록</div>
          <div id="eventList">
            <div class="event-item"><div class="event-time">14:20</div><div class="event-content"><strong>맞춤 충전 완료</strong><span>필요한 만큼만 채우고 자동으로 멈췄습니다.</span></div></div>
            <div class="event-item"><div class="event-time">10:15</div><div class="event-content"><strong>청소 준비 완료</strong><span>거실 상태에 맞춰 로보킹이 준비했습니다.</span></div></div>
            <div class="event-item"><div class="event-time">08:40</div><div class="event-content"><strong>배터리 컨디션 정상</strong><span>배터리 온도와 건강도가 안정 범위에 있습니다.</span></div></div>
          </div>
        </div>
      </section>

      <section class="page" id="eventPage">
        <div class="section-kicker">EVENT</div>
        <div class="section-title">이벤트</div>

        <div class="panel event-hero">
          <div class="event-hero-title">이벤트 페이지 준비 중</div>
          <div class="event-hero-desc">
            이 페이지는 팀원이 추가로 수정할 공간이에요.<br>
            앞으로 부품 상태 확인, 배터리 케어 내역, 출퇴근 맞춤 청소, 미션, 사진첩 같은 기능을 이곳에 확장할 수 있어요.
          </div>
        </div>

        <div class="event-placeholder-grid">
          <div class="event-placeholder-card">
            <div class="event-placeholder-icon">🧩</div>
            <div class="event-placeholder-title">부품 상태 확인</div>
            <div class="event-placeholder-text">필터, 브러시, 물걸레 패드 상태를 보여줄 예정이에요.</div>
          </div>
          <div class="event-placeholder-card">
            <div class="event-placeholder-icon">📌</div>
            <div class="event-placeholder-title">케어 이벤트 기록</div>
            <div class="event-placeholder-text">배터리를 어떻게 아껴 썼는지 내역으로 남길 예정이에요.</div>
          </div>
          <div class="event-placeholder-card">
            <div class="event-placeholder-icon">🚶</div>
            <div class="event-placeholder-title">출퇴근 맞춤 청소</div>
            <div class="event-placeholder-text">사용자의 생활 패턴에 맞춘 청소 예약 기능을 넣을 수 있어요.</div>
          </div>
          <div class="event-placeholder-card">
            <div class="event-placeholder-icon">📷</div>
            <div class="event-placeholder-title">미션·사진첩</div>
            <div class="event-placeholder-text">오늘의 미션과 분실물 사진첩을 연결할 수 있어요.</div>
          </div>
        </div>
      </section>

      <section class="page" id="rewardPage">
        <div class="section-kicker">REWARD</div>
        <div class="section-title">로보킹 성장 리워드</div>

        <div class="panel level-panel">
          <div class="level-robot-preview" id="levelRobotPreview"><span class="preview-base">🤖</span></div>
          <div class="level-number">Lv. <span id="levelText">13</span></div>
          <div class="level-track"><div class="level-fill" id="expFill"></div></div>
          <div class="level-caption">경험치 <span id="expText">55</span> / 100</div>
        </div>

        <div class="reward-folder-tabs">
          <button class="reward-folder-btn active" id="rewardTabItems" data-action="rewardTabItems">꾸미기 아이템</button>
          <button class="reward-folder-btn" id="rewardTabCoupons" data-action="rewardTabCoupons">LG 혜택 쿠폰</button>
        </div>

        <div class="reward-panel" id="rewardItemsPanel">
          <div class="reward-grid">
            <div class="reward-card" id="cardFood"><div class="reward-icon">🥣</div><div class="reward-title">에너지 간식</div><div class="reward-desc">먹으면 배터리가 조금 회복돼요.</div><div class="reward-status" id="statusFood"></div><button class="reward-btn" id="btnFood" data-action="buyFood">50 코인</button></div>
            <div class="reward-card" id="cardRibbon"><div class="reward-icon">🎀</div><div class="reward-title">빨간 리본</div><div class="reward-desc">머리 위에 귀엽게 달아줘요.</div><div class="reward-status" id="statusRibbon"></div><button class="reward-btn" id="btnRibbon" data-action="itemRibbon">60 코인</button></div>
            <div class="reward-card" id="cardHat"><div class="reward-icon">🧢</div><div class="reward-title">탐험가 모자</div><div class="reward-desc">로보킹 머리에 딱 맞게 씌워줘요.</div><div class="reward-status" id="statusHat"></div><button class="reward-btn" id="btnHat" data-action="itemHat">120 코인</button></div>
            <div class="reward-card" id="cardSparkle"><div class="reward-icon">✨</div><div class="reward-title">반짝이 오라</div><div class="reward-desc">로보킹 주변이 반짝여요.</div><div class="reward-status" id="statusSparkle"></div><button class="reward-btn" id="btnSparkle" data-action="itemSparkle">80 코인</button></div>
            <div class="reward-card" id="cardBunny"><div class="reward-icon">🐰</div><div class="reward-title">토끼 귀</div><div class="reward-desc">로보킹 머리에 토끼 귀가 쏙!</div><div class="reward-status" id="statusBunny"></div><button class="reward-btn" id="btnBunny" data-action="itemBunny">90 코인</button></div>
            <div class="reward-card" id="cardCat"><div class="reward-icon">🐱</div><div class="reward-title">고양이 귀</div><div class="reward-desc">새침한 고양이 로보킹으로 변신!</div><div class="reward-status" id="statusCat"></div><button class="reward-btn" id="btnCat" data-action="itemCat">70 코인</button></div>
          </div>
        </div>

        <div class="reward-panel hidden" id="rewardCouponsPanel">
          <div class="reward-grid">
            <div class="reward-card coupon-card" id="cardCouponLg5"><div class="reward-icon">🎟</div><div class="reward-title">LG 생활가전 5% 쿠폰</div><div class="reward-desc">LG 생활가전 1개를 구매할 때 사용할 수 있는 기본 할인 쿠폰이에요.</div><div class="coupon-benefit">혜택: 단일 제품 5% 할인</div><div class="reward-status" id="statusCouponLg5"></div><button class="reward-btn" id="btnCouponLg5" data-action="couponLg5">300 코인</button></div>
            <div class="reward-card coupon-card" id="cardCouponCleanKit"><div class="reward-icon">🧹</div><div class="reward-title">로보킹 클린 키트 쿠폰</div><div class="reward-desc">필터, 브러시, 물걸레 패드처럼 자주 바꾸는 소모품을 준비할 때 사용해요.</div><div class="coupon-benefit">혜택: 소모품 키트 구매 할인</div><div class="reward-status" id="statusCouponCleanKit"></div><button class="reward-btn" id="btnCouponCleanKit" data-action="couponCleanKit">180 코인</button></div>
            <div class="reward-card coupon-card" id="cardCouponBatteryCare"><div class="reward-icon">🔋</div><div class="reward-title">배터리 케어 쿠폰</div><div class="reward-desc">로보킹을 오래 쓰기 위해 배터리 점검이나 관리 서비스를 받을 때 사용해요.</div><div class="coupon-benefit">혜택: 배터리 점검/케어 서비스</div><div class="reward-status" id="statusCouponBatteryCare"></div><button class="reward-btn" id="btnCouponBatteryCare" data-action="couponBatteryCare">250 코인</button></div>
            <div class="reward-card coupon-card" id="cardCouponMoveIn"><div class="reward-icon">🏠</div><div class="reward-title">이사·입주 패키지 쿠폰</div><div class="reward-desc">새집에 필요한 LG 생활가전을 2개 이상 함께 구매할 때 추가 혜택을 받아요.</div><div class="coupon-benefit">혜택: 2개 이상 구매 시 패키지 추가 할인</div><div class="reward-status" id="statusCouponMoveIn"></div><button class="reward-btn" id="btnCouponMoveIn" data-action="couponMoveIn">300 코인</button></div>
          </div>
        </div>
      </section>

    </main>

    <div class="modal" id="modal">
      <div class="modal-card">
        <div class="modal-title" id="modalTitle"></div>
        <div class="modal-body" id="modalBody"></div>
        <div class="modal-actions single" id="modalActions">
          <button class="modal-btn modal-secondary" id="modalCancel">취소</button>
          <button class="modal-btn modal-primary" id="modalConfirm">확인</button>
        </div>
      </div>
    </div>
    <div class="toast" id="toast"></div>
  </div>
</div>

<script>
"use strict";

const predictionData = __UI_PREDICTION_DATA__;
let activeRun = null;
const mappingSteps=[
  {key:'map',label:'집 구조 매핑'},
  {key:'area',label:'구역별 면적 저장'},
  {key:'floor',label:'바닥 타입 인식'},
  {key:'dirt',label:'오염도 기록'},
  {key:'obstacle',label:'장애물 수준 기록'},
  {key:'soc',label:'배터리 사용 기록'}
];

const $=(id)=>document.getElementById(id);
const clamp=(v,min,max)=>Math.min(Math.max(v,min),max);
const fmtSoc=(v)=>Number(v || 0).toFixed(1).replace(/\.0$/,"");
const cleanMinutes=()=>Math.max(0,Math.round(state.soc*.56));

// ============================================================
// 배터리 보호/학습 주행 기준값
// 최근 UX 문구 수정 과정에서 이 상수들이 빠지면
// 1회차 학습 버튼 클릭 시 startFirstMapping() 내부에서 ReferenceError가 발생합니다.
// 그래서 사용자에게 숫자를 직접 노출하지 않더라도, 내부 로직에는 반드시 유지합니다.
// ============================================================
const MIN_RESERVE_SOC = 15;
const MAX_CHARGE_SOC = 90;
const MAX_SINGLE_PASS_USE = MAX_CHARGE_SOC - MIN_RESERVE_SOC;
const CRITICAL_DOCK_SOC = MIN_RESERVE_SOC;
const targetFromRequired = (required)=>clamp(Math.ceil(Number(required||0)+MIN_RESERVE_SOC),MIN_RESERVE_SOC,MAX_CHARGE_SOC);
const expectedEndSoc = (startSoc,required)=>Math.round((Number(startSoc||0)-Number(required||0))*10)/10;

const MIN_SOC_AFTER_LEARNING = MIN_RESERVE_SOC;
const MIN_LEARNING_SOC_USE = 5;
const MAX_LEARNING_SOC_USE = 30;
const LEARNING_SOC_RATIO = 0.35;

function setGuide(message,tone="normal"){
  state.userGuide=message;
  state.userGuideTone=tone;
  const guide=$('flowGuide');
  if(guide){
    guide.className="flow-guide"+(tone&&tone!=="normal"?" "+tone:"");
    guide.innerHTML="<span class='guide-step'>다음 안내</span>"+message;
  }
}
function guideForCurrentState(){
  if(state.mapping)return "로보킹이 우리 집을 배우는 중이에요. 집 구조와 바닥 상태를 차근차근 기억하고 있어요.";
  if(!state.profileReady)return "<b>1단계</b> 먼저 1회차 학습 청소로 우리 집을 알려주세요.";
  if(state.profileReady && !state.predicted)return "<b>2단계</b> 오늘 청소 조건을 고르면 로보킹이 알아서 준비해요.";
  if(state.charging)return "로보킹이 잠깐 쉬면서 힘을 채우고 있어요. 필요한 만큼 채우면 알아서 멈춰요.";
  if(state.cleaning)return "청소 중이에요. 배터리가 무리하지 않도록 로보킹이 알아서 조절하고 있어요.";
  if(state.celebrating || state.missionDone)return "청소가 끝났어요! 로보킹이 배터리를 아끼며 마무리했어요.";
  if(state.predicted && state.soc<state.targetSoc)return "<b>3단계</b> 준비가 끝났어요. 같은 버튼을 한 번 더 누르면 필요한 만큼만 충전하고 바로 출발해요.";
  if(state.predicted)return "<b>3단계</b> 지금 바로 출동할 수 있어요. 같은 버튼을 한 번 더 누르면 바로 청소를 시작해요.";
  return state.userGuide||"현재 상태를 확인 중입니다.";
}

function getLearningSocUse(run,startSoc){
  const fullRequired=Math.max(0,Number(run&&run.home?run.home.requiredSoc:0));
  const available=Math.max(0,Number(startSoc||0)-MIN_SOC_AFTER_LEARNING);
  if(fullRequired<=0 || available<=0)return 0;
  let mappedUse=fullRequired*LEARNING_SOC_RATIO;
  mappedUse=Math.max(MIN_LEARNING_SOC_USE,mappedUse);
  mappedUse=Math.min(mappedUse,MAX_LEARNING_SOC_USE,fullRequired,available);
  return Math.round(mappedUse*10)/10;
}

const cleanModeLabels={dry:"건식",mop:"물걸레",both:"건식+물걸레"};
const intensityLabels={fast:"빠른",standard:"표준",careful:"꼼꼼"};
const todayStateLabels={normal:"평소와 같음",dust:"먼지 많음",pet:"반려동물 털 많음",obstacle:"바닥 물건 많음"};
// 아래 선택값은 배율을 곱하는 보정계수가 아니라,
// 기록 안에서 조건이 가장 가까운 우리 집 기록 준비 행을 찾기 위한 검색 조건으로 사용됩니다.
const intensityAliases={fast:["약","중"],standard:["중","강"],careful:["강","터보"]};
const todayStateAliases={normal:"학습 프로필 기준",dust:"오염도 높은 조건",pet:"오염도 높음 + 강한 흡입 조건",obstacle:"장애물 많은 조건"};

const closetDefault={
  owned:{ribbon:false,hat:false,bunny:false,cat:false,sparkle:false},
  equipped:{head:"crown",aura:null}
};
const shopItems={
  ribbon:{name:"빨간 리본",icon:"🎀",cost:60,slot:"head",value:"ribbon",message:"빨간 리본을 달아줬어요! 로보킹이 더 사랑스러워졌어요."},
  hat:{name:"탐험가 모자",icon:"🧢",cost:120,slot:"head",value:"hat",message:"탐험가 모자를 씌워줬어요! 이제 진짜 모험가 로보킹이에요."},
  bunny:{name:"토끼 귀",icon:"🐰",cost:90,slot:"head",value:"bunny",message:"토끼 귀를 달아줬어요! 로보킹이 통통 튀는 기분이에요."},
  cat:{name:"고양이 귀",icon:"🐱",cost:70,slot:"head",value:"cat",message:"고양이 귀를 달아줬어요! 로보킹이 더 새침해졌어요."},
  sparkle:{name:"반짝이 오라",icon:"✨",cost:80,slot:"aura",value:"sparkle",message:"반짝이 오라를 켰어요! 청소할 때마다 기분이 좋아져요."}
};

const couponItems={
  lg5:{name:"LG 생활가전 5% 쿠폰",icon:"🎟",cost:300,benefit:"LG 생활가전 1개 구매 시 5% 할인",message:"LG 생활가전 5% 쿠폰을 보관함에 담았어요."},
  cleanKit:{name:"로보킹 클린 키트 쿠폰",icon:"🧹",cost:180,benefit:"필터·브러시·물걸레 패드 등 소모품 키트 할인",message:"로보킹 클린 키트 쿠폰을 보관함에 담았어요."},
  batteryCare:{name:"배터리 케어 쿠폰",icon:"🔋",cost:250,benefit:"배터리 점검 또는 관리 서비스 혜택",message:"배터리 케어 쿠폰을 보관함에 담았어요."},
  moveIn:{name:"이사·입주 패키지 쿠폰",icon:"🏠",cost:300,benefit:"LG 생활가전 2개 이상 구매 시 패키지 추가 혜택",message:"이사·입주 패키지 쿠폰을 보관함에 담았어요."}
};
function loadCoupons(){
  try{
    const raw=localStorage.getItem("lgRoboCareCouponsV1");
    const defaults={lg5:0,cleanKit:0,batteryCare:0,moveIn:0};
    if(!raw)return defaults;
    return Object.assign(defaults,JSON.parse(raw)||{});
  }catch(e){return {lg5:0,cleanKit:0,batteryCare:0,moveIn:0};}
}
function saveCoupons(){
  try{localStorage.setItem("lgRoboCareCouponsV1",JSON.stringify(state.ownedCoupons));}catch(e){}
}

function loadCloset(){
  try{
    const raw=localStorage.getItem("lgRoboCareClosetV2");
    if(!raw)return JSON.parse(JSON.stringify(closetDefault));
    const saved=JSON.parse(raw);
    const owned=Object.assign({},closetDefault.owned,saved.owned||{});
    // 이전 버전에서 하트 스티커를 샀다면 고양이 귀 보유로 자연스럽게 이전합니다.
    if(saved.owned && saved.owned.heart && !owned.cat)owned.cat=true;
    const equipped=Object.assign({},closetDefault.equipped,saved.equipped||{});
    if(equipped.decal==="heart" && (!equipped.head || equipped.head==="crown"))equipped.head="cat";
    delete equipped.decal;
    return {owned,equipped};
  }catch(e){return JSON.parse(JSON.stringify(closetDefault));}
}
function saveCloset(){
  try{localStorage.setItem("lgRoboCareClosetV2",JSON.stringify({owned:state.ownedItems,equipped:state.equippedItems}));}catch(e){}
}
const initialCloset=loadCloset();
const initialCoupons=loadCoupons();

function pickRandomRun(candidates){
  if(!candidates || candidates.length===0)return null;

  // 현재 화면에 떠 있는 global_run_id와 같은 시나리오는 가능하면 제외
  // 같은 조건으로 1회차 학습 청소를 다시 실행할 때 매번 다른 집 정보가 나오게 하기 위함
  let pool = candidates;
  if(activeRun && activeRun.globalRunId && candidates.length>1){
    const filtered = candidates.filter(r=>String(r.globalRunId)!==String(activeRun.globalRunId));
    if(filtered.length>0)pool = filtered;
  }

  const idx = Math.floor(Math.random()*pool.length);
  return pool[idx];
}

function findRun(areaPyung, mopEnabled){
  const area = Number(areaPyung);
  const mop = Boolean(mopEnabled);

  // 1순위: 사용자가 선택한 평수 + 청소방식이 모두 같은 기록 시나리오 중 랜덤 선택
  let candidates = predictionData.runs.filter(r=>Number(r.areaPyung)===area && Boolean(r.mopEnabled)===mop);
  let run = pickRandomRun(candidates);

  // 2순위: 청소방식까지 완전히 맞는 데이터가 없으면, 같은 평수 안에서 랜덤 선택
  if(!run){
    candidates = predictionData.runs.filter(r=>Number(r.areaPyung)===area);
    run = pickRandomRun(candidates);
  }

  // 3순위: 같은 평수도 없으면 전체 기록 중 랜덤 선택
  if(!run){
    run = pickRandomRun(predictionData.runs);
  }

  return run || predictionData.runs[0];
}

activeRun = pickRandomRun(predictionData.runs) || predictionData.runs[0];

const state={
  page:"homePage",
  soc:predictionData.currentSoc,
  targetSoc:activeRun.home.targetSoc,
  requiredSoc:activeRun.home.requiredSoc,
  selectedScope:"home",
  selectedZone:null,
  selectedLabel:activeRun.home.label,
  selectedScenario:activeRun.home,
  modelName:activeRun.home.modelName,
  globalRunId:activeRun.home.globalRunId,
  areaPyung:activeRun.home.areaPyung,
  cleaningAreaM2:activeRun.home.cleaningAreaM2,
  cleaningType:activeRun.home.cleaningType,
  mopEnabled:activeRun.home.mopEnabled,
  obstacleLevel:activeRun.home.obstacleLevel,
  floorType:activeRun.home.floorType,
  dirtLevel:activeRun.home.dirtLevel,
  suctionMode:activeRun.home.suctionMode,
  cleanModeChoice:activeRun.home.mopEnabled?'mop':'dry',
  cleanModeLabel:activeRun.home.cleaningType,
  intensityChoice:'standard',
  intensityLabel:'표준',
  todayStateChoice:'normal',
  todayStateLabel:'평소와 같음',
  matchNote:"우리 집 기록으로 맞춤 준비",
  matchBasis:"오늘 상태 반영",
  cleaningRemainingSoc:activeRun.home.requiredSoc,
  cleaningSegmentIndex:0,
  splitCleaning:false,
  pendingCleanAfterCharge:false,
  chargeComplete:false,
  predicting:false,
  predicted:false,
  userGuide:"1회차 학습 청소로 집 크기, 구역, 바닥, 오염도, 배터리 사용을 저장해 주세요.",
  userGuideTone:"normal",
  profileReady:false,
  mapping:false,
  mappingProgress:0,
  mappingStepIndex:-1,
  firstRunSocUsed:0,
  firstRunRequiredSoc:0,
  firstRunFullRequiredSoc:0,
  firstRunStartSoc:predictionData.currentSoc,
  firstRunEndSoc:predictionData.currentSoc,
  firstRunSocEnough:true,
  ownedItems:initialCloset.owned,
  equippedItems:initialCloset.equipped,
  rewardTab:"items",
  ownedCoupons:initialCoupons,
  temperature:29,health:100,heart:100,
  level:13,exp:55,coins:50,food:1,cleaning:false,charging:false,
  celebrating:false,progress:0,missionDone:false,cleanCount:0,
  acceptCount:4,area:activeRun.home.cleaningAreaM2||72,average:38
};

function populateConditionSelectors(){
  refreshScopeSelect();
  const cleanModeSelect=$('cleanModeSelect');
  if(cleanModeSelect)cleanModeSelect.value=activeRun.mopEnabled?'mop':'dry';
  const scopeSelect=$('scopeSelect');
  if(scopeSelect)scopeSelect.value='home';
  const intensitySelect=$('intensitySelect');
  if(intensitySelect)intensitySelect.value='standard';
  const todayStateSelect=$('todayStateSelect');
  if(todayStateSelect)todayStateSelect.value='normal';
}

function switchPage(pageId){
  document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(b=>b.classList.toggle("active",b.dataset.page===pageId));
  $(pageId).classList.add("active");
  state.page=pageId;
  render();
}

function render(){
  state.soc=clamp(Math.round(state.soc),0,100);
  state.targetSoc=clamp(Math.round(state.targetSoc),15,90);
  state.temperature=Math.round(state.temperature*10)/10;
  state.exp=clamp(Math.round(state.exp),0,100);

  $("coinText").textContent=String(state.coins).padStart(3,"0");
  $("foodText").textContent=state.food;
  $("cleanTime").textContent=cleanMinutes();
  $("pointer").style.left=state.soc+"%";
  $("cleanFill").style.width=state.progress+"%";
  $("missionFill").style.width=state.missionDone?"100%":state.progress+"%";
  const robotSocBadge=$("robotSocBadge");
  if(robotSocBadge){
    const socState=state.soc<15?"low":(state.soc<state.targetSoc?"need":"ok");
    robotSocBadge.className="robot-soc-badge "+socState;
    robotSocBadge.innerHTML="<span>🔋 현재 배터리</span><b>"+state.soc+"%</b>";
  }

  renderAccessories();renderPlan();renderHome();renderBattery();renderRecord();renderReward();
}

function getScenario(scope,zoneNumber=null){
  if(scope==="home")return activeRun.home;
  const zones=(activeRun && activeRun.zones) ? activeRun.zones : [];
  const direct=zones.find(z=>Number(z.zone)===Number(zoneNumber)) || zones[zoneNumber-1];
  if(direct)return direct;

  // 혹시 예전 CSV/캐시로 해당 영역 데이터가 아직 없으면 가장 가까운 영역 데이터를 임시로 사용합니다.
  // 새 4/6/8구역 CSV로 교체되면 실제 해당 영역 데이터가 자동으로 잡힙니다.
  if(zones.length){
    const idx=Math.min(Math.max(Number(zoneNumber||1)-1,0),zones.length-1);
    return zones[idx];
  }
  return activeRun.home;
}

function getPredictionChoices(scopeOverride=null,zoneOverride=null){
  const scopeSelect=$('scopeSelect');
  const cleanModeSelect=$('cleanModeSelect');
  const intensitySelect=$('intensitySelect');
  const todayStateSelect=$('todayStateSelect');
  const scopeValue=scopeOverride? (scopeOverride==="home"?"home":String(zoneOverride||1)) : (scopeSelect?scopeSelect.value:"home");
  return {
    scopeValue,
    scope:scopeValue==="home"?"home":"zone",
    zoneNumber:scopeValue==="home"?null:Number(scopeValue),
    cleanMode:cleanModeSelect?cleanModeSelect.value:(activeRun.home.mopEnabled?'mop':'dry'),
    intensity:intensitySelect?intensitySelect.value:'standard',
    todayState:todayStateSelect?todayStateSelect.value:'normal'
  };
}

function getBaseScenarioFromChoices(choices){
  if(choices.scope==="home")return activeRun.home;
  return getScenario("zone",choices.zoneNumber);
}

function getCleanModeCandidateValue(scenario){
  const txt=String(scenario.cleaningType||"");
  if(txt.includes("건식+물걸레")||txt.includes("복합")||txt.includes("both"))return "both";
  if(scenario.mopEnabled || txt.includes("물걸레") || txt.toLowerCase().includes("mop"))return "mop";
  return "dry";
}

function cleanModeScore(scenario,choice){
  const v=getCleanModeCandidateValue(scenario);
  if(choice===v)return 120;
  // 데이터셋에 건식+물걸레가 없을 수 있으므로, 복합 청소는 물걸레 조건을 가장 가까운 후보로 인정합니다.
  if(choice==="both" && v==="mop")return 70;
  return -260;
}

function suctionPreferenceScore(scenario,intensity){
  const mode=String(scenario.suctionMode||"");
  const code=Number(scenario.suctionCode||scenario.suctionMaxCode||0);
  if(intensity==="fast"){
    if(mode.includes("약"))return 80;
    if(mode.includes("중"))return 50;
    if(code && code<=2)return 60;
    return -25;
  }
  if(intensity==="careful"){
    if(mode.includes("터보"))return 90;
    if(mode.includes("강"))return 65;
    if(code && code>=3)return 70;
    return -20;
  }
  // 표준은 중/강 또는 학습 프로필과 가까운 후보를 우선합니다.
  if(mode.includes("중"))return 70;
  if(mode.includes("강"))return 45;
  if(code && code>=2 && code<=3)return 55;
  return 10;
}

function todayStateScore(scenario,choice,baseScenario){
  const dirt=Number(scenario.dirtCode||scenario.dirtMaxCode||0);
  const dirtMax=Number(scenario.dirtMaxCode||dirt||0);
  const obs=Number(scenario.obstacleLevelCode||0);
  const suction=Number(scenario.suctionCode||scenario.suctionMaxCode||0);
  const mode=String(scenario.suctionMode||"");
  const baseDirt=Number(baseScenario.dirtCode||baseScenario.dirtMaxCode||0);
  const baseObs=Number(baseScenario.obstacleLevelCode||0);

  if(choice==="dust"){
    if(dirtMax>=3 || dirt>=3 || String(scenario.dirtLevel||"").includes("높"))return 100;
    if(dirt>=2)return 45;
    return -20;
  }
  if(choice==="pet"){
    let score=0;
    if(dirtMax>=3 || dirt>=3 || String(scenario.dirtLevel||"").includes("높"))score+=60;
    if(suction>=3 || mode.includes("강") || mode.includes("터보"))score+=60;
    return score || -20;
  }
  if(choice==="obstacle"){
    if(obs>=3 || String(scenario.obstacleLevel||"").includes("높"))return 100;
    if(obs>=2 || String(scenario.obstacleLevel||"").includes("중"))return 45;
    return -20;
  }
  // 평소와 같음은 1회차 학습 프로필의 오염도/장애물 수준과 가까운 후보를 우선합니다.
  return 70 - Math.abs((dirt||baseDirt)-baseDirt)*12 - Math.abs((obs||baseObs)-baseObs)*12;
}

function scenarioPoolForChoices(choices){
  if(!predictionData.runs || !predictionData.runs.length)return [];
  if(choices.scope==="home"){
    return predictionData.runs.map(r=>r.home).filter(Boolean);
  }
  const zoneNo=Number(choices.zoneNumber||1);
  const pool=[];
  predictionData.runs.forEach(r=>{
    const z=(r.zones||[]).find(item=>Number(item.zone)===zoneNo);
    if(z)pool.push(z);
  });
  return pool;
}

function scoreScenarioForChoices(scenario,choices,baseScenario){
  let score=0;
  score+=cleanModeScore(scenario,choices.cleanMode);
  score+=suctionPreferenceScore(scenario,choices.intensity);
  score+=todayStateScore(scenario,choices.todayState,baseScenario);

  // 1회차 학습한 우리 집 정보과 최대한 가까운 후보를 우선합니다.
  if(Number(scenario.areaPyung)===Number(activeRun.home.areaPyung))score+=180;
  else score-=Math.abs(Number(scenario.areaPyung||0)-Number(activeRun.home.areaPyung||0))*4;

  if(choices.scope==="zone"){
    if(Number(scenario.zone)===Number(choices.zoneNumber))score+=80;
    if(baseScenario.floorType && scenario.floorType===baseScenario.floorType)score+=90;
    else if(baseScenario.floorType && scenario.floorType)score-=35;
    score-=Math.abs(Number(scenario.cleaningAreaM2||0)-Number(baseScenario.cleaningAreaM2||0))*1.5;
  }else{
    score-=Math.abs(Number(scenario.cleaningAreaM2||0)-Number(activeRun.home.cleaningAreaM2||0))*.25;
  }

  // 동점 방지를 위한 아주 작은 랜덤값. 조건 점수 자체에는 영향이 거의 없습니다.
  score+=Math.random()*0.01;
  return score;
}

function findMlScenarioFromChoices(choices){
  const baseScenario=getBaseScenarioFromChoices(choices);
  const pool=scenarioPoolForChoices(choices);
  if(!pool.length){
    const fallback=Object.assign({},baseScenario);
    fallback.matchNote="저장된 우리 집 기록으로 준비";
    return fallback;
  }

  let best=null;
  let bestScore=-Infinity;
  pool.forEach(candidate=>{
    const score=scoreScenarioForChoices(candidate,choices,baseScenario);
    if(score>bestScore){bestScore=score;best=candidate;}
  });

  const scenario=Object.assign({},best||baseScenario);
  scenario.scope=choices.scope;
  if(choices.scope==="zone"){
    scenario.zone=Number(choices.zoneNumber||scenario.zone||1);
    scenario.label=scenario.zone+"구역";
  }else{
    scenario.label="집 전체";
  }
  scenario.cleanModeChoice=choices.cleanMode;
  scenario.cleanModeLabel=cleanModeLabels[choices.cleanMode]||scenario.cleaningType;
  scenario.intensityChoice=choices.intensity;
  scenario.intensityLabel=intensityLabels[choices.intensity]||"표준";
  scenario.todayStateChoice=choices.todayState;
  scenario.todayStateLabel=todayStateLabels[choices.todayState]||"평소와 같음";
  scenario.targetSoc=targetFromRequired(scenario.requiredSoc);
  scenario.matchNote="오늘 상태에 맞춰 로보킹이 준비";
  scenario.matchBasis="청소 방식·오염도·장애물 상태 반영";

  if(choices.cleanMode==="both" && getCleanModeCandidateValue(scenario)!=="both"){
    scenario.matchNote="비슷한 청소 기록으로 준비";
  }
  return scenario;
}

function syncScenarioToState(scenario){
  state.selectedScenario=scenario;
  state.selectedScope=scenario.scope;
  state.selectedZone=scenario.scope==="zone"?scenario.zone:null;
  state.selectedLabel=scenario.label;
  state.requiredSoc=Number(scenario.requiredSoc);
  state.targetSoc=Number(scenario.targetSoc);
  state.modelName=scenario.modelName;
  state.globalRunId=scenario.globalRunId;
  state.areaPyung=scenario.areaPyung;
  state.cleaningAreaM2=scenario.cleaningAreaM2;
  state.cleaningType=scenario.cleaningType;
  state.mopEnabled=Boolean(scenario.mopEnabled);
  state.obstacleLevel=scenario.obstacleLevel;
  state.floorType=scenario.floorType;
  state.dirtLevel=scenario.dirtLevel;
  state.suctionMode=scenario.suctionMode;
  state.cleanModeChoice=scenario.cleanModeChoice||state.cleanModeChoice;
  state.cleanModeLabel=scenario.cleanModeLabel||scenario.cleaningType||state.cleaningType;
  state.intensityChoice=scenario.intensityChoice||state.intensityChoice;
  state.intensityLabel=scenario.intensityLabel||state.intensityLabel;
  state.todayStateChoice=scenario.todayStateChoice||state.todayStateChoice;
  state.todayStateLabel=scenario.todayStateLabel||state.todayStateLabel;
  state.matchNote=scenario.matchNote||"우리 집 기록으로 맞춤 준비";
  state.matchBasis=scenario.matchBasis||"오늘 상태 반영";
  state.cleaningRemainingSoc=Number(state.requiredSoc||0);
  state.cleaningSegmentIndex=0;
  state.splitCleaning=state.requiredSoc>MAX_SINGLE_PASS_USE;
  state.progress=0;
  state.missionDone=false;
  state.area=scenario.cleaningAreaM2||state.area;
}

function predictSocFromConditions(){
  if(state.cleaning||state.charging||state.mapping){showToast("학습/청소/충전이 끝난 뒤 다시 준비할 수 있어요.");return}

  // 오늘 청소 준비가 끝난 뒤에는 같은 버튼이 바로 실행 버튼 역할을 합니다.
  // 사용자가 화면 아래로 다시 스크롤하지 않도록, 준비 버튼 하나에서 충전/청소까지 이어집니다.
  if(state.profileReady && state.predicted && !state.predicting){
    if(state.soc < state.targetSoc){
      if(Number(state.requiredSoc||0)>MAX_SINGLE_PASS_USE && state.soc<MAX_CHARGE_SOC){
        showSplitCleaningModal();
      }else{
        chargeRobot(true);
      }
    }else{
      startCleaning();
    }
    return;
  }

  if(!state.profileReady){
    setGuide("아직 로보킹이 우리 집을 잘 몰라요. 먼저 1회차 학습 청소를 시작해 주세요.","warning");
    showToast("먼저 로보킹에게 우리 집을 알려주세요.");
    $("speech").innerHTML="<strong style='color:#ef8c32'>아직 학습 전이에요!</strong><br>먼저 우리 집을 알려주세요.";
    $("modeChip").textContent="🏠 1회차 학습 필요";
    switchPage("homePage");
    return;
  }
  const choices=getPredictionChoices();
  const matchedScenario=findMlScenarioFromChoices(choices);
  const loading=$('predictLoading');
  state.predicting=true;
  if(loading){loading.textContent="로보킹이 오늘 청소를 준비하고 있어요...";loading.classList.add('active');}
  $("speech").innerHTML="<strong style='color:#2f8b3a'>잠깐만요!</strong><br>오늘 청소 준비를 하고 있어요.";
  $("modeChip").textContent="🤖 우리 집 기록으로 준비 중";
  setGuide("오늘 상태를 보고 로보킹이 청소 준비를 하고 있어요. 잠시만 기다려 주세요.","charging");
  showToast("청소 준비 중: 오늘 상태에 맞춰 준비하고 있어요.");

  setTimeout(()=>{
    syncScenarioToState(matchedScenario);
    state.predicted=true;
    state.predicting=false;
    state.chargeComplete=false;
    if(loading){
      const status=state.soc>=state.targetSoc?"바로 청소 가능":"충전 필요";
      loading.textContent="준비 완료 · "+status+" · 로보킹이 필요한 만큼 준비했어요.";
      loading.classList.remove('active');
    }
    render();
    const statusText=state.soc>=state.targetSoc?"바로 청소할 수 있어요":"잠깐 충전하면 청소할 수 있어요";
    $("speech").innerHTML="<strong style='color:#2f8b3a'>준비 완료!</strong><br>"+statusText;
    $("modeChip").textContent="✅ 청소 준비 완료 · "+state.selectedLabel;
    addEvent("청소 준비 완료",state.selectedLabel+" 청소를 위해 로보킹이 필요한 만큼 준비했어요.");
    setGuide(statusText.includes("바로")?"준비 완료! 같은 버튼을 한 번 더 누르면 바로 출동해요.":"준비 완료! 같은 버튼을 한 번 더 누르면 필요한 만큼만 충전하고 출발해요.", state.soc>=state.targetSoc?"done":"warning");
    showToast("청소 준비 완료! 로보킹이 오늘 청소 준비를 마쳤어요.");
  },900);
}

function floorSummary(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const counts={};
  activeRun.zones.forEach(z=>{const k=z.floorType||"정보 없음";counts[k]=(counts[k]||0)+1;});
  return Object.keys(counts).map(k=>k+" "+counts[k]+"구역").join(", ");
}
function floorKindCount(){
  if(!activeRun || !activeRun.zones)return 0;
  const kinds={};
  activeRun.zones.forEach(z=>{kinds[z.floorType||"정보 없음"]=true;});
  return Object.keys(kinds).length;
}
function dirtSummaryShort(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const high=activeRun.zones.filter(z=>String(z.dirtLevel||"").includes("높")).length;
  const mid=activeRun.zones.filter(z=>String(z.dirtLevel||"").includes("중") || String(z.dirtLevel||"").includes("보통")).length;
  if(high>0)return "높음 "+high+"구역"+(mid>0?" · 보통 "+mid+"구역":"");
  if(mid>0)return "보통 "+mid+"구역";
  return dirtSummary();
}
function dirtSummary(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const counts={};
  activeRun.zones.forEach(z=>{const k=z.dirtLevel||"정보 없음";counts[k]=(counts[k]||0)+1;});
  return Object.keys(counts).map(k=>k+" "+counts[k]+"구역").join(", ");
}
function obstacleSummary(){return activeRun && activeRun.home ? (activeRun.home.obstacleLevel||"중간") : "중간";}
function profileResultBody(){
  const startSoc=Number(state.firstRunStartSoc||0);
  const endSoc=Number(state.firstRunEndSoc||state.soc||0);
  const recorded=Number(state.firstRunSocUsed||state.firstRunRequiredSoc||0);
  const used=Number(state.firstRunSocUsed||0);
  const socLine=state.firstRunSocEnough
    ? "배터리 변화: <b>"+Math.round(startSoc)+"% → "+Math.round(endSoc)+"%</b>"
    : "배터리 변화: <b>"+Math.round(startSoc)+"% → "+Math.round(endSoc)+"%</b> <small>(배터리 부족)</small>";
  return "<b>우리 집 저장 완료</b><br><br>"
    +"집 크기: <b>"+activeRun.areaPyung+"평 · "+activeRun.home.cleaningAreaM2+"㎡</b><br>"
    +"구역: <b>5개</b><br>"
    +"바닥: <b>"+floorKindCount()+"종 혼합</b><br>"
    +"오염도: <b>"+dirtSummaryShort()+"</b><br>"
    +"장애물: <b>"+obstacleSummary()+"</b><br>"
    +"학습 중 사용한 배터리: <b>"+fmtSoc(recorded)+"%</b><br>"
    +socLine+"<br>"
    +"현재 배터리: <b>"+Math.round(state.soc)+"%</b><br><br>"
    +"다음 단계: <b>오늘 청소 준비하기</b>";
}
function startFirstMapping(){
  if(state.cleaning||state.charging||state.mapping){showToast("진행 중인 작업이 끝난 뒤 다시 시도해 주세요.");return}

  const startSoc=clamp(Math.round(Number(state.soc||0)),0,100);
  if(startSoc < MIN_SOC_AFTER_LEARNING + MIN_LEARNING_SOC_USE){
    openModal("학습 전에 잠깐 충전할게요","처음 우리 집을 배우려면<br>로보킹에게 힘이 조금 더 필요해요.<br><br>잠깐 충전한 뒤 시작하면<br>집 구조를 더 안정적으로 배울 수 있어요.");
    return;
  }

  // 현재 배터리 기준으로 학습 주행 후 여유 배터리를 남길 수 있는 기록 시나리오를 우선 선택합니다.
  const safeRuns=predictionData.runs.filter(r=>getLearningSocUse(r,startSoc)>0);
  activeRun=pickRandomRun(safeRuns.length?safeRuns:predictionData.runs) || predictionData.runs[0];
  syncScenarioToState(activeRun.home);
  refreshScopeSelect();

  const fullRequiredSoc=Number(activeRun.home.requiredSoc||0);
  const learningUse=getLearningSocUse(activeRun,startSoc);
  const expectedEndSoc=Math.max(MIN_SOC_AFTER_LEARNING,startSoc-learningUse);

  state.profileReady=false;
  state.predicted=false;
  state.mapping=true;
  state.mappingProgress=0;
  state.mappingStepIndex=0;
  state.firstRunFullRequiredSoc=fullRequiredSoc;
  state.firstRunRequiredSoc=learningUse;
  state.firstRunSocUsed=learningUse;
  state.firstRunStartSoc=startSoc;
  state.firstRunEndSoc=expectedEndSoc;
  state.firstRunSocEnough=true;
  state.soc=startSoc;
  state.chargeComplete=false;
  state.celebrating=false;
  switchPage("homePage");
  setGuide("학습 청소를 시작했어요. 로보킹이 우리 집 구조와 바닥 상태를 차근차근 기억하고 있어요.","charging");
  showToast("학습 시작: 로보킹이 우리 집을 배우고 있어요.");
  render();

  let tick=0;
  const total=mappingSteps.length*4;
  const timer=setInterval(()=>{
    tick+=1;
    const ratio=Math.min(1,tick/total);
    state.mappingProgress=Math.min(100,Math.round(ratio*100));
    state.mappingStepIndex=Math.min(mappingSteps.length-1,Math.floor((tick-1)/4));
    state.progress=state.mappingProgress;
    state.soc=Math.max(MIN_SOC_AFTER_LEARNING,Math.round((startSoc-learningUse*ratio)*10)/10);
    state.firstRunEndSoc=state.soc;
    state.temperature=Math.min(33,state.temperature+0.08);
    render();
    if(tick>=total){
      clearInterval(timer);
      state.mapping=false;
      state.profileReady=true;
      state.predicted=false;
      state.progress=100;
      state.soc=Math.max(MIN_SOC_AFTER_LEARNING,Math.round(expectedEndSoc));
      state.firstRunEndSoc=state.soc;
      const scopeSelect=$("scopeSelect"); if(scopeSelect)scopeSelect.value='home';
      const cleanModeSelect=$("cleanModeSelect"); if(cleanModeSelect)cleanModeSelect.value=activeRun.home.mopEnabled?'mop':'dry';
      const intensitySelect=$("intensitySelect"); if(intensitySelect)intensitySelect.value='standard';
      const todayStateSelect=$("todayStateSelect"); if(todayStateSelect)todayStateSelect.value='normal';
      state.temperature=29;
      const eventMsg="로보킹이 우리 집 구조와 바닥 상태를 기억했어요.";
      addEvent("1회차 학습 청소 완료",eventMsg);
      spawnEffect("🏠",8);spawnEffect("✨",9);
      render();
      setGuide("우리 집 저장 완료! 이제 오늘 청소 조건을 고르면 로보킹이 알아서 준비해요.","done");
      showToast("우리 집 저장 완료! 이제 오늘 청소를 준비할 수 있어요.");
      setTimeout(()=>{render();},350);
    }
  },260);
}
function selectScenario(scope,zoneNumber=null){
  if(state.cleaning||state.charging||state.mapping){showToast("학습/청소/충전이 끝난 뒤 변경할 수 있어요.");return}
  if(!state.profileReady){
    showToast("구역 선택은 1회차 학습 후 가능해요.");
    $("speech").innerHTML="<strong style='color:#ef8c32'>우리 집 학습이 먼저예요</strong><br>1회차 학습 청소를 시작해 주세요.";
    return;
  }
  if(!state.predicted){setGuide("구역을 바꾸기 전 오늘 청소 준비를 먼저 완료해 주세요.","warning");showToast("먼저 오늘 청소 준비하기를 눌러주세요.");return}
  const scopeSelect=$('scopeSelect');
  if(scopeSelect)scopeSelect.value=scope==="home"?"home":String(zoneNumber||1);
  const choices=getPredictionChoices(scope,zoneNumber);
  const matchedScenario=findMlScenarioFromChoices(choices);
  syncScenarioToState(matchedScenario);
  render();
  const status=state.soc>=state.targetSoc?"청소 가능":"충전 필요";
  const loading=$('predictLoading');
  if(loading)loading.textContent=state.selectedLabel+" 선택 · "+status+" · 로보킹이 다시 준비했어요.";
  $("speech").innerHTML="<strong>"+state.selectedLabel+" 선택!</strong><br>이 구역에 맞춰 다시 준비했어요.";
  $("modeChip").textContent="✨ "+state.selectedLabel+" 청소 준비 완료";
  setGuide((state.soc>=state.targetSoc)?state.selectedLabel+" 청소 준비가 끝났어요. 지금 바로 출동할 수 있어요.":state.selectedLabel+" 청소 준비가 끝났어요. 잠깐 충전하고 출발하면 좋아요.", state.soc>=state.targetSoc?"done":"warning");
  showToast(state.selectedLabel+" 청소 준비를 다시 맞췄어요.");
}

function openScenarioModal(){
  const enough=state.soc>=state.targetSoc;
  const title=enough?"바로 출동할 수 있어요!":"조금만 더 힘을 채울게요!";
  const scopeText=state.selectedScope==="home"?"집 전체 청소":state.selectedLabel+" 청소";
  const conditionLine="오늘 조건: <b>"+state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel+"</b><br><br>";
  const zoneLine=state.selectedScope==="zone"
    ? state.selectedLabel+"은 <b>"+(state.floorType||"바닥 정보")+"</b> 바닥이고, 오늘은 <b>"+(state.dirtLevel||"평소")+"</b> 상태로 준비했어요.<br><br>"
    : "저장해둔 우리 집 정보를 바탕으로 집 전체 청소를 준비했어요.<br><br>";
  const body=enough
    ? scopeText+" 준비가 끝났어요.<br><br>"+conditionLine+zoneLine+"지금 바로 시작해도 충분해요.<br>제가 배터리를 아끼면서 청소할게요!"
    : scopeText+" 준비가 끝났어요.<br><br>"+conditionLine+zoneLine+"지금 바로 출발하기엔 힘이 조금 부족해요.<br><br><b>잠깐 충전하고 나면</b><br>더 편하게 청소를 마칠 수 있어요.";
  if(enough){
    openModal(title,body);
  }else{
    openModal(title,body,{showCancel:true,cancelText:"취소",confirmText:"충전하고 시작",onConfirm:()=>chargeRobot(false)});
  }
}


function getHomeSizeType(areaPyung){
  const area=Number(areaPyung||0);
  if(area<=24)return "small";
  if(area<=49)return "medium";
  return "large";
}
function getHomeSizeLabel(areaPyung){
  const type=getHomeSizeType(areaPyung);
  if(type==="small")return "소형";
  if(type==="medium")return "중형";
  return "대형";
}
function getExpectedZoneCount(areaPyung){
  const type=getHomeSizeType(areaPyung);
  if(type==="small")return 4;
  if(type==="medium")return 6;
  return 8;
}
function getActualZoneCount(){
  return (activeRun && activeRun.zones && activeRun.zones.length) ? activeRun.zones.length : 0;
}
function getDisplayZoneCount(){
  const area=(activeRun && activeRun.areaPyung) ? activeRun.areaPyung : state.areaPyung;
  const expected=getExpectedZoneCount(area);
  const actual=getActualZoneCount();

  // 새 데이터셋은 평수 규모에 따라 4/6/8개 영역이 기준입니다.
  // 기존 5구역 CSV가 남아 있거나 Streamlit 캐시가 섞여도 화면 표시는 평수 기준으로 자동 보정합니다.
  if(expected && actual!==expected){
    return expected;
  }
  return actual || expected;
}
function getZoneByNumber(zoneNo){
  const zones=(activeRun && activeRun.zones) ? activeRun.zones : [];
  return zones.find(z=>Number(z.zone)===Number(zoneNo)) || zones[zoneNo-1] || null;
}
function normalizeDirtCode(zone){
  if(!zone)return 2;
  const code=Number(zone.dirtCode || zone.dirtLevelCode || 0);
  if(Number.isFinite(code) && code>0)return code;

  const text=String(zone.dirtLevel || zone.dirt || "").toLowerCase();
  if(text.includes("매우") || text.includes("심함") || text.includes("높") || text.includes("heavy") || text.includes("high"))return 4;
  if(text.includes("중") || text.includes("보통") || text.includes("normal") || text.includes("medium"))return 2;
  if(text.includes("낮") || text.includes("깨끗") || text.includes("low") || text.includes("clean"))return 1;
  return 2;
}
function getZoneConditionScore(zoneNo){
  const zone=getZoneByNumber(zoneNo);
  if(!zone){
    // CSV에 아직 해당 영역 데이터가 없을 때도 화면이 비어 보이지 않도록 부드럽게 분산
    return Number(zoneNo||1) * 0.35;
  }

  const dirt=normalizeDirtCode(zone);
  const suction=Number(zone.suctionCode || zone.suctionModeCode || 0);
  const required=Number(zone.requiredSoc || 0);
  const obstacle=Number(zone.obstacleLevelCode || 0);

  // 바닥 상태 색상은 오염도 중심으로 보되,
  // 흡입 강도/장애물/필요 배터리를 조금 섞어서 구역별 차이가 잘 보이게 합니다.
  return dirt*10 + suction*2 + obstacle*1.2 + required*0.18 + Number(zoneNo||1)*0.03;
}
function getDirtVisual(zoneNo){
  const count=getDisplayZoneCount();
  const scores=[];
  for(let i=1;i<=count;i++){
    scores.push({zone:i,score:getZoneConditionScore(i)});
  }
  scores.sort((a,b)=>a.score-b.score || a.zone-b.zone);
  const rank=Math.max(0,scores.findIndex(s=>Number(s.zone)===Number(zoneNo)));
  const ratio=(rank+1)/Math.max(scores.length,1);

  // 사용자에게는 '오염도 수치'가 아니라 같은 집 안에서 상대적으로 더 신경쓸 구역을 색으로 보여줍니다.
  // 그래서 데이터가 전부 낮음/보통에 몰려도 맵에서는 구역 차이가 한눈에 보이도록 색을 넓게 분산합니다.
  if(ratio<=0.25)return {fill:"#cfeec0", label:"깨끗"};
  if(ratio<=0.55)return {fill:"#ffe08a", label:"보통"};
  if(ratio<=0.82)return {fill:"#ffb169", label:"먼지"};
  return {fill:"#ff7d68", label:"집중"};
}
function mapRoom(x,y,w,h,rx,zoneNo,label,dashed=false){
  const visual=getDirtVisual(zoneNo);

  // 작은 칸에서는 두 줄 텍스트가 겹치기 쉬워서
  // 방 이름은 중앙에 크게, 영역 번호는 우측 상단 작은 배지로 분리합니다.
  const compact = h < 42 || w < 66;
  const labelSize = compact ? 11.8 : 13.2;
  const labelY = compact ? y + h * 0.56 : y + h * 0.40;
  const subY = y + h * 0.68;
  const badgeR = compact ? 8 : 9;
  const badgeX = x + w - badgeR - 5;
  const badgeY = y + badgeR + 5;

  let html = "<g>"
    +"<rect class='map-room"+(dashed?" dashed":"")+"' x='"+x+"' y='"+y+"' width='"+w+"' height='"+h+"' rx='"+rx+"' fill='"+visual.fill+"'></rect>";

  if(compact){
    html += "<circle cx='"+badgeX+"' cy='"+badgeY+"' r='"+badgeR+"' fill='rgba(255,255,255,.72)'></circle>"
      +"<text class='map-room-sub' style='font-size:7.8px' x='"+badgeX+"' y='"+(badgeY+0.5)+"'>"+zoneNo+"</text>"
      +"<text class='map-room-label' style='font-size:"+labelSize+"px' x='"+(x+w/2)+"' y='"+labelY+"'>"+label+"</text>";
  }else{
    html += "<text class='map-room-label' style='font-size:"+labelSize+"px' x='"+(x+w/2)+"' y='"+labelY+"'>"+label+"</text>"
      +"<text class='map-room-sub' style='font-size:9.4px' x='"+(x+w/2)+"' y='"+subY+"'>영역 "+zoneNo+"</text>";
  }

  html += "</g>";
  return html;
}
function getMapSvg(type){
  let rooms="";
  if(type==="small"){
    rooms += mapRoom(18,18,112,54,12,1,"거실");
    rooms += mapRoom(134,18,92,54,12,2,"주방");
    rooms += mapRoom(18,76,130,68,12,3,"침실");
    rooms += mapRoom(152,76,74,68,12,4,"현관",true);
    return "<svg class='home-map-svg' viewBox='0 0 244 162' role='img' aria-label='소형 집 구조 맵'>"
      +"<path class='map-route' d='M42 48 C94 48, 112 96, 176 108'></path>"
      +rooms+"</svg>";
  }
  if(type==="medium"){
    rooms += mapRoom(14,14,92,50,12,1,"침실");
    rooms += mapRoom(110,14,112,50,12,2,"주방");
    rooms += mapRoom(14,68,124,58,12,3,"거실");
    rooms += mapRoom(142,68,80,58,12,4,"카펫",true);
    rooms += mapRoom(14,130,92,32,10,5,"현관");
    rooms += mapRoom(110,130,112,32,10,6,"다용도");
    return "<svg class='home-map-svg' viewBox='0 0 236 174' role='img' aria-label='중형 집 구조 맵'>"
      +"<path class='map-route' d='M48 42 C96 52, 114 94, 182 98 C170 128, 118 138, 64 146'></path>"
      +rooms+"</svg>";
  }
  rooms += mapRoom(12,12,72,44,11,1,"침실1");
  rooms += mapRoom(88,12,72,44,11,2,"침실2");
  rooms += mapRoom(164,12,70,44,11,3,"주방");
  rooms += mapRoom(12,60,106,58,12,4,"거실");
  rooms += mapRoom(122,60,58,58,12,5,"현관");
  rooms += mapRoom(184,60,50,58,12,6,"카펫",true);
  rooms += mapRoom(12,122,106,38,10,7,"서재");
  rooms += mapRoom(122,122,112,38,10,8,"다용도");
  return "<svg class='home-map-svg' viewBox='0 0 246 172' role='img' aria-label='대형 집 구조 맵'>"
    +"<path class='map-route' d='M46 34 C96 44, 146 36, 202 36 C174 76, 162 98, 210 92 C166 126, 102 142, 54 140'></path>"
    +rooms+"</svg>";
}
function getDirtLegendHtml(){
  return "<div class='map-legend' aria-label='바닥 상태 색상 안내'>"
    +"<span class='map-legend-title'>바닥 상태</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-clean'></i>깨끗</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-normal'></i>보통</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-dusty'></i>먼지</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-focus'></i>집중</span>"
    +"</div>";
}
function getLearnedMapHtml(){
  try{console.log('[LG ROBO CARE] area/actual/expected zones', state.areaPyung, getActualZoneCount(), getExpectedZoneCount(state.areaPyung));}catch(e){}
  const area=(activeRun && activeRun.areaPyung) ? activeRun.areaPyung : state.areaPyung;
  const type=getHomeSizeType(area);
  const sizeLabel=getHomeSizeLabel(area);
  const zoneCount=getDisplayZoneCount();
  return "<div class='home-map-card'>"
    +"<div class='home-map-head'><div class='home-map-badge'>"+sizeLabel+" · "+zoneCount+"개 영역</div></div>"
    +"<div class='home-map-img-wrap'>"+getMapSvg(type)+"</div>"
    +getDirtLegendHtml()
    +"</div>";
}
function refreshScopeSelect(){
  const scopeSelect=$('scopeSelect');
  if(!scopeSelect)return;

  const area=(activeRun && activeRun.areaPyung) ? activeRun.areaPyung : state.areaPyung;
  const expected=getExpectedZoneCount(area);
  const actual=(activeRun && activeRun.zones && activeRun.zones.length) ? activeRun.zones.length : expected;
  const count=Math.max(expected, actual || 0);
  const before=scopeSelect.value || "home";

  let html="<option value='home'>집 전체</option>";
  for(let i=1;i<=count;i++){
    html += "<option value='"+i+"'>"+i+"영역</option>";
  }
  scopeSelect.innerHTML=html;
  const values=Array.from(scopeSelect.options).map(o=>o.value);
  scopeSelect.value=values.includes(before)?before:"home";
}


function renderPlan(){
  if(!$('planSummary'))return;
  refreshScopeSelect();
  const conditionPanel=$('conditionPanel');
  const predictBtn=$('predictBtn');
  const conditionTitle=$('conditionTitle');
  const learnBtn=$('learnBtn');
  const learnPill=$('learnPill');
  const learnStatus=$('learnStatus');
  const learnFill=$('learnFill');
  const learnSteps=$('learnSteps');
  const firstLearnInputs=$('firstLearnInputs');
  const predictionInputs=$('predictionInputs');
  const startCleanPrimary=$('startCleanPrimary');
  const flowGuide=$('flowGuide');
  if(flowGuide){
    const guideText=guideForCurrentState();
    let tone=state.userGuideTone||"normal";
    if(state.soc<15)tone="danger";
    else if(state.charging)tone="charging";
    else if(state.predicted && state.soc<state.targetSoc)tone="warning";
    else if(state.missionDone || state.celebrating)tone="done";
    flowGuide.className="flow-guide"+(tone&&tone!=="normal"?" "+tone:"");
    flowGuide.innerHTML="<span class='guide-step'>다음 안내</span>"+guideText;
  }

  if(learnSteps){
    if(state.profileReady && !state.mapping){
      learnSteps.classList.add('map-ready');
      learnSteps.innerHTML=getLearnedMapHtml();
    }else{
      learnSteps.classList.remove('map-ready');
      learnSteps.innerHTML=mappingSteps.map((s,i)=>{
        let cls='learn-step';
        if(state.profileReady || i<state.mappingStepIndex)cls+=' done';
        else if(state.mapping && i===state.mappingStepIndex)cls+=' active';
        return '<div class="'+cls+'">'+s.label+'</div>';
      }).join('');
    }
  }
  if(learnFill)learnFill.style.width=(state.profileReady?100:state.mappingProgress)+'%';

  if(state.mapping){
    if(learnPill)learnPill.textContent="학습 중";
    if(learnStatus){
      const currentStep=mappingSteps[state.mappingStepIndex]||mappingSteps[0];
      learnStatus.innerHTML=currentStep.label+" 중 · "+state.mappingProgress+"%<br><b>배터리 "+Math.round(state.firstRunStartSoc)+"% → "+Math.round(state.soc)+"%</b>";
    }
    if(learnBtn){learnBtn.textContent="로보킹이 집을 배우는 중...";learnBtn.disabled=true;}
    if(conditionPanel)conditionPanel.classList.add('locked-area');
  }else if(state.profileReady){
    if(learnPill)learnPill.textContent="프로필 저장됨";
    if(learnStatus)learnStatus.innerHTML="매핑 완료 · "+getHomeSizeLabel(activeRun.areaPyung)+" 집 구조 저장";
    if(learnBtn){learnBtn.textContent="🔄 1회차 학습 다시 실행";learnBtn.disabled=false;learnBtn.classList.add('ready');}
    if(conditionPanel)conditionPanel.classList.remove('locked-area');
  }else{
    if(learnPill)learnPill.textContent="초기 학습";
    if(learnStatus)learnStatus.textContent="시작 버튼을 누르면 집 정보를 저장해요.";
    if(learnBtn){learnBtn.textContent="🏠 1회차 학습 청소 시작";learnBtn.disabled=false;learnBtn.classList.remove('ready');}
    if(conditionPanel)conditionPanel.classList.remove('locked-area');
  }

  if(firstLearnInputs)firstLearnInputs.style.display=state.profileReady?'none':'block';
  if(predictionInputs)predictionInputs.style.display=state.profileReady?'block':'none';

  if(predictBtn){
    const mainBtnDisabled=!state.profileReady || state.mapping || state.predicting || state.cleaning || state.charging;
    predictBtn.disabled=mainBtnDisabled;
    predictBtn.style.opacity=mainBtnDisabled?'.55':'1';

    if(!state.profileReady){
      predictBtn.textContent='🤖 학습 후 청소 준비 가능';
    }else if(state.predicting){
      predictBtn.textContent='🤖 오늘 청소 준비 중...';
    }else if(!state.predicted){
      predictBtn.textContent='🤖 오늘 청소 준비하기';
    }else if(state.soc<state.targetSoc){
      predictBtn.textContent='🔋 충전하고 청소하기';
    }else{
      predictBtn.textContent='🧹 바로 청소하기';
    }
  }
  if(conditionTitle){
    conditionTitle.textContent=state.profileReady?'오늘 청소 조건 선택':'1회차 학습 준비';
  }

  document.querySelectorAll('.scope-btn').forEach(btn=>{
    btn.classList.remove('active');
    btn.disabled=!state.profileReady || !state.predicted || state.mapping;
    btn.style.opacity=(!state.profileReady || !state.predicted || state.mapping)?'.55':'1';
  });
  if(state.selectedScope==="home")$('scopeHome').classList.add('active');
  else if($('scopeZone'+state.selectedZone))$('scopeZone'+state.selectedZone).classList.add('active');

  $('planModel').textContent=state.mapping?'집 배우는 중':(!state.profileReady?'처음 학습 전':(state.predicted?'로보킹 맞춤 준비':'우리 집 저장 완료'));


  if(startCleanPrimary){
    const canStart=state.profileReady && state.predicted && !state.mapping && !state.cleaning && !state.charging;
    startCleanPrimary.disabled=!canStart;
    if(state.mapping){
      startCleanPrimary.innerHTML='🏠 우리 집을 배우는 중이에요<small id="startCleanHint">학습이 끝나면 청소 미션을 시작할 수 있어요</small>';
    }else if(!state.profileReady){
      startCleanPrimary.innerHTML='🏠 1회차 학습 청소가 먼저예요<small id="startCleanHint">집 구조를 저장한 뒤 청소할 수 있어요</small>';
    }else if(!state.predicted){
      startCleanPrimary.innerHTML='🤖 오늘 청소 준비가 먼저예요<small id="startCleanHint">로보킹이 필요한 만큼 알아서 준비해요</small>';
    }else if(state.soc<state.targetSoc){
      startCleanPrimary.innerHTML='🔋 충전하고 청소하기<small id="startCleanHint">필요한 만큼만 채우고 출발해요</small>'; 
    }else{
      startCleanPrimary.innerHTML='🧹 청소 미션 수행하기<small id="startCleanHint">'+state.selectedLabel+' · 바로 출동 가능</small>'; 
    }
  }

  if(!state.profileReady){
    $('planTargetSoc').textContent='--';
    $('planSummary').innerHTML="<div class='summary-card'><div class='summary-title'>학습 대기</div><div class='summary-row'><span class='summary-key'>상태</span><span class='summary-val'>집 정보 없음</span></div><div class='summary-row'><span class='summary-key'>다음 단계</span><span class='summary-val green'>1회차 학습 시작</span></div></div>";
    $('planSocSub').textContent="학습 후 표시";
    return;
  }
  if(!state.predicted){
    $('planTargetSoc').textContent='--';
    $('planSummary').innerHTML="<div class='summary-card'><div class='summary-title'>우리 집 저장 완료</div><div class='summary-row'><span class='summary-key'>집 크기</span><span class='summary-val'>"+state.areaPyung+"평 · "+state.cleaningAreaM2+"㎡</span></div><div class='summary-row'><span class='summary-key'>학습 중 사용</span><span class='summary-val em'>"+Math.round(state.firstRunStartSoc)+"% → "+Math.round(state.soc)+"%</span></div><div class='summary-row'><span class='summary-key'>다음 단계</span><span class='summary-val green'>오늘 청소 준비하기</span></div></div>";
    $('planSocSub').textContent="준비 대기";
    return;
  }

  $('planTargetSoc').textContent=state.targetSoc;
  const scopeText=state.selectedScope==="home"?"집 전체":state.selectedLabel;
  const detail=state.selectedScope==="home"
    ? state.areaPyung+"평 프로필 · "+state.cleaningAreaM2+"㎡"
    : (state.floorType||"바닥재질")+" · 오염도 "+(state.dirtLevel||"-")+" · "+state.cleaningAreaM2+"㎡";
  const conditionDetail=state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel;
  $('planSummary').innerHTML="<div class='summary-card'>"
    +"<div class='summary-title'>"+scopeText+"</div>"
    +"<div class='summary-row'><span class='summary-key'>조건</span><span class='summary-val'>"+conditionDetail+"</span></div>"
    +"<div class='summary-row'><span class='summary-key'>프로필</span><span class='summary-val'>"+detail+"</span></div>"
    +"<div class='summary-row'><span class='summary-key'>청소 준비</span><span class='summary-val em'>완료</span></div>"
    +"<div class='summary-row'><span class='summary-key'>준비 방식</span><span class='summary-val green'>"+state.matchNote+"</span></div>"
    +"</div>";
  $('planSocSub').textContent="필요한 만큼만 충전";
}

function renderHome(){
  const room=$("room");room.className="room";

  if(state.chargeComplete){
    room.classList.add("celebrate");
    $("speech").innerHTML="<strong>배불러요!</strong><br>이제 청소 가능해요!";
    $("modeChip").textContent="💖 충전 완료 · 출동 준비";
    $("batteryFace").textContent="😍";$("spark").textContent="💖";
    $("batteryMessage").innerHTML="필요한 만큼 채웠어요.<br>출동 준비 완료!";
    $("timeTip").textContent=state.selectedLabel+" 청소를 시작할 수 있어요.";
  }else if(state.celebrating){
    room.classList.add("celebrate");
    $("speech").innerHTML="<strong>청소 완료!</strong><br>보상을 받았어요!";
    $("modeChip").textContent="🏆 미션 완료 · +50 코인";
    $("batteryFace").textContent="🥳";$("spark").textContent="🎉";
  }else if(state.mapping){
    room.classList.add("cleaning");
    const step=mappingSteps[state.mappingStepIndex]||mappingSteps[0];
    $("speech").innerHTML="<strong style='color:#2f8b3a'>우리 집을 배우는 중!</strong><br>"+step.label+" 중이에요.";
    $("modeChip").textContent="🏠 학습 청소 · 배터리 "+Math.round(state.firstRunStartSoc)+"% → "+Math.round(state.soc)+"%";
    $("batteryFace").textContent="🧭";$("spark").textContent="📡";
    $("batteryMessage").innerHTML="학습 청소 중입니다.<br>배터리가 실제로 소모돼요.";
    $("timeTip").textContent="학습 진행 "+state.mappingProgress+"% · 현재 배터리 "+Math.round(state.soc)+"%";
  }else if(state.predicting){
    $("speech").innerHTML="<strong style='color:#2f8b3a'>준비 중이에요!</strong><br>오늘 상태에 맞춰 준비하고 있어요.";
    $("modeChip").textContent="🤖 우리 집 기록으로 준비 중";
    $("batteryFace").textContent="🤔";$("spark").textContent="✨";
  }else if(!state.profileReady){
    $("speech").innerHTML="<strong style='color:#ef8c32'>처음 만났어요!</strong><br>1회차 청소로 우리 집을 알려주세요.";
    $("modeChip").textContent="🏠 집 구조 학습 필요";
    $("batteryFace").textContent="🙂";$("spark").textContent="✨";
    $("batteryMessage").innerHTML="아직 우리 집 정보를 몰라요.<br>학습 청소가 필요합니다.";
    $("timeTip").textContent="1회차 학습 후 청소 준비 가능";
  }else if(!state.predicted){
    $("speech").innerHTML="<strong>집을 배웠어요!</strong><br>이제 청소 준비를 맡겨주세요.";
    $("modeChip").textContent="✅ 우리 집 저장 완료";
    $("batteryFace").textContent="😊";$("spark").textContent="✨";
    $("batteryMessage").innerHTML="집 구조 학습 완료!<br>오늘 청소 준비하기를 눌러주세요.";
    $("timeTip").textContent="청소 준비 대기 중";
  }else if(state.cleaning){
    room.classList.add("cleaning");
    $("speech").innerHTML="<strong>열심히 청소 중이에요!</strong><br>진행률 "+state.progress+"%";
    $("modeChip").textContent="🧹 "+state.selectedLabel+" 청소 중 · "+state.progress+"%";
    $("batteryFace").textContent="🧹";
    $("batteryMessage").innerHTML="청소 중입니다.<br>로보킹이 청소하면서 배터리를 사용하고 있어요.";
    $("timeTip").textContent="청소 진행률 "+state.progress+"%";
    $("spark").textContent="💨";
  }else if(state.charging){
    room.classList.add("charging");
    $("speech").innerHTML="<strong style='color:#e48627'>잠깐 쉬는 중이에요</strong><br>필요한 만큼만 충전할게요.";
    $("modeChip").textContent="⚡ "+state.selectedLabel+" 출동 준비 중";
    $("batteryFace").textContent="😌";
    $("batteryMessage").innerHTML="충전 스테이션에서 쉬면서<br>필요한 만큼만 채우고 있어요.";
    $("timeTip").textContent="로보킹이 필요한 만큼만 채우고 있어요.";
    $("spark").textContent="⚡";
  }else if(state.soc<15){
    room.classList.add("low");
    $("speech").innerHTML="<strong style='color:#ef4e45'>배가 너무 고파요...</strong><br>충전이 필요해요.";
    $("modeChip").textContent="⚠️ 배터리 부족";
    $("batteryFace").textContent="🥴";
    $("batteryMessage").innerHTML="배터리가 부족해요.<br>먼저 충전해 주세요.";
    $("timeTip").textContent="충전 후 청소를 시작해 주세요.";
    $("spark").textContent="💦";
  }else{
    $("modeChip").textContent="✨ 로보킹 맞춤 준비";
    $("batteryFace").textContent=state.soc>90?"😮":"😊";
    $("spark").textContent="✨";

    if(state.soc < state.targetSoc){
      $("speech").innerHTML=
        "<strong style='color:#ef8c32'>아직 배고파요!</strong><br>"
        + "필요한 만큼만<br>충전하고 청소할게요.";
      $("batteryMessage").innerHTML=state.selectedLabel+" 청소를 위해<br>조금 더 충전이 필요해요.";
      $("timeTip").textContent="잠깐 충전하면 청소를 시작할 수 있어요.";
    }else{
      $("speech").innerHTML="<strong>배가 든든해요!</strong><br>"+state.selectedLabel+" 청소를 준비할게요!";
      $("batteryMessage").innerHTML="현재 배터리로 충분해요.<br>바로 출동할 수 있어요.";
      $("timeTip").textContent="현재 배터리로 "+state.selectedLabel+" 청소가 가능합니다.";
    }
  }
}

function renderBattery(){
  $("socGauge").style.setProperty("--value",state.soc);
  $("socGaugeText").textContent=state.soc+"%";

  const tempPercent=clamp((state.temperature-15)/35*100,0,100);
  $("tempGauge").style.setProperty("--value",tempPercent);
  $("tempGaugeText").textContent=state.temperature+"℃";
  $("targetLabel").textContent=state.targetSoc+"%";
  $("targetSlider").value=state.targetSoc;
  $("tempLabel").textContent=state.temperature+"℃";
  $("tempSlider").value=state.temperature;
  if(!state.profileReady){
    $("insightText").innerHTML="아직 1회차 학습 청소 전입니다. 집 구조와 구역 정보를 먼저 저장하면 오늘 청소 준비를 시작할 수 있습니다.";
  }else if(!state.predicted){
    $("insightText").innerHTML="우리 집 정보가 저장됐어요. 오늘 청소 준비하기를 누르면 로보킹이 오늘 상태에 맞춰 필요한 만큼만 준비합니다.";
  }else{
    $("insightText").innerHTML="<b>"+state.selectedLabel+"</b> · "+state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel+"<br>로보킹이 오늘 청소 준비를 마쳤어요.<br>필요하면 잠깐 충전하고 바로 출발할 수 있어요.";
  }

  const y=132-(state.targetSoc-15)/75*104;
  const middleY=Math.round((82+y)/2);
  $("aiLine").setAttribute("points","30,128 80,103 128,"+middleY+" 180,"+Math.round(y)+" 235,"+Math.round(y)+" 285,"+Math.round(y)+" 328,"+Math.round(y));
}

function renderRecord(){
  $("avgText").textContent=state.average;
  $("recordAvgText").textContent=state.average;
  $("areaText").textContent=state.area;
  $("acceptText").textContent=state.acceptCount;
  const sunday=34+state.cleanCount*8;
  $("sunValue").textContent=sunday;
  $("sunBar").style.height=Math.min(96,56+state.cleanCount*10)+"%";
}

function renderAccessories(){
  const robot=$("robot");
  const head=$("robotHeadDeco");
  const aura=$("robotAuraDeco");
  const decal=$("robotBodyDeco");
  if(!robot || !head || !aura)return;

  robot.classList.toggle("has-custom-head",state.equippedItems.head && state.equippedItems.head!=="crown");

  const headItem=state.equippedItems.head;
  head.className="robot-accessory robot-head-deco";
  head.innerHTML="";
  if(headItem && headItem!=="crown"){
    if(headItem==="bunny"){
      head.classList.add("show","ears","bunny");
      head.innerHTML='<span class="robo-ear left"></span><span class="robo-ear right"></span>';
    }else if(headItem==="cat"){
      head.classList.add("show","ears","cat");
      head.innerHTML='<span class="robo-ear left"></span><span class="robo-ear right"></span>';
    }else{
      const headMap={ribbon:"🎀",hat:"🧢"};
      head.textContent=headMap[headItem]||"";
      head.classList.add("show",headItem);
    }
  }

  aura.className="robot-aura-deco";
  if(state.equippedItems.aura==="sparkle"){
    aura.innerHTML="<span>✨</span><span>✨</span><span>✨</span><span>✨</span>";
    aura.classList.add("show");
  }else{
    aura.innerHTML="";
  }

  // 이전 버전 호환용: 더 이상 몸통 스티커를 사용하지 않으므로 화면에서 숨깁니다.
  if(decal){
    decal.className="robot-accessory robot-body-deco";
    decal.textContent="";
  }
}

function renderReward(){
  $("levelText").textContent=state.level;
  $("expText").textContent=state.exp;
  $("expFill").style.width=state.exp+"%";

  const preview=$("levelRobotPreview");
  if(preview){
    const head=state.equippedItems.head;
    let html='<span class="preview-base">🤖</span>';
    if(head && head!=="crown"){
      if(head==="bunny" || head==="cat"){
        html+='<span class="preview-head ears '+head+'"><span class="p-ear left"></span><span class="p-ear right"></span></span>';
      }else{
        const headMap={ribbon:"🎀",hat:"🧢"};
        html+='<span class="preview-head '+head+'">'+(headMap[head]||'')+'</span>';
      }
    }
    if(state.equippedItems.aura==="sparkle")html+='<span class="preview-aura"><span class="a1">✨</span><span class="a2">✨</span><span class="a3">✨</span></span>';
    preview.innerHTML=html;
  }

  const itemTab=$("rewardTabItems");
  const couponTab=$("rewardTabCoupons");
  const itemPanel=$("rewardItemsPanel");
  const couponPanel=$("rewardCouponsPanel");
  if(itemTab)itemTab.classList.toggle("active",state.rewardTab==="items");
  if(couponTab)couponTab.classList.toggle("active",state.rewardTab==="coupons");
  if(itemPanel)itemPanel.classList.toggle("hidden",state.rewardTab!=="items");
  if(couponPanel)couponPanel.classList.toggle("hidden",state.rewardTab!=="coupons");

  updateRewardButton("ribbon","Ribbon");
  updateRewardButton("hat","Hat");
  updateRewardButton("bunny","Bunny");
  updateRewardButton("cat","Cat");
  updateRewardButton("sparkle","Sparkle");
  updateCouponButton("lg5","CouponLg5");
  updateCouponButton("cleanKit","CouponCleanKit");
  updateCouponButton("batteryCare","CouponBatteryCare");
  updateCouponButton("moveIn","CouponMoveIn");

  const foodBtn=$("btnFood");
  const foodStatus=$("statusFood");
  if(foodBtn){
    foodBtn.textContent=state.coins>=50?"50 코인":"50 코인 필요";
    foodBtn.classList.toggle("need-coins",state.coins<50);
  }
  if(foodStatus)foodStatus.textContent="보유 간식 "+state.food+"개";
}

function updateRewardButton(key,suffix){
  const item=shopItems[key];
  const btn=$("btn"+suffix);
  const card=$("card"+suffix);
  const status=$("status"+suffix);
  if(!item || !btn)return;
  const owned=Boolean(state.ownedItems[key]);
  const equipped=state.equippedItems[item.slot]===item.value;
  btn.classList.remove("owned","equipped","need-coins");
  if(card){card.classList.toggle("owned",owned);card.classList.toggle("equipped",equipped);}
  if(status)status.textContent=equipped?"장착 중":(owned?"보유 중":"");
  if(equipped){btn.textContent="해제하기";btn.classList.add("equipped");}
  else if(owned){btn.textContent="장착하기";btn.classList.add("owned");}
  else{
    btn.textContent=state.coins<item.cost ? item.cost+" 코인 필요" : item.cost+" 코인";
    if(state.coins<item.cost)btn.classList.add("need-coins");
  }
}

function updateCouponButton(key,suffix){
  const item=couponItems[key];
  const btn=$("btn"+suffix);
  const card=$("card"+suffix);
  const status=$("status"+suffix);
  if(!item || !btn)return;
  const count=Number(state.ownedCoupons[key]||0);
  btn.classList.remove("owned","equipped","need-coins");
  if(card)card.classList.toggle("owned",count>0);
  if(status)status.textContent=count>0?"보유 쿠폰 "+count+"장":"";
  if(state.coins<item.cost){
    btn.textContent=item.cost+" 코인 필요";
    btn.classList.add("need-coins");
  }
  else{btn.textContent=item.cost+" 코인으로 교환";}
}


function showToast(message){
  const toast=$("toast");toast.textContent=message;toast.classList.add("show");
  clearTimeout(window.toastTimer);
  window.toastTimer=setTimeout(()=>toast.classList.remove("show"),3500);
}
let modalConfirmHandler=closeModal;
function openModal(title,body,options={}){
  $("modalTitle").textContent=title;
  $("modalBody").innerHTML=body;
  const actions=$("modalActions");
  const cancelBtn=$("modalCancel");
  const confirmBtn=$("modalConfirm");
  const showCancel=Boolean(options.showCancel);
  actions.classList.toggle("single",!showCancel);
  cancelBtn.textContent=options.cancelText||"취소";
  confirmBtn.textContent=options.confirmText||"확인";
  modalConfirmHandler=typeof options.onConfirm==="function"?options.onConfirm:closeModal;
  $("modal").classList.add("show");
}
function closeModal(){$("modal").classList.remove("show")}

function spawnEffect(symbol,count=7){
  const layer=$("effectLayer");
  for(let i=0;i<count;i++){
    const p=document.createElement("span");
    p.className="effect";p.textContent=symbol;
    p.style.setProperty("--move-x",Math.round(Math.random()*160-80)+"px");
    p.style.setProperty("--rotate",Math.round(Math.random()*100-50)+"deg");
    p.style.left=(42+Math.random()*16)+"%";
    p.style.animationDelay=(Math.random()*.22)+"s";
    layer.appendChild(p);setTimeout(()=>p.remove(),1500);
  }
}
function pulseRobot(){const robot=$("robot");robot.classList.remove("tap");void robot.offsetWidth;robot.classList.add("tap");setTimeout(()=>robot.classList.remove("tap"),650)}
function levelCheck(){if(state.exp>=100){state.exp-=100;state.level+=1;spawnEffect("⭐",10);showToast("레벨 업! Lv."+state.level)}}
function addEvent(title,description){const row=document.createElement("div");row.className="event-item";row.innerHTML='<div class="event-time">지금</div><div class="event-content"><strong>'+title+'</strong><span>'+description+'</span></div>';$("eventList").prepend(row)}

function petRobot(){if(state.cleaning){showToast("청소가 끝난 후 로보킹을 쓰다듬어 주세요.");return}state.heart=Math.min(100,state.heart+2);state.exp+=1;pulseRobot();spawnEffect("💖",7);levelCheck();render();showToast("로보킹의 기분이 좋아졌어요.")}
function feedRobot(){if(state.food<=0){showToast("음식이 부족해요. 리워드에서 구매해 주세요.");return}state.food-=1;state.soc+=12;state.exp+=8;pulseRobot();spawnEffect("⚡",8);levelCheck();render();showToast("배터리가 12% 회복되었습니다.")}
function playRobot(){if(state.soc<5){showToast("배터리가 부족해서 놀 수 없어요.");return}state.soc-=3;state.exp+=5;pulseRobot();spawnEffect("💖",8);levelCheck();render();showToast("로보킹의 친밀도와 경험치가 올랐어요.")}
function trainRobot(){if(state.soc<8){showToast("훈련 전에 충전이 필요해요.");return}state.soc-=6;state.health=Math.min(100,state.health+3);state.exp+=12;pulseRobot();spawnEffect("✨",8);levelCheck();render();showToast("로보킹이 훈련을 완료했습니다.")}
function takePhoto(){pulseRobot();spawnEffect("📸",5);openModal("오늘의 사진","왕관을 쓴 로보킹의 사진을 촬영했습니다.<br><br>향후 장식 아이템과 청소 완료 장면을 사진첩에 저장할 수 있습니다.")}
function decorateRobot(){
  switchPage("rewardPage");
  showToast("리워드에서 아이템을 사면 로보킹에게 계속 장착돼요.");
}

function showStatus(){
  if(!state.profileReady){
    openModal("먼저 우리 집을 배울게요","아직 로보킹이 우리 집을 잘 몰라요.<br><br>1회차 학습 청소를 시작하면 방 구조와 바닥 상태를 기억하고, 다음부터 더 똑똑하게 청소를 준비할 수 있어요.");
    return;
  }
  if(!state.predicted){
    openModal("우리 집을 기억했어요","1회차 학습 청소가 끝났어요.<br><br>이제 오늘 청소 조건을 고르고 <b>오늘 청소 준비하기</b>를 눌러 주세요.<br>로보킹이 알아서 필요한 만큼 준비할게요.");
    return;
  }
  const scopeText=state.selectedScope==="home"?"집 전체":state.selectedLabel;
  const zoneInfo=state.selectedScope==="zone"?"<br>바닥: <b>"+(state.floorType||"정보 없음")+"</b><br>상태: <b>"+(state.dirtLevel||"평소")+"</b>":"";
  const readyText=state.soc>=state.targetSoc?"지금 바로 출동할 수 있어요.":"잠깐만 충전하면 출동할 수 있어요.";
  openModal("오늘 청소 준비 완료",scopeText+" 청소를 준비했어요."+zoneInfo+"<br><br>오늘 조건: <b>"+state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel+"</b><br><br>"+readyText+"<br>로보킹이 배터리를 아끼면서 청소할게요.");
}

function getRemainingCleaningSoc(){
  const total=Math.max(0,Number(state.requiredSoc||0));
  let remaining=Number(state.cleaningRemainingSoc);
  if(!Number.isFinite(remaining) || remaining<=0 || state.progress>=100 || state.missionDone){
    remaining=total;
  }
  return Math.round(Math.min(Math.max(remaining,0),total)*10)/10;
}

function resetCleaningMissionPlan(){
  state.cleaningRemainingSoc=Math.max(0,Number(state.requiredSoc||0));
  state.cleaningSegmentIndex=0;
  state.splitCleaning=state.cleaningRemainingSoc>MAX_SINGLE_PASS_USE;
  state.progress=0;
  state.missionDone=false;
}

function showSplitCleaningModal(){
  state.targetSoc=MAX_CHARGE_SOC;
  state.splitCleaning=true;
  render();
  const body="청소할 양이 많아서<br>"
    +"한 번에 무리하면 로보킹이 금방 지칠 수 있어요.<br><br>"
    +"배터리를 아끼기 위해<br>"
    +"잠깐 쉬어가며 이어서 청소할게요.";
  openModal("이번 청소는 나눠서 할게요",body,{
    showCancel:true,
    cancelText:"취소",
    confirmText:state.soc<MAX_CHARGE_SOC?"충전하고 시작":"청소 시작",
    onConfirm:()=>{
      closeModal();
      if(state.soc<MAX_CHARGE_SOC){
        chargeRobot(true);
      }else{
        startCleaning();
      }
    }
  });
}

function showReserveChargeModal(autoStartAfterCharge=false){
  const remaining=getRemainingCleaningSoc();
  const needed=targetFromRequired(remaining);
  state.targetSoc=needed;
  render();
  const body=state.selectedLabel+" 청소를 바로 시작하기엔<br>로보킹의 힘이 조금 부족해요.<br><br>잠깐 충전하고 나면<br>청소를 더 편하게 마칠 수 있어요.<br><br>필요한 만큼만 채우고 바로 출발할게요!";
  openModal("먼저 힘을 채울게요",body,{
    showCancel:true,
    cancelText:"취소",
    confirmText:"충전하고 시작",
    onConfirm:()=>{
      closeModal();
      switchPage("homePage");
      chargeRobot(autoStartAfterCharge);
    }
  });
}

function showChargeChoiceModal(autoStartAfterCharge=false){
  const remaining=getRemainingCleaningSoc();
  const needed=targetFromRequired(remaining);
  state.targetSoc=needed;
  render();
  const scopeText=state.selectedScope==="zone"?state.selectedLabel+"은 <b>"+(state.floorType||"바닥 정보")+"</b> 바닥이라 조금 더 힘이 필요해요.<br><br>":"";
  const body=scopeText+"이번 청소를 끝까지 편하게 마치려면<br>로보킹이 힘을 조금 더 채우면 좋아요.<br><br>필요한 만큼만 충전하고<br>바로 청소를 시작할게요.";
  openModal("아직 배가 조금 고파요!",body,{
    showCancel:true,
    cancelText:"취소",
    confirmText:"충전하고 시작",
    onConfirm:()=>{
      closeModal();
      switchPage("homePage");
      chargeRobot(autoStartAfterCharge);
    }
  });
}

function startCleaning(){
  if(state.cleaning){showToast("이미 청소 중이에요.");return}
  if(state.charging){showToast("충전이 끝난 후 청소할게요.");return}
  if(state.mapping){showToast("1회차 학습이 끝난 뒤 청소할 수 있어요.");return}
  if(!state.profileReady){
    setGuide("아직 로보킹이 우리 집을 잘 몰라요. 먼저 1회차 학습 청소를 시작해 주세요.","warning");
    showToast("먼저 로보킹에게 우리 집을 알려주세요.");
    $("speech").innerHTML="<strong style='color:#ef8c32'>학습이 먼저예요</strong><br>집 정보를 저장한 뒤 청소할 수 있어요.";
    switchPage("homePage");
    return;
  }
  if(!state.predicted){
    showToast("청소 전 오늘 청소 준비하기를 먼저 눌러주세요.");
    $("speech").innerHTML="<strong style='color:#2f8b3a'>청소 준비가 필요해요</strong><br>오늘 상태를 먼저 알려주세요.";
    switchPage("homePage");
    return;
  }

  const totalRequired=Math.max(0,Number(state.requiredSoc||0));
  if(totalRequired<=0){showToast("오늘 청소 준비를 다시 실행해 주세요.");return}

  if(state.missionDone || state.progress>=100){
    resetCleaningMissionPlan();
  }

  let remaining=getRemainingCleaningSoc();

  // 90% 상한과 15% 잔량 기준으로 한 번에 끝낼 수 없는 경우에만 분할 청소 안내를 띄웁니다.
  if(remaining>MAX_SINGLE_PASS_USE && state.soc<MAX_CHARGE_SOC){
    showSplitCleaningModal();
    return;
  }

  const neededStart=targetFromRequired(remaining);
  state.targetSoc=neededStart;

  // 청소 시작 전 Reserve 배터리 Guard
  if(remaining<=MAX_SINGLE_PASS_USE && state.soc<neededStart){
    showReserveChargeModal(true);
    return;
  }

  if(state.soc<=MIN_RESERVE_SOC){
    showReserveChargeModal(true);
    return;
  }

  const availableUse=Math.max(0,Number(state.soc||0)-MIN_RESERVE_SOC);
  let segmentUse=remaining;
  let segmentWillComplete=true;

  // 분할 청소 중 첫 구간: 현재 배터리에서 15%를 남길 수 있는 만큼만 청소
  if(remaining>availableUse){
    segmentUse=availableUse;
    segmentWillComplete=false;
  }

  if(segmentUse<=0){
    showReserveChargeModal(true);
    return;
  }

  state.cleaning=true;
  state.chargeComplete=false;
  state.missionDone=false;
  const startSoc=Number(state.soc||0);
  const startProgress=Number(state.progress||0);
  const progressGain=Math.max(1,Math.round(segmentUse/totalRequired*100));
  const endProgress=segmentWillComplete?100:Math.min(99,startProgress+progressGain);
  const endSoc=Math.max(MIN_RESERVE_SOC,Math.round((startSoc-segmentUse)*10)/10);
  state.cleaningSegmentIndex+=1;
  render();
  setGuide(state.selectedLabel+" 청소를 시작했어요. 로보킹이 배터리를 아끼면서 깨끗하게 청소할게요.","normal");
  showToast("청소 시작! 로보킹이 배터리를 아끼며 청소해요.");

  let step=0;
  const totalSteps=20;
  const timer=setInterval(()=>{
    step+=1;
    const ratio=step/totalSteps;
    state.progress=Math.round(startProgress+(endProgress-startProgress)*ratio);
    state.soc=Math.max(MIN_RESERVE_SOC,Math.round((startSoc-segmentUse*ratio)*10)/10);
    state.temperature=Math.min(36,state.temperature+.25);
    render();

    if(state.soc<=CRITICAL_DOCK_SOC && !segmentWillComplete){
      step=totalSteps;
    }

    if(step>=totalSteps){
      clearInterval(timer);
      state.cleaning=false;
      state.temperature=29;
      state.soc=endSoc;
      const newRemaining=Math.max(0,Math.round((remaining-segmentUse)*10)/10);
      state.cleaningRemainingSoc=newRemaining;

      if(newRemaining>0.2){
        state.progress=endProgress;
        state.targetSoc=targetFromRequired(newRemaining);
        addEvent("잠깐 쉬어가기",state.selectedLabel+" 청소 중 로보킹이 잠깐 충전한 뒤 남은 곳을 이어서 청소하기로 했어요.");
        render();
        $("speech").innerHTML="<strong style='color:#ef8c32'>잠깐 쉬어갈게요!</strong><br>조금만 쉬고 다시 힘낼게요.";
        setGuide("로보킹이 조금 지쳤어요. 잠깐 충전하고 남은 곳을 이어서 청소할게요.","warning");
        showToast("잠깐 충전하고 남은 곳을 이어서 청소할게요.");
        setTimeout(()=>openModal("잠깐 쉬어갈게요!","제가 조금 지쳤어요.<br>잠깐 충전하고 나면<br>남은 곳도 다시 힘내서 청소할게요!<br><br>지금 배터리: <b>"+fmtSoc(state.soc)+"%</b>",{
          showCancel:true,
          cancelText:"나중에",
          confirmText:"충전하고 이어서",
          onConfirm:()=>{closeModal();chargeRobot(true);}
        }),450);
        return;
      }

      state.cleaningRemainingSoc=0;
      state.progress=100;
      state.missionDone=true;
      state.celebrating=true;
      state.cleanCount+=1;
      state.coins+=50;
      state.exp+=20;
      state.area=Math.round((state.area||0)+(state.cleaningAreaM2||0));
      state.average=Math.round((state.average+Math.max(15,Math.round(state.requiredSoc*1.4)))/2);
      levelCheck();
      addEvent(state.selectedLabel+" 청소 완료","로보킹이 배터리를 아끼며 청소를 마쳤어요.");
      spawnEffect("🎉",15);spawnEffect("⭐",9);
      render();
      $("speech").innerHTML="<strong style='color:#2f8b3a'>청소 완료!</strong><br>+50코인을 받았어요.";
      $("modeChip").textContent="🏆 "+state.selectedLabel+" 완료 · +50코인";
      setGuide("청소 완료! 로보킹이 무리하지 않고 잘 마쳤어요. 보상으로 +50코인을 받았어요.","done");
      showToast("청소 완료! 로보킹이 +50코인을 가져왔어요.");
      setTimeout(()=>{state.celebrating=false;render()},2200);
    }
  },320);
}

function chargeRobot(autoStart=false){
  if(state.cleaning){showToast("청소가 끝난 후 충전할 수 있어요.");return}
  if(state.charging){showToast("이미 충전 중이에요.");return}
  if(state.soc>=state.targetSoc){
    if(autoStart){setTimeout(startCleaning,250);return}
    state.chargeComplete=true;
    render();
    $("speech").innerHTML="<strong>배불러요!</strong><br>이제 "+state.selectedLabel+" 청소가 가능해요.";
    $("modeChip").textContent="💖 출동 준비 완료";
    setGuide("이미 충분히 준비됐어요. 바로 청소를 시작할 수 있어요.","done");
    showToast("이미 충분히 준비됐어요. 바로 출동할 수 있어요.");
    setTimeout(()=>{state.chargeComplete=false;render()},2600);
    return;
  }
  closeModal();
  switchPage("homePage");
  state.charging=true;
  state.chargeComplete=false;
  render();
  setGuide("맞춤 충전을 시작했어요. 로보킹이 필요한 만큼만 채우고 알아서 멈춰요.","charging");
  showToast("맞춤 충전 시작! 필요한 만큼만 채울게요.");
  const timer=setInterval(()=>{
    state.soc=Math.min(state.targetSoc,state.soc+2);
    state.temperature=Math.min(32,state.temperature+.1);
    spawnEffect("⚡",2);
    render();
    if(state.soc>=state.targetSoc){
      clearInterval(timer);
      state.charging=false;
      state.temperature=29;
      state.acceptCount+=1;
      state.chargeComplete=true;
      addEvent("맞춤 충전 완료",state.selectedLabel+" 청소에 필요한 만큼만 채우고 멈췄어요.");
      spawnEffect("💖",12);
      spawnEffect("✨",8);
      render();
      $("speech").innerHTML="<strong>배불러요!</strong><br>출동할 준비가 됐어요!";
      $("modeChip").textContent="💖 충전 완료 · 출동 준비";
      setGuide("충전 완료! 로보킹이 곧 바로 출동할게요.","done");
      showToast("충전 완료! 이제 로보킹이 출동할 수 있어요.");
      setTimeout(()=>{state.chargeComplete=false;render()},3200);
      if(autoStart){setTimeout(startCleaning,1000)}
    }
  },150);
}
function buyFood(){
  if(state.coins<50){showToast("코인이 조금 부족해요. 청소 미션으로 코인을 모아보세요.");return}
  state.coins-=50;
  state.food+=1;
  render();
  showToast("냠냠! 에너지 간식 1개를 챙겼어요. 필요할 때 먹여주세요.");
}
function handleRewardItem(key){
  const item=shopItems[key];
  if(!item)return;
  if(!state.ownedItems[key]){
    if(state.coins<item.cost){
      showToast(item.name+"을(를) 데려오려면 코인이 조금 더 필요해요.");
      return;
    }
    state.coins-=item.cost;
    state.ownedItems[key]=true;
    state.equippedItems[item.slot]=item.value;
    saveCloset();
    switchPage("homePage");
    setTimeout(()=>{spawnEffect(item.icon,10);showToast(item.message);render();},250);
    render();
    return;
  }
  const isEquipped=state.equippedItems[item.slot]===item.value;
  if(isEquipped){
    state.equippedItems[item.slot]=(item.slot==="head"?"crown":null);
    saveCloset();
    render();
    showToast(item.name+"을(를) 잠시 벗겨뒀어요.");
  }else{
    state.equippedItems[item.slot]=item.value;
    saveCloset();
    switchPage("homePage");
    setTimeout(()=>{spawnEffect(item.icon,8);showToast(item.message);render();},250);
    render();
  }
}

function switchRewardTab(tab){
  state.rewardTab=tab;
  render();
}
function handleCoupon(key){
  const item=couponItems[key];
  if(!item)return;
  if(state.coins<item.cost){
    const need=Math.max(0,item.cost-state.coins);
    showToast(item.name+" 교환까지 "+need+"코인 더 필요해요.");
    return;
  }
  state.coins-=item.cost;
  state.ownedCoupons[key]=Number(state.ownedCoupons[key]||0)+1;
  saveCoupons();
  render();
  showToast(item.message+" 혜택: "+item.benefit);
}


const actions={
  startFirstMapping:startFirstMapping,
  predictSoc:predictSocFromConditions,
  selectHome:()=>selectScenario("home"),selectZone1:()=>selectScenario("zone",1),selectZone2:()=>selectScenario("zone",2),selectZone3:()=>selectScenario("zone",3),selectZone4:()=>selectScenario("zone",4),selectZone5:()=>selectScenario("zone",5),selectZone6:()=>selectScenario("zone",6),selectZone7:()=>selectScenario("zone",7),selectZone8:()=>selectScenario("zone",8),
  pet:petRobot,feed:feedRobot,play:playRobot,train:trainRobot,photo:takePhoto,clean:startCleaning,charge:chargeRobot,status:showStatus,
  record:()=>switchPage("recordPage"),event:()=>switchPage("eventPage"),decorate:decorateRobot,shop:()=>switchPage("rewardPage"),chargeFromBattery:()=>{switchPage("homePage");setTimeout(chargeRobot,220)},buyFood:buyFood,
  itemRibbon:()=>handleRewardItem("ribbon"),itemHat:()=>handleRewardItem("hat"),itemBunny:()=>handleRewardItem("bunny"),itemCat:()=>handleRewardItem("cat"),itemSparkle:()=>handleRewardItem("sparkle"),
  rewardTabItems:()=>switchRewardTab("items"),rewardTabCoupons:()=>switchRewardTab("coupons"),
  couponLg5:()=>handleCoupon("lg5"),couponCleanKit:()=>handleCoupon("cleanKit"),couponBatteryCare:()=>handleCoupon("batteryCare"),couponMoveIn:()=>handleCoupon("moveIn"),
  ribbon:()=>handleRewardItem("ribbon"),sparkle:()=>handleRewardItem("sparkle"),hat:()=>handleRewardItem("hat")
};

document.addEventListener("click",(event)=>{const nav=event.target.closest("[data-page]");if(nav){switchPage(nav.dataset.page);return}const action=event.target.closest("[data-action]");if(action&&typeof actions[action.dataset.action]==="function"){actions[action.dataset.action]()}});
// 1회차 학습 청소는 핵심 CTA라서, 이벤트 위임/터치/겹침 이슈가 있어도 반드시 동작하도록 여러 경로로 직접 연결합니다.
let lastLearnClickAt=0;
function triggerLearnButton(event){
  if(event){
    event.preventDefault();
    event.stopPropagation();
    if(event.stopImmediatePropagation)event.stopImmediatePropagation();
  }
  const now=Date.now();
  if(now-lastLearnClickAt<700)return;
  lastLearnClickAt=now;
  if(typeof startFirstMapping==="function")startFirstMapping();
}
window.__forceStartFirstMapping=triggerLearnButton;
const learnBtnDirect=$("learnBtn");
if(learnBtnDirect){
  learnBtnDirect.onclick=triggerLearnButton;
  learnBtnDirect.onpointerdown=triggerLearnButton;
  learnBtnDirect.onmousedown=triggerLearnButton;
  learnBtnDirect.ontouchstart=triggerLearnButton;
  learnBtnDirect.addEventListener("click",triggerLearnButton,true);
  learnBtnDirect.addEventListener("pointerdown",triggerLearnButton,true);
  learnBtnDirect.addEventListener("pointerup",triggerLearnButton,true);
  learnBtnDirect.addEventListener("mousedown",triggerLearnButton,true);
  learnBtnDirect.addEventListener("touchstart",triggerLearnButton,{capture:true,passive:false});
  learnBtnDirect.addEventListener("touchend",triggerLearnButton,{capture:true,passive:false});
}
document.addEventListener("pointerdown",(event)=>{
  const btn=event.target && event.target.closest ? event.target.closest("#learnBtn") : null;
  if(btn)triggerLearnButton(event);
},true);
document.addEventListener("touchstart",(event)=>{
  const target=event.target;
  const btn=target && target.closest ? target.closest("#learnBtn") : null;
  if(btn)triggerLearnButton(event);
},{capture:true,passive:false});

$("modalCancel").addEventListener("click",closeModal);$("modalConfirm").addEventListener("click",()=>modalConfirmHandler());$("modal").addEventListener("click",(event)=>{if(event.target===$("modal"))closeModal()});
$("targetSlider").addEventListener("input",(event)=>{state.targetSoc=Number(event.target.value);render()});
$("tempSlider").addEventListener("input",(event)=>{state.temperature=Number(event.target.value);render()});
["scopeSelect","cleanModeSelect","intensitySelect","todayStateSelect"].forEach(id=>{
  const el=$(id);
  if(el)el.addEventListener("change",()=>{
    if(state.profileReady && state.predicted){
      state.predicted=false;
      const loading=$('predictLoading');
      if(loading)loading.textContent="조건이 바뀌었어요. 오늘 청소 준비하기를 다시 눌러주세요.";
      render();
    }
  });
});

setInterval(()=>{if(state.cleaning||state.charging||state.celebrating)return;const robot=$("robot");robot.classList.remove("look-left","look-right");const d=Math.random();if(d<.33)robot.classList.add("look-left");else if(d<.66)robot.classList.add("look-right");setTimeout(()=>robot.classList.remove("look-left","look-right"),1100)},2800);
populateConditionSelectors();
render();
</script>
</body>
</html>
"""

APP_HTML = APP_HTML.replace("__UI_PREDICTION_DATA__", UI_PREDICTION_JSON)

components.html(APP_HTML, height=1010, scrolling=False)
