import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="로봇청소기 키우기",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# Streamlit 기본 화면 숨기기
st.markdown(
    """
    <style>
        [data-testid="stHeader"] {
            display: none;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stSidebar"] {
            display: none;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .stApp {
            background:
                radial-gradient(circle at 20% 10%, #fff8ec 0, transparent 30%),
                radial-gradient(circle at 90% 85%, #f4dfbd 0, transparent 28%),
                #efe6d9;
        }

        .block-container {
            max-width: 100%;
            padding: 18px 8px 22px 8px;
        }

        iframe {
            border: none !important;
            border-radius: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


mobile_ui = """
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
        --cream: #fff3d9;
        --cream-dark: #f2d7a8;
        --brown: #4b3324;
        --brown-soft: #7a5840;
        --orange: #ff982f;
        --red: #f4513a;
        --green: #64a641;
        --yellow: #ffd44f;
        --card: rgba(255, 248, 230, 0.96);
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
        width: min(100%, 402px);
        min-height: 880px;
        overflow: hidden;
        border: 8px solid #22211f;
        border-radius: 39px;
        background: #e9c692;
        box-shadow:
            0 28px 70px rgba(55, 34, 18, 0.30),
            0 8px 20px rgba(55, 34, 18, 0.18);
    }

    .notch {
        position: absolute;
        z-index: 30;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 125px;
        height: 24px;
        background: #22211f;
        border-radius: 0 0 18px 18px;
    }

    .screen {
        position: relative;
        min-height: 864px;
        overflow: hidden;
        background:
            linear-gradient(
                180deg,
                rgba(89, 61, 38, 0.12),
                rgba(255, 244, 220, 0.1) 40%,
                #e8bd80 68%,
                #deb06e 100%
            );
    }

    /* 상단 상태바 */
    .top-bar {
        position: relative;
        z-index: 20;
        height: 62px;
        display: grid;
        grid-template-columns: 48px 1fr 1fr 40px;
        align-items: center;
        gap: 5px;
        padding: 12px 8px 7px 8px;
        color: white;
        background:
            linear-gradient(
                90deg,
                rgba(38, 31, 25, 0.90),
                rgba(57, 43, 33, 0.82)
            );
        box-shadow: 0 5px 15px rgba(33, 23, 16, 0.2);
    }

    .profile {
        position: relative;
        width: 43px;
        height: 43px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        background: #f5deb2;
        border: 3px solid #fff1c5;
        box-shadow: 0 3px 8px rgba(0,0,0,0.24);
        font-size: 25px;
    }

    .mini-crown {
        position: absolute;
        top: -10px;
        font-size: 15px;
        transform: rotate(-8deg);
    }

    .level-area {
        min-width: 82px;
    }

    .coin-line {
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 15px;
        font-weight: 900;
    }

    .level-text {
        margin-top: 1px;
        font-size: 10px;
        color: #f5ead9;
        font-weight: 800;
    }

    .exp-bar {
        height: 6px;
        margin-top: 3px;
        overflow: hidden;
        border-radius: 10px;
        background: rgba(255,255,255,0.25);
    }

    .exp-fill {
        width: 55%;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #ff5e3a, #ff9f3c);
    }

    .status-set {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 7px;
        font-size: 11px;
        font-weight: 800;
        white-space: nowrap;
    }

    .status-item {
        display: flex;
        align-items: center;
        gap: 2px;
    }

    .soc-low {
        color: #ff5b42;
    }

    .setting-button {
        width: 35px;
        height: 35px;
        border: 0;
        border-radius: 50%;
        color: white;
        background: rgba(0,0,0,0.30);
        font-size: 20px;
        cursor: pointer;
    }

    /* 방 배경 */
    .room {
        position: relative;
        height: 327px;
        overflow: hidden;
        background:
            linear-gradient(
                180deg,
                #b99066 0%,
                #cba77f 46%,
                #d8b686 47%,
                #cc9b5e 100%
            );
    }

    .wall-light {
        position: absolute;
        top: -60px;
        left: 50%;
        width: 390px;
        height: 250px;
        transform: translateX(-50%);
        border-radius: 50%;
        background:
            radial-gradient(
                circle,
                rgba(255,246,220,0.82),
                rgba(255,240,201,0.20) 55%,
                transparent 72%
            );
    }

    .floor-line {
        position: absolute;
        top: 170px;
        width: 100%;
        height: 3px;
        background: rgba(105,69,38,0.16);
    }

    .floor {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 158px;
        background:
            repeating-linear-gradient(
                90deg,
                rgba(111,69,31,0.12) 0,
                rgba(111,69,31,0.12) 2px,
                transparent 2px,
                transparent 65px
            ),
            linear-gradient(180deg, #d5ad74, #c89354);
    }

    .floor::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            repeating-linear-gradient(
                0deg,
                transparent 0,
                transparent 36px,
                rgba(112,70,31,0.10) 37px,
                rgba(112,70,31,0.10) 39px
            );
    }

    /* 소파 */
    .sofa {
        position: absolute;
        right: -9px;
        top: 67px;
        width: 132px;
        height: 95px;
        border-radius: 27px 0 7px 7px;
        background: linear-gradient(145deg, #5d6f6b, #324c49);
        box-shadow: 0 9px 14px rgba(57,39,24,0.27);
    }

    .sofa::before {
        content: "";
        position: absolute;
        top: -17px;
        left: 10px;
        width: 75px;
        height: 45px;
        border-radius: 17px 17px 7px 7px;
        background: #657874;
    }

    .sofa::after {
        content: "";
        position: absolute;
        top: 17px;
        left: 4px;
        width: 117px;
        height: 5px;
        border-radius: 10px;
        background: rgba(255,255,255,0.10);
    }

    /* 화분 */
    .plant {
        position: absolute;
        left: 15px;
        top: 58px;
        width: 66px;
        height: 120px;
    }

    .pot {
        position: absolute;
        bottom: 0;
        left: 15px;
        width: 40px;
        height: 38px;
        border-radius: 4px 4px 17px 17px;
        background: linear-gradient(90deg, #c68d55, #e0aa70);
        box-shadow: 0 4px 8px rgba(66,42,25,0.25);
    }

    .stem {
        position: absolute;
        left: 35px;
        top: 17px;
        width: 4px;
        height: 72px;
        background: #476d3c;
        transform: rotate(-3deg);
    }

    .leaf {
        position: absolute;
        width: 29px;
        height: 14px;
        border-radius: 90% 10% 90% 10%;
        background: linear-gradient(135deg, #69964c, #345d35);
    }

    .leaf.one {
        left: 4px;
        top: 22px;
        transform: rotate(26deg);
    }

    .leaf.two {
        left: 32px;
        top: 34px;
        transform: scaleX(-1) rotate(24deg);
    }

    .leaf.three {
        left: 4px;
        top: 50px;
        transform: rotate(18deg);
    }

    .leaf.four {
        left: 33px;
        top: 63px;
        transform: scaleX(-1) rotate(23deg);
    }

    /* 로봇 집 */
    .robot-home {
        position: absolute;
        left: 82px;
        top: 110px;
        width: 66px;
        height: 56px;
        border-radius: 28px 28px 6px 6px;
        background: linear-gradient(145deg, #a28b71, #776550);
        box-shadow: 0 6px 10px rgba(55,37,23,0.22);
    }

    .robot-home::before {
        content: "";
        position: absolute;
        left: 18px;
        bottom: 0;
        width: 31px;
        height: 31px;
        border-radius: 16px 16px 0 0;
        background: #3e3933;
    }

    .robot-home::after {
        content: "HOME";
        position: absolute;
        top: 11px;
        left: 16px;
        font-size: 7px;
        color: rgba(255,255,255,0.55);
        font-weight: 900;
    }

    /* 말풍선 */
    .speech {
        position: absolute;
        z-index: 10;
        top: 24px;
        left: 50%;
        width: 172px;
        min-height: 72px;
        padding: 14px 12px;
        transform: translateX(-50%);
        text-align: center;
        border-radius: 13px;
        background: rgba(255,255,255,0.97);
        box-shadow: 0 7px 16px rgba(60,39,21,0.18);
        color: #453126;
        font-size: 12px;
        line-height: 1.55;
        font-weight: 800;
    }

    .speech strong {
        color: var(--red);
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

    /* 러그 */
    .rug {
        position: absolute;
        z-index: 2;
        left: 50%;
        bottom: 11px;
        width: 242px;
        height: 87px;
        transform: translateX(-50%);
        border-radius: 50%;
        background:
            radial-gradient(
                ellipse,
                rgba(241,224,198,0.88),
                rgba(194,156,110,0.78)
            );
        box-shadow: inset 0 0 18px rgba(104,72,43,0.15);
    }

    /* 로봇 캐릭터 */
    .robot {
        position: absolute;
        z-index: 7;
        left: 50%;
        bottom: 29px;
        width: 172px;
        height: 95px;
        transform: translateX(-50%);
        border-radius: 62% 62% 40% 40%;
        border: 2px solid #a39d93;
        background:
            linear-gradient(
                180deg,
                #fffefb 0%,
                #e8e8e3 70%,
                #bdbeb8 100%
            );
        box-shadow:
            0 13px 18px rgba(56,38,21,0.32),
            inset 0 -8px 12px rgba(84,84,79,0.12);
    }

    .robot-top {
        position: absolute;
        left: 50%;
        top: -5px;
        width: 121px;
        height: 56px;
        transform: translateX(-50%);
        border-radius: 50%;
        border-top: 2px solid rgba(120,120,115,0.4);
        background:
            radial-gradient(
                ellipse at center,
                #fbfbf8 0%,
                #d5d6d2 73%,
                #b8b9b3 100%
            );
    }

    .robot-face {
        position: absolute;
        z-index: 3;
        left: 50%;
        bottom: 8px;
        width: 122px;
        height: 52px;
        transform: translateX(-50%);
        border-radius: 25px 25px 30px 30px;
        background:
            linear-gradient(
                180deg,
                #292b2c,
                #101213 75%
            );
        box-shadow: inset 0 4px 5px rgba(255,255,255,0.13);
    }

    .eye {
        position: absolute;
        top: 14px;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        border: 2px solid #f2f0dc;
        background: #111;
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
    }

    .eye.left {
        left: 19px;
    }

    .eye.right {
        right: 19px;
    }

    .mouth {
        position: absolute;
        left: 50%;
        bottom: 8px;
        width: 19px;
        height: 11px;
        transform: translateX(-50%);
        border: 2px solid #f2d4c8;
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
        z-index: 9;
        left: 50%;
        top: -39px;
        transform: translateX(-50%);
        font-size: 44px;
        filter: drop-shadow(0 4px 3px rgba(81,52,17,0.25));
    }

    .sweat {
        position: absolute;
        z-index: 8;
        right: -17px;
        top: -14px;
        font-size: 28px;
        transform: rotate(-15deg);
    }

    .robot-slot {
        position: absolute;
        left: 50%;
        bottom: -2px;
        width: 42px;
        height: 5px;
        transform: translateX(-50%);
        border-radius: 10px;
        background: #484a48;
    }

    /* 좌우 퀵 메뉴 */
    .quick-left,
    .quick-right {
        position: absolute;
        z-index: 14;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .quick-left {
        left: 7px;
        bottom: 14px;
    }

    .quick-right {
        right: 7px;
        top: 92px;
    }

    .quick-button {
        width: 50px;
        min-height: 50px;
        padding: 4px 2px;
        border: 0;
        border-radius: 15px;
        background: rgba(255,248,231,0.96);
        box-shadow: 0 4px 10px rgba(61,39,20,0.22);
        color: var(--brown);
        font-size: 8px;
        font-weight: 900;
        cursor: pointer;
    }

    .quick-button .icon {
        display: block;
        margin-bottom: 3px;
        font-size: 20px;
    }

    .mission-mini {
        width: 83px;
        padding: 8px 7px;
        border-radius: 13px;
        background: rgba(255,249,232,0.96);
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
        background: var(--orange);
        transition: width 0.35s;
    }

    .reward {
        white-space: nowrap;
        color: #8d5814;
        font-size: 9px;
        font-weight: 900;
    }

    /* 아래 앱 영역 */
    .dashboard {
        position: relative;
        z-index: 15;
        margin-top: -1px;
        padding: 9px 8px 13px 8px;
        background:
            linear-gradient(
                180deg,
                rgba(239,205,151,0.98),
                rgba(226,181,111,0.98)
            );
    }

    .action-menu {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 4px;
        margin-bottom: 8px;
        padding: 8px 5px;
        border: 1px solid rgba(139,91,40,0.18);
        border-radius: 13px;
        background: rgba(255,247,224,0.93);
        box-shadow: 0 4px 9px rgba(87,54,25,0.15);
    }

    .action-button {
        min-width: 0;
        padding: 3px 0;
        border: 0;
        background: transparent;
        color: var(--brown);
        cursor: pointer;
        font-size: 8px;
        font-weight: 900;
    }

    .action-button .action-icon {
        display: block;
        margin-bottom: 4px;
        font-size: 23px;
        transition: transform 0.16s ease;
    }

    .action-button:active .action-icon {
        transform: scale(0.86);
    }

    .cards {
        display: grid;
        grid-template-columns: 1.18fr 1fr 0.78fr;
        gap: 6px;
    }

    .card {
        min-height: 181px;
        padding: 11px 9px;
        border: 1px solid rgba(140,92,39,0.17);
        border-radius: 13px;
        background: var(--card);
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
        margin: 8px 0 5px;
        text-align: center;
        font-size: 31px;
    }

    .battery-scale {
        position: relative;
        height: 7px;
        margin: 20px 7px 14px;
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
        left: 18%;
        width: 14px;
        height: 14px;
        transform: translateX(-50%);
        border: 3px solid white;
        border-radius: 50%;
        background: #e64c39;
        box-shadow: 0 2px 5px rgba(0,0,0,0.23);
        transition: left 0.35s;
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
        margin-top: 16px;
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
        margin: 25px auto 10px;
        border-radius: 6px 6px 25px 25px;
        background:
            linear-gradient(
                180deg,
                #d84849,
                #ad2e36
            );
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
        border-radius: 50%;
        background:
            radial-gradient(
                circle at 30% 35%,
                #f1ab36 0 4px,
                transparent 5px
            ),
            radial-gradient(
                circle at 60% 45%,
                #d57d24 0 5px,
                transparent 6px
            ),
            radial-gradient(
                circle at 78% 30%,
                #f3c248 0 4px,
                transparent 5px
            ),
            #944827;
        border: 4px solid #d54749;
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

    /* 하단 홈 인디케이터 */
    .home-indicator {
        width: 135px;
        height: 5px;
        margin: 9px auto 0;
        border-radius: 10px;
        background: rgba(45,37,30,0.72);
    }

    /* 팝업 */
    .modal {
        position: absolute;
        z-index: 100;
        inset: 0;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 30px;
        background: rgba(45,33,23,0.60);
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
        animation: pop 0.18s ease-out;
    }

    @keyframes pop {
        from {
            opacity: 0;
            transform: scale(0.88);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
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

    .modal-close {
        width: 100%;
        padding: 11px;
        border: 0;
        border-radius: 12px;
        background: #ef8c32;
        color: white;
        font-weight: 900;
        cursor: pointer;
    }

    /* 토스트 */
    .toast {
        position: absolute;
        z-index: 120;
        left: 50%;
        bottom: 26px;
        width: max-content;
        max-width: 84%;
        padding: 11px 17px;
        transform:
            translateX(-50%)
            translateY(30px);
        border-radius: 18px;
        background: rgba(44,37,31,0.93);
        color: white;
        font-size: 11px;
        font-weight: 800;
        opacity: 0;
        pointer-events: none;
        transition: all 0.25s ease;
    }

    .toast.show {
        opacity: 1;
        transform:
            translateX(-50%)
            translateY(0);
    }

    @media (max-width: 430px) {
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

        <!-- 상단 정보 -->
        <header class="top-bar">
            <div class="profile">
                <span class="mini-crown">👑</span>
                🤖
            </div>

            <div class="level-area">
                <div class="coin-line">
                    🪙 <span id="coinValue">000</span>
                </div>
                <div class="level-text">
                    Lv.<span id="levelValue">12</span>
                </div>
                <div class="exp-bar">
                    <div class="exp-fill" id="expFill"></div>
                </div>
            </div>

            <div class="status-set">
                <div class="status-item soc-low">
                    ⚡ <span id="socTop">18</span>%
                </div>
                <div class="status-item">
                    🌡️ <span id="tempTop">28</span>℃
                </div>
                <div class="status-item">
                    ❤️ <span id="heartTop">75</span>
                </div>
                <div class="status-item">
                    🛡️ <span id="healthTop">82</span>%
                </div>
            </div>

            <button
                class="setting-button"
                onclick="openPanel(
                    '환경 설정',
                    '배터리 알림, 자동 충전 상한, 효과음 및 테마 설정을 관리하는 화면입니다.'
                )"
            >
                ⚙
            </button>
        </header>

        <!-- 캐릭터 공간 -->
        <section class="room">
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
                <strong>배가 너무 고파요...</strong><br>
                충전이 필요해요!
            </div>

            <div class="rug"></div>

            <div class="robot" id="robotCharacter">
                <div class="crown">👑</div>
                <div class="sweat" id="sweatIcon">💧</div>
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

            <div class="quick-left">
                <div class="mission-mini">
                    <div class="mission-mini-title">
                        오늘의 미션
                    </div>

                    <div class="mission-mini-text">
                        거실 청소 1회 완료하기
                    </div>

                    <div class="mission-progress">
                        <div class="mission-track">
                            <div
                                class="mission-fill"
                                id="missionFill"
                            ></div>
                        </div>

                        <span class="reward">
                            +50 🪙
                        </span>
                    </div>
                </div>
            </div>

            <div class="quick-right">
                <button
                    class="quick-button"
                    onclick="openBatteryPanel()"
                >
                    <span class="icon">💖</span>
                    상태보기
                </button>

                <button
                    class="quick-button"
                    onclick="chargeRobot()"
                >
                    <span class="icon">🔋</span>
                    배터리 관리
                </button>

                <button
                    class="quick-button"
                    onclick="openPanel(
                        '청소 기록',
                        '오늘 거실 청소 0회 · 이번 주 총 청소시간 124분 · 평균 소비 SOC 27%입니다.'
                    )"
                >
                    <span class="icon">📋</span>
                    청소 기록
                </button>

                <button
                    class="quick-button"
                    onclick="decorateRobot()"
                >
                    <span class="icon">🎩</span>
                    꾸미기
                </button>
            </div>
        </section>

        <!-- 아래 대시보드 -->
        <main class="dashboard">

            <div class="action-menu">
                <button
                    class="action-button"
                    onclick="feedRobot()"
                >
                    <span class="action-icon">🥣</span>
                    먹여주기
                </button>

                <button
                    class="action-button"
                    onclick="playRobot()"
                >
                    <span class="action-icon">🏐</span>
                    놀아주기
                </button>

                <button
                    class="action-button"
                    onclick="exerciseRobot()"
                >
                    <span class="action-icon">🏋️</span>
                    훈련하기
                </button>

                <button
                    class="action-button"
                    onclick="takePhoto()"
                >
                    <span class="action-icon">📷</span>
                    사진첩
                </button>

                <button
                    class="action-button"
                    onclick="completeMission()"
                >
                    <span class="action-icon">🏆</span>
                    미션
                </button>

                <button
                    class="action-button"
                    onclick="openShop()"
                >
                    <span class="action-icon">🛒</span>
                    상점
                </button>
            </div>

            <div class="cards">

                <section class="card">
                    <div class="card-title">
                        배터리 상태
                    </div>

                    <div class="battery-range">
                        15%~90% 사이에서<br>
                        사용하는 것이<br>
                        수명 연장에 가장 좋아요!
                    </div>

                    <div class="battery-pet" id="batteryPet">
                        😵
                    </div>

                    <div class="battery-scale">
                        <div
                            class="battery-pointer"
                            id="batteryPointer"
                        ></div>
                    </div>

                    <div class="scale-labels">
                        <span>0%</span>
                        <span>15%</span>
                        <span>90%</span>
                        <span>100%</span>
                    </div>

                    <div
                        class="battery-message"
                        id="batteryMessage"
                    >
                        배고파서 힘이 없어요...<br>
                        충전해주시면 청소를 더 잘할 수 있어요!
                    </div>
                </section>

                <section class="card time-card">
                    <div class="card-title">
                        예상 청소 가능 시간
                    </div>

                    <div class="time-robot">
                        🤖
                    </div>

                    <div class="time-value">
                        <span id="cleaningTime">10</span>
                        <span class="time-unit">분</span>
                    </div>

                    <div class="time-sub">
                        현재 배터리 기준
                    </div>

                    <div
                        class="time-tip"
                        id="timeTip"
                    >
                        💡 충전 후 더 넓은 공간을<br>
                        청소할 수 있어요!
                    </div>
                </section>

                <section class="card food-card">
                    <div class="food-title">
                        오늘의 음식
                    </div>

                    <div class="food-bowl"></div>

                    <div class="food-count">
                        보유량:
                        <span id="foodCount">1</span>개
                    </div>
                </section>

            </div>

            <div class="home-indicator"></div>
        </main>

        <!-- 팝업 -->
        <div class="modal" id="modal">
            <div class="modal-card">
                <div
                    class="modal-title"
                    id="modalTitle"
                >
                </div>

                <div
                    class="modal-body"
                    id="modalBody"
                >
                </div>

                <button
                    class="modal-close"
                    onclick="closePanel()"
                >
                    확인
                </button>
            </div>
        </div>

        <div class="toast" id="toast"></div>

    </div>
</div>


<script>
    const state = {
        soc: 18,
        temperature: 28,
        heart: 75,
        health: 82,
        level: 12,
        exp: 55,
        coins: 0,
        food: 1,
        missionComplete: false,
        cleaning: false
    };


    function clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    }


    function calculateCleaningTime() {
        return Math.max(
            0,
            Math.round(state.soc * 0.56)
        );
    }


    function render() {
        state.soc = clamp(state.soc, 0, 100);
        state.health = clamp(state.health, 0, 100);
        state.heart = clamp(state.heart, 0, 100);
        state.exp = clamp(state.exp, 0, 100);

        document.getElementById("socTop").innerText =
            state.soc;

        document.getElementById("tempTop").innerText =
            state.temperature;

        document.getElementById("heartTop").innerText =
            state.heart;

        document.getElementById("healthTop").innerText =
            state.health;

        document.getElementById("coinValue").innerText =
            String(state.coins).padStart(3, "0");

        document.getElementById("levelValue").innerText =
            state.level;

        document.getElementById("foodCount").innerText =
            state.food;

        document.getElementById("expFill").style.width =
            state.exp + "%";

        document.getElementById("cleaningTime").innerText =
            calculateCleaningTime();

        document.getElementById("batteryPointer").style.left =
            state.soc + "%";

        const speech =
            document.getElementById("speechBubble");

        const batteryPet =
            document.getElementById("batteryPet");

        const batteryMessage =
            document.getElementById("batteryMessage");

        const timeTip =
            document.getElementById("timeTip");

        const sweat =
            document.getElementById("sweatIcon");


        if (state.cleaning) {
            speech.innerHTML =
                "<strong style='color:#31944b'>열심히 청소 중이에요!</strong><br>조금만 기다려 주세요.";

            batteryPet.innerText = "🧹";
            sweat.innerText = "💨";

            batteryMessage.innerHTML =
                "현재 청소 중이에요.<br>배터리 SOC가 점차 감소합니다.";

            timeTip.innerHTML =
                "🧹 청소가 진행되는 동안<br>예상 시간이 줄어듭니다.";

        } else if (state.soc < 15) {
            speech.innerHTML =
                "<strong>배가 너무 고파요...</strong><br>바로 충전해 주세요!";

            batteryPet.innerText = "🥴";
            sweat.innerText = "💦";

            batteryMessage.innerHTML =
                "배터리가 매우 부족해요.<br>현재 상태에서는 청소를 시작할 수 없어요.";

            timeTip.innerHTML =
                "⚠️ 충전 후 청소를<br>시작해 주세요.";

        } else if (state.soc < 30) {
            speech.innerHTML =
                "<strong>배가 너무 고파요...</strong><br>충전이 필요해요!";

            batteryPet.innerText = "😵";
            sweat.innerText = "💧";

            batteryMessage.innerHTML =
                "배고파서 힘이 없어요...<br>충전해주시면 청소를 더 잘할 수 있어요!";

            timeTip.innerHTML =
                "💡 충전 후 더 넓은 공간을<br>청소할 수 있어요!";

        } else if (state.soc <= 90) {
            speech.innerHTML =
                "<strong style='color:#4b9b40'>배가 든든해요!</strong><br>청소를 준비할게요!";

            batteryPet.innerText = "😊";
            sweat.innerText = "✨";

            batteryMessage.innerHTML =
                "배터리 상태가 좋아요.<br>수명 보호 범위 안에서 사용 중이에요.";

            timeTip.innerHTML =
                "✅ 현재 배터리로 거실 청소가<br>가능합니다.";

        } else {
            speech.innerHTML =
                "<strong style='color:#de8b26'>배가 너무 불러요!</strong><br>충전을 멈춰도 좋아요.";

            batteryPet.innerText = "😮";
            sweat.innerText = "⚡";

            batteryMessage.innerHTML =
                "충전량이 권장 상한을 넘었어요.<br>90% 이하 충전을 권장합니다.";

            timeTip.innerHTML =
                "🔋 충분히 충전되었어요.<br>청소를 시작해 주세요.";
        }

        const missionFill =
            document.getElementById("missionFill");

        missionFill.style.width =
            state.missionComplete ? "100%" : "0%";
    }


    function showToast(message) {
        const toast =
            document.getElementById("toast");

        toast.innerText = message;
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 1800);
    }


    function openPanel(title, body) {
        document.getElementById("modalTitle").innerText =
            title;

        document.getElementById("modalBody").innerHTML =
            body;

        document.getElementById("modal").classList.add(
            "show"
        );
    }


    function closePanel() {
        document.getElementById("modal").classList.remove(
            "show"
        );
    }


    function feedRobot() {
        if (state.food <= 0) {
            showToast("오늘의 음식이 부족해요.");
            return;
        }

        state.food -= 1;
        state.soc += 14;
        state.heart += 5;
        state.exp += 8;

        showToast("맛있게 먹고 SOC가 14% 올랐어요!");
        levelCheck();
        render();
    }


    function playRobot() {
        if (state.soc < 5) {
            showToast("배터리가 부족해서 놀 수 없어요.");
            return;
        }

        state.soc -= 3;
        state.heart += 8;
        state.exp += 5;

        showToast("신나게 놀았어요! 친밀도 +8");
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

        showToast("훈련 완료! 건강도와 경험치가 올랐어요.");
        levelCheck();
        render();
    }


    function takePhoto() {
        showToast("귀여운 사진을 저장했어요! 📷");
    }


    function decorateRobot() {
        openPanel(
            "로봇 꾸미기",
            "현재 장착 아이템은 <b>황금 왕관</b>입니다.<br><br>" +
            "상점에서 리본, 모자, 표정 스킨 등을 구매할 수 있도록 확장할 수 있습니다."
        );
    }


    function completeMission() {
        if (state.missionComplete) {
            showToast("오늘의 미션을 이미 완료했어요.");
            return;
        }

        if (state.soc < 15) {
            showToast("미션을 시작하려면 충전이 필요해요.");
            return;
        }

        startCleaning();
    }


    function startCleaning() {
        if (state.cleaning) {
            showToast("이미 청소 중이에요.");
            return;
        }

        if (state.soc < 15) {
            showToast("SOC가 부족합니다. 먼저 충전해 주세요.");
            return;
        }

        state.cleaning = true;
        render();
        showToast("거실 청소를 시작합니다!");

        let cleanStep = 0;

        const cleaningTimer = setInterval(() => {
            cleanStep += 1;
            state.soc -= 2;
            state.temperature =
                Math.min(36, state.temperature + 1);

            render();

            if (cleanStep >= 6 || state.soc <= 10) {
                clearInterval(cleaningTimer);

                state.cleaning = false;
                state.temperature = 29;
                state.missionComplete = true;
                state.coins += 50;
                state.exp += 20;

                levelCheck();
                render();

                openPanel(
                    "청소 완료!",
                    "거실 청소를 완료했습니다.<br><br>" +
                    "미션 보상으로 <b>50 코인</b>과 경험치 20을 획득했습니다."
                );
            }
        }, 700);
    }


    function chargeRobot() {
        if (state.soc >= 90) {
            showToast("이미 권장 충전 범위에 도달했어요.");
            return;
        }

        showToast("스마트 충전을 시작합니다.");

        const chargeTimer = setInterval(() => {
            state.soc += 4;

            if (state.soc >= 90) {
                state.soc = 90;
                clearInterval(chargeTimer);

                showToast(
                    "배터리 보호를 위해 90%에서 충전을 멈췄어요."
                );
            }

            render();
        }, 180);
    }


    function openBatteryPanel() {
        openPanel(
            "배터리 상태",
            "현재 SOC는 <b>" + state.soc + "%</b>입니다.<br>" +
            "배터리 건강도는 <b>" + state.health + "%</b>이며, " +
            "예상 청소 가능 시간은 <b>" +
            calculateCleaningTime() +
            "분</b>입니다.<br><br>" +
            "배터리 수명 보호를 위해 15~90% 범위 사용을 권장합니다."
        );
    }


    function openShop() {
        openPanel(
            "로봇 상점",
            "보유 코인: <b>" + state.coins + "개</b><br><br>" +
            "🎀 리본 80코인<br>" +
            "🧢 탐험가 모자 120코인<br>" +
            "🍖 고급 배터리 음식 50코인<br>" +
            "✨ 반짝이 효과 150코인"
        );
    }


    function levelCheck() {
        if (state.exp >= 100) {
            state.exp -= 100;
            state.level += 1;

            showToast(
                "레벨 업! Lv." + state.level + "이 되었어요."
            );
        }
    }


    render();
</script>

</body>
</html>
"""


components.html(
    mobile_ui,
    height=930,
    scrolling=False,
)
