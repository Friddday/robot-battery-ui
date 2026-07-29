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

</style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ML SOC 예측 결과 CSV 연결부
# GitHub에는 아래 구조로 CSV를 올리면 됩니다.
# data/home_model_predictions.csv
# data/zone_model_predictions.csv
# ============================================================

BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"
HOME_PRED_PATH = DATA_DIR / "home_model_predictions.csv"
ZONE_PRED_PATH = DATA_DIR / "zone_model_predictions.csv"

# 데모용 현재 SOC. 실제 제품에서는 로봇/앱에서 받은 현재 SOC로 교체하면 됩니다.
CURRENT_SOC = 20


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
                    "mopEnabled": mop_enabled,
                    "obstacleLevel": "중간",
                    "floorType": floor_types[i-1],
                    "dirtLevel": dirt_levels[i-1],
                    "suctionMode": "AI 자동",
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
                "mopEnabled": mop_enabled,
                "obstacleLevel": "중간",
                "floorType": "혼합",
                "dirtLevel": "평균",
                "suctionMode": "AI 자동",
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
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(home_row, ["obstacle_level_first", "obstacle_level"], ""),
        "floorType": "혼합",
        "dirtLevel": "평균",
        "suctionMode": "AI 자동",
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
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(zrow, ["obstacle_level"], home.get("obstacleLevel", "")),
        "floorType": _safe_text(zrow, ["floor_type"], ""),
        "dirtLevel": _safe_text(zrow, ["dirt_level"], ""),
        "suctionMode": _safe_text(zrow, ["effective_suction_mode"], ""),
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
                for idx, (_, zrow) in enumerate(zdf.head(5).iterrows(), start=1):
                    zone = _build_zone_scenario(zrow, idx, home)
                    # home의 청소방식과 일관되게 표시
                    zone["cleaningType"] = home["cleaningType"]
                    zone["mopEnabled"] = home["mopEnabled"]
                    zones.append(zone)

            if len(zones) >= 5:
                runs.append({
                    "globalRunId": gid,
                    "areaPyung": home["areaPyung"],
                    "mopEnabled": home["mopEnabled"],
                    "cleaningType": home["cleaningType"],
                    "home": home,
                    "zones": zones[:5],
                })

    # home CSV가 없고 zone CSV만 있을 때도 최소 동작하도록 처리
    if not runs and zone_df is not None and len(zone_df) > 0 and "global_run_id" in zone_df.columns:
        for gid, zdf in zone_df.groupby("global_run_id"):
            if len(zdf) < 5:
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
                "cleaningType": "물걸레" if mop_enabled else "건식", "mopEnabled": mop_enabled,
                "obstacleLevel": _safe_text(first, ["obstacle_level"], ""), "floorType": "혼합",
                "dirtLevel": "평균", "suctionMode": "AI 자동"
            }
            zones = []
            for idx, (_, zrow) in enumerate(zdf.head(5).iterrows(), start=1):
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
.nav{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-top:12px}
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


