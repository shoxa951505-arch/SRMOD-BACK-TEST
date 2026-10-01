from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import random

app = FastAPI(title="SRMOD Backtest Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/history")
def get_history(symbol: str = "XAUUSD", timeframe: str = "H1", limit: int = 2000):
    data = []
    t = 1451606400  # 2016-yil boshlanishi
    p = 1200.0      # Oltin boshlang'ich narxi
    
    for i in range(limit):
        change = (random.random() - 0.495) * 4.0
        c = p + change
        h = max(p, c) + random.random() * 2.0
        l = min(p, c) - random.random() * 2.0
        data.append({"time": t + i * 3600, "open": round(p, 2), "high": round(h, 2), "low": round(l, 2), "close": round(c, 2)})
        p = c
    return data

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>SRMOD Backtest Engine — Trading Platform</title>
        <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { background-color: #131722; color: #d1d4dc; font-family: sans-serif; overflow: hidden; }
            #header { height: 50px; background: #1e222d; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 1px solid #2a2e39; }
            .logo { font-size: 18px; font-weight: bold; color: #f0b90b; }
            button { background: #2962ff; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }
            #chart { width: 100vw; height: calc(100vh - 50px); }
        </style>
    </head>
    <body>
        <div id="header">
            <div class="logo">SRMOD TRADING PLATFORM</div>
            <button id="btn-replay">▶ Replay Play</button>
            <span id="status" style="color: #787b86;">Grafik yuklanmoqda...</span>
        </div>
        <div id="chart"></div>

        <script>
            const chart = LightweightCharts.createChart(document.getElementById('chart'), {
                layout: { backgroundColor: '#131722', textColor: '#d1d4dc' },
                grid: { vertLines: { color: '#2a2e39' }, horzLines: { color: '#2a2e39' } },
                timeScale: { timeVisible: true }
            });
            const series = chart.addCandlestickSeries({
                upColor: '#26a69a', downColor: '#ef5350',
                borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350'
            });

            let fullData = [];
            let currentIndex = 200;
            let timer = null;

            fetch('/api/v1/history?symbol=XAUUSD&limit=2000')
                .then(res => res.json())
                .then(data => {
                    fullData = data;
                    series.setData(fullData.slice(0, currentIndex));
                    document.getElementById('status').innerText = '10 Yillik Data Yuklandi (XAUUSD)';
                });

            document.getElementById('btn-replay').addEventListener('click', () => {
                if (timer) {
                    clearInterval(timer);
                    timer = null;
                    document.getElementById('btn-replay').innerText = '▶ Replay Play';
                } else {
                    document.getElementById('btn-replay').innerText = '⏸ Pauza';
                    timer = setInterval(() => {
                        if (currentIndex < fullData.length) {
                            series.update(fullData[currentIndex]);
                            currentIndex++;
                        }
                    }, 200);
                }
            });
        </script>
    </body>
    </html>
    """
