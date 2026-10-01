<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SRMOD Backtest Engine — 10 Yillik Bepul Grafillar</title>
    <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #131722; color: #d1d4dc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; overflow: hidden; }
        #header { height: 50px; background-color: #1e222d; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 1px solid #2a2e39; }
        .logo { font-size: 18px; font-weight: bold; color: #f0b90b; letter-spacing: 1px; }
        .controls { display: flex; gap: 10px; align-items: center; }
        button { background-color: #2962ff; color: #fff; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-weight: 600; font-size: 13px; transition: 0.2s; }
        button:hover { background-color: #1e53e5; }
        button.btn-sell { background-color: #ef5350; }
        button.btn-buy { background-color: #26a69a; }
        select { background: #2a2e39; color: #fff; border: none; padding: 6px 10px; border-radius: 4px; }
        #main-container { display: flex; height: calc(100vh - 50px); }
        #chart { flex: 1; height: 100%; }
        #sidebar { width: 280px; background: #1e222d; border-left: 1px solid #2a2e39; padding: 15px; display: flex; flex-direction: column; gap: 15px; }
        .card { background: #131722; border-radius: 6px; padding: 12px; border: 1px solid #2a2e39; }
        .card h4 { font-size: 12px; color: #787b86; margin-bottom: 8px; text-transform: uppercase; }
        .stat-val { font-size: 20px; font-weight: bold; }
    </style>
</head>
<body>

    <div id="header">
        <div class="logo">SRMOD TRADING PLATFORM</div>
        <div class="controls">
            <select id="pair-select">
                <option value="XAUUSD">XAUUSD (Oltin)</option>
                <option value="EURUSD">EURUSD</option>
            </select>
            <select id="tf-select">
                <option value="H1">H1 (1 Soat)</option>
                <option value="M15">M15 (15 Minut)</option>
                <option value="M5">M5 (5 Minut)</option>
            </select>
            <div style="width: 1px; height: 20px; background: #2a2e39; margin: 0 5px;"></div>
            <button id="btn-replay">▶ Replay Play</button>
            <button id="btn-next">⏭ Next Bar</button>
        </div>
        <div>
            <button class="btn-buy" id="btn-buy-order">+ BUY</button>
            <button class="btn-sell" id="btn-sell-order">- SELL</button>
        </div>
    </div>

    <div id="main-container">
        <div id="chart"></div>
        <div id="sidebar">
            <div class="card">
                <h4>Hisob Balansi</h4>
                <div class="stat-val" id="balance-val">$10,000.00</div>
            </div>
            <div class="card">
                <h4>Jami PnL (Foyda/Zarar)</h4>
                <div class="stat-val" style="color: #26a69a;" id="pnl-val">$0.00</div>
            </div>
            <div class="card">
                <h4>Ochiq Pozitsiyalar</h4>
                <div id="positions-list" style="font-size: 13px; color: #787b86;">Pozitsiya yo'q</div>
            </div>
        </div>
    </div>

    <script>
        const chart = LightweightCharts.createChart(document.getElementById('chart'), {
            layout: { backgroundColor: '#131722', textColor: '#d1d4dc' },
            grid: { vertLines: { color: '#1f2431' }, horzLines: { color: '#1f2431' } },
            crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
            timeScale: { timeVisible: true, secondsVisible: false }
        });

        const series = chart.addCandlestickSeries({
            upColor: '#26a69a', downColor: '#ef5350',
            borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350'
        });

        // Demo va Real API ulanishi
        async function loadChartData() {
            try {
                const res = await fetch('/api/v1/history?symbol=XAUUSD&timeframe=H1&limit=5000');
                const data = await res.json();
                if(data.length > 0) {
                    series.setData(data);
                } else {
                    // Test uchun generatsiya
                    generateDemo();
                }
            } catch (e) {
                generateDemo();
            }
        }

        function generateDemo() {
            let data = [];
            let t = new Date(2016, 0, 1).getTime() / 1000;
            let p = 1300.0;
            for(let i=0; i<3000; i++) {
                let c = p + (Math.random() - 0.495) * 5;
                let h = Math.max(p, c) + Math.random() * 2;
                let l = Math.min(p, c) - Math.random() * 2;
                data.push({ time: t + i*3600, open: p, high: h, low: l, close: c });
                p = c;
            }
            series.setData(data);
        }

        loadChartData();

        window.addEventListener('resize', () => {
            chart.resize(document.getElementById('chart').offsetWidth, document.getElementById('main-container').offsetHeight);
        });
    </script>
</body>
</html>
