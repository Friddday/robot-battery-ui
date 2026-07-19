import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="LG ROBO CARE",
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
        [data-testid="stSidebar"] {
            display: none !important;
        }

        #MainMenu,
        footer {
            visibility: hidden !important;
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 12%, #fff8e9 0%, transparent 31%),
                radial-gradient(circle at 88% 87%, #ecd3a9 0%, transparent 28%),
                #eee5d8;
        }

        .block-container {
            max-width: 100%;
            padding: 8px 4px 18px;
        }

        iframe {
            border: none !important;
            border-radius: 28px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


app_html = r"""
<!DOCTYPE html>
<html lang="ko">

<head>
<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<style>
    * {
        box-sizing: border-box;
        -webkit-tap-highlight-color: transparent;
    }

    :root {
        --brown: #4b3324;
        --brown-2: #74523b;

        --cream: #fff7e5;
        --cream-2: #f6e4bf;

        --orange: #ff9635;
        --orange-deep: #ef6540;

        --green: #65a946;
        --green-deep: #388b3f;

        --red: #ef4e45;
        --yellow: #ffd44f;

        --shadow:
            0 8px 18px rgba(74, 45, 21, 0.15);
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

    button,
    input {
        font-family: inherit;
    }

    button {
        cursor: pointer;
    }

    .phone {
        position: relative;

        width: min(100%, 420px);
        height: 900px;

        overflow: hidden;

        border: 8px solid #242321;
        border-radius: 40px;

        background: #e0b56c;

        box-shadow:
            0 30px 80px rgba(51, 33, 18, 0.28),
            0 8px 20px rgba(51, 33, 18, 0.16);
    }

    .notch {
        position: absolute;
        z-index: 100;

        top: 0;
        left: 50%;

        width: 126px;
        height: 25px;

        transform: translateX(-50%);

        border-radius: 0 0 18px 18px;

        background: #242321;
    }

    .screen {
        position: relative;

        width: 100%;
        height: 100%;

        overflow: hidden;

        background:
            linear-gradient(
                180deg,
                #d1aa79 0%,
                #e8c793 44%,
                #e1b36c 100%
            );
    }

    /* ==================================================
       공통 상단 헤더
    ================================================== */

    .app-header {
        position: relative;
        z-index: 50;

        height: 128px;

        padding:
            23px
            14px
            8px;

        color: #fff;

        background:
            linear-gradient(
                120deg,
                #2d2722,
                #5d402c
            );

        box-shadow:
            0 7px 16px rgba(48, 31, 19, 0.22);
    }

    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .brand-small {
        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1.4px;
    }

    .app-title {
        margin-top: 3px;

        font-size: 23px;
        font-weight: 900;
    }

    .coin-pill {
        display: flex;
        align-items: center;
        gap: 5px;

        padding: 8px 12px;

        border:
            1px solid rgba(255, 255, 255, 0.17);
        border-radius: 18px;

        background:
            rgba(255, 255, 255, 0.13);

        font-size: 12px;
        font-weight: 900;
    }

    .top-navigation {
        display: grid;
        grid-template-columns: repeat(4, 1fr);

        gap: 7px;

        margin-top: 12px;
    }

    .nav-button {
        padding: 8px 3px;

        border: 0;
        border-radius: 14px;

        background: transparent;
        color: rgba(255, 255, 255, 0.74);

        font-size: 10px;
        font-weight: 900;

        transition:
            background 0.2s ease,
            color 0.2s ease,
            transform 0.2s ease;
    }

    .nav-button.active {
        background: #4c291c;
        color: #fff;

        box-shadow:
            0 4px 9px rgba(0, 0, 0, 0.18);
    }

    .nav-button:active {
        transform: scale(0.94);
    }

    /* ==================================================
       페이지 구조
    ================================================== */

    .page-container {
        position: relative;

        height: calc(100% - 128px);

        overflow: hidden;
    }

    .page {
        position: absolute;

        inset: 0;

        display: none;

        overflow-y: auto;

        padding: 12px 10px 22px;

        animation:
            pageEnter 0.28s ease-out;
    }

    .page.active {
        display: block;
    }

    .page::-webkit-scrollbar {
        width: 0;
    }

    @keyframes pageEnter {
        from {
            opacity: 0;
            transform: translateX(18px);
        }

        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .section-label {
        margin-bottom: 2px;

        color: #76533b;

        font-size: 9px;
        font-weight: 900;
        letter-spacing: 1.3px;
    }

    .section-title {
        margin-bottom: 11px;

        font-size: 22px;
        font-weight: 900;
    }

    .panel {
        border:
            1px solid rgba(136, 87, 40, 0.14);
        border-radius: 17px;

        background:
            rgba(255, 248, 231, 0.96);

        box-shadow: var(--shadow);
    }

    /* ==================================================
       홈 화면
    ================================================== */

    #homePage {
        padding: 0;

        background:
            linear-gradient(
                180deg,
                #cfaa7d 0%,
                #e0c39a 39%,
                #d29c58 40%,
                #d09850 100%
            );
    }

    .home-room {
        position: relative;

        height: 355px;

        overflow: hidden;
    }

    .wall-light {
        position: absolute;

        top: -80px;
        left: 50%;

        width: 420px;
        height: 280px;

        transform: translateX(-50%);

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(255, 248, 226, 0.88),
                rgba(255, 240, 205, 0.18) 60%,
                transparent 74%
            );
    }

    .home-floor {
        position: absolute;

        left: 0;
        right: 0;
        bottom: 0;

        height: 170px;

        background:
            repeating-linear-gradient(
                90deg,
                rgba(106, 63, 26, 0.10) 0,
                rgba(106, 63, 26, 0.10) 2px,
                transparent 2px,
                transparent 66px
            ),
            repeating-linear-gradient(
                0deg,
                transparent 0,
                transparent 38px,
                rgba(106, 63, 26, 0.09) 39px,
                rgba(106, 63, 26, 0.09) 41px
            ),
            linear-gradient(
                180deg,
                #d9b174,
                #c78e48
            );
    }

    .plant {
        position: absolute;
        z-index: 3;

        left: 14px;
        top: 71px;

        font-size: 74px;

        filter:
            drop-shadow(
                0 7px 5px rgba(68, 41, 21, 0.18)
            );
    }

    .robot-house {
        position: absolute;
        z-index: 3;

        left: 88px;
        top: 128px;

        width: 68px;
        height: 58px;

        border-radius:
            29px 29px 7px 7px;

        background:
            linear-gradient(
                145deg,
                #a38b71,
                #74614d
            );

        box-shadow:
            0 6px 11px rgba(54, 36, 23, 0.22);
    }

    .robot-house::before {
        content: "";

        position: absolute;

        left: 19px;
        bottom: 0;

        width: 31px;
        height: 32px;

        border-radius:
            16px 16px 0 0;

        background: #403b35;
    }

    .robot-house::after {
        content: "HOME";

        position: absolute;

        top: 11px;
        left: 16px;

        color:
            rgba(255, 255, 255, 0.56);

        font-size: 7px;
        font-weight: 900;
    }

    .sofa {
        position: absolute;
        z-index: 2;

        right: -8px;
        top: 72px;

        width: 139px;
        height: 105px;

        border-radius:
            28px 0 8px 8px;

        background:
            linear-gradient(
                145deg,
                #71847f,
                #354e4a
            );

        box-shadow:
            0 10px 14px rgba(54, 37, 23, 0.27);
    }

    .sofa::before {
        content: "";

        position: absolute;

        top: -18px;
        left: 10px;

        width: 80px;
        height: 48px;

        border-radius:
            17px 17px 7px 7px;

        background: #74867f;
    }

    .speech {
        position: absolute;
        z-index: 20;

        top: 17px;
        left: 50%;

        width: 177px;
        min-height: 74px;

        padding: 14px 12px;

        transform: translateX(-50%);

        border-radius: 14px;

        background:
            rgba(255, 255, 255, 0.98);

        box-shadow:
            0 7px 16px rgba(58, 37, 21, 0.18);

        text-align: center;

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

        border-width:
            16px 10px 0 4px;

        border-style: solid;

        border-color:
            white
            transparent
            transparent
            transparent;
    }

    .mode-chip {
        position: absolute;
        z-index: 18;

        top: 106px;
        left: 50%;

        padding: 7px 13px;

        transform: translateX(-50%);

        border-radius: 18px;

        background:
            rgba(255, 248, 229, 0.95);

        box-shadow:
            0 4px 10px rgba(72, 46, 23, 0.16);

        font-size: 9px;
        font-weight: 900;
    }

    .rug {
        position: absolute;
        z-index: 4;

        left: 50%;
        bottom: 12px;

        width: 255px;
        height: 92px;

        transform: translateX(-50%);

        border-radius: 50%;

        background:
            radial-gradient(
                ellipse,
                rgba(241, 224, 197, 0.91),
                rgba(191, 151, 103, 0.79)
            );

        box-shadow:
            inset 0 0 18px rgba(103, 70, 43, 0.14);
    }

    .clean-path {
        position: absolute;
        z-index: 5;

        left: 50%;
        bottom: 41px;

        width: 292px;
        height: 78px;

        transform: translateX(-50%);

        overflow: hidden;

        border:
            2px dashed rgba(255, 255, 255, 0.36);
        border-radius: 50%;

        opacity: 0;
    }

    .clean-path-fill {
        width: 0%;
        height: 100%;

        border-radius: inherit;

        background:
            linear-gradient(
                90deg,
                rgba(95, 177, 105, 0.08),
                rgba(102, 200, 115, 0.51)
            );

        transition: width 0.32s ease;
    }

    .charge-ring {
        position: absolute;
        z-index: 7;

        left: 50%;
        bottom: 19px;

        width: 216px;
        height: 132px;

        transform: translateX(-50%);

        border: 5px solid transparent;
        border-top-color: #ffd345;
        border-right-color: #ff9931;
        border-radius: 50%;

        opacity: 0;
    }

    .dust-layer {
        position: absolute;
        z-index: 8;

        left: 50%;
        bottom: 55px;

        width: 267px;
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

        background:
            rgba(116, 78, 42, 0.50);

        opacity: 0;
    }

    .dust-layer span:nth-child(1) {
        left: 8%;
        animation-delay: 0s;
    }

    .dust-layer span:nth-child(2) {
        left: 21%;
        animation-delay: 0.32s;
    }

    .dust-layer span:nth-child(3) {
        left: 37%;
        animation-delay: 0.68s;
    }

    .dust-layer span:nth-child(4) {
        right: 8%;
        animation-delay: 0.18s;
    }

    .dust-layer span:nth-child(5) {
        right: 23%;
        animation-delay: 0.52s;
    }

    .dust-layer span:nth-child(6) {
        right: 39%;
        animation-delay: 0.88s;
    }

    .robot {
        position: absolute;
        z-index: 10;

        left: 50%;
        bottom: 31px;

        width: 181px;
        height: 99px;

        transform:
            translateX(-50%);

        transform-origin:
            center bottom;

        border:
            2px solid #a29b92;

        border-radius:
            62% 62% 40% 40%;

        background:
            linear-gradient(
                180deg,
                #fffefb 0%,
                #e7e8e3 70%,
                #bbbdb7 100%
            );

        box-shadow:
            0 13px 19px rgba(55, 37, 21, 0.32),
            inset 0 -8px 12px rgba(83, 83, 79, 0.12);

        cursor: pointer;

        animation:
            robotIdle 2.8s ease-in-out infinite;
    }

    .robot-top {
        position: absolute;

        left: 50%;
        top: -5px;

        width: 126px;
        height: 58px;

        transform: translateX(-50%);

        border-top:
            2px solid rgba(119, 119, 114, 0.42);

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

        border-radius:
            26px 26px 30px 30px;

        background:
            linear-gradient(
                180deg,
                #2a2c2d,
                #101213 76%
            );

        box-shadow:
            inset 0 4px 5px rgba(255, 255, 255, 0.13);
    }

    .eye {
        position: absolute;

        top: 14px;

        width: 22px;
        height: 22px;

        border:
            2px solid #f2f0dc;

        border-radius: 50%;

        background: #111;

        transform-origin: center;

        animation:
            eyeBlink 4.8s infinite;
    }

    .eye::after {
        content: "";

        position: absolute;

        top: 4px;
        left: 5px;

        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: white;

        transition:
            transform 0.25s ease;
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

    .mouth {
        position: absolute;

        left: 50%;
        bottom: 8px;

        width: 20px;
        height: 11px;

        transform: translateX(-50%);

        border:
            2px solid #f3d6c9;

        border-top: 0;

        border-radius:
            0 0 12px 12px;
    }

    .crown {
        position: absolute;
        z-index: 12;

        left: 50%;
        top: -40px;

        transform: translateX(-50%);

        font-size: 46px;

        filter:
            drop-shadow(
                0 4px 3px rgba(81, 52, 17, 0.25)
            );
    }

    .spark {
        position: absolute;
        z-index: 11;

        right: -16px;
        top: -9px;

        font-size: 28px;

        animation:
            sparkle 1.3s ease-in-out infinite;
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

        animation:
            effectFly 1.2s ease-out forwards;
    }

    .home-room.is-cleaning .mode-chip {
        color: white;
        background:
            rgba(57, 143, 82, 0.93);
    }

    .home-room.is-cleaning .clean-path {
        opacity: 1;
    }

    .home-room.is-cleaning .dust-layer span {
        animation:
            dustRise 1.35s ease-out infinite;
    }

    .home-room.is-cleaning .robot {
        animation:
            robotPatrol 2.4s ease-in-out infinite;
    }

    .home-room.is-charging .mode-chip {
        color: white;
        background:
            rgba(242, 145, 35, 0.94);
    }

    .home-room.is-charging .charge-ring {
        opacity: 0.92;

        animation:
            chargeRingSpin 1.05s linear infinite;
    }

    .home-room.is-charging .robot {
        animation:
            robotCharging 0.85s ease-in-out infinite;
    }

    .home-room.is-low .robot {
        animation:
            robotLowPower 0.48s linear infinite;
    }

    .home-room.is-celebrating .robot {
        animation:
            robotCelebrate 0.72s ease-in-out 3;
    }

    .robot.tap-motion {
        animation:
            robotTap 0.62s ease-out !important;
    }

    .mission-mini {
        position: absolute;
        z-index: 16;

        left: 8px;
        bottom: 14px;

        width: 90px;

        padding: 9px 7px;

        border-radius: 14px;

        background:
            rgba(255, 248, 230, 0.97);

        box-shadow:
            0 4px 10px rgba(61, 39, 20, 0.22);
    }

    .mission-title {
        font-size: 10px;
        font-weight: 900;
    }

    .mission-text {
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

        background:
            linear-gradient(
                90deg,
                #ff8e33,
                #ffca43
            );

        transition:
            width 0.32s ease;
    }

    .reward {
        color: #8d5814;

        white-space: nowrap;

        font-size: 9px;
        font-weight: 900;
    }

    .quick-right {
        position: absolute;
        z-index: 17;

        right: 7px;
        top: 89px;

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

        background:
            rgba(255, 248, 231, 0.97);

        box-shadow:
            0 4px 10px rgba(61, 39, 20, 0.22);

        color: var(--brown);

        font-size: 8px;
        font-weight: 900;
    }

    .quick-button .icon {
        display: block;

        margin-bottom: 3px;

        font-size: 21px;
    }

    .home-dashboard {
        padding: 9px 8px 15px;

        background:
            linear-gradient(
                180deg,
                rgba(239, 205, 151, 0.99),
                rgba(227, 181, 110, 0.99)
            );
    }

    .action-menu {
        display: grid;
        grid-template-columns: repeat(6, 1fr);

        gap: 4px;

        margin-bottom: 8px;
        padding: 8px 5px;

        border:
            1px solid rgba(138, 91, 40, 0.18);

        border-radius: 14px;

        background:
            rgba(255, 247, 224, 0.94);

        box-shadow:
            0 4px 9px rgba(87, 54, 25, 0.15);
    }

    .action-button {
        min-width: 0;

        padding: 3px 0;

        border: 0;

        background: transparent;
        color: var(--brown);

        font-size: 8px;
        font-weight: 900;
    }

    .action-icon {
        display: block;

        margin-bottom: 4px;

        font-size: 23px;
    }

    .home-cards {
        display: grid;
        grid-template-columns:
            1.16fr 1fr 0.78fr;

        gap: 6px;
    }

    .mini-card {
        min-height: 186px;

        padding: 11px 9px;

        border:
            1px solid rgba(139, 92, 39, 0.17);
        border-radius: 14px;

        background:
            rgba(255, 248, 230, 0.97);

        box-shadow:
            0 4px 10px rgba(79, 48, 21, 0.12);
    }

    .mini-title {
        margin-bottom: 8px;

        font-size: 10px;
        font-weight: 900;
    }

    .battery-info {
        font-size: 9px;
        line-height: 1.55;
        font-weight: 800;
    }

    .battery-face {
        margin: 7px 0 5px;

        text-align: center;

        font-size: 31px;
    }

    .battery-scale {
        position: relative;

        height: 7px;

        margin: 18px 7px 14px;

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

        border:
            3px solid white;
        border-radius: 50%;

        background: #e64c39;

        box-shadow:
            0 2px 5px rgba(0, 0, 0, 0.23);

        transition: left 0.3s ease;
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

    .time-icon {
        margin-top: 10px;

        font-size: 31px;

        animation:
            smallFloat 2s ease-in-out infinite;
    }

    .time-number {
        color: #ef573f;

        font-size: 32px;
        line-height: 1;
        font-weight: 900;
    }

    .time-number small {
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

        border-radius:
            6px 6px 25px 25px;

        background:
            linear-gradient(
                180deg,
                #d84849,
                #ad2e36
            );

        box-shadow:
            0 7px 8px rgba(81, 37, 25, 0.2),
            inset 0 -7px 8px rgba(83, 12, 22, 0.14);
    }

    .food-bowl::before {
        content: "";

        position: absolute;

        left: 4px;
        top: -9px;

        width: 56px;
        height: 19px;

        border:
            4px solid #d54749;
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

    /* ==================================================
       배터리 화면
    ================================================== */

    .battery-summary {
        display: grid;
        grid-template-columns: 1fr 1fr;

        gap: 8px;
    }

    .gauge-card {
        padding: 14px 10px;

        text-align: center;
    }

    .gauge {
        --value: 81;
        --gauge-color: #4ba846;

        position: relative;

        width: 118px;
        height: 118px;

        margin: 0 auto 8px;

        display: grid;
        place-items: center;

        border-radius: 50%;

        background:
            conic-gradient(
                var(--gauge-color)
                calc(var(--value) * 1%),
                #ead9b9 0
            );

        transition:
            background 0.3s ease;
    }

    .gauge::before {
        content: "";

        position: absolute;

        width: 82px;
        height: 82px;

        border-radius: 50%;

        background: #fff4d8;
    }

    .gauge-content {
        position: relative;
        z-index: 2;

        font-weight: 900;
    }

    .gauge-label {
        font-size: 10px;
    }

    .gauge-value {
        margin-top: 2px;

        font-size: 24px;
    }

    .gauge-description {
        font-size: 9px;
        line-height: 1.5;
        font-weight: 800;
    }

    .control-panel {
        margin-top: 9px;
        padding: 15px 14px;
    }

    .control-row {
        margin-bottom: 17px;
    }

    .control-row:last-child {
        margin-bottom: 0;
    }

    .control-heading {
        display: flex;
        justify-content: space-between;
        align-items: center;

        margin-bottom: 8px;

        font-size: 11px;
        font-weight: 900;
    }

    .control-value {
        color: var(--green-deep);
    }

    input[type="range"] {
        width: 100%;

        accent-color: var(--green-deep);
    }

    .control-caption {
        display: flex;
        justify-content: space-between;

        margin-top: 4px;

        color: #806047;

        font-size: 8px;
        font-weight: 800;
    }

    .charge-action {
        width: 100%;

        margin-top: 12px;
        padding: 12px;

        border: 0;
        border-radius: 13px;

        background:
            linear-gradient(
                90deg,
                #4a9b42,
                #75b84e
            );

        color: white;

        font-size: 12px;
        font-weight: 900;

        box-shadow:
            0 5px 12px rgba(63, 132, 57, 0.23);
    }

    .chart-panel {
        margin-top: 9px;
        padding: 15px 14px;
    }

    .panel-heading {
        display: flex;
        justify-content: space-between;
        align-items: center;

        margin-bottom: 8px;
    }

    .panel-title {
        font-size: 13px;
        font-weight: 900;
    }

    .panel-badge {
        padding: 5px 8px;

        border-radius: 12px;

        background: #fff0ce;
        color: #805c35;

        font-size: 8px;
        font-weight: 900;
    }

    .soc-chart {
        width: 100%;
        height: 167px;

        overflow: visible;
    }

    .chart-grid {
        stroke: #d7c6a8;
        stroke-width: 1;
        stroke-dasharray: 4 5;
    }

    .chart-red {
        fill: none;
        stroke: #eb6650;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .chart-green {
        fill: none;
        stroke: #4c9a43;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .chart-label {
        fill: #856347;

        font-size: 9px;
        font-weight: 800;
    }

    .chart-legend {
        display: flex;
        gap: 13px;

        margin-top: 2px;

        font-size: 9px;
        font-weight: 900;
    }

    .legend-dot {
        display: inline-block;

        width: 9px;
        height: 9px;

        margin-right: 4px;

        border-radius: 50%;
    }

    .battery-insight {
        margin-top: 9px;
        padding: 14px;
    }

    .insight-line {
        display: flex;
        align-items: flex-start;

        gap: 9px;

        font-size: 10px;
        line-height: 1.6;
        font-weight: 800;
    }

    .insight-icon {
        font-size: 20px;
    }

    /* ==================================================
       기록 화면
    ================================================== */

    .weekly-panel {
        padding: 15px 14px;
    }

    .weekly-average {
        font-size: 10px;
        font-weight: 900;
    }

    .bar-chart {
        height: 190px;

        display: flex;
        align-items: flex-end;
        justify-content: space-between;

        gap: 8px;

        padding: 17px 5px 0;
    }

    .bar-item {
        flex: 1;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;

        height: 100%;
    }

    .bar {
        width: 100%;
        max-width: 32px;

        border-radius:
            12px 12px 5px 5px;

        background:
            linear-gradient(
                180deg,
                #66b449,
                #138b35
            );

        box-shadow:
            inset 0 -7px 8px rgba(0, 74, 25, 0.10);

        transform-origin: bottom;

        animation:
            barGrow 0.65s ease-out;
    }

    .bar-value {
        margin-bottom: 4px;

        color: #426d32;

        font-size: 8px;
        font-weight: 900;
    }

    .bar-label {
        margin-top: 5px;

        font-size: 9px;
        font-weight: 900;
    }

    .record-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;

        gap: 8px;

        margin-top: 9px;
    }

    .record-card {
        min-height: 90px;

        padding: 14px;

        border:
            1px solid rgba(136, 87, 40, 0.14);
        border-radius: 16px;

        background:
            rgba(255, 248, 231, 0.96);

        box-shadow: var(--shadow);
    }

    .record-label {
        color: #6e503a;

        font-size: 9px;
        font-weight: 900;
    }

    .record-value {
        margin-top: 7px;

        color: #31241b;

        font-size: 23px;
        font-weight: 900;
    }

    .event-panel {
        margin-top: 9px;
        padding: 15px 14px;
    }

    .event-list {
        margin-top: 10px;
    }

    .event-item {
        display: grid;
        grid-template-columns: 43px 1fr;

        gap: 8px;

        padding: 11px 0;

        border-bottom:
            1px solid rgba(122, 87, 51, 0.12);
    }

    .event-item:last-child {
        border-bottom: 0;
    }

    .event-time {
        color: #946c43;

        font-size: 9px;
        font-weight: 900;
    }

    .event-content strong {
        display: block;

        margin-bottom: 3px;

        font-size: 10px;
    }

    .event-content span {
        color: #785a43;

        font-size: 9px;
        line-height: 1.4;
        font-weight: 700;
    }

    /* ==================================================
       리워드 화면
    ================================================== */

    .level-panel {
        padding: 17px 15px;

        text-align: center;

        background:
            linear-gradient(
                145deg,
                #fff3cc,
                #ffd98a
            );
    }

    .level-robot {
        font-size: 72px;

        animation:
            smallFloat 2s ease-in-out infinite;
    }

    .level-number {
        margin-top: 5px;

        font-size: 25px;
        font-weight: 900;
    }

    .level-progress {
        height: 11px;

        margin: 12px 10px 5px;

        overflow: hidden;

        border-radius: 10px;

        background:
            rgba(126, 85, 39, 0.18);
    }

    .level-progress-fill {
        width: 55%;
        height: 100%;

        border-radius: inherit;

        background:
            linear-gradient(
                90deg,
                #ff7f35,
                #ffd244
            );
    }

    .level-caption {
        font-size: 9px;
        font-weight: 900;
    }

    .reward-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;

        gap: 8px;

        margin-top: 9px;
    }

    .reward-card {
        min-height: 125px;

        padding: 14px;

        border:
            1px solid rgba(136, 87, 40, 0.14);
        border-radius: 16px;

        background:
            rgba(255, 248, 231, 0.97);

        box-shadow: var(--shadow);

        text-align: center;
    }

    .reward-icon {
        font-size: 38px;
    }

    .reward-title {
        margin-top: 7px;

        font-size: 11px;
        font-weight: 900;
    }

    .reward-description {
        margin-top: 4px;

        color: #775943;

        font-size: 8px;
        line-height: 1.4;
        font-weight: 800;
    }

    .reward-button {
        width: 100%;

        margin-top: 9px;
        padding: 8px;

        border: 0;
        border-radius: 10px;

        background: #f0dfbc;
        color: #5c422f;

        font-size: 9px;
        font-weight: 900;
    }

    /* ==================================================
       팝업과 토스트
    ================================================== */

    .modal {
        position: absolute;
        z-index: 200;

        inset: 0;

        display: none;
        align-items: center;
        justify-content: center;

        padding: 30px;

        background:
            rgba(45, 33, 23, 0.62);

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

        box-shadow:
            0 18px 45px rgba(28, 19, 12, 0.38);

        animation:
            popup 0.18s ease-out;
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
    }

    .modal-close {
        width: 100%;

        padding: 11px;

        border: 0;
        border-radius: 12px;

        background: #ef8c32;
        color: white;

        font-weight: 900;
    }

    .toast {
        position: absolute;
        z-index: 220;

        left: 50%;
        bottom: 25px;

        width: max-content;
        max-width: 84%;

        padding: 11px 17px;

        transform:
            translateX(-50%)
            translateY(30px);

        border-radius: 18px;

        background:
            rgba(44, 37, 31, 0.95);

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

    /* ==================================================
       애니메이션
    ================================================== */

    @keyframes robotIdle {
        0%,
        100% {
            transform:
                translateX(-50%)
                translateY(0)
                rotate(-1deg);
        }

        50% {
            transform:
                translateX(-50%)
                translateY(-7px)
                rotate(1deg);
        }
    }

    @keyframes robotPatrol {
        0% {
            transform:
                translateX(calc(-50% - 67px))
                rotate(-4deg);
        }

        50% {
            transform:
                translateX(calc(-50% + 67px))
                rotate(4deg);
        }

        100% {
            transform:
                translateX(calc(-50% - 67px))
                rotate(-4deg);
        }
    }

    @keyframes robotCharging {
        0%,
        100% {
            transform:
                translateX(-50%)
                scale(1);
        }

        50% {
            transform:
                translateX(-50%)
                translateY(-4px)
                scale(1.04);
        }
    }

    @keyframes robotLowPower {
        0% {
            transform:
                translateX(-50%)
                translateX(-2px);
        }

        50% {
            transform:
                translateX(-50%)
                translateX(2px);
        }

        100% {
            transform:
                translateX(-50%)
                translateX(-2px);
        }
    }

    @keyframes robotCelebrate {
        0%,
        100% {
            transform:
                translateX(-50%)
                translateY(0);
        }

        50% {
            transform:
                translateX(-50%)
                translateY(-35px)
                rotate(-5deg);
        }

        75% {
            transform:
                translateX(-50%)
                translateY(-7px)
                rotate(5deg);
        }
    }

    @keyframes robotTap {
        0%,
        100% {
            transform:
                translateX(-50%)
                scale(1);
        }

        45% {
            transform:
                translateX(-50%)
                scale(0.92, 1.08);
        }

        70% {
            transform:
                translateX(-50%)
                scale(1.08, 0.94);
        }
    }

    @keyframes eyeBlink {
        0%,
        45%,
        49%,
        100% {
            transform: scaleY(1);
        }

        47% {
            transform: scaleY(0.08);
        }
    }

    @keyframes sparkle {
        0%,
        100% {
            transform:
                scale(0.85)
                rotate(-10deg);

            opacity: 0.55;
        }

        50% {
            transform:
                scale(1.18)
                rotate(8deg);

            opacity: 1;
        }
    }

    @keyframes chargeRingSpin {
        from {
            transform:
                translateX(-50%)
                rotate(0deg);
        }

        to {
            transform:
                translateX(-50%)
                rotate(360deg);
        }
    }

    @keyframes dustRise {
        0% {
            transform:
                translateY(0)
                scale(0.6);

            opacity: 0;
        }

        25% {
            opacity: 0.65;
        }

        100% {
            transform:
                translateY(-45px)
                translateX(15px)
                scale(1.25);

            opacity: 0;
        }
    }

    @keyframes effectFly {
        0% {
            transform:
                translate(0, 0)
                scale(0.7);

            opacity: 0;
        }

        20% {
            opacity: 1;
        }

        100% {
            transform:
                translate(
                    var(--move-x),
                    -125px
                )
                scale(1.35)
                rotate(var(--rotate));

            opacity: 0;
        }
    }

    @keyframes smallFloat {
        0%,
        100% {
            transform: translateY(0);
        }

        50% {
            transform: translateY(-5px);
        }
    }

    @keyframes barGrow {
        from {
            transform: scaleY(0);
        }

        to {
            transform: scaleY(1);
        }
    }

    @keyframes popup {
        from {
            opacity: 0;
            transform: scale(0.88);
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
            height: 100vh;

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

        <header class="app-header">

            <div class="header-top">

                <div>
                    <div class="brand-small">
                        LG ROBO CARE
                    </div>

                    <div class="app-title">
                        몽글이 키우기
                    </div>
                </div>

                <div class="coin-pill">
                    🪙
                    <span id="globalCoin">
                        050
                    </span>
                </div>

            </div>

            <nav class="top-navigation">

                <button
                    class="nav-button active"
                    data-page="homePage"
                    onclick="switchPage('homePage', this)"
                >
                    홈
                </button>

                <button
                    class="nav-button"
                    data-page="batteryPage"
                    onclick="switchPage('batteryPage', this)"
                >
                    배터리
                </button>

                <button
                    class="nav-button"
                    data-page="recordPage"
                    onclick="switchPage('recordPage', this)"
                >
                    기록
                </button>

                <button
                    class="nav-button"
                    data-page="rewardPage"
                    onclick="switchPage('rewardPage', this)"
                >
                    리워드
                </button>

            </nav>

        </header>


        <div class="page-container">

            <!-- ========================================
                 홈 화면
            ========================================= -->

            <section
                class="page active"
                id="homePage"
            >

                <div
                    class="home-room"
                    id="homeRoom"
                >

                    <div class="wall-light"></div>
                    <div class="home-floor"></div>

                    <div class="plant">
                        🪴
                    </div>

                    <div class="robot-house"></div>
                    <div class="sofa"></div>

                    <div
                        class="speech"
                        id="speechBubble"
                    >
                        <strong>배가 든든해요!</strong>
                        <br>
                        청소를 준비할게요!
                    </div>

                    <div
                        class="mode-chip"
                        id="modeChip"
                    >
                        ✨ AI 권장 SOC 81%
                    </div>

                    <div class="rug"></div>

                    <div class="clean-path">
                        <div
                            class="clean-path-fill"
                            id="cleanPathFill"
                        ></div>
                    </div>

                    <div class="charge-ring"></div>

                    <div class="dust-layer">
                        <span></span>
                        <span></span>
                        <span></span>
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>

                    <div
                        class="robot"
                        id="robotCharacter"
                        onclick="petRobot()"
                    >

                        <div class="crown">
                            👑
                        </div>

                        <div
                            class="spark"
                            id="sparkIcon"
                        >
                            ✨
                        </div>

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

                        <div class="mission-title">
                            오늘의 미션
                        </div>

                        <div class="mission-text">
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
                                +50
                            </span>

                        </div>

                    </div>

                    <div class="quick-right">

                        <button
                            class="quick-button"
                            onclick="openBatterySummary()"
                        >
                            <span class="icon">
                                💖
                            </span>

                            상태보기
                        </button>

                        <button
                            class="quick-button"
                            onclick="chargeRobot()"
                        >
                            <span class="icon">
                                🔋
                            </span>

                            배터리 관리
                        </button>

                        <button
                            class="quick-button"
                            onclick="goToRecordPage()"
                        >
                            <span class="icon">
                                📋
                            </span>

                            청소 기록
                        </button>

                        <button
                            class="quick-button"
                            onclick="decorateRobot()"
                        >
                            <span class="icon">
                                🎩
                            </span>

                            꾸미기
                        </button>

                    </div>

                    <div
                        class="effect-layer"
                        id="effectLayer"
                    ></div>

                </div>


                <div class="home-dashboard">

                    <div class="action-menu">

                        <button
                            class="action-button"
                            onclick="feedRobot()"
                        >
                            <span class="action-icon">
                                🥣
                            </span>

                            먹여주기
                        </button>

                        <button
                            class="action-button"
                            onclick="playRobot()"
                        >
                            <span class="action-icon">
                                🏐
                            </span>

                            놀아주기
                        </button>

                        <button
                            class="action-button"
                            onclick="exerciseRobot()"
                        >
                            <span class="action-icon">
                                🏋️
                            </span>

                            훈련하기
                        </button>

                        <button
                            class="action-button"
                            onclick="takePhoto()"
                        >
                            <span class="action-icon">
                                📷
                            </span>

                            사진첩
                        </button>

                        <button
                            class="action-button"
                            onclick="startCleaning()"
                        >
                            <span class="action-icon">
                                🏆
                            </span>

                            미션
                        </button>

                        <button
                            class="action-button"
                            onclick="openShop()"
                        >
                            <span class="action-icon">
                                🛒
                            </span>

                            상점
                        </button>

                    </div>


                    <div class="home-cards">

                        <section class="mini-card">

                            <div class="mini-title">
                                배터리 상태
                            </div>

                            <div class="battery-info">
                                15%~90% 사이에서
                                <br>
                                사용하는 것이
                                <br>
                                수명 연장에 좋아요!
                            </div>

                            <div
                                class="battery-face"
                                id="batteryFace"
                            >
                                😊
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
                                배터리 상태가 좋아요.
                            </div>

                        </section>


                        <section class="mini-card time-card">

                            <div class="mini-title">
                                예상 청소 가능 시간
                            </div>

                            <div class="time-icon">
                                🤖
                            </div>

                            <div class="time-number">

                                <span id="homeCleaningTime">
                                    45
                                </span>

                                <small>
                                    분
                                </small>

                            </div>

                            <div class="time-sub">
                                현재 배터리 기준
                            </div>

                            <div
                                class="time-tip"
                                id="homeTimeTip"
                            >
                                현재 배터리로
                                청소가 가능합니다.
                            </div>

                        </section>


                        <section class="mini-card food-card">

                            <div class="food-title">
                                오늘의 음식
                            </div>

                            <div class="food-bowl"></div>

                            <div class="food-count">
                                보유량:
                                <span id="foodCount">
                                    1
                                </span>개
                            </div>

                        </section>

                    </div>

                </div>

            </section>


            <!-- ========================================
                 배터리 화면
            ========================================= -->

            <section
                class="page"
                id="batteryPage"
            >

                <div class="section-label">
                    BATTERY HEALTH
                </div>

                <div class="section-title">
                    배터리 건강 관리
                </div>


                <div class="battery-summary">

                    <div class="panel gauge-card">

                        <div
                            class="gauge"
                            id="socGauge"
                            style="
                                --value:81;
                                --gauge-color:#49a646;
                            "
                        >

                            <div class="gauge-content">

                                <div class="gauge-label">
                                    SOC
                                </div>

                                <div
                                    class="gauge-value"
                                    id="batterySocValue"
                                >
                                    81%
                                </div>

                            </div>

                        </div>

                        <div class="gauge-description">
                            권장 운용 구간
                            <br>
                            15%~90%
                        </div>

                    </div>


                    <div class="panel gauge-card">

                        <div
                            class="gauge"
                            id="temperatureGauge"
                            style="
                                --value:58;
                                --gauge-color:#ff7c22;
                            "
                        >

                            <div class="gauge-content">

                                <div class="gauge-label">
                                    온도
                                </div>

                                <div
                                    class="gauge-value"
                                    id="batteryTempValue"
                                >
                                    29℃
                                </div>

                            </div>

                        </div>

                        <div class="gauge-description">
                            안정 온도 구간
                            <br>
                            15℃~50℃
                        </div>

                    </div>

                </div>


                <div class="panel control-panel">

                    <div class="control-row">

                        <div class="control-heading">

                            <span>
                                목표 SOC 조절
                            </span>

                            <span
                                class="control-value"
                                id="targetSocLabel"
                            >
                                81%
                            </span>

                        </div>

                        <input
                            id="targetSocSlider"
                            type="range"
                            min="50"
                            max="90"
                            value="81"
                            oninput="changeTargetSoc(this.value)"
                        >

                        <div class="control-caption">
                            <span>50%</span>
                            <span>배터리 보호 권장</span>
                            <span>90%</span>
                        </div>

                    </div>


                    <div class="control-row">

                        <div class="control-heading">

                            <span>
                                온도 시뮬레이션
                            </span>

                            <span
                                class="control-value"
                                id="temperatureLabel"
                            >
                                29℃
                            </span>

                        </div>

                        <input
                            id="temperatureSlider"
                            type="range"
                            min="15"
                            max="50"
                            value="29"
                            oninput="changeTemperature(this.value)"
                        >

                        <div class="control-caption">
                            <span>15℃</span>
                            <span>현재 배터리 온도</span>
                            <span>50℃</span>
                        </div>

                    </div>

                    <button
                        class="charge-action"
                        onclick="chargeRobotFromBatteryPage()"
                    >
                        AI 권장 SOC까지 맞춤 충전
                    </button>

                </div>


                <div class="panel chart-panel">

                    <div class="panel-heading">

                        <div class="panel-title">
                            오늘 SOC 변화
                        </div>

                        <div class="panel-badge">
                            고SOC 방치 감소
                        </div>

                    </div>

                    <svg
                        class="soc-chart"
                        viewBox="0 0 340 165"
                    >

                        <line
                            class="chart-grid"
                            x1="30"
                            y1="28"
                            x2="330"
                            y2="28"
                        ></line>

                        <line
                            class="chart-grid"
                            x1="30"
                            y1="132"
                            x2="330"
                            y2="132"
                        ></line>

                        <text
                            class="chart-label"
                            x="3"
                            y="32"
                        >
                            90%
                        </text>

                        <text
                            class="chart-label"
                            x="5"
                            y="136"
                        >
                            15%
                        </text>

                        <polyline
                            class="chart-red"
                            points="
                                30,128
                                80,102
                                128,54
                                180,35
                                235,31
                                285,29
                                328,28
                            "
                        ></polyline>

                        <polyline
                            class="chart-green"
                            id="aiSocLine"
                            points="
                                30,128
                                80,103
                                128,82
                                180,74
                                235,74
                                285,74
                                328,74
                            "
                        ></polyline>

                    </svg>

                    <div class="chart-legend">

                        <span>
                            <span
                                class="legend-dot"
                                style="background:#eb6650;"
                            ></span>

                            기존 완충 방식
                        </span>

                        <span>
                            <span
                                class="legend-dot"
                                style="background:#4c9a43;"
                            ></span>

                            AI 가변 충전
                        </span>

                    </div>

                </div>


                <div class="panel battery-insight">

                    <div class="insight-line">

                        <div class="insight-icon">
                            💡
                        </div>

                        <div id="batteryInsightText">
                            최근 청소 패턴을 분석한 결과,
                            오늘은 SOC 81%까지만 충전해도
                            예상 청소를 완료할 수 있습니다.
                        </div>

                    </div>

                </div>

            </section>


            <!-- ========================================
                 기록 화면
            ========================================= -->

            <section
                class="page"
                id="recordPage"
            >

                <div class="section-label">
                    ACTIVITY LOG
                </div>

                <div class="section-title">
                    청소 활동 기록
                </div>


                <div class="panel weekly-panel">

                    <div class="panel-heading">

                        <div class="panel-title">
                            주간 청소 시간
                        </div>

                        <div class="weekly-average">
                            평균
                            <span id="weeklyAverage">
                                38
                            </span>분
                        </div>

                    </div>

                    <div class="bar-chart">

                        <div class="bar-item">
                            <div class="bar-value">25</div>
                            <div class="bar" style="height:42%;"></div>
                            <div class="bar-label">월</div>
                        </div>

                        <div class="bar-item">
                            <div class="bar-value">41</div>
                            <div class="bar" style="height:68%;"></div>
                            <div class="bar-label">화</div>
                        </div>

                        <div class="bar-item">
                            <div class="bar-value">34</div>
                            <div class="bar" style="height:56%;"></div>
                            <div class="bar-label">수</div>
                        </div>

                        <div class="bar-item">
                            <div class="bar-value">49</div>
                            <div class="bar" style="height:81%;"></div>
                            <div class="bar-label">목</div>
                        </div>

                        <div class="bar-item">
                            <div class="bar-value">40</div>
                            <div class="bar" style="height:66%;"></div>
                            <div class="bar-label">금</div>
                        </div>

                        <div class="bar-item">
                            <div class="bar-value">57</div>
                            <div class="bar" style="height:94%;"></div>
                            <div class="bar-label">토</div>
                        </div>

                        <div class="bar-item">
                            <div
                                class="bar-value"
                                id="sundayValue"
                            >
                                34
                            </div>

                            <div
                                class="bar"
                                id="sundayBar"
                                style="height:56%;"
                            ></div>

                            <div class="bar-label">
                                일
                            </div>
                        </div>

                    </div>

                </div>


                <div class="record-grid">

                    <div class="record-card">

                        <div class="record-label">
                            이번 주 청소 면적
                        </div>

                        <div class="record-value">
                            <span id="cleaningArea">
                                72
                            </span>㎡
                        </div>

                    </div>


                    <div class="record-card">

                        <div class="record-label">
                            평균 청소 시간
                        </div>

                        <div class="record-value">
                            <span id="averageCleaningTime">
                                38
                            </span>분
                        </div>

                    </div>


                    <div class="record-card">

                        <div class="record-label">
                            고온 복귀
                        </div>

                        <div class="record-value">
                            0회
                        </div>

                    </div>


                    <div class="record-card">

                        <div class="record-label">
                            AI 추천 수락
                        </div>

                        <div class="record-value">
                            <span id="aiAcceptCount">
                                4
                            </span>회
                        </div>

                    </div>

                </div>


                <div class="panel event-panel">

                    <div class="panel-title">
                        이벤트 기록
                    </div>

                    <div
                        class="event-list"
                        id="eventList"
                    >

                        <div class="event-item">

                            <div class="event-time">
                                14:20
                            </div>

                            <div class="event-content">

                                <strong>
                                    맞춤 충전 완료
                                </strong>

                                <span>
                                    목표 SOC 81%에서
                                    자동 충전을 종료했습니다.
                                </span>

                            </div>

                        </div>


                        <div class="event-item">

                            <div class="event-time">
                                10:15
                            </div>

                            <div class="event-content">

                                <strong>
                                    사용자 패턴 분석
                                </strong>

                                <span>
                                    거실 청소 예상 소비량
                                    27%를 반영했습니다.
                                </span>

                            </div>

                        </div>


                        <div class="event-item">

                            <div class="event-time">
                                08:40
                            </div>

                            <div class="event-content">

                                <strong>
                                    배터리 상태 정상
                                </strong>

                                <span>
                                    배터리 온도와 건강도가
                                    안정 범위에 있습니다.
                                </span>

                            </div>

                        </div>

                    </div>

                </div>

            </section>


            <!-- ========================================
                 리워드 화면
            ========================================= -->

            <section
                class="page"
                id="rewardPage"
            >

                <div class="section-label">
                    REWARD
                </div>

                <div class="section-title">
                    몽글이 성장 리워드
                </div>


                <div class="panel level-panel">

                    <div class="level-robot">
                        🤖
                    </div>

                    <div class="level-number">
                        Lv.
                        <span id="rewardLevel">
                            13
                        </span>
                    </div>

                    <div class="level-progress">

                        <div
                            class="level-progress-fill"
                            id="rewardExpFill"
                        ></div>

                    </div>

                    <div class="level-caption">
                        경험치
                        <span id="rewardExp">
                            55
                        </span>
                        / 100
                    </div>

                </div>


                <div class="reward-grid">

                    <div class="reward-card">

                        <div class="reward-icon">
                            🥣
                        </div>

                        <div class="reward-title">
                            배터리 음식
                        </div>

                        <div class="reward-description">
                            SOC를 12% 회복합니다.
                        </div>

                        <button
                            class="reward-button"
                            onclick="buyFood()"
                        >
                            50 코인
                        </button>

                    </div>


                    <div class="reward-card">

                        <div class="reward-icon">
                            🎀
                        </div>

                        <div class="reward-title">
                            빨간 리본
                        </div>

                        <div class="reward-description">
                            몽글이를 꾸며주세요.
                        </div>

                        <button
                            class="reward-button"
                            onclick="previewEffect('🎀')"
                        >
                            미리보기
                        </button>

                    </div>


                    <div class="reward-card">

                        <div class="reward-icon">
                            🧢
                        </div>

                        <div class="reward-title">
                            탐험가 모자
                        </div>

                        <div class="reward-description">
                            청소 미션 전용 아이템입니다.
                        </div>

                        <button
                            class="reward-button"
                            onclick="showToast('120 코인이 필요해요.')"
                        >
                            120 코인
                        </button>

                    </div>


                    <div class="reward-card">

                        <div class="reward-icon">
                            ✨
                        </div>

                        <div class="reward-title">
                            반짝이 효과
                        </div>

                        <div class="reward-description">
                            청소 완료 효과를 변경합니다.
                        </div>

                        <button
                            class="reward-button"
                            onclick="previewEffect('✨')"
                        >
                            효과 체험
                        </button>

                    </div>

                </div>

            </section>

        </div>


        <!-- 팝업 -->
        <div
            class="modal"
            id="modal"
        >

            <div class="modal-card">

                <div
                    class="modal-title"
                    id="modalTitle"
                ></div>

                <div
                    class="modal-body"
                    id="modalBody"
                ></div>

                <div
                    class="modal-actions"
                    id="modalActions"
                ></div>

                <button
                    class="modal-close"
                    onclick="closePanel()"
                >
                    확인
                </button>

            </div>

        </div>


        <div
            class="toast"
            id="toast"
        ></div>

    </div>

</div>


<script>
    const state = {
        currentPage: "homePage",

        soc: 81,
        targetSoc: 81,

        temperature: 29,
        health: 100,
        heart: 100,

        level: 13,
        exp: 55,

        coins: 50,
        food: 1,

        cleaning: false,
        charging: false,
        celebrating: false,

        cleanProgress: 0,
        missionComplete: false,

        todayCleanCount: 0,
        aiAcceptCount: 4,

        cleaningArea: 72,
        averageCleaningTime: 38
    };


    function clamp(
        value,
        min,
        max
    ) {
        return Math.min(
            Math.max(value, min),
            max
        );
    }


    function calculateCleaningTime() {
        return Math.max(
            0,
            Math.round(state.soc * 0.56)
        );
    }


    function switchPage(
        pageId,
        button
    ) {
        document
            .querySelectorAll(".page")
            .forEach(page => {
                page.classList.remove(
                    "active"
                );
            });

        document
            .querySelectorAll(".nav-button")
            .forEach(nav => {
                nav.classList.remove(
                    "active"
                );
            });

        document
            .getElementById(pageId)
            .classList.add("active");

        button.classList.add("active");

        state.currentPage = pageId;

        if (pageId === "recordPage") {
            renderRecordPage();
        }

        if (pageId === "batteryPage") {
            renderBatteryPage();
        }

        if (pageId === "rewardPage") {
            renderRewardPage();
        }
    }


    function goToRecordPage() {
        const button =
            document.querySelector(
                '[data-page="recordPage"]'
            );

        switchPage(
            "recordPage",
            button
        );
    }


    function renderAll() {
        state.soc = clamp(
            Math.round(state.soc),
            0,
            100
        );

        state.targetSoc = clamp(
            Math.round(state.targetSoc),
            50,
            90
        );

        state.temperature =
            Math.round(
                state.temperature * 10
            ) / 10;

        state.health = clamp(
            Math.round(state.health),
            0,
            100
        );

        state.heart = clamp(
            Math.round(state.heart),
            0,
            100
        );

        state.exp = clamp(
            Math.round(state.exp),
            0,
            100
        );


        document
            .getElementById("globalCoin")
            .innerText =
                String(state.coins)
                    .padStart(3, "0");

        document
            .getElementById("foodCount")
            .innerText =
                state.food;

        document
            .getElementById("homeCleaningTime")
            .innerText =
                calculateCleaningTime();

        document
            .getElementById("batteryPointer")
            .style.left =
                state.soc + "%";


        renderHomeState();
        renderBatteryPage();
        renderRecordPage();
        renderRewardPage();
    }


    function renderHomeState() {
        const room =
            document.getElementById(
                "homeRoom"
            );

        const speech =
            document.getElementById(
                "speechBubble"
            );

        const modeChip =
            document.getElementById(
                "modeChip"
            );

        const batteryFace =
            document.getElementById(
                "batteryFace"
            );

        const batteryMessage =
            document.getElementById(
                "batteryMessage"
            );

        const timeTip =
            document.getElementById(
                "homeTimeTip"
            );

        const spark =
            document.getElementById(
                "sparkIcon"
            );

        const cleanPathFill =
            document.getElementById(
                "cleanPathFill"
            );

        const missionFill =
            document.getElementById(
                "missionFill"
            );


        room.classList.remove(
            "is-cleaning",
            "is-charging",
            "is-low",
            "is-celebrating"
        );


        if (state.celebrating) {
            room.classList.add(
                "is-celebrating"
            );

            speech.innerHTML =
                "<strong>청소 완료!</strong><br>" +
                "보상을 받았어요!";

            modeChip.innerHTML =
                "🏆 미션 완료 · +50 코인";

            batteryFace.innerText =
                "🥳";

            spark.innerText =
                "🎉";
        }

        else if (state.cleaning) {
            room.classList.add(
                "is-cleaning"
            );

            speech.innerHTML =
                "<strong>열심히 청소 중이에요!</strong><br>" +
                "진행률 " +
                state.cleanProgress +
                "%";

            modeChip.innerHTML =
                "🧹 거실 청소 중 · " +
                state.cleanProgress +
                "%";

            batteryFace.innerText =
                "🧹";

            batteryMessage.innerHTML =
                "청소 중입니다.<br>" +
                "SOC와 예상 시간이 변하고 있어요.";

            timeTip.innerHTML =
                "청소 진행률 " +
                state.cleanProgress +
                "%";

            spark.innerText =
                "💨";
        }

        else if (state.charging) {
            room.classList.add(
                "is-charging"
            );

            speech.innerHTML =
                "<strong style='color:#e48627'>" +
                "에너지를 먹고 있어요!</strong><br>" +
                "필요한 만큼 충전할게요.";

            modeChip.innerHTML =
                "⚡ 맞춤 충전 중 · " +
                state.soc +
                " → " +
                state.targetSoc +
                "%";

            batteryFace.innerText =
                "⚡";

            batteryMessage.innerHTML =
                "AI 권장 SOC까지<br>" +
                "맞춤 충전 중입니다.";

            timeTip.innerHTML =
                "현재 SOC " +
                state.soc +
                "%";

            spark.innerText =
                "⚡";
        }

        else if (state.soc < 15) {
            room.classList.add(
                "is-low"
            );

            speech.innerHTML =
                "<strong style='color:#ef4e45'>" +
                "배가 너무 고파요...</strong><br>" +
                "충전이 필요해요.";

            modeChip.innerHTML =
                "⚠️ 배터리 부족";

            batteryFace.innerText =
                "🥴";

            batteryMessage.innerHTML =
                "배터리가 부족해요.<br>" +
                "먼저 충전해 주세요.";

            timeTip.innerHTML =
                "충전 후 청소를 시작해 주세요.";

            spark.innerText =
                "💦";
        }

        else if (state.soc <= 90) {
            speech.innerHTML =
                "<strong>배가 든든해요!</strong><br>" +
                "청소를 준비할게요!";

            modeChip.innerHTML =
                "✨ AI 권장 SOC " +
                state.targetSoc +
                "%";

            batteryFace.innerText =
                "😊";

            batteryMessage.innerHTML =
                "배터리 상태가 좋아요.<br>" +
                "수명 보호 범위 안입니다.";

            timeTip.innerHTML =
                "현재 배터리로 청소가 가능합니다.";

            spark.innerText =
                "✨";
        }

        else {
            speech.innerHTML =
                "<strong style='color:#e48627'>" +
                "배가 너무 불러요!</strong><br>" +
                "충전을 멈춰도 좋아요.";

            modeChip.innerHTML =
                "⚠️ 권장 SOC 초과";

            batteryFace.innerText =
                "😮";

            batteryMessage.innerHTML =
                "고SOC 상태입니다.<br>" +
                "90% 이하 운용을 권장합니다.";

            timeTip.innerHTML =
                "충전량이 충분합니다.";

            spark.innerText =
                "⚡";
        }


        cleanPathFill.style.width =
            state.cleanProgress +
            "%";

        missionFill.style.width =
            state.missionComplete
                ? "100%"
                : state.cleanProgress + "%";
    }


    function renderBatteryPage() {
        const socGauge =
            document.getElementById(
                "socGauge"
            );

        const temperatureGauge =
            document.getElementById(
                "temperatureGauge"
            );

        socGauge.style.setProperty(
            "--value",
            state.soc
        );

        document
            .getElementById(
                "batterySocValue"
            )
            .innerText =
                state.soc + "%";


        const temperaturePercent =
            clamp(
                (
                    state.temperature - 15
                ) / 35 * 100,
                0,
                100
            );

        temperatureGauge.style.setProperty(
            "--value",
            temperaturePercent
        );

        document
            .getElementById(
                "batteryTempValue"
            )
            .innerText =
                state.temperature + "℃";

        document
            .getElementById(
                "targetSocLabel"
            )
            .innerText =
                state.targetSoc + "%";

        document
            .getElementById(
                "targetSocSlider"
            )
            .value =
                state.targetSoc;

        document
            .getElementById(
                "temperatureLabel"
            )
            .innerText =
                state.temperature + "℃";

        document
            .getElementById(
                "temperatureSlider"
            )
            .value =
                state.temperature;


        document
            .getElementById(
                "batteryInsightText"
            )
            .innerHTML =
                "최근 청소 패턴을 분석한 결과, " +
                "오늘은 SOC <b>" +
                state.targetSoc +
                "%</b>까지만 충전해도 " +
                "예상 청소를 완료할 수 있습니다.";


        updateSocGraph();
    }


    function renderRecordPage() {
        document
            .getElementById(
                "cleaningArea"
            )
            .innerText =
                state.cleaningArea;

        document
            .getElementById(
                "averageCleaningTime"
            )
            .innerText =
                state.averageCleaningTime;

        document
            .getElementById(
                "weeklyAverage"
            )
            .innerText =
                state.averageCleaningTime;

        document
            .getElementById(
                "aiAcceptCount"
            )
            .innerText =
                state.aiAcceptCount;


        const sundayValue =
            34 +
            state.todayCleanCount * 8;

        document
            .getElementById(
                "sundayValue"
            )
            .innerText =
                sundayValue;

        document
            .getElementById(
                "sundayBar"
            )
            .style.height =
                Math.min(
                    96,
                    56 +
                    state.todayCleanCount * 10
                ) + "%";
    }


    function renderRewardPage() {
        document
            .getElementById(
                "rewardLevel"
            )
            .innerText =
                state.level;

        document
            .getElementById(
                "rewardExp"
            )
            .innerText =
                state.exp;

        document
            .getElementById(
                "rewardExpFill"
            )
            .style.width =
                state.exp + "%";
    }


    function changeTargetSoc(value) {
        state.targetSoc =
            Number(value);

        document
            .getElementById(
                "targetSocLabel"
            )
            .innerText =
                state.targetSoc + "%";

        document
            .getElementById(
                "batteryInsightText"
            )
            .innerHTML =
                "설정한 목표 SOC는 <b>" +
                state.targetSoc +
                "%</b>입니다. " +
                "사용자의 청소 패턴과 필요 에너지에 따라 " +
                "충전 상한을 조절합니다.";

        updateSocGraph();
        renderHomeState();
    }


    function changeTemperature(value) {
        state.temperature =
            Number(value);

        renderBatteryPage();
    }


    function updateSocGraph() {
        const y =
            132 -
            (
                state.targetSoc - 15
            ) / 75 * 104;

        const points =
            "30,128 " +
            "80,103 " +
            "128," +
            Math.round(
                (82 + y) / 2
            ) +
            " " +
            "180," +
            Math.round(y) +
            " " +
            "235," +
            Math.round(y) +
            " " +
            "285," +
            Math.round(y) +
            " " +
            "328," +
            Math.round(y);

        document
            .getElementById(
                "aiSocLine"
            )
            .setAttribute(
                "points",
                points
            );
    }


    function chargeRobotFromBatteryPage() {
        const homeButton =
            document.querySelector(
                '[data-page="homePage"]'
            );

        switchPage(
            "homePage",
            homeButton
        );

        setTimeout(() => {
            chargeRobot();
        }, 250);
    }


    function chargeRobot() {
        if (state.cleaning) {
            showToast(
                "청소가 끝난 후 충전할 수 있어요."
            );

            return;
        }

        if (state.charging) {
            showToast(
                "이미 충전 중이에요."
            );

            return;
        }

        if (state.soc >= state.targetSoc) {
            openPanel(
                "맞춤 충전 안내",
                "현재 SOC는 <b>" +
                state.soc +
                "%</b>입니다.<br><br>" +
                "오늘의 목표 SOC인 <b>" +
                state.targetSoc +
                "%</b>에 이미 도달했으므로 " +
                "추가 충전을 하지 않습니다."
            );

            return;
        }

        state.charging = true;

        renderAll();

        showToast(
            "AI 맞춤 충전을 시작합니다."
        );


        const timer =
            setInterval(() => {

                state.soc =
                    Math.min(
                        state.targetSoc,
                        state.soc + 2
                    );

                state.temperature =
                    Math.min(
                        32,
                        state.temperature + 0.1
                    );

                spawnEffect(
                    "⚡",
                    2
                );

                renderAll();


                if (
                    state.soc >=
                    state.targetSoc
                ) {
                    clearInterval(
                        timer
                    );

                    state.charging =
                        false;

                    state.temperature =
                        29;

                    state.aiAcceptCount += 1;

                    addEvent(
                        "지금",
                        "맞춤 충전 완료",
                        "목표 SOC " +
                        state.targetSoc +
                        "%에서 자동 충전을 종료했습니다."
                    );

                    spawnEffect(
                        "✨",
                        10
                    );

                    renderAll();

                    setTimeout(() => {
                        openPanel(
                            "맞춤 충전 완료",
                            "필요한 만큼만 충전했습니다.<br><br>" +
                            "목표 SOC <b>" +
                            state.targetSoc +
                            "%</b>에서 충전을 종료하여 " +
                            "고SOC 유지 시간을 줄였습니다."
                        );
                    }, 400);
                }

            }, 150);
    }


    function startCleaning() {
        if (state.cleaning) {
            showToast(
                "이미 청소 중이에요."
            );

            return;
        }

        if (state.charging) {
            showToast(
                "충전이 끝난 후 청소할게요."
            );

            return;
        }

        if (state.soc < 15) {
            showToast(
                "SOC가 부족합니다. 먼저 충전해 주세요."
            );

            return;
        }

        state.cleaning = true;
        state.cleanProgress = 0;

        renderAll();

        showToast(
            "거실 청소를 시작합니다!"
        );


        let step = 0;
        const totalSteps = 18;


        const timer =
            setInterval(() => {

                step += 1;

                state.cleanProgress =
                    Math.round(
                        step /
                        totalSteps *
                        100
                    );

                state.soc =
                    Math.max(
                        0,
                        state.soc - 1
                    );

                state.temperature =
                    Math.min(
                        36,
                        state.temperature + 0.25
                    );

                renderAll();


                if (
                    step >= totalSteps ||
                    state.soc <= 10
                ) {
                    clearInterval(
                        timer
                    );

                    state.cleaning =
                        false;

                    state.cleanProgress =
                        100;

                    state.temperature =
                        29;

                    state.missionComplete =
                        true;

                    state.celebrating =
                        true;

                    state.todayCleanCount += 1;
                    state.coins += 50;
                    state.exp += 20;

                    state.cleaningArea += 18;
                    state.averageCleaningTime =
                        Math.round(
                            (
                                state.averageCleaningTime +
                                32
                            ) / 2
                        );

                    levelCheck();

                    addEvent(
                        "지금",
                        "거실 청소 완료",
                        "청소 완료 보상으로 50코인과 경험치 20을 획득했습니다."
                    );

                    spawnEffect(
                        "🎉",
                        15
                    );

                    spawnEffect(
                        "⭐",
                        9
                    );

                    renderAll();


                    setTimeout(() => {
                        state.celebrating =
                            false;

                        renderAll();
                    }, 2200);


                    setTimeout(() => {
                        openPanel(
                            "청소 완료!",
                            "거실 청소를 완료했습니다.<br><br>" +
                            "보상으로 <b>50코인</b>과 " +
                            "경험치 20을 획득했습니다."
                        );
                    }, 600);
                }

            }, 320);
    }


    function feedRobot() {
        if (state.food <= 0) {
            showToast(
                "음식이 부족해요. 리워드 화면에서 구매해 주세요."
            );

            return;
        }

        state.food -= 1;
        state.soc += 12;
        state.exp += 8;

        pulseRobot();

        spawnEffect(
            "⚡",
            8
        );

        levelCheck();
        renderAll();

        showToast(
            "SOC가 12% 회복되었습니다."
        );
    }


    function playRobot() {
        if (state.soc < 5) {
            showToast(
                "배터리가 부족해서 놀 수 없어요."
            );

            return;
        }

        state.soc -= 3;
        state.heart += 6;
        state.exp += 5;

        pulseRobot();

        spawnEffect(
            "💖",
            8
        );

        levelCheck();
        renderAll();

        showToast(
            "친밀도와 경험치가 올랐어요."
        );
    }


    function exerciseRobot() {
        if (state.soc < 8) {
            showToast(
                "훈련 전에 충전이 필요해요."
            );

            return;
        }

        state.soc -= 6;
        state.health += 3;
        state.exp += 12;

        pulseRobot();

        spawnEffect(
            "✨",
            8
        );

        levelCheck();
        renderAll();

        showToast(
            "훈련을 완료했습니다."
        );
    }


    function petRobot() {
        if (state.cleaning) {
            showToast(
                "청소가 끝난 후 쓰다듬어 주세요."
            );

            return;
        }

        state.heart =
            Math.min(
                100,
                state.heart + 2
            );

        state.exp += 1;

        pulseRobot();

        spawnEffect(
            "💖",
            7
        );

        levelCheck();
        renderAll();

        showToast(
            "몽글이의 기분이 좋아졌어요."
        );
    }


    function takePhoto() {
        pulseRobot();

        spawnEffect(
            "📸",
            5
        );

        openPanel(
            "오늘의 사진",
            "왕관을 쓴 몽글이의 사진을 촬영했습니다.<br><br>" +
            "향후에는 장식 아이템과 청소 완료 화면을 " +
            "사진첩에 저장할 수 있습니다."
        );
    }


    function decorateRobot() {
        openPanel(
            "몽글이 꾸미기",
            "현재 장착 아이템은 <b>황금 왕관</b>입니다.<br><br>" +
            "리본, 탐험가 모자, 표정 스킨 등을 " +
            "리워드 화면에서 확인할 수 있습니다.",
            '<button class="modal-action" ' +
            'onclick="previewEffect(\\'🎀\\')">' +
            '리본 체험</button>' +

            '<button class="modal-action" ' +
            'onclick="previewEffect(\\'✨\\')">' +
            '반짝이 체험</button>'
        );
    }


    function openShop() {
        const button =
            document.querySelector(
                '[data-page="rewardPage"]'
            );

        switchPage(
            "rewardPage",
            button
        );
    }


    function previewEffect(symbol) {
        closePanel();

        const button =
            document.querySelector(
                '[data-page="homePage"]'
            );

        switchPage(
            "homePage",
            button
        );

        setTimeout(() => {
            spawnEffect(
                symbol,
                10
            );
        }, 300);
    }


    function buyFood() {
        if (state.coins < 50) {
            showToast(
                "코인이 부족해요."
            );

            return;
        }

        state.coins -= 50;
        state.food += 1;

        renderAll();

        showToast(
            "배터리 음식 1개를 구매했습니다."
        );
    }


    function openBatterySummary() {
        openPanel(
            "배터리 상태",
            "현재 SOC는 <b>" +
            state.soc +
            "%</b>입니다.<br>" +

            "배터리 온도는 <b>" +
            state.temperature +
            "℃</b>입니다.<br>" +

            "예상 청소 가능 시간은 <b>" +
            calculateCleaningTime() +
            "분</b>입니다.<br><br>" +

            "AI 목표 SOC는 <b>" +
            state.targetSoc +
            "%</b>입니다.",

            '<button class="modal-action" ' +
            'onclick="goToBatteryPageFromModal()">' +
            '상세보기</button>' +

            '<button class="modal-action" ' +
            'onclick="closePanel(); chargeRobot();">' +
            '맞춤 충전</button>'
        );
    }


    function goToBatteryPageFromModal() {
        closePanel();

        const button =
            document.querySelector(
                '[data-page="batteryPage"]'
            );

        switchPage(
            "batteryPage",
            button
        );
    }


    function levelCheck() {
        if (state.exp >= 100) {
            state.exp -= 100;
            state.level += 1;

            spawnEffect(
                "⭐",
                10
            );

            showToast(
                "레벨 업! Lv." +
                state.level
            );
        }
    }


    function addEvent(
        time,
        title,
        description
    ) {
        const list =
            document.getElementById(
                "eventList"
            );

        const item =
            document.createElement(
                "div"
            );

        item.className =
            "event-item";

        item.innerHTML =
            '<div class="event-time">' +
            time +
            '</div>' +

            '<div class="event-content">' +

                '<strong>' +
                title +
                '</strong>' +

                '<span>' +
                description +
                '</span>' +

            '</div>';

        list.prepend(item);
    }


    function pulseRobot() {
        const robot =
            document.getElementById(
                "robotCharacter"
            );

        robot.classList.remove(
            "tap-motion"
        );

        void robot.offsetWidth;

        robot.classList.add(
            "tap-motion"
        );

        setTimeout(() => {
            robot.classList.remove(
                "tap-motion"
            );
        }, 650);
    }


    function spawnEffect(
        symbol,
        count = 6
    ) {
        const layer =
            document.getElementById(
                "effectLayer"
            );

        for (
            let i = 0;
            i < count;
            i++
        ) {
            const particle =
                document.createElement(
                    "span"
                );

            particle.className =
                "effect";

            particle.innerText =
                symbol;

            particle
                .style
                .setProperty(
                    "--move-x",
                    Math.round(
                        Math.random() * 160 - 80
                    ) + "px"
                );

            particle
                .style
                .setProperty(
                    "--rotate",
                    Math.round(
                        Math.random() * 100 - 50
                    ) + "deg"
                );

            particle.style.left =
                42 +
                Math.random() * 16 +
                "%";

            particle.style.animationDelay =
                Math.random() * 0.25 +
                "s";

            layer.appendChild(
                particle
            );

            setTimeout(() => {
                particle.remove();
            }, 1600);
        }
    }


    function openPanel(
        title,
        body,
        actions = ""
    ) {
        document
            .getElementById(
                "modalTitle"
            )
            .innerText =
                title;

        document
            .getElementById(
                "modalBody"
            )
            .innerHTML =
                body;

        document
            .getElementById(
                "modalActions"
            )
            .innerHTML =
                actions;

        document
            .getElementById(
                "modal"
            )
            .classList.add(
                "show"
            );
    }


    function closePanel() {
        document
            .getElementById(
                "modal"
            )
            .classList.remove(
                "show"
            );
    }


    function showToast(message) {
        const toast =
            document.getElementById(
                "toast"
            );

        toast.innerText =
            message;

        toast.classList.add(
            "show"
        );

        setTimeout(() => {
            toast.classList.remove(
                "show"
            );
        }, 1800);
    }


    setInterval(() => {
        if (
            state.cleaning ||
            state.charging ||
            state.celebrating
        ) {
            return;
        }

        const robot =
            document.getElementById(
                "robotCharacter"
            );

        robot.classList.remove(
            "look-left",
            "look-right"
        );

        const direction =
            Math.random();

        if (direction < 0.33) {
            robot.classList.add(
                "look-left"
            );
        }

        else if (direction < 0.66) {
            robot.classList.add(
                "look-right"
            );
        }

        setTimeout(() => {
            robot.classList.remove(
                "look-left",
                "look-right"
            );
        }, 1100);

    }, 2800);


    renderAll();
</script>

</body>
</html>
"""


components.html(
    app_html,
    height=930,
    scrolling=False,
)