/* ML SOC Plan Selector */
.plan-panel{margin-bottom:8px;padding:11px 10px;background:rgba(255,248,231,.98)}
.plan-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.plan-title{font-size:11px;font-weight:900}.plan-model{padding:4px 7px;border-radius:11px;background:#eaf4df;color:#367b36;font-size:8px;font-weight:900}
.scope-buttons{display:grid;grid-template-columns:1.05fr repeat(5,1fr);gap:5px;margin-bottom:8px}
.scope-btn{min-height:37px;padding:5px 2px;border:1px solid rgba(124,83,43,.16);border-radius:12px;background:#f3e2be;color:#5a412e;font-size:8px;font-weight:900;line-height:1.2;box-shadow:0 3px 7px rgba(69,43,20,.09)}
.scope-btn.active{background:linear-gradient(180deg,#65ae4b,#368e3d);color:#fff;border-color:transparent;box-shadow:0 5px 12px rgba(47,139,58,.25)}
.learn-panel{margin-bottom:8px;padding:9px;border-radius:13px;background:linear-gradient(145deg,#fff8df,#f3dfb2);border:1px solid rgba(124,83,43,.13)}.learn-top{display:flex;justify-content:space-between;align-items:center;gap:8px}.learn-title{font-size:10px;font-weight:900}.learn-pill{padding:4px 7px;border-radius:11px;background:#fff;color:#8b6139;font-size:8px;font-weight:900}.learn-desc{margin-top:5px;color:#6f4f38;font-size:8px;line-height:1.45;font-weight:800}.learn-progress{height:8px;margin-top:7px;overflow:hidden;border-radius:12px;background:#dcc79f}.learn-fill{width:0;height:100%;border-radius:inherit;background:linear-gradient(90deg,#62aa49,#ffd44f);transition:width .25s}.learn-status{margin-top:6px;font-size:8px;line-height:1.45;font-weight:900;color:#4b3324}.learn-steps{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-top:7px}.learn-step{padding:5px 4px;border-radius:9px;background:rgba(255,255,255,.58);color:#806047;font-size:7px;font-weight:900;text-align:center}.learn-step.done{background:#e7f4d9;color:#2f8b3a}.learn-step.active{background:#fff;color:#ef8c32;box-shadow:0 2px 6px rgba(89,56,26,.12)}.learn-btn{width:100%;min-height:34px;margin-top:7px;border:0;border-radius:11px;background:linear-gradient(90deg,#ef8c32,#ffb24b);color:#fff;font-size:10px;font-weight:900;box-shadow:0 5px 10px rgba(239,140,50,.22)}.learn-btn.ready{background:linear-gradient(90deg,#4a9b42,#75b84e)}.locked-area{opacity:.45;filter:grayscale(.15)}.condition-panel{margin-bottom:8px;padding:8px;border-radius:13px;background:#fff2cf;border:1px solid rgba(124,83,43,.12)}
.condition-title{margin-bottom:7px;font-size:10px;font-weight:900;color:#6f4f38;line-height:1.4}
.condition-row{display:grid;grid-template-columns:.7fr 1fr .7fr 1fr;gap:6px;align-items:center}.condition-row label{font-size:9px;font-weight:900;color:#6c4a2f}.condition-select{width:100%;min-height:34px;border:1px solid rgba(124,83,43,.22);border-radius:10px;background:#fffaf0;color:#4b3324;font-size:10px;font-weight:900;padding:0 7px}.predict-condition-grid{display:grid;grid-template-columns:.72fr 1fr .72fr 1fr;gap:6px;align-items:center;margin-top:8px}.predict-condition-grid label{font-size:9px;font-weight:900;color:#6c4a2f;white-space:nowrap}.condition-help{font-size:9px;line-height:1.5;color:#8a6a45;margin:7px 0 0;font-weight:800}.first-learn-note{padding:8px 9px;border-radius:11px;background:rgba(255,255,255,.58);font-size:10px;line-height:1.55;color:#6f4f38}.predict-btn{width:100%;min-height:36px;margin-top:8px;border:0;border-radius:11px;background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;font-size:11px;font-weight:900;box-shadow:0 5px 10px rgba(47,139,58,.2)}.predict-loading{margin-top:6px;min-height:18px;font-size:9px;line-height:1.45;color:#745431;font-weight:800}.predict-loading.active{color:#2f8b3a}
.selected-plan{display:grid;grid-template-columns:1fr .9fr;gap:7px;align-items:stretch}.plan-summary{padding:9px;border-radius:12px;background:#fff4d5;font-size:9px;line-height:1.55;font-weight:800}.plan-summary strong{color:#2f8b3a}.plan-soc{padding:9px;border-radius:12px;background:#f0e0be;text-align:center;font-weight:900}.plan-soc-label{font-size:8px;color:#79583e}.plan-soc-value{margin-top:2px;color:#ef573f;font-size:22px;line-height:1}.plan-soc-sub{margin-top:4px;font-size:8px;color:#76553e;line-height:1.35}

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
        <button class="nav-btn" data-page="rewardPage">리워드</button>
      </nav>
    </header>

    <main class="pages">

      <section class="page active" id="homePage">
        <div class="room" id="room">
          <div class="wall-light"></div><div class="floor"></div>
          <div class="plant">🪴</div><div class="house"></div><div class="sofa"></div>
          <div class="speech" id="speech"><strong>배가 든든해요!</strong><br>청소를 준비할게요!</div>
          <div class="mode-chip" id="modeChip">✨ AI 권장 SOC 81%</div>
          <div class="rug"></div>
          <div class="clean-path"><div class="clean-fill" id="cleanFill"></div></div>
          <div class="charge-ring"></div>
          <div class="dust"><span></span><span></span><span></span><span></span><span></span><span></span></div>

          <div class="robot" id="robot" data-action="pet">
            <div class="crown">👑</div><div class="spark" id="spark">✨</div><div class="robot-top"></div>
            <div class="face">
              <div class="eye left"></div><div class="eye right"></div>
              <div class="cheek left"></div><div class="cheek right"></div><div class="mouth"></div>
            </div>
            <div class="slot"></div>
          </div>

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
              <div class="plan-title">우리 집 학습 & AI SOC 예측</div>
              <div class="plan-model" id="planModel">1회차 학습 전</div>
            </div>
            <div class="learn-panel" id="learnPanel">
              <div class="learn-top">
                <div class="learn-title">처음 사용할 때는 로보킹이 집을 먼저 배워요</div>
                <div class="learn-pill" id="learnPill">초기 학습</div>
              </div>
              <div class="learn-desc">1회차 청소로 집 구조, 구역 면적, 바닥 타입, 오염도, 장애물 수준, 실제 SOC 소모 기록을 저장한 뒤 AI 예측을 시작합니다.</div>
              <div class="learn-progress"><div class="learn-fill" id="learnFill"></div></div>
              <div class="learn-status" id="learnStatus">1회차 학습 청소를 시작하면 로보킹이 집 구조와 구역 정보를 자동으로 기록해요.</div>
              <div class="learn-steps" id="learnSteps"></div>
              <button class="learn-btn" id="learnBtn" data-action="startFirstMapping">🏠 1회차 학습 청소 시작</button>
            </div>
            <div class="condition-panel" id="conditionPanel">
              <div class="condition-title" id="conditionTitle">1회차 학습 청소로 우리 집 프로필을 먼저 만들어요</div>

              <div id="firstLearnInputs">
                <div class="condition-help first-learn-note">
                  평수, 구역별 면적, 바닥 타입, 오염도, 장애물 수준은 1회차 학습 청소에서 자동으로 기록돼요.<br>
                  프로토타입에서는 CSV에 저장된 여러 집 프로필 중 하나를 랜덤으로 불러와 학습 과정을 보여줍니다.
                </div>
              </div>

              <div id="predictionInputs" style="display:none;">
                <div class="condition-help">저장된 우리 집 프로필을 기준으로, 오늘 청소 조건만 선택해 주세요.</div>
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

              <button class="predict-btn" id="predictBtn" data-action="predictSoc">🤖 AI 예측하기</button>
              <div class="predict-loading" id="predictLoading">1회차 학습 청소가 끝나면 AI 예측을 실행할 수 있어요.</div>
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
                <div class="plan-soc-label">AI 목표 SOC</div>
                <div class="plan-soc-value"><span id="planTargetSoc">81</span>%</div>
                <div class="plan-soc-sub" id="planSocSub">예상 소모량 + 안전마진 15%</div>
              </div>
            </div>
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
              <div class="mini-title">배터리 상태</div>
              <div class="battery-info">15%~90% 사이에서<br>사용하는 것이<br>수명 연장에 좋아요!</div>
              <div class="battery-face" id="batteryFace">😊</div>
              <div class="scale"><div class="pointer" id="pointer"></div></div>
              <div class="scale-labels"><span>0%</span><span>15%</span><span>90%</span><span>100%</span></div>
              <div class="battery-message" id="batteryMessage">배터리 상태가 좋아요.</div>
            </section>

            <section class="mini-card time-card">
              <div class="mini-title">예상 청소 가능 시간</div>
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
        <div class="section-title">배터리 건강 관리</div>

        <div class="gauge-grid">
          <div class="panel gauge-card">
            <div class="gauge" id="socGauge" style="--value:81;--color:#49a646">
              <div class="gauge-content"><div class="gauge-label">SOC</div><div class="gauge-value" id="socGaugeText">81%</div></div>
            </div>
            <div class="gauge-desc">권장 운용 구간<br>15%~90%</div>
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
            <div class="control-head"><span>목표 SOC 조절</span><span class="control-value" id="targetLabel">81%</span></div>
            <input id="targetSlider" type="range" min="15" max="90" value="81">
            <div class="control-caption"><span>15%</span><span>배터리 보호 권장</span><span>90%</span></div>
          </div>
          <div class="control-row">
            <div class="control-head"><span>온도 시뮬레이션</span><span class="control-value" id="tempLabel">29℃</span></div>
            <input id="tempSlider" type="range" min="15" max="50" value="29">
            <div class="control-caption"><span>15℃</span><span>현재 배터리 온도</span><span>50℃</span></div>
          </div>
          <button class="primary-btn" data-action="chargeFromBattery">AI 권장 SOC까지 맞춤 충전</button>
        </div>

        <div class="panel chart-panel">
          <div class="panel-head"><div class="panel-title">오늘 SOC 변화</div><div class="badge">고SOC 방치 감소</div></div>
          <svg class="soc-chart" viewBox="0 0 340 165">
            <line class="grid-line" x1="30" y1="28" x2="330" y2="28"></line>
            <line class="grid-line" x1="30" y1="132" x2="330" y2="132"></line>
            <text class="chart-text" x="3" y="32">90%</text><text class="chart-text" x="5" y="136">15%</text>
            <polyline class="line-red" points="30,128 80,102 128,54 180,35 235,31 285,29 328,28"></polyline>
            <polyline class="line-green" id="aiLine" points="30,128 80,103 128,82 180,74 235,74 285,74 328,74"></polyline>
          </svg>
          <div class="legend">
            <span><span class="dot" style="background:#eb6650"></span>기존 완충 방식</span>
            <span><span class="dot" style="background:#4c9a43"></span>AI 가변 충전</span>
          </div>
        </div>

        <div class="panel insight"><div class="insight-row"><div class="insight-icon">💡</div><div id="insightText">최근 청소 패턴을 분석한 결과, 오늘은 SOC 81%까지만 충전해도 예상 청소를 완료할 수 있습니다.</div></div></div>
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
          <div class="record-card"><div class="record-label">AI 추천 수락</div><div class="record-value"><span id="acceptText">4</span>회</div></div>
        </div>

        <div class="panel events">
          <div class="panel-title">이벤트 기록</div>
          <div id="eventList">
            <div class="event-item"><div class="event-time">14:20</div><div class="event-content"><strong>맞춤 충전 완료</strong><span>목표 SOC 81%에서 자동 충전을 종료했습니다.</span></div></div>
            <div class="event-item"><div class="event-time">10:15</div><div class="event-content"><strong>사용자 패턴 분석</strong><span>거실 청소 예상 소비량 27%를 반영했습니다.</span></div></div>
            <div class="event-item"><div class="event-time">08:40</div><div class="event-content"><strong>배터리 상태 정상</strong><span>배터리 온도와 건강도가 안정 범위에 있습니다.</span></div></div>
          </div>
        </div>
      </section>

      <section class="page" id="rewardPage">
        <div class="section-kicker">REWARD</div>
        <div class="section-title">로보킹 성장 리워드</div>

        <div class="panel level-panel">
          <div class="level-robot">🤖</div>
          <div class="level-number">Lv. <span id="levelText">13</span></div>
          <div class="level-track"><div class="level-fill" id="expFill"></div></div>
          <div class="level-caption">경험치 <span id="expText">55</span> / 100</div>
        </div>

        <div class="reward-grid">
          <div class="reward-card"><div class="reward-icon">🥣</div><div class="reward-title">배터리 음식</div><div class="reward-desc">SOC를 12% 회복합니다.</div><button class="reward-btn" data-action="buyFood">50 코인</button></div>
          <div class="reward-card"><div class="reward-icon">🎀</div><div class="reward-title">빨간 리본</div><div class="reward-desc">로보킹을 꾸며주세요.</div><button class="reward-btn" data-action="ribbon">미리보기</button></div>
          <div class="reward-card"><div class="reward-icon">🧢</div><div class="reward-title">탐험가 모자</div><div class="reward-desc">청소 미션 전용 아이템입니다.</div><button class="reward-btn" data-action="hat">120 코인</button></div>
          <div class="reward-card"><div class="reward-icon">✨</div><div class="reward-title">반짝이 효과</div><div class="reward-desc">청소 완료 효과를 변경합니다.</div><button class="reward-btn" data-action="sparkle">효과 체험</button></div>
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
  {key:'soc',label:'실제 SOC 소모 기록'}
];

const $=(id)=>document.getElementById(id);
const clamp=(v,min,max)=>Math.min(Math.max(v,min),max);
const fmtSoc=(v)=>Number(v || 0).toFixed(1).replace(/\.0$/,"");
const cleanMinutes=()=>Math.max(0,Math.round(state.soc*.56));
const targetFromRequired=(required)=>clamp(Math.round(Number(required||0)+15),15,90);

const cleanModeLabels={dry:"건식",mop:"물걸레",both:"건식+물걸레"};
const intensityLabels={fast:"빠른",standard:"표준",careful:"꼼꼼"};
const todayStateLabels={normal:"평소와 같음",dust:"먼지 많음",pet:"반려동물 털 많음",obstacle:"바닥 물건 많음"};
const cleanModeMultipliers={dry:1.00,mop:1.08,both:1.15};
const intensityMultipliers={fast:0.90,standard:1.00,careful:1.12};
const todayStateMultipliers={normal:1.00,dust:1.05,pet:1.08,obstacle:1.06};

function pickRandomRun(candidates){
  if(!candidates || candidates.length===0)return null;

  // 현재 화면에 떠 있는 global_run_id와 같은 시나리오는 가능하면 제외
  // 같은 조건으로 1회차 학습 청소를 다시 실행할 때 매번 다른 집 프로필이 나오게 하기 위함
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

  // 1순위: 사용자가 선택한 평수 + 청소방식이 모두 같은 CSV 시나리오 중 랜덤 선택
  let candidates = predictionData.runs.filter(r=>Number(r.areaPyung)===area && Boolean(r.mopEnabled)===mop);
  let run = pickRandomRun(candidates);

  // 2순위: 청소방식까지 완전히 맞는 데이터가 없으면, 같은 평수 안에서 랜덤 선택
  if(!run){
    candidates = predictionData.runs.filter(r=>Number(r.areaPyung)===area);
    run = pickRandomRun(candidates);
  }

  // 3순위: 같은 평수도 없으면 전체 CSV 중 랜덤 선택
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
  adjustmentMultiplier:1,
  pendingCleanAfterCharge:false,
  chargeComplete:false,
  predicting:false,
  predicted:false,
  profileReady:false,
  mapping:false,
  mappingProgress:0,
  mappingStepIndex:-1,
  firstRunSocUsed:0,
  temperature:29,health:100,heart:100,
  level:13,exp:55,coins:50,food:1,cleaning:false,charging:false,
  celebrating:false,progress:0,missionDone:false,cleanCount:0,
  acceptCount:4,area:activeRun.home.cleaningAreaM2||72,average:38
};

function populateConditionSelectors(){
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

  renderPlan();renderHome();renderBattery();renderRecord();renderReward();
}

function getScenario(scope,zoneNumber=null){
  if(scope==="home")return activeRun.home;
  return activeRun.zones.find(z=>Number(z.zone)===Number(zoneNumber)) || activeRun.zones[zoneNumber-1] || activeRun.home;
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

function makeAdjustedScenario(baseScenario,choices){
  const mClean=cleanModeMultipliers[choices.cleanMode]||1;
  const mIntensity=intensityMultipliers[choices.intensity]||1;
  const mToday=todayStateMultipliers[choices.todayState]||1;
  const multiplier=mClean*mIntensity*mToday;
  const required=Math.max(1,Number(baseScenario.requiredSoc||0)*multiplier);
  const scenario=Object.assign({},baseScenario);
  scenario.requiredSoc=Math.round(required*10)/10;
  scenario.targetSoc=targetFromRequired(scenario.requiredSoc);
  scenario.cleaningType=cleanModeLabels[choices.cleanMode]||baseScenario.cleaningType;
  scenario.mopEnabled=choices.cleanMode!=="dry";
  scenario.cleanModeChoice=choices.cleanMode;
  scenario.cleanModeLabel=cleanModeLabels[choices.cleanMode]||baseScenario.cleaningType;
  scenario.intensityChoice=choices.intensity;
  scenario.intensityLabel=intensityLabels[choices.intensity]||"표준";
  scenario.todayStateChoice=choices.todayState;
  scenario.todayStateLabel=todayStateLabels[choices.todayState]||"평소와 같음";
  scenario.adjustmentMultiplier=Math.round(multiplier*100)/100;
  if(choices.todayState==="dust")scenario.dirtLevel=(baseScenario.dirtLevel||"보통")+" + 먼지 보정";
  if(choices.todayState==="pet")scenario.dirtLevel=(baseScenario.dirtLevel||"보통")+" + 털 보정";
  if(choices.todayState==="obstacle")scenario.obstacleLevel="높음 보정";
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
  state.adjustmentMultiplier=scenario.adjustmentMultiplier||1;
  state.area=scenario.cleaningAreaM2||state.area;
}

function predictSocFromConditions(){
  if(state.cleaning||state.charging||state.mapping){showToast("학습/청소/충전이 끝난 뒤 다시 예측할 수 있어요.");return}
  if(!state.profileReady){
    openModal("1회차 학습이 먼저예요","아직 로보킹이 우리 집 구조를 배우지 못했어요.<br><br>먼저 <b>1회차 학습 청소</b>를 실행하면 집 구조, 구역별 면적, 바닥 타입, 오염도, 장애물 수준, 실제 SOC 소모 기록을 저장합니다.<br><br>그 다음부터 AI가 다음 청소에 필요한 SOC를 예측할 수 있어요.");
    return;
  }
  const choices=getPredictionChoices();
  const baseScenario=getBaseScenarioFromChoices(choices);
  const adjustedScenario=makeAdjustedScenario(baseScenario,choices);
  const loading=$('predictLoading');
  state.predicting=true;
  if(loading){loading.textContent="저장된 우리 집 프로필에 오늘 청소 조건을 반영해 SOC를 계산 중이에요...";loading.classList.add('active');}
  $("speech").innerHTML="<strong style='color:#2f8b3a'>잠깐만요!</strong><br>오늘 조건을 반영해 SOC를 계산하고 있어요.";
  $("modeChip").textContent="🤖 우리 집 기록 기반 AI 예측 중";
  showToast("우리 집 프로필에 오늘 청소 조건을 반영합니다.");

  setTimeout(()=>{
    syncScenarioToState(adjustedScenario);
    state.predicted=true;
    state.predicting=false;
    if(loading){
      loading.textContent=state.selectedLabel+" · "+state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel+" 조건 예측 완료";
      loading.classList.remove('active');
    }
    render();
    const scopeText=state.selectedScope==="home"?"집 전체":state.selectedLabel;
    const body="1회차 학습 청소로 저장한 우리 집 프로필을 기준으로 예측했어요.<br><br>"
      +"선택 범위: <b>"+scopeText+"</b><br>"
      +"청소 방식: <b>"+state.cleanModeLabel+"</b><br>"
      +"청소 강도: <b>"+state.intensityLabel+"</b><br>"
      +"오늘 상태: <b>"+state.todayStateLabel+"</b><br><br>"
      +"기준 예측값에 오늘 조건 보정값을 반영한 예상 SOC 소모량은 <b>"+fmtSoc(state.requiredSoc)+"%</b>예요.<br>"
      +"안전 마진 15%를 더해서 목표 SOC는 <b>"+state.targetSoc+"%</b>입니다.";
    openModal("AI 예측 완료!",body);
  },900);
}

function floorSummary(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const counts={};
  activeRun.zones.forEach(z=>{const k=z.floorType||"정보 없음";counts[k]=(counts[k]||0)+1;});
  return Object.keys(counts).map(k=>k+" "+counts[k]+"구역").join(", ");
}
function dirtSummary(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const counts={};
  activeRun.zones.forEach(z=>{const k=z.dirtLevel||"정보 없음";counts[k]=(counts[k]||0)+1;});
  return Object.keys(counts).map(k=>k+" "+counts[k]+"구역").join(", ");
}
function obstacleSummary(){return activeRun && activeRun.home ? (activeRun.home.obstacleLevel||"중간") : "중간";}
function profileResultBody(){
  return "1회차 청소를 통해 우리 집 프로필을 만들었어요.<br><br>"
    +"✅ 집 구조 매핑: <b>"+activeRun.areaPyung+"평, 5개 구역</b><br>"
    +"✅ 구역별 면적 저장: <b>총 "+activeRun.home.cleaningAreaM2+"㎡</b><br>"
    +"✅ 바닥 타입 인식: <b>"+floorSummary()+"</b><br>"
    +"✅ 오염도 기록: <b>"+dirtSummary()+"</b><br>"
    +"✅ 장애물 수준 기록: <b>"+obstacleSummary()+"</b><br>"
    +"✅ 실제 SOC 소모 기록: <b>"+fmtSoc(state.firstRunSocUsed)+"%</b><br><br>"
    +"이제부터는 이 기록을 기준으로 다음 청소에 필요한 SOC만 예측할 수 있어요.";
}
function startFirstMapping(){
  if(state.cleaning||state.charging||state.mapping){showToast("진행 중인 작업이 끝난 뒤 다시 시도해 주세요.");return}
  activeRun=pickRandomRun(predictionData.runs) || predictionData.runs[0];
  syncScenarioToState(activeRun.home);
  state.profileReady=false;
  state.predicted=false;
  state.mapping=true;
  state.mappingProgress=0;
  state.mappingStepIndex=0;
  state.firstRunSocUsed=Number(activeRun.home.requiredSoc||0);
  switchPage("homePage");
  showToast("1회차 학습 청소를 시작합니다.");
  render();
  let tick=0;
  const total=mappingSteps.length*4;
  const timer=setInterval(()=>{
    tick+=1;
    state.mappingProgress=Math.min(100,Math.round(tick/total*100));
    state.mappingStepIndex=Math.min(mappingSteps.length-1,Math.floor((tick-1)/4));
    state.progress=state.mappingProgress;
    state.temperature=Math.min(33,state.temperature+0.08);
    render();
    if(tick>=total){
      clearInterval(timer);
      state.mapping=false;
      state.profileReady=true;
      state.predicted=false;
      state.progress=100;
      const scopeSelect=$('scopeSelect'); if(scopeSelect)scopeSelect.value='home';
      const cleanModeSelect=$('cleanModeSelect'); if(cleanModeSelect)cleanModeSelect.value=activeRun.home.mopEnabled?'mop':'dry';
      const intensitySelect=$('intensitySelect'); if(intensitySelect)intensitySelect.value='standard';
      const todayStateSelect=$('todayStateSelect'); if(todayStateSelect)todayStateSelect.value='normal';
      state.temperature=29;
      addEvent("1회차 학습 청소 완료","집 구조, 바닥 타입, 오염도, 장애물 수준, SOC 소모 기록을 저장했습니다.");
      spawnEffect("🏠",8);spawnEffect("✨",9);
      render();
      setTimeout(()=>openModal("우리 집 프로필 저장 완료!",profileResultBody()),350);
    }
  },260);
}

function selectScenario(scope,zoneNumber=null){
  if(state.cleaning||state.charging||state.mapping){showToast("학습/청소/충전이 끝난 뒤 변경할 수 있어요.");return}
  if(!state.profileReady){openModal("우리 집 학습이 먼저예요","구역별 바닥 타입과 오염도는 1회차 학습 청소 후 확인할 수 있어요.<br><br>먼저 <b>1회차 학습 청소 시작</b>을 눌러 로보킹에게 우리 집을 알려주세요.");return}
  if(!state.predicted){showToast("AI 예측하기를 먼저 눌러주세요.");return}
  const scopeSelect=$('scopeSelect');
  if(scopeSelect)scopeSelect.value=scope==="home"?"home":String(zoneNumber||1);
  const choices=getPredictionChoices(scope,zoneNumber);
  const baseScenario=getBaseScenarioFromChoices(choices);
  const adjustedScenario=makeAdjustedScenario(baseScenario,choices);
  syncScenarioToState(adjustedScenario);
  render();
  openScenarioModal();
}

function openScenarioModal(){
  const enough=state.soc>=state.targetSoc;
  const title=enough?"배가 든든해요!":"아직 배고파요!";
  const scopeText=state.selectedScope==="home"?"집 전체 청소":state.selectedLabel+" 청소";
  const conditionLine="청소 방식 <b>"+state.cleanModeLabel+"</b> · 청소 강도 <b>"+state.intensityLabel+"</b> · 오늘 상태 <b>"+state.todayStateLabel+"</b><br><br>";
  const zoneLine=state.selectedScope==="zone"
    ? "1회차 학습 결과, "+state.selectedLabel+"의 바닥 타입은 <b>"+(state.floorType||"정보 없음")+"</b>입니다.<br>오염도는 <b>"+(state.dirtLevel||"정보 없음")+"</b>, 흡입 모드는 <b>"+(state.suctionMode||"AI 자동")+"</b>로 기록됐어요.<br><br>"
    : "1회차 학습으로 저장한 5개 구역 기록을 모두 합산해서 예측했어요.<br><br>";
  const body=enough
    ? scopeText+"를 선택했어요.<br><br>"+conditionLine+zoneLine+"예상 SOC 소모량은 <b>"+fmtSoc(state.requiredSoc)+"%</b>이고, 목표 SOC는 <b>"+state.targetSoc+"%</b>예요.<br>지금 SOC가 <b>"+state.soc+"%</b>라서 바로 청소를 시작할 수 있어요!"
    : scopeText+"를 선택했어요.<br><br>"+conditionLine+zoneLine+"예상 SOC 소모량은 <b>"+fmtSoc(state.requiredSoc)+"%</b>예요.<br>안전 마진 15%를 더해서 목표 SOC는 <b>"+state.targetSoc+"%</b>입니다.<br><br><b>목표 SOC까지만 충전하고 청소를 시작할게요.</b> 과충전은 줄이고 배터리는 오래 지켜볼게요!";
  if(enough){
    openModal(title,body);
  }else{
    openModal(title,body,{showCancel:true,cancelText:"취소",confirmText:"충전하기",onConfirm:()=>chargeRobot(false)});
  }
}

function renderPlan(){
  if(!$('planSummary'))return;
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

  if(learnSteps){
    learnSteps.innerHTML=mappingSteps.map((s,i)=>{
      let cls='learn-step';
      if(state.profileReady || i<state.mappingStepIndex)cls+=' done';
      else if(state.mapping && i===state.mappingStepIndex)cls+=' active';
      return '<div class="'+cls+'">'+s.label+'</div>';
    }).join('');
  }
  if(learnFill)learnFill.style.width=(state.profileReady?100:state.mappingProgress)+'%';

  if(state.mapping){
    if(learnPill)learnPill.textContent="학습 중";
    if(learnStatus)learnStatus.textContent=mappingSteps[state.mappingStepIndex].label+" 중... "+state.mappingProgress+"%";
    if(learnBtn){learnBtn.textContent="로보킹이 집을 배우는 중...";learnBtn.disabled=true;}
    if(conditionPanel)conditionPanel.classList.add('locked-area');
  }else if(state.profileReady){
    if(learnPill)learnPill.textContent="프로필 저장됨";
    if(learnStatus)learnStatus.innerHTML="우리 집 프로필 저장 완료 · 총 "+activeRun.home.cleaningAreaM2+"㎡ · 바닥 타입 "+floorSummary();
    if(learnBtn){learnBtn.textContent="🔄 1회차 학습 다시 실행";learnBtn.disabled=false;learnBtn.classList.add('ready');}
    if(conditionPanel)conditionPanel.classList.remove('locked-area');
  }else{
    if(learnPill)learnPill.textContent="초기 학습";
    if(learnStatus)learnStatus.textContent="평수와 학습 청소 방식을 선택한 뒤 1회차 학습 청소를 시작해 주세요.";
    if(learnBtn){learnBtn.textContent="🏠 1회차 학습 청소 시작";learnBtn.disabled=false;learnBtn.classList.remove('ready');}
    if(conditionPanel)conditionPanel.classList.remove('locked-area');
  }

  if(firstLearnInputs)firstLearnInputs.style.display=state.profileReady?'none':'block';
  if(predictionInputs)predictionInputs.style.display=state.profileReady?'block':'none';

  if(predictBtn){
    predictBtn.disabled=!state.profileReady || state.mapping;
    predictBtn.style.opacity=(!state.profileReady || state.mapping)?'.55':'1';
    predictBtn.textContent=state.profileReady?'🤖 AI 예측하기':'🤖 학습 후 AI 예측 가능';
  }
  if(conditionTitle){
    conditionTitle.textContent=state.profileReady?'저장된 우리 집 프로필 기준으로 오늘 청소 조건을 선택하세요':'평수와 학습 청소 방식을 선택해 1회차 학습 청소를 시작하세요';
  }

  document.querySelectorAll('.scope-btn').forEach(btn=>{
    btn.classList.remove('active');
    btn.disabled=!state.profileReady || !state.predicted || state.mapping;
    btn.style.opacity=(!state.profileReady || !state.predicted || state.mapping)?'.55':'1';
  });
  if(state.selectedScope==="home")$('scopeHome').classList.add('active');
  else if($('scopeZone'+state.selectedZone))$('scopeZone'+state.selectedZone).classList.add('active');

  $('planModel').textContent=state.mapping?'1회차 학습 중':(!state.profileReady?'1회차 학습 전':(state.predicted?(predictionData.dataStatus==="csv"?state.modelName:"DEMO")+" 기반":"프로필 저장 완료"));

  if(!state.profileReady){
    $('planTargetSoc').textContent='--';
    $('planSummary').innerHTML="<strong>1회차 학습 전</strong><br>아직 우리 집의 구역 면적, 바닥 타입, 오염도, 장애물 수준을 모릅니다.<br>먼저 로보킹에게 집 구조를 알려주세요.";
    $('planSocSub').textContent="학습 완료 후 AI 목표 SOC 표시";
    return;
  }
  if(!state.predicted){
    $('planTargetSoc').textContent='--';
    $('planSummary').innerHTML="<strong>우리 집 프로필 저장됨</strong><br>구역 면적, 바닥 타입, 오염도, 장애물 수준, SOC 소모 기록을 저장했어요.<br>이제 AI 예측하기를 눌러주세요.";
    $('planSocSub').textContent="1회차 기록 기반 예측 대기";
    return;
  }

  $('planTargetSoc').textContent=state.targetSoc;
  const scopeText=state.selectedScope==="home"?"집 전체":state.selectedLabel;
  const detail=state.selectedScope==="home"
    ? state.areaPyung+"평 프로필 · "+state.cleaningAreaM2+"㎡"
    : (state.floorType||"바닥재질")+" · 오염도 "+(state.dirtLevel||"-")+" · "+state.cleaningAreaM2+"㎡";
  const conditionDetail="청소 방식 "+state.cleanModeLabel+" · 강도 "+state.intensityLabel+" · 오늘 상태 "+state.todayStateLabel;
  $('planSummary').innerHTML="<strong>"+scopeText+"</strong> 선택됨<br>"+detail+"<br>"+conditionDetail+"<br>예상 SOC 소모량 <strong>"+fmtSoc(state.requiredSoc)+"%</strong> → 목표 SOC <strong>"+state.targetSoc+"%</strong>";
  $('planSocSub').textContent="예상 "+fmtSoc(state.requiredSoc)+"% + 안전마진 15%";
}

function renderHome(){
  const room=$("room");room.className="room";

  if(state.chargeComplete){
    room.classList.add("celebrate");
    $("speech").innerHTML="<strong>배불러요!</strong><br>이제 청소 가능해요!";
    $("modeChip").textContent="💖 맞춤 충전 완료 · SOC "+state.soc+"%";
    $("batteryFace").textContent="😍";$("spark").textContent="💖";
    $("batteryMessage").innerHTML="목표 SOC까지 채웠어요.<br>과충전 없이 준비 완료!";
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
    $("modeChip").textContent="🏠 1회차 학습 청소 · "+state.mappingProgress+"%";
    $("batteryFace").textContent="🧭";$("spark").textContent="📡";
    $("batteryMessage").innerHTML="집 구조와 청소 조건을<br>처음으로 저장하고 있어요.";
    $("timeTip").textContent="학습 진행률 "+state.mappingProgress+"%";
  }else if(state.predicting){
    $("speech").innerHTML="<strong style='color:#2f8b3a'>분석 중이에요!</strong><br>저장된 기록으로 SOC를 계산하고 있어요.";
    $("modeChip").textContent="🤖 우리 집 기록 기반 AI 예측 중";
    $("batteryFace").textContent="🤔";$("spark").textContent="✨";
  }else if(!state.profileReady){
    $("speech").innerHTML="<strong style='color:#ef8c32'>처음 만났어요!</strong><br>1회차 청소로 우리 집을 알려주세요.";
    $("modeChip").textContent="🏠 집 구조 학습 필요";
    $("batteryFace").textContent="🙂";$("spark").textContent="✨";
    $("batteryMessage").innerHTML="아직 우리 집 정보를 몰라요.<br>학습 청소가 필요합니다.";
    $("timeTip").textContent="1회차 학습 후 AI 예측 가능";
  }else if(!state.predicted){
    $("speech").innerHTML="<strong>집을 배웠어요!</strong><br>이제 필요한 SOC를 예측할게요.";
    $("modeChip").textContent="✅ 우리 집 프로필 저장 완료";
    $("batteryFace").textContent="😊";$("spark").textContent="✨";
    $("batteryMessage").innerHTML="집 구조 학습 완료!<br>AI 예측하기를 눌러주세요.";
    $("timeTip").textContent="AI 예측 대기 중";
  }else if(state.cleaning){
    room.classList.add("cleaning");
    $("speech").innerHTML="<strong>열심히 청소 중이에요!</strong><br>진행률 "+state.progress+"%";
    $("modeChip").textContent="🧹 "+state.selectedLabel+" 청소 중 · "+state.progress+"%";
    $("batteryFace").textContent="🧹";
    $("batteryMessage").innerHTML="청소 중입니다.<br>SOC와 시간이 변하고 있어요.";
    $("timeTip").textContent="청소 진행률 "+state.progress+"%";
    $("spark").textContent="💨";
  }else if(state.charging){
    room.classList.add("charging");
    $("speech").innerHTML="<strong style='color:#e48627'>잠깐 쉬는 중이에요</strong><br>목표 SOC까지만 충전할게요.";
    $("modeChip").textContent="⚡ "+state.selectedLabel+" 맞춤 충전 · "+state.soc+" → "+state.targetSoc+"%";
    $("batteryFace").textContent="😌";
    $("batteryMessage").innerHTML="충전 스테이션에서 쉬면서<br>필요한 만큼만 채우고 있어요.";
    $("timeTip").textContent="현재 SOC "+state.soc+"% · 목표 "+state.targetSoc+"%";
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
    $("modeChip").textContent="✨ "+state.selectedLabel+" AI 권장 SOC "+state.targetSoc+"%";
    $("batteryFace").textContent=state.soc>90?"😮":"😊";
    $("spark").textContent="✨";

    if(state.soc < state.targetSoc){
      $("speech").innerHTML=
        "<strong style='color:#ef8c32'>아직 배고파요!</strong><br>"
        + "목표 SOC "+state.targetSoc+"%까지만<br>충전하고 청소할게요.";
      $("batteryMessage").innerHTML=state.selectedLabel+" 청소에는<br>약 "+fmtSoc(state.requiredSoc)+"% SOC가 필요해요.";
      $("timeTip").textContent="현재 SOC "+state.soc+"% → 목표 SOC "+state.targetSoc+"%까지 충전 필요";
    }else{
      $("speech").innerHTML="<strong>배가 든든해요!</strong><br>"+state.selectedLabel+" 청소를 준비할게요!";
      $("batteryMessage").innerHTML="현재 SOC로 충분해요.<br>목표 SOC "+state.targetSoc+"% 이상입니다.";
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
    $("insightText").innerHTML="아직 1회차 학습 청소 전입니다. 집 구조와 구역 정보를 먼저 저장하면 AI SOC 예측을 시작할 수 있습니다.";
  }else if(!state.predicted){
    $("insightText").innerHTML="우리 집 프로필이 저장되었습니다. AI 예측하기를 누르면 1회차 청소 기록을 기준으로 다음 청소 목표 SOC를 계산합니다.";
  }else{
    $("insightText").innerHTML="우리 집 "+state.areaPyung+"평 프로필에서 <b>"+state.selectedLabel+"</b> 범위를 선택했어요. "+state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel+" 조건을 반영한 예상 SOC 소모량은 <b>"+fmtSoc(state.requiredSoc)+"%</b>입니다. 안전 마진 15%를 반영하여 SOC <b>"+state.targetSoc+"%</b>까지만 충전하면 청소를 완료할 수 있습니다.";
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

function renderReward(){
  $("levelText").textContent=state.level;
  $("expText").textContent=state.exp;
  $("expFill").style.width=state.exp+"%";
}

function showToast(message){
  const toast=$("toast");toast.textContent=message;toast.classList.add("show");
  clearTimeout(window.toastTimer);
  window.toastTimer=setTimeout(()=>toast.classList.remove("show"),1800);
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
function feedRobot(){if(state.food<=0){showToast("음식이 부족해요. 리워드에서 구매해 주세요.");return}state.food-=1;state.soc+=12;state.exp+=8;pulseRobot();spawnEffect("⚡",8);levelCheck();render();showToast("SOC가 12% 회복되었습니다.")}
function playRobot(){if(state.soc<5){showToast("배터리가 부족해서 놀 수 없어요.");return}state.soc-=3;state.exp+=5;pulseRobot();spawnEffect("💖",8);levelCheck();render();showToast("로보킹의 친밀도와 경험치가 올랐어요.")}
function trainRobot(){if(state.soc<8){showToast("훈련 전에 충전이 필요해요.");return}state.soc-=6;state.health=Math.min(100,state.health+3);state.exp+=12;pulseRobot();spawnEffect("✨",8);levelCheck();render();showToast("로보킹이 훈련을 완료했습니다.")}
function takePhoto(){pulseRobot();spawnEffect("📸",5);openModal("오늘의 사진","왕관을 쓴 로보킹의 사진을 촬영했습니다.<br><br>향후 장식 아이템과 청소 완료 장면을 사진첩에 저장할 수 있습니다.")}
function decorateRobot(){spawnEffect("🎀",9);openModal("로보킹 꾸미기","현재 장착 아이템은 <b>황금 왕관</b>입니다.<br><br>리본, 탐험가 모자, 표정 스킨 등을 리워드 화면에서 확인할 수 있습니다.")}

function showStatus(){
  if(!state.profileReady){openModal("우리 집 학습 전","아직 1회차 학습 청소가 실행되지 않았어요.<br><br>로보킹이 집 구조, 구역별 면적, 바닥 타입, 오염도, 장애물 수준, SOC 소모 기록을 저장하면 AI 예측을 시작할 수 있습니다.");return}
  if(!state.predicted){openModal("우리 집 프로필","1회차 학습 청소 기록이 저장됐어요.<br><br>"+profileResultBody()+"<br><br>다음 단계로 AI 예측하기를 눌러주세요.");return}
  const scopeText=state.selectedScope==="home"?"집 전체 청소":state.selectedLabel+" 청소";
  const zoneInfo=state.selectedScope==="zone"?"<br>바닥 타입 <b>"+(state.floorType||"정보 없음")+"</b><br>오염도 <b>"+(state.dirtLevel||"정보 없음")+"</b>":"";
  openModal("AI SOC 예측 결과","저장된 프로필 <b>"+state.areaPyung+"평</b><br>선택 범위 <b>"+scopeText+"</b>"+zoneInfo+"<br>청소 방식 <b>"+state.cleanModeLabel+"</b><br>청소 강도 <b>"+state.intensityLabel+"</b><br>오늘 상태 <b>"+state.todayStateLabel+"</b><br>현재 SOC <b>"+state.soc+"%</b><br>예상 SOC 소모량 <b>"+fmtSoc(state.requiredSoc)+"%</b><br>AI 목표 SOC <b>"+state.targetSoc+"%</b><br><br>사용 모델: <b>"+state.modelName+"</b>");
}

function showChargeChoiceModal(autoStartAfterCharge=false){
  const body=state.selectedLabel+" 청소를 선택했어요.<br><br>"
    +(state.selectedScope==="zone"?state.selectedLabel+"의 바닥 타입은 <b>"+(state.floorType||"정보 없음")+"</b>입니다.<br>오염도는 <b>"+(state.dirtLevel||"정보 없음")+"</b>, 흡입 모드는 <b>"+(state.suctionMode||"AI 자동")+"</b>예요.<br><br>":"")
    +"예상 SOC 소모량은 <b>"+fmtSoc(state.requiredSoc)+"%</b>예요.<br>안전 마진 15%를 더해 목표 SOC는 <b>"+state.targetSoc+"%</b>입니다.<br><br>"
    +"아직 배고파요. 목표 SOC까지만 충전할까요?";
  openModal("아직 배고파요!",body,{
    showCancel:true,
    cancelText:"취소",
    confirmText:"충전하기",
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
  if(!state.profileReady){openModal("1회차 학습이 먼저예요","아직 우리 집 구조와 구역 정보가 저장되지 않았어요.<br><br>먼저 <b>1회차 학습 청소</b>를 실행해 주세요.");return}
  if(!state.predicted){openModal("AI 예측이 필요해요","우리 집 프로필은 저장됐어요.<br><br>청소를 시작하기 전에 <b>AI 예측하기</b>로 필요한 목표 SOC를 계산해 주세요.");return}
  if(state.soc<state.targetSoc){
    showChargeChoiceModal(false);
    return;
  }
  if(state.soc<15){showToast("SOC가 부족합니다. 먼저 충전해 주세요.");return}
  state.cleaning=true;state.progress=0;
  const startSoc=state.soc;const plannedUse=Math.min(state.requiredSoc,state.soc);render();showToast(state.selectedLabel+" 청소를 시작합니다!");
  let step=0;const totalSteps=20;
  const timer=setInterval(()=>{
    step+=1;state.progress=Math.round(step/totalSteps*100);state.soc=Math.max(0,startSoc-plannedUse*(step/totalSteps));state.temperature=Math.min(36,state.temperature+.25);render();
    if(step>=totalSteps||state.soc<=10){
      clearInterval(timer);state.cleaning=false;state.progress=100;state.temperature=29;state.missionDone=true;state.celebrating=true;state.cleanCount+=1;state.coins+=50;state.exp+=20;state.area=Math.round((state.area||0)+(state.cleaningAreaM2||0));state.average=Math.round((state.average+Math.max(15,Math.round(state.requiredSoc*1.4)))/2);levelCheck();
      addEvent(state.selectedLabel+" 청소 완료","AI 예측 SOC "+fmtSoc(state.requiredSoc)+"%를 기준으로 청소를 완료했습니다.");spawnEffect("🎉",15);spawnEffect("⭐",9);render();
      setTimeout(()=>{state.celebrating=false;render()},2200);
      setTimeout(()=>openModal("청소 완료!",state.selectedLabel+" 청소를 완료했습니다.<br><br>예상 SOC 소모량은 <b>"+fmtSoc(state.requiredSoc)+"%</b>였고, 보상으로 <b>50코인</b>과 경험치 20을 획득했습니다."),550);
    }
  },320);
}

function chargeRobot(autoStart=false){
  if(state.cleaning){showToast("청소가 끝난 후 충전할 수 있어요.");return}
  if(state.charging){showToast("이미 충전 중이에요.");return}
  if(state.soc>=state.targetSoc){
    openModal("배불러요!","현재 SOC가 목표 SOC <b>"+state.targetSoc+"%</b>에 이미 도달했어요.<br><br>이제 "+state.selectedLabel+" 청소를 시작할 수 있어요.");
    return;
  }
  closeModal();
  switchPage("homePage");
  state.charging=true;
  state.chargeComplete=false;
  render();
  showToast("로보킹이 쉬면서 맞춤 충전을 시작합니다.");
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
      addEvent("맞춤 충전 완료",state.selectedLabel+" 목표 SOC "+state.targetSoc+"%에서 자동 충전을 종료했습니다.");
      spawnEffect("💖",12);
      spawnEffect("✨",8);
      render();
      setTimeout(()=>openModal("배불러요!","목표 SOC <b>"+state.targetSoc+"%</b>까지 딱 맞게 충전했어요.<br><br>과충전은 줄이고, 배터리는 아껴둘게요.<br>이제 <b>"+state.selectedLabel+" 청소가 가능해요!</b>"),450);
      setTimeout(()=>{state.chargeComplete=false;render()},3200);
      if(autoStart){setTimeout(startCleaning,1300)}
    }
  },150);
}
function buyFood(){if(state.coins<50){showToast("코인이 부족해요.");return}state.coins-=50;state.food+=1;render();showToast("배터리 음식 1개를 구매했습니다.")}

const actions={
  startFirstMapping:startFirstMapping,
  predictSoc:predictSocFromConditions,
  selectHome:()=>selectScenario("home"),selectZone1:()=>selectScenario("zone",1),selectZone2:()=>selectScenario("zone",2),selectZone3:()=>selectScenario("zone",3),selectZone4:()=>selectScenario("zone",4),selectZone5:()=>selectScenario("zone",5),
  pet:petRobot,feed:feedRobot,play:playRobot,train:trainRobot,photo:takePhoto,clean:startCleaning,charge:chargeRobot,status:showStatus,
  record:()=>switchPage("recordPage"),decorate:decorateRobot,shop:()=>switchPage("rewardPage"),chargeFromBattery:()=>{switchPage("homePage");setTimeout(chargeRobot,220)},buyFood:buyFood,
  ribbon:()=>{switchPage("homePage");setTimeout(()=>spawnEffect("🎀",10),220)},sparkle:()=>{switchPage("homePage");setTimeout(()=>spawnEffect("✨",10),220)},hat:()=>showToast("탐험가 모자는 120코인이 필요해요.")
};

document.addEventListener("click",(event)=>{const nav=event.target.closest("[data-page]");if(nav){switchPage(nav.dataset.page);return}const action=event.target.closest("[data-action]");if(action&&typeof actions[action.dataset.action]==="function"){actions[action.dataset.action]()}});
$("modalCancel").addEventListener("click",closeModal);$("modalConfirm").addEventListener("click",()=>modalConfirmHandler());$("modal").addEventListener("click",(event)=>{if(event.target===$("modal"))closeModal()});
$("targetSlider").addEventListener("input",(event)=>{state.targetSoc=Number(event.target.value);render()});
$("tempSlider").addEventListener("input",(event)=>{state.temperature=Number(event.target.value);render()});
["scopeSelect","cleanModeSelect","intensitySelect","todayStateSelect"].forEach(id=>{
  const el=$(id);
  if(el)el.addEventListener("change",()=>{
    if(state.profileReady && state.predicted){
      state.predicted=false;
      const loading=$('predictLoading');
      if(loading)loading.textContent="조건이 바뀌었어요. AI 예측하기를 다시 눌러주세요.";
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

components.html(APP_HTML, height=1060, scrolling=False)
