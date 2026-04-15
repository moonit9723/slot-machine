<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>OPS 등급 계산기</title>
    <style>
        body { background: #121212; color: #e8fefe; font-family: 'Segoe UI', Arial; text-align: center; }
        
        .container { 
            width: 520px; 
            margin: 100px auto; 
            padding: 40px; 
            border-radius: 18px; 
            background: #1a1a1a; 
            border: 1px solid #2ee6c9; 
            box-shadow: 0 0 30px rgba(0,255,200,0.25); 
            position: relative;
            transition: width 0.3s, padding 0.3s;
        }
        .container.wide {
            width: 820px;
            padding: 40px 50px;
        }

        .title-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
        }
        h1 { color: #b9fff7; text-shadow: 0 0 12px #00ffe1; margin: 0; font-size: 32px; }

        .info-icon {
            position: relative;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            width: 28px; height: 28px;
            border-radius: 50%;
            border: 2px solid #3eeed2;
            color: #3eeed2;
            font-weight: bold;
            cursor: pointer;
            user-select: none;
            transition: background 0.15s, color 0.15s, box-shadow 0.15s;
        }
        .info-icon:hover {
            background: #3eeed2;
            color: #121212;
            border-color: #3eeed2;
            box-shadow: 0 0 12px #3eeed2aa;
        }
        .info-icon.pinned {
            background: #3eeed2;
            color: #121212;
            border-color: #3eeed2;
            box-shadow: 0 0 12px #3eeed2aa;
        }

        .info-tooltip {
            visibility: hidden; opacity: 0;
            width: 300px; background: #1a1a1a; color: #e8fefe;
            text-align: left; border-radius: 10px; padding: 15px;
            position: absolute; z-index: 10; top: 150%; left: 50%;
            transform: translateX(-50%); border: 1px solid #3eeed2;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
            font-size: 14px; line-height: 1.8; transition: 0.2s;
        }
        .info-tooltip.show { visibility: visible; opacity: 1; }
        
        .t-ss { color: #ffb84d; font-weight: bold; }
        .t-s  { color: #fff176; font-weight: bold; }
        .t-a  { color: #ff8a80; font-weight: bold; }
        .t-b  { color: #81c784; font-weight: bold; }
        .t-c  { color: #64b5f6; font-weight: bold; }
        .t-d  { color: #bcaaa4; font-weight: bold; }

        .labels { display: flex; justify-content: space-around; margin-bottom: 10px; color: #9efcff; font-weight: bold; }

        /* 키 힌트 안내 */
        .key-hint {
            font-size: 12px;
            color: #4a8f8a;
            margin-bottom: 14px;
            letter-spacing: 0.03em;
        }
        .key-hint kbd {
            background: #1f2e2e;
            border: 1px solid #3eeed2;
            border-radius: 4px;
            padding: 1px 6px;
            color: #3eeed2;
            font-size: 11px;
            font-family: monospace;
        }

        .inputs { display: flex; justify-content: space-around; gap: 10px; }

        /* 입력 래퍼: 포커스 시 화살표 버튼 표시 */
        .input-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }

        .arrow-btn {
            background: transparent;
            border: 1px solid #2a6660;
            border-radius: 5px;
            color: #3eeed2;
            width: 120px;
            height: 22px;
            font-size: 13px;
            cursor: pointer;
            transition: background 0.15s, border-color 0.15s;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            line-height: 1;
            opacity: 0.35;
            pointer-events: auto;
        }
        /* 포커스 된 래퍼의 화살표 버튼만 활성 */
        .input-wrapper.focused .arrow-btn {
            opacity: 1;
            pointer-events: auto;
        }
        .arrow-btn:hover {
            background: #00ffe122;
            border-color: #00ffe1;
        }

        input {
            width: 120px;
            padding: 12px;
            background: #0f0f0f;
            border: 1px solid #3eeed2;
            border-radius: 8px;
            color: #b9fff7;
            text-align: center;
            font-size: 18px;
            box-sizing: border-box;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        input:focus { border: 1px solid #00ffe1; box-shadow: 0 0 12px #00ffe1; outline: none; }

        /* 포커스된 input-wrapper 강조 */
        .input-wrapper.focused input {
            border-color: #00ffe1;
            box-shadow: 0 0 14px #00ffe188;
        }
        
        button.calc-btn {
            display: block; margin: 30px auto 0; width: 280px; padding: 15px;
            font-size: 20px; font-weight: bold; background: transparent;
            border: 2px solid #00ffe1; color: #b9fff7; border-radius: 10px;
            cursor: pointer; transition: 0.3s;
        }
        button.calc-btn:hover { background: #00ffe1; color: black; box-shadow: 0 0 20px #00ffe1; }

        .result-box { margin-top: 30px; padding: 25px; border-radius: 12px; display: none; border: 3px solid; transition: 0.3s; }
        
        .ss { border-color: #ffb84d; background: rgba(255, 184, 77, 0.1); color: #ffd699; text-shadow: 0 0 10px #ffb84d; }
        .s  { border-color: #fff176; background: rgba(255, 241, 118, 0.1); color: #fff9c4; }
        .a  { border-color: #ff8a80; background: rgba(255, 138, 128, 0.1); color: #ffcdd2; }
        .b  { border-color: #81c784; background: rgba(129, 199, 132, 0.1); color: #c8e6c9; }
        .c  { border-color: #64b5f6; background: rgba(100, 181, 246, 0.1); color: #bbdefb; }
        .d  { border-color: #bcaaa4; background: rgba(188, 170, 164, 0.1); color: #d7ccc8; }

        .grade { font-size: 32px; font-weight: bold; margin-top: 10px; }
        #error { color: #ff9b9b; margin-top: 15px; font-weight: bold; }

        /* 단계 표시 */
        #stageSection {
            border-top: 1px solid #2a4444;
            padding-top: 16px;
        }
        .stage-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        .stage-label {
            width: 42px;
            text-align: right;
            font-size: 13px;
            color: #7ecfcf;
            flex-shrink: 0;
        }
        .stage-dots {
            display: flex;
            gap: 5px;
            flex: 1;
        }
        .stage-dot {
            flex: 1;
            height: 10px;
            border-radius: 4px;
            background: #1f3333;
            border: 1px solid #2a5555;
            transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
        }
        .stage-dot.active-1 { background: #bcaaa4; border-color: #bcaaa4; }
        .stage-dot.active-2 { background: #64b5f6; border-color: #64b5f6; box-shadow: 0 0 4px #64b5f6aa; }
        .stage-dot.active-3 { background: #81c784; border-color: #81c784; box-shadow: 0 0 4px #81c784aa; }
        .stage-dot.active-4 { background: #ff8a80; border-color: #ff8a80; box-shadow: 0 0 4px #ff8a80aa; }
        .stage-dot.active-5 { background: #fff176; border-color: #fff176; box-shadow: 0 0 6px #fff176bb; }
        .stage-dot.active-plus { background: #ffb84d; border-color: #ffb84d; box-shadow: 0 0 8px #ffb84dcc; }
        .stage-num { width: 42px; font-size: 12px; font-weight: bold; text-align: left; flex-shrink: 0; }
        .stage-num.sn-1 { color: #bcaaa4; }
        .stage-num.sn-2 { color: #64b5f6; }
        .stage-num.sn-3 { color: #81c784; }
        .stage-num.sn-4 { color: #ff8a80; }
        .stage-num.sn-5 { color: #fff176; }
        .stage-num.sn-plus { color: #ffb84d; }

        /* 타자/투수 모드 탭 */
        .mode-tabs {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 24px;
        }
        .mode-tab {
            flex: 1;
            padding: 10px 0;
            font-size: 16px;
            font-weight: bold;
            background: transparent;
            border: 2px solid #3eeed2;
            color: #3eeed2;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.2s;
            width: auto; margin: 0;
        }
        .mode-tab.active {
            background: #3eeed2;
            color: #121212;
            box-shadow: 0 0 14px #3eeed2aa;
        }
        .mode-tab:not(.active):hover { background: #3eeed222; }

        /* 투수 유형 탭 */
        .pitcher-tabs {
            display: flex;
            gap: 8px;
            justify-content: center;
            margin-bottom: 20px;
        }
        .pitcher-tab {
            flex: 1;
            padding: 8px 0;
            font-size: 14px;
            font-weight: bold;
            background: transparent;
            border: 1px solid #5a9a90;
            color: #7ecfcf;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
            width: auto; margin: 0;
        }
        .pitcher-tab.active {
            background: #1a4a44;
            border-color: #3eeed2;
            color: #3eeed2;
            box-shadow: 0 0 8px #3eeed255;
        }
        .pitcher-tab:not(.active):hover { background: #1a3333; }

        /* 투수 입력 */
        .p-labels {
            display: flex;
            justify-content: space-around;
            margin-bottom: 8px;
            color: #9efcff;
            font-weight: bold;
        }
        .p-inputs {
            display: flex;
            justify-content: space-around;
            gap: 10px;
            margin-bottom: 18px;
        }
        .p-input-wrap { display: flex; flex-direction: column; align-items: center; }
        .p-input {
            width: 140px;
            padding: 12px;
            background: #0f0f0f;
            border: 1px solid #3eeed2;
            border-radius: 8px;
            color: #b9fff7;
            text-align: center;
            font-size: 18px;
            box-sizing: border-box;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .p-input:focus { border-color: #00ffe1; box-shadow: 0 0 12px #00ffe1; outline: none; }
        .p-role-fields { margin-top: 4px; }

        /* 4개 가로 나열 투수 입력 */
        .p-row-labels {
            display: flex;
            justify-content: space-around;
            margin-bottom: 8px;
            color: #9efcff;
            font-weight: bold;
            text-align: center;
        }
        .p-row-labels div { flex: 1; }
        .p-row-inputs {
            display: flex;
            justify-content: space-around;
            gap: 6px;
        }
        .p-row-inputs .input-wrapper { flex: 1; }
        .p-field-input {
            width: 100%;
            padding: 12px 4px;
            background: #0f0f0f;
            border: 1px solid #3eeed2;
            border-radius: 8px;
            color: #b9fff7;
            text-align: center;
            font-size: 16px;
            box-sizing: border-box;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .p-field-input:focus { border-color: #00ffe1; box-shadow: 0 0 12px #00ffe1; outline: none; }
        .p-arrowbtn { width: 100%; }

        /* 세부/비교 서브탭 */
        .sub-tabs {
            display: flex;
            gap: 8px;
            justify-content: center;
            margin-bottom: 20px;
        }
        .sub-tab {
            flex: 1;
            padding: 8px 0;
            font-size: 14px;
            font-weight: bold;
            background: transparent;
            border: 1px solid #2a6660;
            color: #7ecfcf;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
            width: auto; margin: 0;
        }
        .sub-tab.active {
            background: #1a4a44;
            border-color: #3eeed2;
            color: #3eeed2;
            box-shadow: 0 0 8px #3eeed255;
        }
        .sub-tab:not(.active):hover { background: #1a3333; }

        /* 비교 섹션 */
        .compare-wrapper {
            display: flex;
            gap: 16px;
            align-items: flex-start;
            margin-top: 16px;
        }
        .compare-player {
            flex: 1;
            background: #141414;
            border: 1px solid #2a5555;
            border-radius: 12px;
            padding: 16px 12px;
        }
        .compare-title {
            font-size: 16px;
            font-weight: bold;
            color: #9efcff;
            margin-bottom: 12px;
            text-align: center;
        }
        .compare-labels {
            display: flex;
            justify-content: space-around;
            font-size: 12px;
            color: #7ecfcf;
            font-weight: bold;
            margin-bottom: 6px;
        }
        .compare-inputs {
            display: flex;
            gap: 6px;
        }
        .cmp-input {
            flex: 1;
            padding: 10px 4px;
            background: #0f0f0f;
            border: 1px solid #3eeed2;
            border-radius: 8px;
            color: #b9fff7;
            text-align: center;
            font-size: 15px;
            box-sizing: border-box;
            min-width: 0;
        }
        .cmp-input:focus { border-color: #00ffe1; box-shadow: 0 0 8px #00ffe1; outline: none; }
        .compare-divider {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            color: #3eeed2;
            padding-top: 60px;
            flex-shrink: 0;
        }

        /* 세부 모달 */
        .detail-modal {
            background: #1a1a1a;
            border: 1px solid #3eeed2;
            box-shadow: 0 0 40px rgba(0,255,200,0.2);
            border-radius: 18px;
            width: 560px;
            margin: 60px auto;
            overflow: hidden;
        }
        .detail-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 28px;
            border-bottom: 1px solid #2a4444;
            background: #141414;
        }
        .detail-modal-header span {
            font-size: 20px;
            font-weight: bold;
            color: #b9fff7;
            text-shadow: 0 0 10px #00ffe155;
        }
        .detail-modal-close {
            background: transparent;
            border: 1px solid #3eeed2;
            color: #3eeed2;
            border-radius: 50%;
            width: 32px; height: 32px;
            font-size: 16px;
            cursor: pointer;
            transition: 0.2s;
            display: flex; align-items: center; justify-content: center;
            width: auto; margin: 0; padding: 0 10px; border-radius: 8px;
        }
        .detail-modal-close:hover { background: #3eeed2; color: #121212; }
        .detail-modal-body { padding: 28px; }
        .detail-modal-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 12px;
        }
        .detail-modal-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
        }
        .detail-modal-item label {
            font-size: 12px;
            color: #7ecfcf;
            font-weight: bold;
        }
        .detail-modal-input {
            width: 100%;
            padding: 10px 4px;
            background: #0f0f0f;
            border: 1px solid #3eeed2;
            border-radius: 8px;
            color: #b9fff7;
            text-align: center;
            font-size: 15px;
            box-sizing: border-box;
        }
        .detail-modal-input:focus { border-color: #00ffe1; box-shadow: 0 0 10px #00ffe1; outline: none; }

        /* 세부 화면 그리드 */
        .detail-section-title {
            font-size: 20px;
            font-weight: bold;
            color: #b9fff7;
            text-shadow: 0 0 10px #00ffe155;
            text-align: center;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #2a4444;
        }
        .detail-input-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 10px;
        }
        .detail-input-cell {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
        }
        .detail-input-cell label {
            font-size: 13px;
            color: #9efcff;
            font-weight: bold;
        }
        .detail-labels {
            display: flex;
            justify-content: space-around;
            margin-bottom: 8px;
            color: #9efcff;
            font-weight: bold;
            font-size: 14px;
            gap: 10px;
        }
        .detail-labels div { flex: 1; text-align: center; }
        .detail-row {
            display: flex;
            justify-content: space-around;
            gap: 10px;
        }
        .detail-row .input-wrapper { flex: 1; }
        .detail-field-input {
            width: 100%;
            padding: 12px 4px;
            background: #0f0f0f;
            border: 1px solid #3eeed2;
            border-radius: 8px;
            color: #b9fff7;
            text-align: center;
            font-size: 16px;
            box-sizing: border-box;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .detail-field-input:focus { border-color: #00ffe1; box-shadow: 0 0 12px #00ffe1; outline: none; }
        .detail-switch-wrap {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            user-select: none;
        }
        .detail-switch-label {
            font-size: 14px;
            font-weight: bold;
            color: #7ecfcf;
        }
        .detail-switch {
            width: 42px; height: 22px;
            background: #1f3333;
            border: 1px solid #3eeed2;
            border-radius: 11px;
            position: relative;
            transition: background 0.2s;
            cursor: pointer;
        }
        .detail-switch.on {
            background: #1a4a44;
            box-shadow: 0 0 8px #3eeed255;
        }
        .detail-switch-knob {
            width: 16px; height: 16px;
            background: #3eeed2;
            border-radius: 50%;
            position: absolute;
            top: 2px; left: 3px;
            transition: left 0.2s;
        }
        .detail-switch.on .detail-switch-knob { left: 21px; }
        .detail-section-title {
            font-size: 15px;
            font-weight: bold;
            color: #9efcff;
            margin-bottom: 12px;
            text-align: center;
        }
        .detail-group-label {
            font-size: 12px;
            color: #7ecfcf;
            margin-bottom: 8px;
            font-weight: bold;
            letter-spacing: 0.05em;
        }
        .detail-toggle-group {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .detail-toggle {
            padding: 6px 14px;
            font-size: 13px;
            background: transparent;
            border: 1px solid #2a6660;
            color: #7ecfcf;
            border-radius: 20px;
            cursor: pointer;
            transition: 0.2s;
            width: auto; margin: 0;
        }
        .detail-toggle.on {
            background: #1a4a44;
            border-color: #3eeed2;
            color: #3eeed2;
            box-shadow: 0 0 6px #3eeed255;
        }
        .detail-toggle:not(.on):hover { background: #1a3333; }
        .detail-stat-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .detail-stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }
        .detail-stat-item label {
            font-size: 11px;
            color: #7ecfcf;
            font-weight: bold;
        }
        .detail-input {
            width: 80px;
            padding: 7px 4px;
            background: #0f0f0f;
            border: 1px solid #3eeed2;
            border-radius: 8px;
            color: #b9fff7;
            text-align: center;
            font-size: 14px;
            box-sizing: border-box;
        }
        .detail-input:focus { border-color: #00ffe1; box-shadow: 0 0 8px #00ffe1; outline: none; }
    </style>
</head>
<body>

<div class="container">

    <!-- 세부 / 비교 탭 -->
    <div class="sub-tabs">
        <button class="sub-tab active" id="subtab-main" onclick="switchSubTab('main')">기록 계산기</button>
        <label class="detail-switch-wrap" onclick="toggleDetail()">
            <span class="detail-switch-label">세부</span>
            <div class="detail-switch" id="detail-switch">
                <div class="detail-switch-knob"></div>
            </div>
        </label>
        <button class="sub-tab" id="subtab-compare" onclick="switchSubTab('compare')">비교</button>
    </div>

    <!-- 메인 섹션 -->
    <div id="section-main">
    <div class="title-wrapper">
        <h1 id="mainTitle">OPS 등급 계산기</h1>
        <div class="info-icon" onclick="toggleTooltip(event)" onmouseenter="hoverTooltip(true)" onmouseleave="hoverTooltip(false)">
            ?
            <div class="info-tooltip" id="tooltip">
                <!-- 타자 툴팁 (기본) -->
                <div id="tt-batter">
                    <span class="t-ss">SS (1.050)</span> : 역사에 남을 만한 시즌<br>
                    <span class="t-s">S+ (1.000)</span> : MVP급 시즌<br>
                    <span class="t-s">S (0.950)</span> : 리그 최상위권<br>
                    <span class="t-a">A+ (0.900)</span> : 리그 상위권<br>
                    <span class="t-a">A (0.850)</span> : 훌륭한 시즌<br>
                    <span class="t-b">B+ (0.800)</span> : 좋은 시즌<br>
                    <span class="t-b">B (0.750)</span> : 평균적인 지표<br>
                    <span class="t-c">C+ (0.700)</span> : 수비형 선수의 하한선<br>
                    <span class="t-c">C (0.650)</span> : 아쉬운 시즌<br>
                    <span class="t-d">D (0.600↓)</span> : 최악의 시즌
                </div>
                <!-- 선발 툴팁 -->
                <div id="tt-starter" style="display:none;">
                    <b style="color:#9efcff;">선발 ERA 기준</b><br>
                    <span class="t-ss">SS (1.80↓)</span> : 역사에 남을 시즌<br>
                    <span class="t-s">S+ (2.50↓)</span> : 에이스 중의 에이스<br>
                    <span class="t-s">S (3.00↓)</span> : 리그 최상위 선발<br>
                    <span class="t-a">A+ (3.50↓)</span> : 리그 상위권<br>
                    <span class="t-a">A (4.00↓)</span> : 훌륭한 선발<br>
                    <span class="t-b">B+ (4.50↓)</span> : 좋은 선발<br>
                    <span class="t-b">B (5.00↓)</span> : 평균적인 선발<br>
                    <span class="t-c">C+ (5.50↓)</span> : 아쉬운 선발<br>
                    <span class="t-c">C (6.00↓)</span> : 불안정한 선발<br>
                    <span class="t-d">D (6.00↑)</span> : 최악의 시즌
                </div>
                <!-- 불펜 툴팁 -->
                <div id="tt-bullpen" style="display:none;">
                    <b style="color:#9efcff;">불펜 ERA 기준</b><br>
                    <span class="t-ss">SS (1.50↓)</span> : 역사에 남을 시즌<br>
                    <span class="t-s">S+ (2.20↓)</span> : 압도적인 불펜<br>
                    <span class="t-s">S (2.80↓)</span> : 리그 최상위 불펜<br>
                    <span class="t-a">A+ (3.20↓)</span> : 리그 상위권<br>
                    <span class="t-a">A (3.80↓)</span> : 훌륭한 불펜<br>
                    <span class="t-b">B+ (4.30↓)</span> : 좋은 불펜<br>
                    <span class="t-b">B (4.80↓)</span> : 평균적인 불펜<br>
                    <span class="t-c">C+ (5.50↓)</span> : 아쉬운 불펜<br>
                    <span class="t-c">C (6.50↓)</span> : 불안정한 불펜<br>
                    <span class="t-d">D (6.50↑)</span> : 최악의 시즌
                </div>
                <!-- 마무리 툴팁 -->
                <div id="tt-closer" style="display:none;">
                    <b style="color:#9efcff;">마무리 ERA 기준</b><br>
                    <span class="t-ss">SS (1.20↓)</span> : 역사에 남을 시즌<br>
                    <span class="t-s">S+ (1.80↓)</span> : 압도적인 마무리<br>
                    <span class="t-s">S (2.50↓)</span> : 리그 최상위 마무리<br>
                    <span class="t-a">A+ (3.00↓)</span> : 리그 상위권<br>
                    <span class="t-a">A (3.50↓)</span> : 훌륭한 마무리<br>
                    <span class="t-b">B+ (4.00↓)</span> : 좋은 마무리<br>
                    <span class="t-b">B (4.80↓)</span> : 평균적인 마무리<br>
                    <span class="t-c">C+ (5.50↓)</span> : 아쉬운 마무리<br>
                    <span class="t-c">C (6.50↓)</span> : 불안정한 마무리<br>
                    <span class="t-d">D (6.50↑)</span> : 최악의 시즌
                </div>
            </div>
        </div>
    </div>

    <!-- 타자/투수 탭 -->
    <div class="mode-tabs">
        <button class="mode-tab active" id="tab-batter" onclick="switchMode('batter')">⚾ 타자</button>
        <button class="mode-tab" id="tab-pitcher" onclick="switchMode('pitcher')">🥎 투수</button>
    </div>

    <div id="batter-keyhint" class="key-hint">
        <kbd>↑</kbd> <kbd>↓</kbd> 또는 🖱️ 휠로 값 0.001 조절 &nbsp;|&nbsp; <kbd>Enter</kbd> 계산
    </div>

    <div id="batter-labels" class="labels">
        <div>타율</div><div>출루율</div><div>장타율</div>
    </div>
    <div id="batter-inputs" class="inputs">
        <div class="input-wrapper" id="wrap-avg">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'avg',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
            <input id="avg" type="text" placeholder=".000">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'avg',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
        </div>
        <div class="input-wrapper" id="wrap-obp">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'obp',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
            <input id="obp" type="text" placeholder=".000">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'obp',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
        </div>
        <div class="input-wrapper" id="wrap-slg">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'slg',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
            <input id="slg" type="text" placeholder=".000">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'slg',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
        </div>
    </div>

    <!-- 타석 입력 -->
    <div id="batter-pa-row" style="margin-top:14px; display:flex; align-items:center; justify-content:center; gap:12px;">
        <label style="color:#9efcff; font-weight:bold; font-size:14px;">타석</label>
        <div class="input-wrapper" id="wrap-b-pa">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'b-pa',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
            <input id="b-pa" type="text" placeholder="0" style="width:100px; padding:8px; background:#0f0f0f; border:1px solid #3eeed2; border-radius:8px; color:#b9fff7; text-align:center; font-size:16px; box-sizing:border-box;">
            <button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'b-pa',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
        </div>
    </div>
    
    <button id="batter-calcbtn" class="calc-btn" onclick="calculate()">기록 계산하기</button>

    <!-- 투수 섹션 -->
    <div id="pitcherSection" style="display:none;">
        <!-- 투수 유형 선택 -->
        <div class="pitcher-tabs">
            <button class="pitcher-tab active" id="ptab-starter" onclick="switchPitcher('starter')">선발</button>
            <button class="pitcher-tab" id="ptab-bullpen" onclick="switchPitcher('bullpen')">불펜</button>
            <button class="pitcher-tab" id="ptab-closer" onclick="switchPitcher('closer')">마무리</button>
        </div>

        <!-- 4개 가로 나열: 공통(이닝,ERA) + 역할별 -->
        <div class="p-row-labels" id="p-row-labels">
            <div>이닝</div><div>ERA</div><div id="pl-3">승리</div><div id="pl-4">패배</div>
        </div>
        <div class="p-row-inputs" id="p-row-inputs">
            <!-- 이닝 -->
            <div class="input-wrapper">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'p-innings',0.1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
                <input id="p-innings" type="text" placeholder="0.0" class="p-field-input">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'p-innings',-0.1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
            </div>
            <!-- ERA -->
            <div class="input-wrapper">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'p-era',0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
                <input id="p-era" type="text" placeholder="0.00" class="p-field-input">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'p-era',-0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
            </div>
            <!-- 역할별 3번째 칸 -->
            <div class="input-wrapper">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" id="pbtn-up3" onmousedown="stepPRole(event,3,1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
                <input id="p-field3" type="text" placeholder="0" class="p-field-input">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" id="pbtn-dn3" onmousedown="stepPRole(event,3,-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
            </div>
            <!-- 역할별 4번째 칸 -->
            <div class="input-wrapper">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" id="pbtn-up4" onmousedown="stepPRole(event,4,1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
                <input id="p-field4" type="text" placeholder="0" class="p-field-input">
                <button class="arrow-btn p-arrowbtn" tabindex="-1" id="pbtn-dn4" onmousedown="stepPRole(event,4,-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
            </div>
        </div>

        <!-- 출장경기 / 팀경기 -->
        <div style="margin-top:14px; display:flex; align-items:center; justify-content:center; gap:20px;">
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
                <label style="color:#9efcff; font-weight:bold; font-size:13px;">출장 경기</label>
                <div class="input-wrapper" id="wrap-p-games">
                    <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepInt(event,'p-games',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
                    <input id="p-games" type="text" placeholder="0" style="width:90px; padding:8px; background:#0f0f0f; border:1px solid #3eeed2; border-radius:8px; color:#b9fff7; text-align:center; font-size:16px; box-sizing:border-box;">
                    <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepInt(event,'p-games',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
                </div>
            </div>
            <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
                <label style="color:#9efcff; font-weight:bold; font-size:13px;">팀 경기</label>
                <div class="input-wrapper" id="wrap-p-teamgames">
                    <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepInt(event,'p-teamgames',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button>
                    <input id="p-teamgames" type="text" placeholder="0" style="width:90px; padding:8px; background:#0f0f0f; border:1px solid #3eeed2; border-radius:8px; color:#b9fff7; text-align:center; font-size:16px; box-sizing:border-box;">
                    <button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepInt(event,'p-teamgames',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button>
                </div>
            </div>
        </div>

        <div id="p-games-warn" style="display:none; margin-top:6px; font-size:12px; color:#ff9b9b; opacity:1;">
            출장경기는 팀경기보다 적어야합니다!
        </div>

        <button class="calc-btn" onclick="calculatePitcher()">기록 계산하기</button>
        <p id="p-error" style="color:#ff9b9b; margin-top:15px; font-weight:bold;"></p>
        <div id="p-resultBox" class="result-box" style="display:none;">
            <p style="font-size:15px; margin:0; opacity:0.7;" id="p-resultLabel">ERA 등급</p>
            <span id="p-era-display" style="font-size:26px; font-weight:bold;"></span>
            <div class="grade" id="p-grade"></div>
            <div id="p-stats" style="margin-top:12px; font-size:14px; opacity:0.8; line-height:2;"></div>
        </div>
        <div id="p-overuse-warn" style="display:none; margin-top:10px; font-size:13px; color:#ffcc80; font-style:italic;">
            ⚠️ 혹사의 우려가 있습니다. 휴식이 필요합니다.
        </div>
    </div>

    <p id="error"></p>
    <div id="resultBox" class="result-box">
        <p style="font-size: 18px; margin:0; opacity: 0.8;">최종 OPS</p>
        <span id="ops" style="font-size: 26px; font-weight: bold;"></span>
        <div class="grade" id="grade"></div>
    </div>

    <div id="stageSection" style="display:none; margin-top: 20px;">
        <div class="stage-row">
            <span class="stage-label">타율</span>
            <div class="stage-dots" id="stage-avg"></div>
            <span class="stage-num" id="stagenum-avg"></span>
        </div>
        <div class="stage-row">
            <span class="stage-label">출루율</span>
            <div class="stage-dots" id="stage-obp"></div>
            <span class="stage-num" id="stagenum-obp"></span>
        </div>
        <div class="stage-row">
            <span class="stage-label">장타율</span>
            <div class="stage-dots" id="stage-slg"></div>
            <span class="stage-num" id="stagenum-slg"></span>
        </div>
    </div>
    <div id="specialMsg" style="display:none; margin-top: 14px; font-size: 14px; color: #ffb84d; font-style: italic; text-shadow: 0 0 8px #ffb84d88;"></div>
    <div id="obp-warn" style="display:none; margin-top: 10px; font-size: 13px; color: #fff9c4; opacity: 0.85;">
        ⚠️ 타율은 보통 출루율보다 값이 낮습니다. 기록을 재확인해주세요.
    </div>
    <div id="pa-warn" style="display:none; margin-top: 10px; font-size: 13px; font-style: italic;"></div>

    </div><!-- /section-main -->

    <!-- 세부 섹션 (토글 시 section-main과 교체) -->
    <div id="section-detail" style="display:none;">

        <!-- 타자 세부 -->
        <div id="detail-batter">
            <div class="detail-section-title">타자 세부 기록</div>
            <div class="detail-group-label">타선 위치</div>
            <div class="detail-toggle-group" style="margin-bottom:20px;">
                <button class="detail-toggle" id="dt-leadoff" data-group="batting-order" onclick="toggleDetailBtn('batting-order','leadoff')">테이블세터</button>
                <button class="detail-toggle" id="dt-cleanup" data-group="batting-order" onclick="toggleDetailBtn('batting-order','cleanup')">중심타선</button>
                <button class="detail-toggle" id="dt-lower" data-group="batting-order" onclick="toggleDetailBtn('batting-order','lower')">하위타선</button>
            </div>

            <div class="detail-labels"><div>타율</div><div>출루율</div><div>장타율</div></div>
            <div class="detail-row">
                <div class="input-wrapper" id="wrap-d-avg"><button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'d-avg',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-avg" type="text" placeholder=".000" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'d-avg',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-obp"><button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'d-obp',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-obp" type="text" placeholder=".000" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'d-obp',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-slg"><button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'d-slg',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-slg" type="text" placeholder=".000" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepValue(event,'d-slg',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <div class="detail-labels" style="margin-top:14px;"><div>홈런</div><div>타점</div><div>득점</div></div>
            <div class="detail-row">
                <div class="input-wrapper" id="wrap-d-hr"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-hr',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-hr" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-hr',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-rbi"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-rbi',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-rbi" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-rbi',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-r"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-r',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-r" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-r',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <div class="detail-labels" style="margin-top:14px;"><div>삼진</div><div>도루</div><div>도루실패</div></div>
            <div class="detail-row">
                <div class="input-wrapper" id="wrap-d-so"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-so',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-so" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-so',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-sb"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-sb',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-sb" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-sb',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-cs"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-cs',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-cs" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-cs',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <div class="detail-labels" style="margin-top:14px; justify-content:center;"><div style="flex:0 0 calc(33% - 7px); text-align:center;">타석</div></div>
            <div class="detail-row" style="justify-content:center;">
                <div class="input-wrapper" id="wrap-d-pa" style="flex:0 0 calc(33% - 7px);"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-pa',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-pa" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-pa',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <button class="calc-btn" style="margin-top:24px;" onclick="calculateDetail()">기록 계산하기</button>
            <p id="detail-error" style="color:#ff9b9b; margin-top:12px; font-weight:bold;"></p>
            <div id="detail-result" class="result-box" style="display:none; margin-top:16px;">
                <p style="font-size:15px; margin:0; opacity:0.7;">최종 OPS</p>
                <span id="detail-ops" style="font-size:26px; font-weight:bold;"></span>
                <div class="grade" id="detail-grade"></div>
                <div id="detail-extra" style="margin-top:10px; font-size:13px; opacity:0.8; line-height:1.9;"></div>
            </div>
        </div>

        <!-- 투수 세부 -->
        <div id="detail-pitcher" style="display:none;">
            <div class="detail-section-title">투수 세부 기록</div>
            <div class="detail-group-label">투구폼</div>
            <div class="detail-toggle-group" style="margin-bottom:12px;">
                <button class="detail-toggle" id="dt-over" data-group="pitch-form" onclick="toggleDetailBtn('pitch-form','over')">오버스로</button>
                <button class="detail-toggle" id="dt-three" data-group="pitch-form" onclick="toggleDetailBtn('pitch-form','three')">쓰리쿼터</button>
                <button class="detail-toggle" id="dt-side" data-group="pitch-form" onclick="toggleDetailBtn('pitch-form','side')">사이드암</button>
                <button class="detail-toggle" id="dt-under" data-group="pitch-form" onclick="toggleDetailBtn('pitch-form','under')">언더스로</button>
            </div>
            <div class="detail-group-label">투구 방향</div>
            <div class="detail-toggle-group" style="margin-bottom:20px;">
                <button class="detail-toggle" id="dt-lefty" data-group="handedness" onclick="toggleDetailBtn('handedness','lefty')">좌완</button>
                <button class="detail-toggle" id="dt-righty" data-group="handedness" onclick="toggleDetailBtn('handedness','righty')">우완</button>
            </div>

            <div class="detail-labels"><div>이닝</div><div>승리</div><div>패배</div></div>
            <div class="detail-row">
                <div class="input-wrapper" id="wrap-d-ip"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-ip',0.1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-ip" type="text" placeholder="0.0" class="detail-field-input"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-ip',-0.1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-win"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-win',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-win" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-win',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-loss"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-loss',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-loss" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-loss',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <div class="detail-labels" style="margin-top:14px;"><div>ERA</div><div>WHIP</div><div>FIP</div></div>
            <div class="detail-row">
                <div class="input-wrapper" id="wrap-d-era"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-era',0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-era" type="text" placeholder="0.00" class="detail-field-input"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-era',-0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-whip"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-whip',0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-whip" type="text" placeholder="0.00" class="detail-field-input"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-whip',-0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-fip"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-fip',0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-fip" type="text" placeholder="0.00" class="detail-field-input"><button class="arrow-btn p-arrowbtn" tabindex="-1" onmousedown="stepPValue(event,'d-fip',-0.01)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <div class="detail-labels" style="margin-top:14px;"><div>탈삼진</div><div>볼넷</div><div>피안타</div></div>
            <div class="detail-row">
                <div class="input-wrapper" id="wrap-d-k"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-k',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-k" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-k',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-bb"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-bb',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-bb" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-bb',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-h"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-h',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-h" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-h',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <div class="detail-labels" style="margin-top:14px; justify-content:center; gap:10px;"><div style="flex:0 0 calc(33% - 7px); text-align:center;">출장경기</div><div style="flex:0 0 calc(33% - 7px); text-align:center;">팀경기</div></div>
            <div class="detail-row" style="justify-content:center; gap:10px;">
                <div class="input-wrapper" id="wrap-d-games" style="flex:0 0 calc(33% - 7px);"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-games',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-games" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-games',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
                <div class="input-wrapper" id="wrap-d-teamgames" style="flex:0 0 calc(33% - 7px);"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-teamgames',1)" onmouseup="stopStep()" onmouseleave="stopStep()">▲</button><input id="d-teamgames" type="text" placeholder="0" class="detail-field-input"><button class="arrow-btn" tabindex="-1" onmousedown="stepInt(event,'d-teamgames',-1)" onmouseup="stopStep()" onmouseleave="stopStep()">▼</button></div>
            </div>

            <button class="calc-btn" style="margin-top:24px;" onclick="calculateDetailPitcher()">기록 계산하기</button>
            <p id="detail-p-error" style="color:#ff9b9b; margin-top:12px; font-weight:bold;"></p>
            <div id="detail-p-result" class="result-box" style="display:none; margin-top:16px;">
                <p style="font-size:15px; margin:0; opacity:0.7;" id="detail-p-label">ERA 등급</p>
                <span id="detail-p-era" style="font-size:26px; font-weight:bold;"></span>
                <div class="grade" id="detail-p-grade"></div>
                <div id="detail-p-extra" style="margin-top:10px; font-size:13px; opacity:0.8; line-height:1.9;"></div>
            </div>
        </div>

    </div><!-- /section-detail -->

    <!-- 비교 섹션 -->
    <div id="section-compare" style="display:none;">
        <div class="compare-wrapper">
            <!-- 선수 A -->
            <div class="compare-player">
                <div class="compare-title">선수 A</div>
                <div class="compare-labels"><div>타율</div><div>출루율</div><div>장타율</div></div>
                <div class="compare-inputs">
                    <input id="cmp-a-avg" type="text" placeholder=".000" class="cmp-input">
                    <input id="cmp-a-obp" type="text" placeholder=".000" class="cmp-input">
                    <input id="cmp-a-slg" type="text" placeholder=".000" class="cmp-input">
                </div>
                <button class="calc-btn" style="margin-top:16px;" onclick="calculateCompare('a')">계산</button>
                <div id="cmp-a-result" class="result-box" style="display:none; margin-top:16px;">
                    <p style="font-size:15px; margin:0; opacity:0.7;">OPS</p>
                    <span id="cmp-a-ops" style="font-size:26px; font-weight:bold;"></span>
                    <div class="grade" id="cmp-a-grade"></div>
                </div>
                <p id="cmp-a-error" style="color:#ff9b9b; margin-top:10px; font-size:13px;"></p>
            </div>

            <div class="compare-divider">VS</div>

            <!-- 선수 B -->
            <div class="compare-player">
                <div class="compare-title">선수 B</div>
                <div class="compare-labels"><div>타율</div><div>출루율</div><div>장타율</div></div>
                <div class="compare-inputs">
                    <input id="cmp-b-avg" type="text" placeholder=".000" class="cmp-input">
                    <input id="cmp-b-obp" type="text" placeholder=".000" class="cmp-input">
                    <input id="cmp-b-slg" type="text" placeholder=".000" class="cmp-input">
                </div>
                <button class="calc-btn" style="margin-top:16px;" onclick="calculateCompare('b')">계산</button>
                <div id="cmp-b-result" class="result-box" style="display:none; margin-top:16px;">
                    <p style="font-size:15px; margin:0; opacity:0.7;">OPS</p>
                    <span id="cmp-b-ops" style="font-size:26px; font-weight:bold;"></span>
                    <div class="grade" id="cmp-b-grade"></div>
                </div>
                <p id="cmp-b-error" style="color:#ff9b9b; margin-top:10px; font-size:13px;"></p>
            </div>
        </div>
    </div>

</div>

<script>
    const inputIds = ["avg", "obp", "slg"];

    /* ── 툴팁: 호버시 표시, 클릭시 고정 ── */
    let tooltipPinned = false;

    function hoverTooltip(entering) {
        if (tooltipPinned) return;
        document.getElementById('tooltip').classList.toggle('show', entering);
    }

    function toggleTooltip(event) {
        event.stopPropagation();
        tooltipPinned = !tooltipPinned;
        document.getElementById('tooltip').classList.toggle('show', tooltipPinned);
        event.currentTarget.classList.toggle('pinned', tooltipPinned);
    }

    document.addEventListener('click', function(event) {
        if (!event.target.closest('.info-icon')) {
            tooltipPinned = false;
            document.getElementById('tooltip').classList.remove('show');
            document.querySelector('.info-icon').classList.remove('pinned');
        }
    });

    /* ── 포커스 래퍼 강조 ── */
    function setFocusedWrapper(id) {
        inputIds.forEach(i => {
            document.getElementById('wrap-' + i).classList.toggle('focused', i === id);
        });
    }

    inputIds.forEach(id => {
        const el = document.getElementById(id);

        el.addEventListener('focus', () => setFocusedWrapper(id));
        el.addEventListener('blur', () => {
            // 마우스로 화살표 버튼 클릭 시 blur 후 즉시 포커스 복귀 → 짧은 딜레이로 체크
            setTimeout(() => {
                if (!inputIds.some(i => document.getElementById(i) === document.activeElement)) {
                    setFocusedWrapper(null);
                }
            }, 150);
        });

        el.addEventListener('blur', function() { autoFormat(this); });

        let bKeyTimer = null;
        let bKeyInterval = null;

        el.addEventListener('keydown', function(e) {
            if (e.key === '-') { e.preventDefault(); return; }
            if (e.key === 'Enter') { calculate(); return; }
            if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
            if (bKeyTimer || bKeyInterval) return;
            e.preventDefault();
            const dir = e.key === 'ArrowUp' ? 1 : -1;
            changeValue(id, dir);
            bKeyTimer = setTimeout(() => {
                bKeyInterval = setInterval(() => changeValue(id, dir), 50);
            }, 400);
        });

        el.addEventListener('keyup', function(e) {
            if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
                clearTimeout(bKeyTimer);
                clearInterval(bKeyInterval);
                bKeyTimer = null;
                bKeyInterval = null;
            }
        });
    });

    /* ── 휠: 포커스된 입력창이면 커서 위치 무관 작동 ── */
    window.addEventListener('wheel', function(e) {
        const focused = inputIds.find(i => document.getElementById(i) === document.activeElement);
        if (!focused) return;
        e.preventDefault();
        changeValue(focused, e.deltaY < 0 ? 1 : -1);
    }, { passive: false });

    /* ── 단계 커트라인 (각 경계값: 이 값 이상이면 다음 단계) ── */
    const stageCuts = {
        avg: [0.241, 0.261, 0.281, 0.301, 0.355],
        obp: [0.301, 0.341, 0.366, 0.401, 0.444],
        slg: [0.321, 0.381, 0.421, 0.501, 0.633]
    };

    function getStage(id, val) {
        const cuts = stageCuts[id];
        let stage = 1;
        for (let i = 0; i < cuts.length; i++) {
            if (val >= cuts[i]) stage = i + 2; // 2~6
        }
        return stage; // 1~6 (6 = 5+단계)
    }

    function updateStage(id) {
        const val = parseFloat(document.getElementById(id).value) || 0;
        const stage = getStage(id, val);
        const container = document.getElementById('stage-' + id);
        const numEl = document.getElementById('stagenum-' + id);
        const isPlus = stage === 6;
        const displayStage = isPlus ? 5 : stage; // 칸은 항상 5개

        container.innerHTML = '';
        for (let i = 1; i <= 5; i++) {
            const dot = document.createElement('div');
            if (i <= displayStage) {
                dot.className = isPlus ? 'stage-dot active-plus' : 'stage-dot active-' + stage;
            } else {
                dot.className = 'stage-dot';
            }
            container.appendChild(dot);
        }
        numEl.textContent = isPlus ? '5+단계' : stage + '단계';
        numEl.className = 'stage-num sn-' + (isPlus ? 'plus' : stage);
    }

    /* ── 값 조절 공통 함수 ── */
    function changeValue(id, direction) {
        const el = document.getElementById(id);
        let val = parseFloat(el.value) || 0;
        val = Math.round((val + direction * 0.001) * 1000) / 1000;
        // slg는 최대 4, 나머지는 최대 1
        const isSlg = id === 'slg' || id === 'd-slg';
        val = Math.max(0, Math.min(isSlg ? 4 : 1, val));
        el.value = val.toFixed(3);
    }

    /* ── 세부 입력창 포커스/휠/키보드 ── */
    const detailDecIds = ['d-avg','d-obp','d-slg'];
    detailDecIds.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('focus', () => {
            const wrap = document.getElementById('wrap-' + id);
            if (wrap) wrap.classList.add('focused');
        });
        el.addEventListener('blur', () => {
            setTimeout(() => {
                const wrap = document.getElementById('wrap-' + id);
                if (wrap && document.activeElement !== el) wrap.classList.remove('focused');
            }, 150);
            autoFormat(el);
        });
        let dKeyTimer = null, dKeyInterval = null;
        el.addEventListener('keydown', e => {
            if (e.key === '-') { e.preventDefault(); return; }
            if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
            if (dKeyTimer || dKeyInterval) return;
            e.preventDefault();
            const dir = e.key === 'ArrowUp' ? 1 : -1;
            changeValue(id, dir);
            dKeyTimer = setTimeout(() => { dKeyInterval = setInterval(() => changeValue(id, dir), 50); }, 400);
        });
        el.addEventListener('keyup', e => {
            if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
                clearTimeout(dKeyTimer); clearInterval(dKeyInterval);
                dKeyTimer = null; dKeyInterval = null;
            }
        });
    });

    // 세부 .000 칸 휠 지원
    window.addEventListener('wheel', function(e) {
        const focused = detailDecIds.find(id => document.getElementById(id) === document.activeElement);
        if (!focused) return;
        e.preventDefault();
        changeValue(focused, e.deltaY < 0 ? 1 : -1);
    }, { passive: false });

    /* ── 화살표 버튼 꾹 누르기: 가속 지원 ── */
    let holdTimer = null;
    let holdInterval = null;
    let holdCount = 0;

    function stepValue(event, id, direction) {
        event.preventDefault();
        document.getElementById(id).focus();
        changeValue(id, direction);

        holdCount = 0;
        clearTimeout(holdTimer);
        clearInterval(holdInterval);

        holdTimer = setTimeout(() => {
            holdInterval = setInterval(() => {
                holdCount++;
                // 0.5초 후 빠르게, 2초 후 더 빠르게
                const speed = holdCount > 40 ? 5 : holdCount > 15 ? 3 : 1;
                for (let i = 0; i < speed; i++) changeValue(id, direction);
            }, 50);
        }, 400);
    }

    function stopStep() {
        clearTimeout(holdTimer);
        clearInterval(holdInterval);
        holdCount = 0;
    }

    document.addEventListener('mouseup', stopStep);
    document.addEventListener('mouseleave', stopStep);

    /* ── 정수 스텝 (타석/출장/팀경기 공통) ── */
    function getMax(id) {
        if (id === 'p-games') {
            const teamVal = parseInt(document.getElementById('p-teamgames').value);
            if (isNaN(teamVal) || teamVal === 0) return 0; // 팀경기 0이면 출장경기 못 올림
            return Math.min(144, teamVal);
        }
        return 144;
    }

    let gamesWarnTimer = null;
    function showGamesWarn() {
        const w = document.getElementById('p-games-warn');
        w.style.opacity = '1';
        w.style.display = 'block';
        clearTimeout(gamesWarnTimer);
        gamesWarnTimer = setTimeout(() => {
            w.style.transition = 'opacity 1s';
            w.style.opacity = '0';
            setTimeout(() => { w.style.display = 'none'; w.style.transition = ''; }, 1000);
        }, 1500);
    }

    function stepInt(event, id, dir) {
        event.preventDefault();
        const el = document.getElementById(id);
        el.focus();
        const max = getMax(id);
        const cur = parseInt(el.value) || 0;
        if (id === 'p-games' && dir > 0 && cur >= max) {
            showGamesWarn(); return;
        }
        el.value = Math.min(max, Math.max(0, cur + dir)).toString();
        if (id === 'p-games') gamesOriginal = parseInt(el.value) || null;
        if (id === 'p-teamgames') clampGames();

        holdCount = 0;
        clearTimeout(holdTimer);
        clearInterval(holdInterval);
        holdTimer = setTimeout(() => {
            holdInterval = setInterval(() => {
                holdCount++;
                const speed = holdCount > 40 ? 5 : holdCount > 15 ? 3 : 1;
                for (let i = 0; i < speed; i++) {
                    const m = getMax(id);
                    const c = parseInt(el.value) || 0;
                    if (id === 'p-games' && dir > 0 && c >= m) { showGamesWarn(); break; }
                    el.value = Math.min(m, Math.max(0, c + dir)).toString();
                    if (id === 'p-games') gamesOriginal = parseInt(el.value) || null;
                    if (id === 'p-teamgames') clampGames();
                }
            }, 50);
        }, 400);
    }

    // 출장경기 원래 값 기억 (팀경기가 다시 올라올 때 복원용)
    let gamesOriginal = null;

    // 팀경기가 바뀌면 출장경기를 즉시 clamp, 원래 값 복원
    function clampGames() {
        const gEl = document.getElementById('p-games');
        const tVal = parseInt(document.getElementById('p-teamgames').value);

        if (isNaN(tVal) || tVal === 0) {
            const cur = parseInt(gEl.value) || 0;
            if (cur > 0) {
                if (gamesOriginal === null) gamesOriginal = cur;
                gEl.value = '';
                showGamesWarn();
            }
            return;
        }

        const max = Math.min(144, tVal);
        const cur = parseInt(gEl.value) || 0;

        if (cur > max) {
            // 줄어드는 경우: 원래 값 기억하고 clamp
            if (gamesOriginal === null) gamesOriginal = cur;
            gEl.value = max.toString();
        } else if (gamesOriginal !== null && tVal >= gamesOriginal) {
            // 팀경기가 다시 올라와서 원래 값 이상이 되면 복원
            gEl.value = gamesOriginal.toString();
            gamesOriginal = null;
        } else if (gamesOriginal !== null && tVal > cur) {
            // 팀경기가 올라오는 중이지만 아직 원래 값 미만
            gEl.value = max.toString();
        }
    }

    // 타석/출장/팀경기 키보드+휠 이벤트
    ['b-pa','p-games','p-teamgames'].forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;

        el.addEventListener('focus', () => {
            const wrap = document.getElementById('wrap-' + id);
            if (wrap) wrap.classList.add('focused');
        });
        el.addEventListener('blur', () => {
            setTimeout(() => {
                const wrap = document.getElementById('wrap-' + id);
                if (wrap && document.activeElement !== el) wrap.classList.remove('focused');
            }, 150);
            let v = parseInt(el.value);
            if (isNaN(v) || v < 0) { el.value = ''; }
            else {
                v = Math.min(getMax(id), v);
                el.value = v.toString();
            }
            // 출장경기 직접 수정 시 원래 값 업데이트
            if (id === 'p-games') {
                gamesOriginal = parseInt(el.value) || null;
            }
            if (id === 'p-teamgames') clampGames();
        });
        el.addEventListener('keydown', e => {
            if (e.key === '-' || e.key === '.') { e.preventDefault(); return; }
        });

        // 키보드 ↑↓
        let kTimer = null, kInterval = null;
        el.addEventListener('keydown', e => {
            if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
            if (kTimer || kInterval) return;
            e.preventDefault();
            const dir = e.key === 'ArrowUp' ? 1 : -1;
            const step = () => {
                const m = getMax(id);
                const c = parseInt(el.value) || 0;
                if (id === 'p-games' && dir > 0 && c >= m) { showGamesWarn(); return; }
                el.value = Math.min(m, Math.max(0, c + dir)).toString();
                if (id === 'p-games') gamesOriginal = parseInt(el.value) || null;
                if (id === 'p-teamgames') clampGames();
            };
            step();
            kTimer = setTimeout(() => { kInterval = setInterval(step, 50); }, 400);
        });
        el.addEventListener('keyup', e => {
            if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
                clearTimeout(kTimer); clearInterval(kInterval);
                kTimer = null; kInterval = null;
            }
        });
    });

    // 타석/출장/팀경기 휠 이벤트
    window.addEventListener('wheel', function(e) {
        const intIds = ['b-pa','p-games','p-teamgames'];
        const focused = intIds.find(id => document.getElementById(id) === document.activeElement);
        if (!focused) return;
        e.preventDefault();
        const el = document.getElementById(focused);
        const dir = e.deltaY < 0 ? 1 : -1;
        const m = getMax(focused);
        const c = parseInt(el.value) || 0;
        if (focused === 'p-games' && dir > 0 && c >= m) { showGamesWarn(); return; }
        el.value = Math.min(m, Math.max(0, c + dir)).toString();
        if (focused === 'p-games') gamesOriginal = parseInt(el.value) || null;
        if (focused === 'p-teamgames') clampGames();
    }, { passive: false });

    /* ── 포맷 ── */
    function autoFormat(el) {
        let val = el.value.trim();
        if (val === "" || isNaN(val)) return;
        el.value = parseFloat(val).toFixed(3);
    }

    /* ── 등급 순서 (업그레이드용) ── */
    const gradeList = [
        ["D - 최악의 시즌",      "d"],
        ["C - 아쉬운 시즌",      "c"],
        ["C+ - 수비형 하한선",   "c"],
        ["B - 평균적인 지표",    "b"],
        ["B+ - 좋은 시즌",       "b"],
        ["A - 훌륭한 시즌",      "a"],
        ["A+ - 리그 상위권",     "a"],
        ["S - 리그 최상위권",    "s"],
        ["S+ - MVP급 시즌",      "s"],
        ["SS - 역사에 남을 시즌","ss"],
        ["SS+ - 미친 시즌",      "ss"],
    ];

    /* ── 등급 ── */
    function getGrade(ops) {
        if (ops >= 1.050) return gradeList[9];
        if (ops >= 1.000) return gradeList[8];
        if (ops >= 0.950) return gradeList[7];
        if (ops >= 0.900) return gradeList[6];
        if (ops >= 0.850) return gradeList[5];
        if (ops >= 0.800) return gradeList[4];
        if (ops >= 0.750) return gradeList[3];
        if (ops >= 0.700) return gradeList[2];
        if (ops >= 0.650) return gradeList[1];
        return gradeList[0];
    }

    /* ── 계산 ── */
    function calculate() {
        inputIds.forEach(id => autoFormat(document.getElementById(id)));
        let avg = parseFloat(document.getElementById("avg").value) || 0;
        let obp = parseFloat(document.getElementById("obp").value) || 0;
        let slg = parseFloat(document.getElementById("slg").value) || 0;

        let error = "";
        if (avg > 1 || obp > 1) error = "타율/출루율은 1을 넘을 수 없습니다.";
        else if (slg > 4) error = "장타율은 4를 넘을 수 없습니다.";
        else if (avg > slg) error = "타율이 장타율보다 높을 수 없습니다.";

        if (error !== "") {
            document.getElementById("error").innerHTML = error;
            document.getElementById("resultBox").style.display = "none";
            return;
        }

        document.getElementById("error").innerHTML = "";
        inputIds.forEach(id => updateStage(id));
        document.getElementById('stageSection').style.display = 'block';

        let ops = obp + slg;
        let [gradeText, gradeClass] = getGrade(ops);

        // 5+단계 개수 계산
        const plusCount = inputIds.filter(id => {
            const val = parseFloat(document.getElementById(id).value) || 0;
            return getStage(id, val) === 6;
        }).length;

        if (plusCount >= 2) {
            gradeText = "SS+ - 미친 시즌";
            gradeClass = "ss";
        } else if (plusCount === 1) {
            const idx = gradeList.findIndex(g => g[0] === gradeText);
            if (idx === gradeList.length - 1) {
                gradeText = "SS+ - 미친 시즌";
                gradeClass = "ss";
            } else {
                const upgraded = gradeList[idx + 1];
                gradeText = upgraded[0];
                gradeClass = upgraded[1];
            }
        }

        let box = document.getElementById("resultBox");
        const pa = parseInt(document.getElementById('b-pa').value) || 0;
        document.getElementById("ops").innerText = ops.toFixed(3);
        // grade는 아래 PA 처리에서 설정
        // 타석 표시
        let paHtml = pa ? `<div style="margin-top:8px; font-size:13px; opacity:0.7;">타석: <b>${pa}</b></div>` : '';
        const existingPaEl = document.getElementById('b-pa-display');
        if (existingPaEl) existingPaEl.remove();
        if (paHtml) {
            const paEl = document.createElement('div');
            paEl.id = 'b-pa-display';
            paEl.innerHTML = paHtml;
            box.appendChild(paEl);
        }
        box.className = "result-box " + gradeClass;
        box.style.display = "block";
        batterResultShown = true;

        // 타율 > 출루율 경고
        const obpWarnEl = document.getElementById('obp-warn');
        obpWarnEl.style.display = avg > obp ? 'block' : 'none';

        // 타석 표본 경고 및 등급 텍스트 페이스 처리
        const paWarnEl = document.getElementById('pa-warn');
        const underQuota = pa > 0 && pa < 447;
        if (underQuota) {
            paWarnEl.textContent = '⚠️ 규정타석이 아닙니다. 정보가 부정확할 수 있습니다.';
            paWarnEl.style.color = '#ffcc80';
            paWarnEl.style.display = 'block';
            // 등급 텍스트에 "페이스" 추가
            const gradeEl = document.getElementById("grade");
            gradeEl.innerText = gradeText + ' 페이스';
        } else {
            paWarnEl.style.display = 'none';
            document.getElementById("grade").innerText = gradeText;
        }
    }

    /* ── 투수 입력창 화살표 버튼 ── */
    // 이닝 유효값: 소수점이 0, .1, .2만 허용 (야구 이닝 규칙)
    function nextInnings(val, dir) {
        const whole = Math.floor(val);
        const dec = Math.round((val - whole) * 10); // 0, 1, 2
        let newDec = dec + dir;
        let newWhole = whole;
        if (newDec > 2) { newWhole += 1; newDec = 0; }
        else if (newDec < 0) { newWhole -= 1; newDec = 2; }
        newWhole = Math.max(0, newWhole);
        return parseFloat((newWhole + newDec * 0.1).toFixed(1));
    }

    function stepPValue(event, id, step) {
        event.preventDefault();
        document.getElementById(id).focus();
        const el = document.getElementById(id);

        function applyStep() {
            let val = parseFloat(el.value) || 0;
            let newVal;
            if (id === 'p-innings') {
                newVal = nextInnings(val, step > 0 ? 1 : -1);
                el.value = newVal.toFixed(1);
            } else if (Math.abs(step) < 1) {
                newVal = Math.max(0, Math.round((val + step) * 100) / 100);
                el.value = newVal.toFixed(2);
            } else {
                newVal = Math.max(0, Math.round(val + step));
                el.value = newVal.toString();
            }
        }

        applyStep();

        holdCount = 0;
        clearTimeout(holdTimer);
        clearInterval(holdInterval);
        holdTimer = setTimeout(() => {
            holdInterval = setInterval(() => {
                holdCount++;
                const speed = holdCount > 40 ? 5 : holdCount > 15 ? 3 : 1;
                for (let i = 0; i < speed; i++) applyStep();
            }, 50);
        }, 400);
    }

    /* ══════════════════════════════
       타자 / 투수 모드 전환
    ══════════════════════════════ */
    let currentMode = 'batter';
    let currentPitcherRole = 'starter';

    function updateTooltipContent(key) {
        ['batter','starter','bullpen','closer'].forEach(k => {
            document.getElementById('tt-' + k).style.display = k === key ? 'block' : 'none';
        });
    }

    let batterResultShown = false; // 타자 계산 결과가 보여진 적 있는지 추적

    function switchMode(mode) {
        currentMode = mode;
        const isBatter = mode === 'batter';

        document.getElementById('tab-batter').classList.toggle('active', isBatter);
        document.getElementById('tab-pitcher').classList.toggle('active', !isBatter);

        // 타자 UI 요소 (항상 show/hide)
        ['batter-keyhint','batter-labels','batter-inputs','batter-calcbtn','error','batter-pa-row'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = isBatter ? '' : 'none';
        });

        // 타자 결과/단계는 이전에 계산한 적 있을 때만 복원
        document.getElementById('resultBox').style.display  = (isBatter && batterResultShown) ? 'block' : 'none';
        document.getElementById('stageSection').style.display = (isBatter && batterResultShown) ? 'block' : 'none';
        document.getElementById('specialMsg').style.display = 'none';
        document.getElementById('obp-warn').style.display = 'none';

        document.getElementById('pitcherSection').style.display = isBatter ? 'none' : 'block';
        document.getElementById('mainTitle').textContent = isBatter ? 'OPS 등급 계산기' : '투수 등급 계산기';
        document.getElementById('p-resultBox').style.display = 'none';
        document.getElementById('p-error').textContent = '';

        updateTooltipContent(isBatter ? 'batter' : currentPitcherRole);
        updateDetailPanel();
    }

    // 역할별 3,4번째 필드 정보
    const roleFields = {
        starter: { l3: '승리', l4: '패배' },
        bullpen:  { l3: '홀드', l4: '패'   },
        closer:   { l3: '세이브', l4: '블론세이브' }
    };

    const roleValues = {
        starter: { innings: '', era: '', f3: '', f4: '', games: '', teamGames: '' },
        bullpen:  { innings: '', era: '', f3: '', f4: '', games: '', teamGames: '' },
        closer:   { innings: '', era: '', f3: '', f4: '', games: '', teamGames: '' }
    };

    function switchPitcher(role) {
        roleValues[currentPitcherRole].innings   = document.getElementById('p-innings').value;
        roleValues[currentPitcherRole].era       = document.getElementById('p-era').value;
        roleValues[currentPitcherRole].f3        = document.getElementById('p-field3').value;
        roleValues[currentPitcherRole].f4        = document.getElementById('p-field4').value;
        roleValues[currentPitcherRole].games     = document.getElementById('p-games').value;
        roleValues[currentPitcherRole].teamGames = document.getElementById('p-teamgames').value;

        currentPitcherRole = role;
        ['starter','bullpen','closer'].forEach(r => {
            document.getElementById('ptab-' + r).classList.toggle('active', r === role);
        });

        const rf = roleFields[role];
        document.getElementById('pl-3').textContent = rf.l3;
        document.getElementById('pl-4').textContent = rf.l4;

        document.getElementById('p-innings').value   = roleValues[role].innings;
        document.getElementById('p-era').value       = roleValues[role].era;
        document.getElementById('p-field3').value    = roleValues[role].f3;
        document.getElementById('p-field4').value    = roleValues[role].f4;
        document.getElementById('p-games').value     = roleValues[role].games;
        document.getElementById('p-teamgames').value = roleValues[role].teamGames;

        document.getElementById('p-resultBox').style.display = 'none';
        document.getElementById('p-error').textContent = '';
        updateTooltipContent(role);
        updateDetailPanel();
    }

    // 투수 단일 스텝 (휠 전용 - holdTimer 없음)
    function applyPitcherStep(pid, dir) {
        if (pid === 'p-innings') {
            const el = document.getElementById('p-innings');
            const val = parseFloat(el.value) || 0;
            el.value = nextInnings(val, dir).toFixed(1);
        } else if (pid === 'p-era') {
            const el = document.getElementById('p-era');
            const val = parseFloat(el.value) || 0;
            el.value = Math.max(0, Math.round((val + dir * 0.01) * 100) / 100).toFixed(2);
        } else {
            const el = document.getElementById(pid);
            el.value = Math.max(0, (parseInt(el.value) || 0) + dir).toString();
        }
    }

    // 투수 휠 지원
    window.addEventListener('wheel', function(e) {
        const active = document.activeElement;
        const pitcherInputs = ['p-innings','p-era','p-field3','p-field4'];
        const pid = pitcherInputs.find(id => document.getElementById(id) === active);
        if (!pid) return;
        e.preventDefault();
        const dir = e.deltaY < 0 ? 1 : -1;
        const targetId = (pid === 'p-field3' || pid === 'p-field4') ? pid : pid;
        applyPitcherStep(targetId, dir);
    }, { passive: false });

    // 투수 입력창 포커스 시 화살표 반짝임
    ['p-innings','p-era','p-field3','p-field4'].forEach(pid => {
        const el = document.getElementById(pid);
        if (!el) return;
        el.addEventListener('focus', () => {
            el.closest('.input-wrapper').classList.add('focused');
        });
        el.addEventListener('blur', () => {
            setTimeout(() => {
                if (document.activeElement !== el)
                    el.closest('.input-wrapper').classList.remove('focused');
            }, 150);

            // 이닝: .0/.1/.2 외 소수는 제거, 경고 표시 / "188 2/3" 형식 파싱
            if (pid === 'p-innings') {
                const raw = el.value.trim();
                const errEl = document.getElementById('p-error');

                // "숫자 1/3" 또는 "숫자 2/3" 형식 파싱
                const fracMatch = raw.match(/^(\d+)\s+(1|2)\/3$/);
                if (fracMatch) {
                    const whole = parseInt(fracMatch[1]);
                    const frac = parseInt(fracMatch[2]); // 1 or 2
                    el.value = (whole + frac * 0.1).toFixed(1);
                    errEl.textContent = '';
                    return;
                }

                const v = parseFloat(raw);
                if (!isNaN(v)) {
                    const whole = Math.floor(v);
                    const decRaw = Math.round((v - whole) * 10);
                    const isValid = decRaw === 0 || decRaw === 1 || decRaw === 2;
                    if (!isValid) {
                        errEl.textContent = '이닝은 .0, .1, .2 이닝만 가능합니다';
                        setTimeout(() => { if (errEl.textContent.includes('이닝')) errEl.textContent = ''; }, 3000);
                        el.value = whole.toFixed(1);
                    } else {
                        errEl.textContent = '';
                        el.value = v.toFixed(1);
                    }
                }
            }
            // ERA: 반올림 소수 2자리
            if (pid === 'p-era') {
                const v = parseFloat(el.value);
                if (!isNaN(v)) el.value = Math.max(0, v).toFixed(2);
            }
            // 승/패/홀드 등 정수
            if (pid === 'p-field3' || pid === 'p-field4') {
                const v = parseInt(el.value);
                el.value = isNaN(v) || v < 0 ? '' : v.toString();
            }
        });

        // 키보드 ↑↓로 값 조절 (keydown/keyup으로 누름 상태 관리)
        let keyHoldTimer = null;
        let keyHoldInterval = null;

        el.addEventListener('keydown', e => {
            if (e.key === '-') { e.preventDefault(); return; }
            if (pid === 'p-field3' || pid === 'p-field4') {
                if (e.key === '.') { e.preventDefault(); return; }
            }
            if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
            if (keyHoldTimer || keyHoldInterval) return; // 이미 누르고 있으면 무시
            e.preventDefault();

            const dir = e.key === 'ArrowUp' ? 1 : -1;
            function applyKey() {
                if (pid === 'p-innings') stepPValue({ preventDefault:()=>{} }, 'p-innings', dir * 0.1);
                else if (pid === 'p-era') stepPValue({ preventDefault:()=>{} }, 'p-era', dir * 0.01);
                else stepPRole({ preventDefault:()=>{} }, pid === 'p-field3' ? 3 : 4, dir);
            }

            applyKey();
            keyHoldTimer = setTimeout(() => {
                keyHoldInterval = setInterval(applyKey, 50);
            }, 400);
        });

        el.addEventListener('keyup', e => {
            if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
                clearTimeout(keyHoldTimer);
                clearInterval(keyHoldInterval);
                keyHoldTimer = null;
                keyHoldInterval = null;
            }
        });
    });

    // 역할별 3,4번 칸 step
    function stepPRole(event, col, dir) {
        event.preventDefault();
        const id = col === 3 ? 'p-field3' : 'p-field4';
        document.getElementById(id).focus();
        const el = document.getElementById(id);
        let val = Math.min(144, Math.max(0, Math.round((parseFloat(el.value) || 0) + dir)));
        el.value = val.toString();

        holdCount = 0;
        clearTimeout(holdTimer);
        clearInterval(holdInterval);
        holdTimer = setTimeout(() => {
            holdInterval = setInterval(() => {
                holdCount++;
                const speed = holdCount > 40 ? 5 : holdCount > 15 ? 3 : 1;
                for (let i = 0; i < speed; i++) {
                    el.value = Math.min(144, Math.max(0, (parseInt(el.value) || 0) + dir)).toString();
                }
            }, 50);
        }, 400);
    }

    /* ── 투수 ERA 등급 ── */
    function getPitcherGrade(era, role) {
        // 역할별 ERA 기준 다름
        const thresholds = {
            starter: [
                [1.80, "SS - 역사에 남을 시즌", "ss"],
                [2.50, "S+ - 에이스 중의 에이스", "s"],
                [3.00, "S - 리그 최상위 선발", "s"],
                [3.50, "A+ - 리그 상위권 선발", "a"],
                [4.00, "A - 훌륭한 선발", "a"],
                [4.50, "B+ - 좋은 선발", "b"],
                [5.00, "B - 평균적인 선발", "b"],
                [5.50, "C+ - 아쉬운 선발", "c"],
                [6.00, "C - 불안정한 선발", "c"],
            ],
            bullpen: [
                [1.50, "SS - 역사에 남을 시즌", "ss"],
                [2.20, "S+ - 압도적인 불펜", "s"],
                [2.80, "S - 리그 최상위 불펜", "s"],
                [3.20, "A+ - 리그 상위권 불펜", "a"],
                [3.80, "A - 훌륭한 불펜", "a"],
                [4.30, "B+ - 좋은 불펜", "b"],
                [4.80, "B - 평균적인 불펜", "b"],
                [5.50, "C+ - 아쉬운 불펜", "c"],
                [6.50, "C - 불안정한 불펜", "c"],
            ],
            closer: [
                [1.20, "SS - 역사에 남을 시즌", "ss"],
                [1.80, "S+ - 압도적인 마무리", "s"],
                [2.50, "S - 리그 최상위 마무리", "s"],
                [3.00, "A+ - 리그 상위권 마무리", "a"],
                [3.50, "A - 훌륭한 마무리", "a"],
                [4.00, "B+ - 좋은 마무리", "b"],
                [4.80, "B - 평균적인 마무리", "b"],
                [5.50, "C+ - 아쉬운 마무리", "c"],
                [6.50, "C - 불안정한 마무리", "c"],
            ]
        };
        const list = thresholds[role];
        for (let i = 0; i < list.length; i++) {
            if (era <= list[i][0]) return [list[i][1], list[i][2]];
        }
        return ["D - 최악의 시즌", "d"];
    }

    /* ── 투수 계산 ── */
    function calculatePitcher() {
        const innings  = parseFloat(document.getElementById('p-innings').value);
        const era      = parseFloat(document.getElementById('p-era').value);
        const gamesVal = document.getElementById('p-games').value.trim();
        const teamVal  = document.getElementById('p-teamgames').value.trim();
        const v3raw    = document.getElementById('p-field3').value.trim();
        const v4raw    = document.getElementById('p-field4').value.trim();
        const errEl    = document.getElementById('p-error');

        const games     = gamesVal !== '' ? parseInt(gamesVal) : null;
        const teamGames = teamVal  !== '' ? parseInt(teamVal)  : null;
        const v3num     = v3raw !== '' ? parseInt(v3raw) : null;
        const v4num     = v4raw !== '' ? parseInt(v4raw) : null;

        // ── 기본 유효성 검사 ──
        if (isNaN(innings) || isNaN(era)) { errEl.textContent = '이닝과 ERA를 입력해주세요.'; return; }
        if (era < 0) { errEl.textContent = 'ERA는 0 이상이어야 합니다.'; return; }

        // 출장경기 > 팀경기 체크
        if (games !== null && teamGames !== null && games > teamGames) {
            errEl.textContent = '출장 경기는 팀 경기를 초과할 수 없습니다.'; return;
        }

        // 개별 144 초과 체크
        if (games !== null && games > 144) { errEl.textContent = '출장 경기는 144를 넘을 수 없습니다.'; return; }
        if (teamGames !== null && teamGames > 144) { errEl.textContent = '팀 경기는 144를 넘을 수 없습니다.'; return; }
        if (v3num !== null && v3num > 144) { errEl.textContent = `${roleFields[currentPitcherRole].l3}은 144를 넘을 수 없습니다.`; return; }
        if (v4num !== null && v4num > 144) { errEl.textContent = `${roleFields[currentPitcherRole].l4}은 144를 넘을 수 없습니다.`; return; }

        // 선발: 승+패 ≤ 출장경기, 합계 ≤ 144
        if (currentPitcherRole === 'starter' && v3num !== null && v4num !== null) {
            if (v3num + v4num > 144) {
                errEl.textContent = `승리(${v3num}) + 패배(${v4num}) = ${v3num+v4num}이 144를 넘을 수 없습니다.`; return;
            }
            if (games !== null && v3num + v4num > games) {
                errEl.textContent = `승리(${v3num}) + 패배(${v4num}) = ${v3num+v4num}이 출장 경기(${games})를 초과할 수 없습니다.`; return;
            }
        }

        // 불펜: 홀드+패 ≤ 출장경기, 합계 ≤ 144
        if (currentPitcherRole === 'bullpen' && v3num !== null && v4num !== null) {
            if (v3num + v4num > 144) {
                errEl.textContent = `홀드(${v3num}) + 패(${v4num}) = ${v3num+v4num}이 144를 넘을 수 없습니다.`; return;
            }
            if (games !== null && v3num + v4num > games) {
                errEl.textContent = `홀드(${v3num}) + 패(${v4num}) = ${v3num+v4num}이 출장 경기(${games})를 초과할 수 없습니다.`; return;
            }
        }

        // 마무리: 세이브+블론세이브 합계 ≤ 144
        if (currentPitcherRole === 'closer' && v3num !== null && v4num !== null) {
            if (v3num + v4num > 144) {
                errEl.textContent = `세이브(${v3num}) + 블론세이브(${v4num}) = ${v3num+v4num}이 144를 넘을 수 없습니다.`; return;
            }
        }

        errEl.textContent = '';

        // ── 혹사 판단 (불펜/마무리) ──
        let overuse = false;
        if ((currentPitcherRole === 'bullpen' || currentPitcherRole === 'closer') && games !== null && teamGames !== null && teamGames > 0) {
            const ratio = games / teamGames; // 출장 비율
            // 이닝/출장경기 = 평균 이닝
            const avgInnings = games > 0 ? innings / games : 0;
            // 혹사 기준: 출장 비율 50% 이상이면서 평균 이닝 1.0 이상, 또는 출장 비율 70% 이상
            if (ratio >= 0.7 || (ratio >= 0.5 && avgInnings >= 1.0)) {
                overuse = true;
            }
        }

        document.getElementById('p-overuse-warn').style.display = overuse ? 'block' : 'none';

        // ── 결과 표시 ──
        let [gradeText, gradeClass] = getPitcherGrade(era, currentPitcherRole);
        const rf = roleFields[currentPitcherRole];
        const v3 = v3raw || '-';
        const v4 = v4raw || '-';

        let statsHtml = `이닝: <b>${innings.toFixed(1)}</b> &nbsp;|&nbsp; ERA: <b>${era.toFixed(2)}</b><br>`;
        statsHtml += `${rf.l3}: <b>${v3}</b> &nbsp;|&nbsp; ${rf.l4}: <b>${v4}</b>`;
        if (gamesVal || teamVal) {
            statsHtml += `<br>출장: <b>${gamesVal || '-'}</b>경기 &nbsp;|&nbsp; 팀: <b>${teamVal || '-'}</b>경기`;
        }

        const roleName = { starter: '선발', bullpen: '불펜', closer: '마무리' }[currentPitcherRole];
        document.getElementById('p-resultLabel').textContent = roleName + ' ERA 등급';
        document.getElementById('p-era-display').textContent = era.toFixed(2);
        document.getElementById('p-grade').textContent = gradeText;
        document.getElementById('p-stats').innerHTML = statsHtml;

        const box = document.getElementById('p-resultBox');
        box.className = 'result-box ' + gradeClass;
        box.style.display = 'block';
    }

    /* ── 서브탭 전환 ── */
    /* ── 세부 토글: section-main ↔ section-detail 교체 ── */
    let detailOpen = false;
    function toggleDetail() {
        detailOpen = !detailOpen;
        document.getElementById('section-main').style.display = detailOpen ? 'none' : '';
        document.getElementById('section-detail').style.display = detailOpen ? '' : 'none';
        // 비교 탭도 닫기
        if (detailOpen) {
            document.getElementById('section-compare').style.display = 'none';
            document.querySelector('.container').classList.remove('wide');
            document.getElementById('subtab-main').classList.remove('active');
        } else {
            document.getElementById('subtab-main').classList.add('active');
        }
        document.getElementById('detail-switch').classList.toggle('on', detailOpen);
        if (detailOpen) updateDetailPanel();
    }

    function switchSubTab(tab) {
        // 세부가 열려있으면 닫기
        if (detailOpen) {
            detailOpen = false;
            document.getElementById('section-detail').style.display = 'none';
            document.getElementById('detail-switch').classList.remove('on');
        }
        ['main','compare'].forEach(t => {
            document.getElementById('subtab-' + t)?.classList.toggle('active', t === tab);
            const sec = document.getElementById('section-' + t);
            if (sec) sec.style.display = t === tab ? '' : 'none';
        });
        document.querySelector('.container').classList.toggle('wide', tab === 'compare');
    }

    /* ── 세부 계산 (타자) ── */
    function calculateDetail() {
        const avg = parseFloat(document.getElementById('d-avg').value) || 0;
        const obp = parseFloat(document.getElementById('d-obp').value) || 0;
        const slg = parseFloat(document.getElementById('d-slg').value) || 0;
        const errEl = document.getElementById('detail-error');

        let error = '';
        if (avg > 1 || obp > 1) error = '타율/출루율은 1을 넘을 수 없습니다.';
        else if (slg > 4) error = '장타율은 4를 넘을 수 없습니다.';
        else if (avg > slg) error = '타율이 장타율보다 높을 수 없습니다.';
        if (error) { errEl.textContent = error; document.getElementById('detail-result').style.display='none'; return; }
        errEl.textContent = '';

        const ops = obp + slg;
        let [gradeText, gradeClass] = getGrade(ops);

        const plusCount = ['avg','obp','slg'].filter(id => {
            const cuts = stageCuts[id];
            const val = id==='avg'?avg:id==='obp'?obp:slg;
            let s=1; for(let i=0;i<cuts.length;i++) if(val>=cuts[i]) s=i+2;
            return s===6;
        }).length;
        if (plusCount >= 2) { gradeText="SS+ - 미친 시즌"; gradeClass="ss"; }
        else if (plusCount === 1) {
            const idx = gradeList.findIndex(g=>g[0]===gradeText);
            if (idx===gradeList.length-1) { gradeText="SS+ - 미친 시즌"; gradeClass="ss"; }
            else { [gradeText,gradeClass]=gradeList[idx+1]; }
        }

        const hr  = document.getElementById('d-hr').value;
        const rbi = document.getElementById('d-rbi').value;
        const so  = document.getElementById('d-so').value;
        const sb  = document.getElementById('d-sb').value;
        const cs  = document.getElementById('d-cs').value;
        const pa  = parseInt(document.getElementById('d-pa').value) || 0;

        let extra = `타율: <b>${avg.toFixed(3)}</b> &nbsp;|&nbsp; 출루율: <b>${obp.toFixed(3)}</b> &nbsp;|&nbsp; 장타율: <b>${slg.toFixed(3)}</b><br>`;
        if (hr)  extra += `홈런: <b>${hr}</b> &nbsp;`;
        if (rbi) extra += `타점: <b>${rbi}</b> &nbsp;`;
        if (so)  extra += `삼진: <b>${so}</b> &nbsp;`;
        if (sb||cs) extra += `<br>도루: <b>${sb||0}</b> &nbsp;|&nbsp; 도루실패: <b>${cs||0}</b>`;
        if (pa)  extra += `<br>타석: <b>${pa}</b>${pa<447?' <span style="color:#ffcc80;font-size:11px;">(규정타석 미달)</span>':''}`;

        const underQuota = pa > 0 && pa < 447;
        document.getElementById('detail-ops').textContent = ops.toFixed(3);
        document.getElementById('detail-grade').textContent = underQuota ? gradeText+' 페이스' : gradeText;
        document.getElementById('detail-extra').innerHTML = extra;
        const box = document.getElementById('detail-result');
        box.className = 'result-box ' + gradeClass;
        box.style.display = 'block';
    }

    /* ── 세부 계산 (투수) ── */
    function calculateDetailPitcher() {
        const era = parseFloat(document.getElementById('d-era').value);
        const errEl = document.getElementById('detail-p-error');
        if (isNaN(era)) { errEl.textContent = 'ERA를 입력해주세요.'; return; }
        errEl.textContent = '';

        const [gradeText, gradeClass] = getPitcherGrade(era, currentPitcherRole);
        const ip   = document.getElementById('d-ip').value;
        const whip = document.getElementById('d-whip').value;
        const k    = document.getElementById('d-k').value;
        const fip  = document.getElementById('d-fip').value;
        const bb   = document.getElementById('d-bb').value;
        const h    = document.getElementById('d-h').value;
        const form = detailSelections['pitch-form'];
        const hand = detailSelections['handedness'];

        let extra = '';
        if (hand) extra += `${hand==='lefty'?'좌완':'우완'} &nbsp;`;
        if (form) { const fn={'over':'오버스로','three':'쓰리쿼터','side':'사이드암','under':'언더스로'}; extra += fn[form]||''; }
        if (extra) extra += '<br>';
        if (ip)   extra += `이닝: <b>${ip}</b> &nbsp;`;
        if (whip) extra += `WHIP: <b>${whip}</b> &nbsp;`;
        if (k)    extra += `탈삼진: <b>${k}</b><br>`;
        if (fip)  extra += `FIP: <b>${fip}</b> &nbsp;`;
        if (bb)   extra += `볼넷: <b>${bb}</b> &nbsp;`;
        if (h)    extra += `피안타: <b>${h}</b>`;

        const roleName = {starter:'선발',bullpen:'불펜',closer:'마무리'}[currentPitcherRole];
        document.getElementById('detail-p-label').textContent = roleName + ' ERA 등급';
        document.getElementById('detail-p-era').textContent = era.toFixed(2);
        document.getElementById('detail-p-grade').textContent = gradeText;
        document.getElementById('detail-p-extra').innerHTML = extra;
        const box = document.getElementById('detail-p-result');
        box.className = 'result-box ' + gradeClass;
        box.style.display = 'block';
    }

    /* ── 세부 토글 버튼 (단일 선택) ── */
    const detailSelections = {};
    function toggleDetailBtn(group, key) {
        const isSame = detailSelections[group] === key;
        detailSelections[group] = isSame ? null : key;

        // 같은 그룹 버튼 전체 off
        document.querySelectorAll(`[id^="dt-"]`).forEach(el => {
            const elGroup = el.dataset.group;
            if (elGroup === group) el.classList.remove('on');
        });
        // 선택된 버튼만 on
        if (!isSame) {
            const btn = document.getElementById('dt-' + key);
            if (btn) btn.classList.add('on');
        }
    }

    // 세부 패널: 타자/투수 전환 연동
    function updateDetailPanel() {
        const isBatter = currentMode === 'batter';
        const role = currentPitcherRole;
        const db = document.getElementById('detail-batter');
        const dp = document.getElementById('detail-pitcher');
        const dbr = document.getElementById('detail-bullpen-role');
        if (db) db.style.display = isBatter ? 'block' : 'none';
        if (dp) dp.style.display = !isBatter ? 'block' : 'none';
        if (dbr) dbr.style.display = (!isBatter && role === 'bullpen') ? 'block' : 'none';
    }

    /* ── 비교 계산 ── */
    const cmpOps = { a: null, b: null };

    function calculateCompare(player) {
        const avg = parseFloat(document.getElementById(`cmp-${player}-avg`).value) || 0;
        const obp = parseFloat(document.getElementById(`cmp-${player}-obp`).value) || 0;
        const slg = parseFloat(document.getElementById(`cmp-${player}-slg`).value) || 0;
        const errEl = document.getElementById(`cmp-${player}-error`);

        let error = '';
        if (avg > 1 || obp > 1) error = '타율/출루율은 1을 넘을 수 없습니다.';
        else if (slg > 4) error = '장타율은 4를 넘을 수 없습니다.';
        else if (avg > slg) error = '타율이 장타율보다 높을 수 없습니다.';

        if (error) {
            errEl.textContent = error;
            document.getElementById(`cmp-${player}-result`).style.display = 'none';
            cmpOps[player] = null;
            updateStars();
            return;
        }
        errEl.textContent = '';

        const ops = obp + slg;
        const [gradeText, gradeClass] = getGrade(ops);
        cmpOps[player] = ops;

        document.getElementById(`cmp-${player}-ops`).textContent = ops.toFixed(3);
        document.getElementById(`cmp-${player}-grade`).textContent = gradeText;
        const result = document.getElementById(`cmp-${player}-result`);
        result.className = 'result-box ' + gradeClass;
        result.style.display = 'block';

        updateStars();
    }

    function updateStars() {
        ['a','b'].forEach(p => {
            const titleEl = document.querySelector(`#section-compare .compare-player:${p === 'a' ? 'first-child' : 'last-child'} .compare-title`);
            if (!titleEl) return;
            titleEl.textContent = p === 'a' ? '선수 A' : '선수 B';
        });

        if (cmpOps.a !== null && cmpOps.b !== null) {
            if (cmpOps.a > cmpOps.b) {
                setTitle('a', '선수 A ⭐');
                setTitle('b', '선수 B');
            } else if (cmpOps.b > cmpOps.a) {
                setTitle('a', '선수 A');
                setTitle('b', '선수 B ⭐');
            } else {
                setTitle('a', '선수 A ★');
                setTitle('b', '선수 B ★');
            }
        }
    }

    function setTitle(player, text) {
        const players = document.querySelectorAll('#section-compare .compare-player');
        const idx = player === 'a' ? 0 : 1;
        if (players[idx]) players[idx].querySelector('.compare-title').textContent = text;
    }
</script>

</body>
</html>