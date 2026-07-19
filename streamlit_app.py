import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="로봇청소기 키우기",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit 기본 UI 숨기기
st.markdown(
    """
    <style>
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stSidebar"] {
            display: none !important;
        }

        #MainMenu,
        footer {
            visibility: hidden !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 12%, #fff9ec 0, transparent 31%),
                radial-gradient(circle at 88% 86%, #edd6ad 0, transparent 27%),
                #eee5d8;
        }

        .block-container {
            max-width: 100%;
            padding: 8px 4px 16px;
        }

        iframe {
            border: none !important;
            border-radius: 28px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


APP_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
    * {
        box-sizing: border-box;
        -webkit-tap-highlight-color: transparent;
    }

    :root {
        --cream: #fff6df;
        --cream-2: #f8e5b9;
        --brown: #4b3324;
        --brown-soft: #76543d;
        --orange: #ff9533;
        --orange-deep: #f66a3d;
        --green: #6aad4c;
        --red: #ef4d44;
        --yellow: #ffd452;
        --shadow: 0 8px 18px rgba(74, 46, 22, 0.16);
    }

    html,
    body {
        margin: 0;
        padding: 0;
        min-height: 100%;
        font-family:
            "Apple SD Gothic Neo",
            "Malgun Gothic",
            "Noto Sans KR",
            sans-serif;
        color: var(--brown);
        background: transparent;
    }

    body {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        padding: 8px;
    }

    button {
        font-family: inherit;
    }

    .phone {
        position: relative;
        width: min(100%, 420px);
        min-height: 900px;
        overflow: hidden;
        border: 8px solid #242321;
        border-radius: 40px;
        background: #dfb66f;
        box-shadow:
            0 30px 80px rgba(51, 34, 19, 0.28),
            0 8px 20px rgba(51, 34, 19, 0.16);
    }

    .notch {
        position: absolute;
        z-index: 50;
        top: 0;
        left: 50%;
        width: 125px;
        height: 25px;
        transform: translateX(-50%);
        border-radius: 0 0 17px 17px;
        background: #242321;
    }

    .screen {
        position: relative;
        min-height: 884px;
        overflow: hidden;
        background:
            linear-gradient(
                180deg,
                #d1aa7a 0%,
                #e7c690 43%,
                #e0b168 68%,
                #e4b56d 100%
            );
    }

    /* ---------- 상단 상태바 ---------- */
    .top-bar {
        position: relative;
        z-index: 30;
        height: 66px;
        display: grid;
        grid-template-columns: 49px 88px 1fr 38px;
        align-items: center;
        gap: 5px;
        padding: 13px 8px 7px;
        color: #fff;
        background:
            linear-gradient(
                90deg,
                rgba(43, 35, 29, 0.96),
                rgba(76, 53, 37, 0.89)
            );
        box-shadow: 0 6px 15px rgba(44, 29, 18, 0.2);
    }

    .profile {
        position: relative;
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border: 3px solid #fff0b9;
        border-radius: 50%;
        background: #ffe0a4;
        box-shadow: 0 3px 8px rgba(0,0,0,0.24);
        font-size: 25px;
    }

    .profile-crown {
        position: absolute;
        top: -12px;
        font-size: 15px;
        transform: rotate(-8deg);
    }

    .profile-info {
        min-width: 0;
    }

    .coin-line {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 15px;
        font-weight: 900;
    }

    .level-line {
        margin-top: 1px;
        font-size: 10px;
        color: #f6e9d7;
        font-weight: 800;
    }

    .exp-track {
        height: 6px;
        margin-top: 3px;
        overflow: hidden;
        border-radius: 10px;
        background: rgba(255,255,255,0.23);
    }

    .exp-fill {
        width: 55%;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #ff5944, #ffb23e);
        transition: width 0.3s ease;
    }

    .top-status {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 7px;
        white-space: nowrap;
        font-size: 10px;
        font-weight: 900;
    }

    .top-status span {
        display: flex;
        align-items: center;
        gap: 1px;
    }

    .setting-button {
        width: 34px;
        height: 34px;
        border: 0;
        border-radius: 50%;
        background: rgba(0,0,0,0.28);
        color: #fff;
        font-size: 19px;
        cursor: pointer;
    }

    /* ---------- 방 ---------- */
    .room {
        position: relative;
        height: 350px;
        overflow: hidden;
        background:
            linear-gradient(
                180deg,
                #c8a476 0%,
                #dfc296 47%,
                #d3a264 48%,
                #c9914d 100%
            );
    }

    .wall-light {
        position: absolute;
        top: -67px;
        left: 50%;
        width: 400px;
        height: 260px;
        transform: translateX(-50%);
        border-radius: 50%;
        background:
            radial-gradient(
                circle,
                rgba(255,246,222,0.88),
                rgba(255,239,204,0.20) 57%,
                transparent 73%
            );
    }

    .floor-line {
        position: absolute;
        top: 185px;
        width: 100%;
        height: 3px;
        background: rgba(103,66,34,0.14);
    }

    .floor {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 165px;
        background:
            repeating-linear-gradient(
                90deg,
                rgba(102,61,25,0.10) 0,
                rgba(102,61,25,0.10) 2px,
                transparent 2px,
                transparent 66px
            ),
            linear-gradient(180deg, #d8b173, #c88e48);
    }

    .floor::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            repeating-linear-gradient(
                0deg,
                transparent 0,
                transparent 38px,
                rgba(102,61,25,0.09) 39px,
                rgba(102,61,25,0.09) 41px
            );
    }

    .sofa {
        position: absolute;
        right: -7px;
        top: 70px;
        width: 136px;
        height: 100px;
        border-radius: 26px 0 7px 7px;
        background: linear-gradient(145deg, #6b7d78, #354e4a);
        box-shadow: 0 10px 14px rgba(54,37,23,0.27);
    }

    .sofa::before {
        content: "";
        position: absolute;
        top: -18px;
        left: 10px;
        width: 78px;
        height: 47px;
        border-radius: 17px 17px 7px 7px;
        background: #71847e;
    }

    .sofa::after {
        content: "";
        position: absolute;
        top: 20px;
        left: 6px;
        width: 120px;
        height: 5px;
        border-radius: 10px;
        background: rgba(255,255,255,0.10);
    }

    .plant {
        position: absolute;
        left: 15px;
        top: 66px;
        width: 70px;
        height: 122px;
    }

    .pot {
        position: absolute;
        left: 17px;
        bottom: 0;
        width: 42px;
        height: 40px;
        border-radius: 5px 5px 18px 18px;
        background: linear-gradient(90deg, #c98e52, #e2a96a);
        box-shadow: 0 4px 8px rgba(66,42,25,0.23);
    }

    .stem {
        position: absolute;
        left: 37px;
        top: 16px;
        width: 4px;
        height: 75px;
        background: #436b3b;
        transform: rotate(-2deg);
    }

    .leaf {
        position: absolute;
        width: 31px;
        height: 14px;
        border-radius: 90% 10% 90% 10%;
        background: linear-gradient(135deg, #6c984f, #355f36);
    }

    .leaf.one {
        left: 5px;
        top: 21px;
        transform: rotate(25deg);
    }

    .leaf.two {
        left: 35px;
        top: 35px;
        transform: scaleX(-1) rotate(24deg);
    }

    .leaf.three {
        left: 5px;
        top: 52px;
        transform: rotate(18deg);
    }

    .leaf.four {
        left: 35px;
        top: 66px;
        transform: scaleX(-1) rotate(22deg);
    }

    .robot-home {
        position: absolute;
        left: 84px;
        top: 120px;
        width: 68px;
        height: 58px;
        border-radius: 29px 29px 7px 7px;
        background: linear-gradient(145deg, #a28a70, #75614d);
        box-shadow: 0 6px 11px rgba(54,36,23,0.22);
    }

    .robot-home::before {
        content: "";
        position: absolute;
        left: 19px;
        bottom: 0;
        width: 31px;
        height: 32px;
        border-radius: 16px 16px 0 0;
        background: #3f3b35;
    }

    .robot-home::after {
        content: "HOME";
        position: absolute;
        top: 11px;
        left: 16px;
        font-size: 7px;
        color: rgba(255,255,255,0.56);
        font-weight: 900;
    }

    .speech {
        position: absolute;
        z-index: 15;
        top: 24px;
        left: 50%;
        width: 174px;
        min-height: 73px;
        padding: 14px 12px;
        transform: translateX(-50%);
        text-align: center;
        border-radius: 14px;
        background: rgba(255,255,255,0.97);
        box-shadow: 0 7px 16px rgba(58,37,21,0.18);
        color: #473127;
        font-size: 12px;
        line-height: 1.55;
        font-weight: 800;
    }

    .speech strong {
        color: var(--green);
        font-size: 14px;
    }

    .speech::after {
        content: "";
        position: absolute;
        left: 52%;
        bottom: -15px;
        border-width: 16px 10px 0 4px;
        border-style: solid;
        border-color: white transparent transparent transparent;
        transform: rotate(-7deg);
    }

    .mode-chip {
        position: absolute;
        z-index: 14;
        left: 50%;
        top: 109px;
        padding: 7px 13px;
        transform: translateX(-50%);
        border: 1px solid rgba(109,72,35,0.16);
        border-radius: 18px;
        background: rgba(255,248,229,0.95);
        box-shadow: 0 4px 10px rgba(72,46,23,0.16);
        color: #5b402b;
        font-size: 9px;
        font-weight: 900;
    }

    .rug {
        position: absolute;
        z-index: 3;
        left: 50%;
        bottom: 12px;
        width: 250px;
        height: 90px;
        transform: translateX(-50%);
        border-radius: 50%;
        background:
            radial-gradient(
                ellipse,
                rgba(240,223,196,0.90),
                rgba(191,150,102,0.78)
            );
        box-shadow: inset 0 0 18px rgba(103,70,43,0.14);
    }

    /* ---------- 로봇 ---------- */
    .robot {
        position: absolute;
        z-index: 9;
        left: 50%;
        bottom: 31px;
        width: 180px;
        height: 98px;
        transform: translateX(-50%);
        transform-origin: center bottom;
        border: 2px solid #a29b92;
        border-radius: 62% 62% 40% 40%;
        background:
            linear-gradient(
                180deg,
                #fffefb 0%,
                #e7e8e3 70%,
                #bbbdb7 100%
            );
        box-shadow:
            0 13px 19px rgba(55,37,21,0.32),
            inset 0 -8px 12px rgba(83,83,79,0.12);
        cursor: pointer;
        animation: robotIdle 2.8s ease-in-out infinite;
        will-change: transform;
    }

    .robot-top {
        position: absolute;
        left: 50%;
        top: -5px;
        width: 126px;
        height: 58px;
        transform: translateX(-50%);
        border-top: 2px solid rgba(119,119,114,0.42);
        border-radius: 50%;
        background:
            radial-gradient(
                ellipse at center,
                #fbfbf8 0%,
                #d5d6d2 74%,
                #b8b9b3 100%
            );
    }

    .robot-face {
        position: absolute;
        z-index: 3;
        left: 50%;
        bottom: 8px;
        width: 128px;
        height: 54px;
        transform: translateX(-50%);
        border-radius: 26px 26px 30px 30px;
        background: linear-gradient(180deg, #2a2c2d, #101213 76%);
        box-shadow: inset 0 4px 5px rgba(255,255,255,0.13);
    }

    .eye {
        position: absolute;
        top: 14px;
        width: 22px;
        height: 22px;
        border: 2px solid #f2f0dc;
        border-radius: 50%;
        background: #111;
        animation: eyeBlink 4.8s infinite;
        transform-origin: center;
    }

    .eye::after {
        content: "";
        position: absolute;
        top: 4px;
        left: 5px;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #fff;
        transition: transform 0.25s ease;
    }

    .eye.left {
        left: 20px;
    }

    .eye.right {
        right: 20px;
    }

    .robot.look-left .eye::after {
        transform: translateX(-4px);
    }

    .robot.look-right .eye::after {
        transform: translateX(4px);
    }

    .mouth {
        position: absolute;
        left: 50%;
        bottom: 8px;
        width: 20px;
        height: 11px;
        transform: translateX(-50%);
        border: 2px solid #f3d6c9;
        border-top: 0;
        border-radius: 0 0 12px 12px;
    }

    .cheek {
        position: absolute;
        bottom: 8px;
        width: 13px;
        height: 6px;
        border-radius: 50%;
        background: #ff8d8d;
        opacity: 0.75;
    }

    .cheek.left {
        left: 8px;
    }

    .cheek.right {
        right: 8px;
    }

    .crown {
        position: absolute;
        z-index: 11;
        left: 50%;
        top: -40px;
        transform: translateX(-50%);
        font-size: 46px;
        filter: drop-shadow(0 4px 3px rgba(81,52,17,0.25));
    }

    .robot-slot {
        position: absolute;
        left: 50%;
        bottom: -2px;
        width: 43px;
        height: 5px;
        transform: translateX(-50%);
        border-radius: 10px;
        background: #484a48;
    }

    .spark {
        position: absolute;
        z-index: 10;
        right: -16px;
        top: -9px;
        font-size: 28px;
        animation: sparkle 1.3s ease-in-out infinite;
    }

    .clean-path {
        position: absolute;
        z-index: 5;
        left: 50%;
        bottom: 40px;
        width: 290px;
        height: 76px;
        transform: translateX(-50%);
        overflow: hidden;
        border: 2px dashed rgba(255,255,255,0.36);
        border-radius: 50%;
        opacity: 0;
        transition: opacity 0.25s;
    }

    .clean-path-fill {
        width: 0%;
        height: 100%;
        border-radius: inherit;
        background:
            linear-gradient(
                90deg,
                rgba(102,182,110,0.08),
                rgba(107,202,118,0.51)
            );
        transition: width 0.32s ease;
    }

    .charge-ring {
        position: absolute;
        z-index: 7;
        left: 50%;
        bottom: 18px;
        width: 214px;
        height: 130px;
        transform: translateX(-50%);
        border: 5px solid transparent;
        border-top-color: #ffd345;
        border-right-color: #ff9931;
        border-radius: 50%;
        opacity: 0;
        pointer-events: none;
    }

    .dust-layer {
        position: absolute;
        z-index: 8;
        left: 50%;
        bottom: 54px;
        width: 265px;
        height: 75px;
        transform: translateX(-50%);
        pointer-events: none;
    }

    .dust-layer span {
        position: absolute;
        bottom: 0;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: rgba(116,78,42,0.50);
        opacity: 0;
    }

    .dust-layer span:nth-child(1) { left: 8%; animation-delay: 0s; }
    .dust-layer span:nth-child(2) { left: 21%; animation-delay: .32s; }
    .dust-layer span:nth-child(3) { left: 37%; animation-delay: .68s; }
    .dust-layer span:nth-child(4) { right: 8%; animation-delay: .18s; }
    .dust-layer span:nth-child(5) { right: 23%; animation-delay: .52s; }
    .dust-layer span:nth-child(6) { right: 39%; animation-delay: .88s; }

    .effect-layer {
        position: absolute;
        z-index: 25;
        inset: 0;
        overflow: hidden;
        pointer-events: none;
    }

    .effect {
        position: absolute;
        left: 50%;
        top: 68%;
        font-size: 20px;
        opacity: 1;
        animation: effectFly 1.2s ease-out forwards;
    }

    .room.is-cleaning .mode-chip {
        color: #fff;
        background: rgba(57,143,82,0.93);
    }

    .room.is-cleaning .clean-path {
        opacity: 1;
    }

    .room.is-cleaning .dust-layer span {
        animation: dustRise 1.35s ease-out infinite;
    }

    .room.is-cleaning .robot {
        animation: robotPatrol 2.4s ease-in-out infinite;
    }

    .room.is-charging .mode-chip {
        color: #fff;
        background: rgba(242,145,35,0.94);
    }

    .room.is-charging .charge-ring {
        opacity: 0.92;
        animation: chargeRingSpin 1.05s linear infinite;
    }

    .room.is-charging .robot {
        animation: robotCharging .85s ease-in-out infinite;
    }

    .room.is-low .robot {
        animation: robotLowPower .48s linear infinite;
    }

    .room.is-celebrating .robot {
        animation: robotCelebrate .72s ease-in-out 3;
    }

    .robot.tap-motion {
        animation: robotTap .62s ease-out !important;
    }

    /* ---------- 좌우 메뉴 ---------- */
    .mission-mini {
        position: absolute;
        z-index: 16;
        left: 8px;
        bottom: 14px;
        width: 88px;
        padding: 9px 7px;
        border-radius: 14px;
        background: rgba(255,248,230,0.97);
        box-shadow: 0 4px 10px rgba(61,39,20,0.22);
    }

    .mission-mini-title {
        font-size: 10px;
        font-weight: 900;
    }

    .mission-mini-text {
        margin-top: 5px;
        font-size: 9px;
        line-height: 1.4;
        font-weight: 800;
    }

    .mission-progress {
        display: flex;
        align-items: center;
        gap: 4px;
        margin-top: 8px;
    }

    .mission-track {
        flex: 1;
        height: 7px;
        overflow: hidden;
        border-radius: 10px;
        background: #c9b794;
    }

    .mission-fill {
        width: 0%;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #ff8e33, #ffca43);
        transition: width 0.32s ease;
    }

    .reward {
        white-space: nowrap;
        color: #8d5814;
        font-size: 9px;
        font-weight: 900;
    }

    .quick-right {
        position: absolute;
        z-index: 17;
        right: 7px;
        top: 90px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .quick-button {
        width: 52px;
        min-height: 51px;
        padding: 4px 2px;
        border: 0;
        border-radius: 15px;
        background: rgba(255,248,231,0.97);
        box-shadow: 0 4px 10px rgba(61,39,20,0.22);
        color: var(--brown);
        font-size: 8px;
        font-weight: 900;
        cursor: pointer;
    }

    .quick-button .icon {
        display: block;
        margin-bottom: 3px;
        font-size: 21px;
    }

    /* ---------- 대시보드 ---------- */
    .dashboard {
        position: relative;
        z-index: 20;
        padding: 9px 8px 14px;
        background:
            linear-gradient(
                180deg,
                rgba(239,205,151,0.99),
                rgba(227,181,110,0.99)
            );
    }

    .action-menu {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 4px;
        margin-bottom: 8px;
        padding: 8px 5px;
        border: 1px solid rgba(138,91,40,0.18);
        border-radius: 14px;
        background: rgba(255,247,224,0.94);
        box-shadow: 0 4px 9px rgba(87,54,25,0.15);
    }

    .action-button {
        min-width: 0;
        padding: 3px 0;
        border: 0;
        background: transparent;
        color: var(--brown);
        font-size: 8px;
        font-weight: 900;
        cursor: pointer;
    }

    .action-icon {
        display: block;
        margin-bottom: 4px;
        font-size: 23px;
        transition: transform .16s ease;
    }

    .action-button:active .action-icon {
        transform: scale(.84);
    }

    .cards {
        display: grid;
        grid-template-columns: 1.16fr 1fr .78fr;
        gap: 6px;
    }

    .card {
        min-height: 188px;
        padding: 11px 9px;
        border: 1px solid rgba(139,92,39,0.17);
        border-radius: 14px;
        background: rgba(255,248,230,0.97);
        box-shadow: 0 4px 10px rgba(79,48,21,0.12);
    }

    .card-title {
        margin-bottom: 8px;
        font-size: 10px;
        font-weight: 900;
    }

    .battery-range {
        font-size: 9px;
        line-height: 1.55;
        font-weight: 800;
    }

    .battery-pet {
        margin: 7px 0 5px;
        text-align: center;
        font-size: 31px;
    }

    .battery-scale {
        position: relative;
        height: 7px;
        margin: 19px 7px 14px;
        border-radius: 10px;
        background:
            linear-gradient(
                90deg,
                #f15b44 0%,
                #ffd25c 44%,
                #76ad51 100%
            );
    }

    .battery-pointer {
        position: absolute;
        top: -7px;
        left: 81%;
        width: 14px;
        height: 14px;
        transform: translateX(-50%);
        border: 3px solid #fff;
        border-radius: 50%;
        background: #e64c39;
        box-shadow: 0 2px 5px rgba(0,0,0,0.23);
        transition: left .32s ease;
    }

    .scale-labels {
        display: flex;
        justify-content: space-between;
        font-size: 7px;
        font-weight: 900;
    }

    .battery-message {
        margin-top: 10px;
        padding: 7px;
        border-radius: 9px;
        background: #f1e4c6;
        font-size: 8px;
        line-height: 1.45;
        font-weight: 800;
    }

    .time-card {
        text-align: center;
    }

    .time-robot {
        margin: 6px 0 1px;
        font-size: 31px;
        animation: tinyFloat 2s ease-in-out infinite;
    }

    .time-value {
        color: #ef573f;
        font-size: 32px;
        line-height: 1;
        font-weight: 900;
    }

    .time-unit {
        font-size: 12px;
    }

    .time-sub {
        margin-top: 4px;
        font-size: 8px;
        font-weight: 800;
    }

    .time-tip {
        margin-top: 15px;
        padding: 7px 5px;
        border-radius: 9px;
        background: #fff0ca;
        color: #745431;
        font-size: 8px;
        line-height: 1.45;
        font-weight: 800;
    }

    .food-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .food-title {
        width: 100%;
        text-align: left;
        font-size: 10px;
        font-weight: 900;
    }

    .food-bowl {
        position: relative;
        width: 64px;
        height: 42px;
        margin: 26px auto 10px;
        border-radius: 6px 6px 25px 25px;
        background: linear-gradient(180deg, #d84849, #ad2e36);
        box-shadow:
            0 7px 8px rgba(81,37,25,0.2),
            inset 0 -7px 8px rgba(83,12,22,0.14);
    }

    .food-bowl::before {
        content: "";
        position: absolute;
        left: 4px;
        top: -9px;
        width: 56px;
        height: 19px;
        border: 4px solid #d54749;
        border-radius: 50%;
        background:
            radial-gradient(circle at 30% 35%, #f1ab36 0 4px, transparent 5px),
            radial-gradient(circle at 60% 45%, #d57d24 0 5px, transparent 6px),
            radial-gradient(circle at 78% 30%, #f3c248 0 4px, transparent 5px),
            #944827;
    }

    .food-bowl::after {
        content: "⚡";
        position: absolute;
        left: 50%;
        top: 10px;
        transform: translateX(-50%);
        color: #ffd542;
        font-size: 20px;
        font-weight: 900;
    }

    .food-count {
        font-size: 9px;
        font-weight: 900;
    }

    .home-indicator {
        width: 135px;
        height: 5px;
        margin: 10px auto 0;
        border-radius: 10px;
        background: rgba(45,37,30,0.72);
    }

    /* ---------- 팝업 / 토스트 ---------- */
    .modal {
        position: absolute;
        z-index: 100;
        inset: 0;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 30px;
        background: rgba(45,33,23,0.61);
        backdrop-filter: blur(4px);
    }

    .modal.show {
        display: flex;
    }

    .modal-card {
        width: 100%;
        padding: 19px;
        border-radius: 20px;
        background: #fff8e8;
        box-shadow: 0 18px 45px rgba(28,19,12,0.38);
        animation: pop .18s ease-out;
    }

    .modal-title {
        font-size: 18px;
        font-weight: 900;
    }

    .modal-body {
        margin: 13px 0 17px;
        color: #6c513c;
        font-size: 12px;
        line-height: 1.65;
        font-weight: 700;
    }

    .modal-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 7px;
        margin-bottom: 8px;
    }

    .modal-action {
        padding: 10px 6px;
        border: 0;
        border-radius: 11px;
        background: #f2e3c4;
        color: #5c402c;
        font-size: 10px;
        font-weight: 900;
        cursor: pointer;
    }

    .modal-close {
        width: 100%;
        padding: 11px;
        border: 0;
        border-radius: 12px;
        background: #ef8c32;
        color: #fff;
        font-weight: 900;
        cursor: pointer;
    }

    .toast {
        position: absolute;
        z-index: 120;
        left: 50%;
        bottom: 26px;
        width: max-content;
        max-width: 84%;
        padding: 11px 17px;
        transform: translateX(-50%) translateY(30px);
        border-radius: 18px;
        background: rgba(44,37,31,0.94);
        color: #fff;
        font-size: 11px;
        font-weight: 800;
        opacity: 0;
        pointer-events: none;
        transition: all .25s ease;
    }

    .toast.show {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }

    /* ---------- 애니메이션 ---------- */
    @keyframes robotIdle {
        0%, 100% {
            transform: translateX(-50%) translateY(0) rotate(-1deg);
        }
        50% {
            transform: translateX(-50%) translateY(-7px) rotate(1deg);
        }
    }

    @keyframes robotPatrol {
        0% {
            transform: translateX(calc(-50% - 67px)) rotate(-4deg);
        }
        50% {
            transform: translateX(calc(-50% + 67px)) rotate(4deg);
        }
        100% {
            transform: translateX(calc(-50% - 67px)) rotate(-4deg);
        }
    }

    @keyframes robotCharging {
        0%, 100% {
            transform: translateX(-50%) translateY(0) scale(1);
            filter: brightness(1);
        }
        50% {
            transform: translateX(-50%) translateY(-3px) scale(1.035);
            filter: brightness(1.12);
        }
    }

    @keyframes robotLowPower {
        0% {
            transform: translateX(-50%) translateX(-2px) rotate(-1deg);
        }
        25% {
            transform: translateX(-50%) translateX(2px) rotate(1deg);
        }
        50% {
            transform: translateX(-50%) translateX(-1px) rotate(-1deg);
        }
        75% {
            transform: translateX(-50%) translateX(1px) rotate(1deg);
        }
        100% {
            transform: translateX(-50%) translateX(-2px) rotate(-1deg);
        }
    }

    @keyframes robotCelebrate {
        0%, 100% {
            transform: translateX(-50%) translateY(0) scale(1);
        }
        45% {
            transform: translateX(-50%) translateY(-35px) scale(1.08) rotate(-5deg);
        }
        70% {
            transform: translateX(-50%) translateY(-7px) scale(1.03) rotate(5deg);
        }
    }

    @keyframes robotTap {
        0%, 100% {
            transform: translateX(-50%) scale(1);
        }
        40% {
            transform: translateX(-50%) scale(.92, 1.08);
        }
        70% {
            transform: translateX(-50%) scale(1.08, .94);
        }
    }

    @keyframes eyeBlink {
        0%, 45%, 49%, 100% {
            transform: scaleY(1);
        }
        47% {
            transform: scaleY(.08);
        }
    }

    @keyframes sparkle {
        0%, 100% {
            transform: scale(.85) rotate(-10deg);
            opacity: .55;
        }
        50% {
            transform: scale(1.18) rotate(8deg);
            opacity: 1;
        }
    }

    @keyframes chargeRingSpin {
        from {
            transform: translateX(-50%) rotate(0deg);
        }
        to {
            transform: translateX(-50%) rotate(360deg);
        }
    }

    @keyframes dustRise {
        0% {
            transform: translateY(0) scale(.6);
            opacity: 0;
        }
        25% {
            opacity: .65;
        }
        100% {
            transform: translateY(-45px) translateX(15px) scale(1.25);
            opacity: 0;
        }
    }

    @keyframes effectFly {
        0% {
            transform: translate(0, 0) scale(.7) rotate(0deg);
            opacity: 0;
        }
        20% {
            opacity: 1;
        }
        100% {
            transform: translate(var(--move-x), -125px) scale(1.35) rotate(var(--rotate));
            opacity: 0;
        }
    }

    @keyframes tinyFloat {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
    }

    @keyframes pop {
        from {
            opacity: 0;
            transform: scale(.88);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    @media (max-width: 440px) {
        body {
            padding: 0;
        }

        .phone {
            width: 100%;
            border-width: 0;
            border-radius: 0;
        }

        .notch {
            display: none;
        }
    }
</style>
</head>

<body>
<div class="phone">
    <div class="notch"></div>

    <div class="screen">
        <header class="top-bar">
            <div class="profile">
                <span class="profile-crown">👑</span>
                🤖
            </div>

            <div class="profile-info">
                <div class="coin-line">
                    🪙 <span id="coinValue">050</span>
                </div>
                <div class="level-line">
                    Lv.<span id="levelValue">13</span>
                </div>
                <div class="exp-track">
                    <div class="exp-fill" id="expFill"></div>
                </div>
            </div>

            <div class="top-status">
                <span>⚡ <b id="socTop">81</b>%</span>
                <span>🌡️ <b id="tempTop">29</b>℃</span>
                <span>💗 <b id="heartTop">100</b></span>
                <span>🛡️ <b id="healthTop">100</b>%</span>
            </div>

            <button class="setting-button" onclick="openSettings()">⚙</button>
        </header>

        <section class="room" id="roomScene">
            <div class="wall-light"></div>
            <div class="floor-line"></div>
            <div class="floor"></div>
            <div class="sofa"></div>

            <div class="plant">
                <div class="stem"></div>
                <div class="leaf one"></div>
                <div class="leaf two"></div>
                <div class="leaf three"></div>
                <div class="leaf four"></div>
                <div class="pot"></div>
            </div>

            <div class="robot-home"></div>

            <div class="speech" id="speechBubble">
                <strong>배가 든든해요!</strong><br>
                청소를 준비할게요!
            </div>

            <div class="mode-chip" id="modeChip">
                ✨ AI 권장 SOC 81%
            </div>

            <div class="rug"></div>

            <div class="clean-path">
                <div class="clean-path-fill" id="cleanPathFill"></div>
            </div>

            <div class="charge-ring"></div>

            <div class="dust-layer">
                <span></span><span></span><span></span>
                <span></span><span></span><span></span>
            </div>

            <div
                class="robot"
                id="robotCharacter"
                onclick="petRobot()"
                title="로봇을 눌러 쓰다듬어 주세요"
            >
                <div class="crown">👑</div>
                <div class="spark" id="sparkIcon">✨</div>
                <div class="robot-top"></div>

                <div class="robot-face">
                    <div class="eye left"></div>
                    <div class="eye right"></div>
                    <div class="cheek left"></div>
                    <div class="cheek right"></div>
                    <div class="mouth"></div>
                </div>

                <div class="robot-slot"></div>
            </div>

            <div class="mission-mini">
                <div class="mission-mini-title">오늘의 미션</div>
                <div class="mission-mini-text">거실 청소 1회 완료하기</div>

                <div class="mission-progress">
                    <div class="mission-track">
                        <div class="mission-fill" id="missionFill"></div>
                    </div>
                    <span class="reward">+50 🪙</span>
                </div>
            </div>

            <div class="quick-right">
                <button class="quick-button" onclick="openBatteryPanel()">
                    <span class="icon">💖</span>
                    상태보기
                </button>

                <button class="quick-button" onclick="chargeRobot()">
                    <span class="icon">🔋</span>
                    배터리 관리
                </button>

                <button class="quick-button" onclick="openCleaningHistory()">
                    <span class="icon">📋</span>
                    청소 기록
                </button>

                <button class="quick-button" onclick="decorateRobot()">
                    <span class="icon">🎩</span>
                    꾸미기
                </button>
            </div>

            <div class="effect-layer" id="effectLayer"></div>
        </section>

        <main class="dashboard">
            <div class="action-menu">
                <button class="action-button" onclick="feedRobot()">
                    <span class="action-icon">🥣</span>
                    먹여주기
                </button>

                <button class="action-button" onclick="playRobot()">
                    <span class="action-icon">🏐</span>
                    놀아주기
                </button>

                <button class="action-button" onclick="exerciseRobot()">
                    <span class="action-icon">🏋️</span>
                    훈련하기
                </button>

                <button class="action-button" onclick="takePhoto()">
                    <span class="action-icon">📷</span>
                    사진첩
                </button>

                <button class="action-button" onclick="completeMission()">
                    <span class="action-icon">🏆</span>
                    미션
                </button>

                <button class="action-button" onclick="openShop()">
                    <span class="action-icon">🛒</span>
                    상점
                </button>
            </div>

            <div class="cards">
                <section class="card">
                    <div class="card-title">배터리 상태</div>

                    <div class="battery-range">
                        15%~90% 사이에서<br>
                        사용하는 것이<br>
                        수명 연장에 가장 좋아요!
                    </div>

                    <div class="battery-pet" id="batteryPet">😊</div>

                    <div class="battery-scale">
                        <div class="battery-pointer" id="batteryPointer"></div>
                    </div>

                    <div class="scale-labels">
                        <span>0%</span>
                        <span>15%</span>
                        <span>90%</span>
                        <span>100%</span>
                    </div>

                    <div class="battery-message" id="batteryMessage">
                        배터리 상태가 좋아요.<br>
                        수명 보호 범위 안에서 사용 중이에요.
                    </div>
                </section>

                <section class="card time-card">
                    <div class="card-title">예상 청소 가능 시간</div>
                    <div class="time-robot">🤖</div>

                    <div class="time-value">
                        <span id="cleaningTime">45</span>
                        <span class="time-unit">분</span>
                    </div>

                    <div class="time-sub">현재 배터리 기준</div>

                    <div class="time-tip" id="timeTip">
                        ✅ 현재 배터리로 거실 청소가 가능합니다.
                    </div>
                </section>

                <section class="card food-card">
                    <div class="food-title">오늘의 음식</div>
                    <div class="food-bowl"></div>

                    <div class="food-count">
                        보유량: <span id="foodCount">1</span>개
                    </div>
                </section>
            </div>

            <div class="home-indicator"></div>
        </main>

        <div class="modal" id="modal">
            <div class="modal-card">
                <div class="modal-title" id="modalTitle"></div>
                <div class="modal-body" id="modalBody"></div>
                <div class="modal-actions" id="modalActions"></div>

                <button class="modal-close" onclick="closePanel()">
                    확인
                </button>
            </div>
        </div>

        <div class="toast" id="toast"></div>
    </div>
</div>

<script>
    const state = {
        soc: 81,
        temperature: 29,
        heart: 100,
        health: 100,
        level: 13,
        exp: 55,
        coins: 50,
        food: 1,

        missionComplete: false,
        cleaning: false,
        charging: false,
        celebrating: false,

        cleanProgress: 0,
        recommendedSoc: 81,
        todayCleanCount: 0
    };


    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }


    function calculateCleaningTime() {
        return Math.max(0, Math.round(state.soc * 0.56));
    }


    function render() {
        state.soc = clamp(Math.round(state.soc), 0, 100);
        state.temperature = Math.round(state.temperature * 10) / 10;
        state.heart = clamp(Math.round(state.heart), 0, 100);
        state.health = clamp(Math.round(state.health), 0, 100);
        state.exp = clamp(Math.round(state.exp), 0, 100);

        document.getElementById("socTop").innerText = state.soc;
        document.getElementById("tempTop").innerText = state.temperature;
        document.getElementById("heartTop").innerText = state.heart;
        document.getElementById("healthTop").innerText = state.health;
        document.getElementById("coinValue").innerText =
            String(state.coins).padStart(3, "0");
        document.getElementById("levelValue").innerText = state.level;
        document.getElementById("foodCount").innerText = state.food;
        document.getElementById("expFill").style.width = state.exp + "%";
        document.getElementById("cleaningTime").innerText =
            calculateCleaningTime();
        document.getElementById("batteryPointer").style.left =
            state.soc + "%";

        const speech = document.getElementById("speechBubble");
        const batteryPet = document.getElementById("batteryPet");
        const batteryMessage = document.getElementById("batteryMessage");
        const timeTip = document.getElementById("timeTip");
        const spark = document.getElementById("sparkIcon");

        if (state.cleaning) {
            speech.innerHTML =
                "<strong style='color:#31944b'>열심히 청소 중이에요!</strong><br>" +
                "진행률 " + state.cleanProgress + "%";

            batteryPet.innerText = "🧹";
            spark.innerText = "💨";

            batteryMessage.innerHTML =
                "현재 청소 중이에요.<br>" +
                "SOC와 예상 시간이 실시간으로 변합니다.";

            timeTip.innerHTML =
                "🧹 청소 진행률 " + state.cleanProgress + "%";

        } else if (state.charging) {
            speech.innerHTML =
                "<strong style='color:#e68b28'>에너지를 먹고 있어요!</strong><br>" +
                "필요한 만큼만 충전할게요.";

            batteryPet.innerText = "⚡";
            spark.innerText = "⚡";

            batteryMessage.innerHTML =
                "사용자 패턴에 맞춰<br>" +
                state.recommendedSoc + "%까지만 충전합니다.";

            timeTip.innerHTML =
                "🔋 맞춤 충전 진행 중: " + state.soc + "%";

        } else if (state.soc < 15) {
            speech.innerHTML =
                "<strong style='color:#ef4d44'>배가 너무 고파요...</strong><br>" +
                "바로 충전해 주세요!";

            batteryPet.innerText = "🥴";
            spark.innerText = "💦";

            batteryMessage.innerHTML =
                "배터리가 매우 부족해요.<br>" +
                "현재 상태에서는 청소를 시작할 수 없어요.";

            timeTip.innerHTML =
                "⚠️ 충전 후 청소를 시작해 주세요.";

        } else if (state.soc < 30) {
            speech.innerHTML =
                "<strong style='color:#ef4d44'>배가 고파요...</strong><br>" +
                "충전이 필요해요!";

            batteryPet.innerText = "😵";
            spark.innerText = "💧";

            batteryMessage.innerHTML =
                "배고파서 힘이 없어요.<br>" +
                "충전하면 더 오래 청소할 수 있어요.";

            timeTip.innerHTML =
                "💡 충전 후 더 넓은 공간을 청소할 수 있어요.";

        } else if (state.soc <= 90) {
            speech.innerHTML =
                "<strong>배가 든든해요!</strong><br>" +
                "청소를 준비할게요!";

            batteryPet.innerText = "😊";
            spark.innerText = "✨";

            batteryMessage.innerHTML =
                "배터리 상태가 좋아요.<br>" +
                "수명 보호 범위 안에서 사용 중이에요.";

            timeTip.innerHTML =
                "✅ 현재 배터리로 거실 청소가 가능합니다.";

        } else {
            speech.innerHTML =
                "<strong style='color:#de8b26'>배가 너무 불러요!</strong><br>" +
                "충전을 멈춰도 좋아요.";

            batteryPet.innerText = "😮";
            spark.innerText = "⚡";

            batteryMessage.innerHTML =
                "권장 충전 상한을 넘었어요.<br>" +
                "90% 이하 충전을 권장합니다.";

            timeTip.innerHTML =
                "🔋 충분히 충전되었습니다.";
        }

        renderMotionState();
    }


    function renderMotionState() {
        const room = document.getElementById("roomScene");
        const robot = document.getElementById("robotCharacter");
        const modeChip = document.getElementById("modeChip");
        const cleanPathFill = document.getElementById("cleanPathFill");
        const missionFill = document.getElementById("missionFill");

        room.classList.remove(
            "is-cleaning",
            "is-charging",
            "is-low",
            "is-celebrating"
        );

        robot.classList.remove("look-left", "look-right");

        if (state.celebrating) {
            room.classList.add("is-celebrating");
            modeChip.innerHTML = "🏆 미션 완료 · +50 코인";

        } else if (state.cleaning) {
            room.classList.add("is-cleaning");
            modeChip.innerHTML =
                "🧹 거실 청소 중 · " + state.cleanProgress + "%";

        } else if (state.charging) {
            room.classList.add("is-charging");
            modeChip.innerHTML =
                "⚡ 맞춤 충전 중 · " +
                state.soc + " → " + state.recommendedSoc + "%";

        } else if (state.soc < 15) {
            room.classList.add("is-low");
            modeChip.innerHTML = "⚠️ 배터리 부족 · 충전 필요";

        } else {
            modeChip.innerHTML =
                "✨ AI 권장 SOC " + state.recommendedSoc + "%";
        }

        cleanPathFill.style.width = state.cleanProgress + "%";

        missionFill.style.width =
            state.missionComplete
                ? "100%"
                : state.cleanProgress + "%";
    }


    function showToast(message) {
        const toast = document.getElementById("toast");

        toast.innerText = message;
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 1800);
    }


    function openPanel(title, body, actions = "") {
        document.getElementById("modalTitle").innerText = title;
        document.getElementById("modalBody").innerHTML = body;
        document.getElementById("modalActions").innerHTML = actions;
        document.getElementById("modal").classList.add("show");
    }


    function closePanel() {
        document.getElementById("modal").classList.remove("show");
    }


    function spawnEffect(symbol, count = 6) {
        const effectLayer = document.getElementById("effectLayer");

        for (let i = 0; i < count; i++) {
            const particle = document.createElement("span");

            particle.className = "effect";
            particle.innerText = symbol;

            particle.style.setProperty(
                "--move-x",
                Math.round(Math.random() * 160 - 80) + "px"
            );

            particle.style.setProperty(
                "--rotate",
                Math.round(Math.random() * 100 - 50) + "deg"
            );

            particle.style.left = 42 + Math.random() * 16 + "%";
            particle.style.animationDelay =
                Math.random() * 0.25 + "s";

            effectLayer.appendChild(particle);

            setTimeout(() => {
                particle.remove();
            }, 1600);
        }
    }


    function pulseRobot() {
        const robot = document.getElementById("robotCharacter");

        robot.classList.remove("tap-motion");
        void robot.offsetWidth;
        robot.classList.add("tap-motion");

        setTimeout(() => {
            robot.classList.remove("tap-motion");
        }, 650);
    }


    function petRobot() {
        if (state.cleaning) {
            showToast("청소 중이에요! 끝나면 쓰다듬어 주세요.");
            return;
        }

        state.heart = Math.min(100, state.heart + 2);
        state.exp = Math.min(100, state.exp + 1);

        pulseRobot();
        spawnEffect("💖", 7);

        showToast("기분이 좋아졌어요! 친밀도 +2");
        render();
    }


    function feedRobot() {
        if (state.food <= 0) {
            showToast("오늘의 음식이 부족해요. 상점에서 구매해 주세요.");
            return;
        }

        state.food -= 1;
        state.soc += 12;
        state.heart += 4;
        state.exp += 8;

        pulseRobot();
        spawnEffect("⚡", 8);

        showToast("맛있게 먹고 SOC가 12% 올랐어요!");
        levelCheck();
        render();
    }


    function playRobot() {
        if (state.soc < 5) {
            showToast("배터리가 부족해서 놀 수 없어요.");
            return;
        }

        state.soc -= 3;
        state.heart += 6;
        state.exp += 5;

        pulseRobot();
        spawnEffect("💖", 8);

        showToast("신나게 놀았어요! 친밀도 +6");
        levelCheck();
        render();
    }


    function exerciseRobot() {
        if (state.soc < 8) {
            showToast("훈련 전에 충전이 필요해요.");
            return;
        }

        state.soc -= 6;
        state.health += 3;
        state.exp += 12;

        pulseRobot();
        spawnEffect("✨", 8);

        showToast("훈련 완료! 건강도와 경험치가 올랐어요.");
        levelCheck();
        render();
    }


    function takePhoto() {
        pulseRobot();
        spawnEffect("📸", 5);

        openPanel(
            "오늘의 사진",
            "왕관을 쓴 로봇청소기가 촬영되었습니다.<br><br>" +
            "향후 실제 구현에서는 사용자가 선택한 장식과 " +
            "청소 완료 장면을 사진첩에 저장할 수 있습니다."
        );
    }


    function decorateRobot() {
        openPanel(
            "로봇 꾸미기",
            "현재 장착 아이템은 <b>황금 왕관</b>입니다.<br><br>" +
            "리본, 모자, 표정 스킨, 청소 완료 이펙트 등을 " +
            "코인으로 구매하는 육성 기능으로 확장할 수 있습니다.",
            '<button class="modal-action" onclick="spawnEffect(\'🎀\',8); closePanel();">리본 체험</button>' +
            '<button class="modal-action" onclick="spawnEffect(\'✨\',10); closePanel();">반짝이 체험</button>'
        );
    }


    function completeMission() {
        if (state.missionComplete) {
            showToast("오늘의 미션을 이미 완료했어요.");
            return;
        }

        startCleaning();
    }


    function startCleaning() {
        if (state.cleaning) {
            showToast("이미 청소 중이에요.");
            return;
        }

        if (state.charging) {
            showToast("충전이 끝난 후 청소할게요.");
            return;
        }

        if (state.soc < 15) {
            showToast("SOC가 부족합니다. 먼저 충전해 주세요.");
            return;
        }

        state.cleaning = true;
        state.cleanProgress = 0;
        render();

        showToast("거실 청소를 시작합니다!");

        let cleanStep = 0;
        const totalSteps = 18;

        const cleaningTimer = setInterval(() => {
            cleanStep += 1;

            state.cleanProgress =
                Math.round(cleanStep / totalSteps * 100);

            state.soc = Math.max(0, state.soc - 1);
            state.temperature =
                Math.min(36, state.temperature + 0.25);

            render();

            if (cleanStep >= totalSteps || state.soc <= 10) {
                clearInterval(cleaningTimer);

                state.cleaning = false;
                state.cleanProgress = 100;
                state.temperature = 29;
                state.missionComplete = true;
                state.todayCleanCount += 1;
                state.coins += 50;
                state.exp += 20;
                state.celebrating = true;

                levelCheck();
                render();

                spawnEffect("🎉", 15);
                spawnEffect("⭐", 9);

                setTimeout(() => {
                    state.celebrating = false;
                    render();
                }, 2300);

                setTimeout(() => {
                    openPanel(
                        "청소 완료!",
                        "거실 청소를 완료했습니다.<br><br>" +
                        "예측된 배터리 범위 안에서 청소를 마쳤으며, " +
                        "미션 보상으로 <b>50 코인</b>과 경험치 20을 획득했습니다."
                    );
                }, 650);
            }
        }, 320);
    }


    function chargeRobot() {
        if (state.cleaning) {
            showToast("청소가 끝난 후 충전할 수 있어요.");
            return;
        }

        if (state.charging) {
            showToast("현재 충전 중이에요.");
            return;
        }

        const targetSoc = state.recommendedSoc;

        if (state.soc >= targetSoc) {
            openPanel(
                "맞춤 충전 안내",
                "사용자의 최근 청소 패턴을 분석한 결과, " +
                "오늘의 권장 충전 상한은 <b>" + targetSoc + "%</b>입니다.<br><br>" +
                "현재 SOC가 이미 권장값에 도달했으므로 추가 충전하지 않습니다."
            );
            return;
        }

        state.charging = true;
        render();
        showToast("AI 맞춤 충전을 시작합니다.");

        const chargeTimer = setInterval(() => {
            state.soc = Math.min(targetSoc, state.soc + 2);
            state.temperature =
                Math.min(32, state.temperature + 0.15);

            spawnEffect("⚡", 2);
            render();

            if (state.soc >= targetSoc) {
                clearInterval(chargeTimer);

                state.soc = targetSoc;
                state.temperature = 29;
                state.charging = false;
                render();

                spawnEffect("✨", 10);

                setTimeout(() => {
                    openPanel(
                        "맞춤 충전 완료",
                        "오늘 예상 청소량에 필요한 SOC는 <b>" +
                        targetSoc + "%</b>입니다.<br><br>" +
                        "불필요한 100% 충전을 피하여 배터리의 " +
                        "고전압 유지 시간을 줄였습니다."
                    );
                }, 450);
            }
        }, 150);
    }


    function openBatteryPanel() {
        openPanel(
            "배터리 상태",
            "현재 SOC는 <b>" + state.soc + "%</b>입니다.<br>" +
            "배터리 건강도는 <b>" + state.health + "%</b>이며, " +
            "예상 청소 가능 시간은 <b>" +
            calculateCleaningTime() + "분</b>입니다.<br><br>" +
            "사용자 패턴 기반 권장 SOC는 <b>" +
            state.recommendedSoc + "%</b>입니다."
        );
    }


    function openCleaningHistory() {
        openPanel(
            "청소 기록",
            "오늘 거실 청소 <b>" + state.todayCleanCount + "회</b><br>" +
            "현재 미션 진행률 <b>" + state.cleanProgress + "%</b><br>" +
            "이번 주 누적 청소시간 <b>124분</b><br>" +
            "평균 소비 SOC <b>27%</b><br><br>" +
            "향후 Python 시뮬레이션 데이터와 연결하면 " +
            "요일별 사용 패턴과 배터리 열화도까지 표시할 수 있습니다."
        );
    }


    function openShop() {
        openPanel(
            "로봇 상점",
            "보유 코인: <b>" + state.coins + "개</b><br><br>" +
            "🥣 배터리 음식 50코인<br>" +
            "🎀 리본 80코인<br>" +
            "🧢 탐험가 모자 120코인<br>" +
            "✨ 반짝이 효과 150코인",
            '<button class="modal-action" onclick="buyFood()">음식 구매</button>' +
            '<button class="modal-action" onclick="spawnEffect(\'✨\',10); closePanel();">효과 체험</button>'
        );
    }


    function buyFood() {
        if (state.coins < 50) {
            showToast("코인이 부족해요.");
            return;
        }

        state.coins -= 50;
        state.food += 1;
        closePanel();
        showToast("배터리 음식 1개를 구매했어요.");
        render();
    }


    function openSettings() {
        openPanel(
            "시연 설정",
            "발표 중 상태 변화를 빠르게 보여주기 위한 시연 모드입니다.",
            '<button class="modal-action" onclick="setLowBattery()">저전력 시연</button>' +
            '<button class="modal-action" onclick="resetDemo()">초기화</button>'
        );
    }


    function setLowBattery() {
        state.soc = 12;
        state.temperature = 28;
        state.cleaning = false;
        state.charging = false;
        state.cleanProgress = 0;
        state.missionComplete = false;

        closePanel();
        render();
        showToast("저전력 시연 상태로 변경했습니다.");
    }


    function resetDemo() {
        state.soc = 81;
        state.temperature = 29;
        state.heart = 100;
        state.health = 100;
        state.level = 13;
        state.exp = 55;
        state.coins = 50;
        state.food = 1;
        state.missionComplete = false;
        state.cleaning = false;
        state.charging = false;
        state.celebrating = false;
        state.cleanProgress = 0;
        state.todayCleanCount = 0;

        closePanel();
        render();
        showToast("초기 상태로 돌아왔어요.");
    }


    function levelCheck() {
        if (state.exp >= 100) {
            state.exp -= 100;
            state.level += 1;
            spawnEffect("⭐", 10);
            showToast("레벨 업! Lv." + state.level + "이 되었어요.");
        }
    }


    setInterval(() => {
        if (
            state.cleaning ||
            state.charging ||
            state.celebrating
        ) {
            return;
        }

        const robot = document.getElementById("robotCharacter");
        robot.classList.remove("look-left", "look-right");

        const direction = Math.random();

        if (direction < 0.33) {
            robot.classList.add("look-left");
        } else if (direction < 0.66) {
            robot.classList.add("look-right");
        }

        setTimeout(() => {
            robot.classList.remove("look-left", "look-right");
        }, 1100);
    }, 2800);


    render();
</script>
</body>
</html>
"""


components.html(
    APP_HTML,
    height=940,
    scrolling=False,
)
