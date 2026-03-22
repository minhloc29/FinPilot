import { useEffect, useState } from "react";
import { TrendingUp, TrendingDown } from "lucide-react";

// ---- P&F ALGORITHM ----
function generatePointFigure(prices, boxSize = 50, reversal = 3) {
  if (!prices || prices.length === 0) return [];

  let columns = [];
  let currentColumn = [];

  let direction = null;
  let lastBoxPrice = Math.floor(prices[0] / boxSize) * boxSize;

  for (let i = 1; i < prices.length; i++) {
    const price = prices[i];

    if (!direction) {
      if (price >= lastBoxPrice + boxSize) {
        direction = "up";
        currentColumn.push("X");
        lastBoxPrice += boxSize;
      } else if (price <= lastBoxPrice - boxSize) {
        direction = "down";
        currentColumn.push("O");
        lastBoxPrice -= boxSize;
      }
      continue;
    }

    if (direction === "up") {
      while (price >= lastBoxPrice + boxSize) {
        currentColumn.push("X");
        lastBoxPrice += boxSize;
      }

      if (price <= lastBoxPrice - boxSize * reversal) {
        columns.push(currentColumn);
        currentColumn = [];
        direction = "down";

        lastBoxPrice -= boxSize;
        currentColumn.push("O");
      }
    } else {
      while (price <= lastBoxPrice - boxSize) {
        currentColumn.push("O");
        lastBoxPrice -= boxSize;
      }

      if (price >= lastBoxPrice + boxSize * reversal) {
        columns.push(currentColumn);
        currentColumn = [];
        direction = "up";

        lastBoxPrice += boxSize;
        currentColumn.push("X");
      }
    }
  }

  if (currentColumn.length) columns.push(currentColumn);
  return columns;
}

export default function MarketSection() {
  const [columns, setColumns] = useState([]);

  // ---- FETCH REAL DATA (BTC example) ----
  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(
          "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
        );
        const data = await res.json();

        const closes = data.map((d) => parseFloat(d[4])); // close price

        const pf = generatePointFigure(closes, 100, 3);
        setColumns(pf);
      } catch (err) {
        console.error(err);
      }
    }

    fetchData();
  }, []);

  const marketData = [
    { name: "Bitcoin", price: "$67,820", change: "+1.2%", up: true },
    { name: "Ethereum", price: "$3,420", change: "-0.6%", up: false },
    { name: "Apple", price: "$182.3", change: "+0.5%", up: true },
  ];

  return (
    <section className="w-full max-w-6xl mx-auto mb-24 px-6">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        
        {/* LEFT */}
        <div>
          <h2 className="text-3xl font-bold mb-4">
            Market Intelligence in Real Time
          </h2>

          <p className="text-gray-600 mb-6">
            Track key financial markets with AI-powered insights. Identify trends
            and react faster with intelligent signals.
          </p>

          <div className="space-y-4">
            {marketData.map((item, i) => (
              <div
                key={i}
                className="bg-white/70 backdrop-blur-md p-4 rounded-xl border border-white/40 flex justify-between items-center"
              >
                <div>
                  <p className="font-medium">{item.name}</p>
                  <p className="text-sm text-gray-500">{item.price}</p>
                </div>

                <div
                  className={`flex items-center gap-1 text-sm font-medium ${
                    item.up ? "text-green-600" : "text-red-600"
                  }`}
                >
                  {item.up ? (
                    <TrendingUp size={16} />
                  ) : (
                    <TrendingDown size={16} />
                  )}
                  {item.change}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 text-sm text-gray-600">
            AI signals indicate structured trend movement using Point & Figure
            analysis, filtering market noise and highlighting true breakouts.
          </div>
        </div>

        {/* RIGHT — REAL POINT & FIGURE */}
        <div className="bg-white/60 backdrop-blur-xl rounded-2xl p-6 shadow-lg border border-white/40 overflow-x-auto">
          
          <div className="flex items-end gap-3 h-[260px]">
            {columns.map((col, i) => (
              <div key={i} className="flex flex-col-reverse gap-1">
                {col.map((item, j) => (
                  <div
                    key={j}
                    className={`w-3 h-3 rounded-full ${
                      item === "X" ? "bg-green-500" : "bg-red-500"
                    }`}
                  />
                ))}
              </div>
            ))}
          </div>

        </div>
      </div>
    </section>
  );
}