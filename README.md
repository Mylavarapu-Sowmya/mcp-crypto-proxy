# 🚀 MCP – Market Crypto Proxy  
### **A Production-Grade Cryptocurrency Market Data Server (FastAPI + CCXT)**  
> **Final Internship Assignment — Completed & Extended**

---

## 📌 Overview  
MCP (Market Crypto Proxy) is a **Python-based FastAPI server** that provides **real-time** and **historical** cryptocurrency market data using CCXT.  
This implementation uses **Option B — Query Parameter API** (the industry‑standard style) and includes **all required features & advanced enhancements**.

---

## ✅ Core Features  
- Real-time ticker data  
- Historical OHLCV data  
- Market listings  
- WebSocket real-time updates  
- Error handling  
- Caching (TTL-based)  

---

## 🔥 Advanced Features  
| Feature | Description |
|--------|-------------|
| Rate Limiting | Token bucket per IP (60 req/min) |
| Retry Logic | Exponential backoff for CCXT failures |
| API Key Auth | Secure endpoints using `X-API-KEY` |
| TTL Caching | Faster responses for ticker & OHLCV |
| Logging Middleware | Structured request logs |
| Prometheus Metrics | `/metrics` endpoint |
| Pagination | `page` + `limit` for OHLCV |
| Docker Support | Dockerfile + docker-compose |
| GitHub Actions CI | Automated testing |
| React Frontend Demo | Basic interface to test API |

---

## 🛠 Tech Stack  
- FastAPI  
- Uvicorn  
- CCXT  
- CacheTools  
- Tenacity  
- Prometheus Client  
- React.js  
- Docker  
- GitHub Actions  
- PyTest  

---

## 📂 Project Structure  
```
mcp/
│── app.py
│── adapters.py
│── auth.py
│── cache.py
│── config.py
│── exceptions.py
│── metrics.py
│── middleware.py
│── ratelimit.py
│── retries.py
│── models.py
tests/
frontend/
config.yaml
requirements.txt
Dockerfile
docker-compose.yml
README.md
```

---

## ⚙️ Installation  
Create a virtual environment:
```
python -m venv venv
```

### Activate the virtualenv  
Windows:
```
venv\Scripts\activate
```
Mac/Linux:
```
source venv/bin/activate
```

### Install dependencies  
```
pip install -r requirements.txt
```

---

## ▶️ Run the Server  
Development (with auto-reload):
```
uvicorn mcp.app:app --reload --host 0.0.0.0 --port 8000
```
Note: use `--reload` only in development. For production, run without `--reload` and consider using a process manager.

Health check:
```
GET /health
```

---

## 🔑 API Key Authentication  
Add header:
```
X-API-KEY: demo-key-123
```
You can also store the key in a `.env` file and load it from `config.yaml` or environment variables for production.

Configure in `config.yaml`.

---

## 📡 API Usage

### ✔ Ticker  
```
GET /ticker?exchange=binance&symbol=BTC/USDT
```

### ✔ Historical (paginated)  
```
GET /historical?exchange=binance&symbol=BTC/USDT&limit=100&page=1
```

### ✔ Markets  
```
GET /markets?exchange=binance
```

### ✔ WebSocket  
```
ws://localhost:8000/ws?exchange=binance&symbol=BTC/USDT
```

---

## 🧪 Tests  
Run:
```
pytest -q
```

Mocked CCXT ensures reliable testing.

---

## 🐳 Docker  
Build and run with docker-compose:
```
docker-compose up --build
```
Service exposes port 8000 (adjust docker-compose as needed).

---

## 🖥 React Frontend  
```
cd frontend
npm install
npm start
```

---

## 🎯 Final Notes  
This project meets and extends the assignment expectations and demonstrates:  
- API design  
- Backend engineering  
- Reliability (retries, rate limit, caching)  
- DevOps (CI/CD, Docker)  
- Monitoring (Prometheus)  
- Full-stack ability (React UI)

---

