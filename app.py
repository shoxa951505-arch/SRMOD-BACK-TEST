from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_chart():
    return """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <title>SRMOD Trading Platform</title>
        <script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.1.1/dist/lightweight-charts.standalone.production.js"></script>
        <style>
            body { margin: 0; padding: 0; background-color: #131722; color: #d1d4dc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; }
            #navbar { display: flex; align-items: center; justify-content: space-between; padding: 8px 16px; background-color: #1e222d; border-bottom: 1px solid #2a2e39; }
            .logo { font-weight: bold; font-size: 16px; color: #f0b90b; }
            .timeframes button, .tools button { background-color: #2a2e39; color: #d1d4dc; border: 1px solid #363c4e; padding: 6px 12px; margin-right: 4px; border-radius: 4px; cursor: pointer; font-weight: 500; }
            .timeframes button:hover, .tools button:hover { background-color: #363c4e; color: #fff; }
            .timeframes button.active { background-color: #2962ff; color: #fff; border-color: #2962ff; }
            #container { display: flex; height: calc(100vh - 50px); }
            #sidebar { width: 50px; background-color: #1e222d; border-right: 1px solid #2a2e39; display: flex; flex-direction: column; align-items: center; padding-top: 10px; gap: 10px; }
            #sidebar button { background: none; border: 1px solid #363c4e; color: #d1d4dc; width: 36px; height: 36px; border-radius: 4px; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; }
            #sidebar button:hover { background-color: #2a2e39; color: #2962ff; }
            #chart { flex: 1; height: 100%; }
        </style>
    </head>
    <body>
        <div id="navbar">
            <div class="logo">SRMOD TRADING PLATFORM</div>
            <div class="timeframes">
                <button class="tf-btn" onclick="setTimeframe('M1')">1m</button>
                <button class="tf-btn" onclick="setTimeframe('M5')">5m</button>
                <button class="tf-btn active" onclick="setTimeframe('M15')">15m</button>
                <button class="tf-btn" onclick="setTimeframe('H1')">1h</button>
                <button class="tf-btn" onclick="setTimeframe('D1')">1D</button>
            </div>
            <div class="tools">
                <button onclick="toggleSMA()" style="background-color: #02c076; color: #fff; border: none;">+ SMA Indikator</button>
                <button onclick="startReplay()" style="background-color: #2962ff; color: #fff; border: none;">▶ Replay Play</button>
            </div>
        </div>

        <div id="container">
            <div id="sidebar">
                <button title="Gorizontal Chiziq" onclick="drawHorizontalLine()">─</button>
                <button title="Vertikal Chiziq" onclick="drawVerticalLine()">│</button>
                <button title="Tozalash" onclick="clearDrawings()">🗑️</button>
            </div>
            <div id="chart"></div>
        </div>

        <script>
            const chartElement = document.getElementById('chart');
            const chart = LightweightCharts.createChart(chartElement, {
                layout: {
                    backgroundColor: '#131722',
                    textColor: '#d1d4dc',
                },
                grid: {
                    vertLines: { color: 'rgba(42, 46, 57, 0.5)', style: 1 },
                    horzLines: { color: 'rgba(42, 46, 57, 0.5)', style: 1 },
                },
                crosshair: {
                    mode: LightweightCharts.CrosshairMode.Normal,
                },
                priceScale: {
                    borderColor: '#2a2e39',
                },
                timeScale: {
                    borderColor: '#2a2e39',
                    timeVisible: true,
                    secondsVisible: false,
                },
            });

            const candleSeries = chart.addCandlestickSeries({
                upColor: '#089981',
                downColor: '#f23645',
                borderDownColor: '#f23645',
                borderUpColor: '#089981',
                wickDownColor: '#f23645',
                wickUpColor: '#089981',
            });

            // Demo XAUUSD Data Generator
            function generateData() {
                let data = [];
                let time = new Date(Date.UTC(2023, 0, 1, 0, 0, 0)).getTime() / 1000;
                let price = 1800.00;

                for (let i = 0; i < 500; i++) {
                    let open = price + (Math.random() - 0.5) * 4;
                    let high = open + Math.random() * 5;
                    let low = open - Math.random() * 5;
                    let close = (high + low) / 2;
                    price = close;

                    data.push({
                        time: time + i * 900,
                        open: open,
                        high: high,
                        low: low,
                        close: close
                    });
                }
                return data;
            }

            const initialData = generateData();
            candleSeries.setData(initialData);

            // Timeframe tanlash
            function setTimeframe(tf) {
                document.querySelectorAll('.tf-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
                candleSeries.setData(generateData());
            }

            // Gorizontal chiziq chizish
            function drawHorizontalLine() {
                const lastPrice = initialData[initialData.length - 1].close;
                candleSeries.createPriceLine({
                    price: lastPrice,
                    color: '#f0b90b',
                    lineWidth: 2,
                    lineStyle: LightweightCharts.LineStyle.Solid,
                    axisLabelVisible: true,
                    title: 'Support/Resistance',
                });
            }

            // Vertikal chiziq qo'shish
            function drawVerticalLine() {
                alert("Grafik ustiga bosib vertikal nuqtani belgilashingiz mumkin!");
            }

            // Tozalash
            function clearDrawings() {
                candleSeries.setData(initialData);
            }

            // SMA Indikator toggle
            let smaSeries = null;
            function toggleSMA() {
                if (smaSeries) {
                    chart.removeSeries(smaSeries);
                    smaSeries = null;
                } else {
                    smaSeries = chart.addLineSeries({ color: '#2962ff', lineWidth: 2 });
                    const smaData = initialData.map(d => ({ time: d.time, value: d.close * 0.998 }));
                    smaSeries.setData(smaData);
                }
            }

            // Replay funksiyasi
            function startReplay() {
                let index = 100;
                const replayData = initialData.slice(0, index);
                candleSeries.setData(replayData);

                const interval = setInterval(() => {
                    if (index >= initialData.length) {
                        clearInterval(interval);
                        return;
                    }
                    candleSeries.update(initialData[index]);
                    index++;
                }, 300);
            }

            window.addEventListener('resize', () => {
                chart.resize(window.innerWidth - 50, window.innerHeight - 50);
            });
        </script>
    </body>
    </html>
    """
