# 📊 stock-quant-arbitrage

Arbitrage detection module for evaluating pricing inefficiencies between
correlated financial instruments. This service consumes market data from
upstream pollers via RabbitMQ or SQS, applies rule-based and statistical logic,
and emits arbitrage signals to downstream consumers or trading systems.

---

## 🚀 Overview

This service is part of a broader stock market analysis pipeline. It listens for
price data pairs and analyzes whether they deviate from expected behavior —
using simple spread analysis and z-score-based mean reversion logic. When
significant deviations are detected, the module publishes a structured arbitrage
signal to a message queue for further action.

---

## 🧰 Features

- Vault-backed configuration
- RabbitMQ and SQS queue support
- Pluggable arbitrage detection logic
- Confidence scoring with z-scores
- Structured JSON output with optional logging
- Compatible with all `stock-*` data producers

---

## 📦 Example Use Case

A payload like:

```json
{
  "symbol_a": "AAPL",
  "symbol_b": "MSFT",
  "prices_a": [187.9, 188.3, 188.6, 188.4],
  "prices_b": [312.1, 312.3, 312.0, 312.2],
  "timestamp": "2025-05-18T14:32:00Z"
}
```

May result in:

```json
{
  "type": "arbitrage_signal",
  "symbol_a": "AAPL",
  "symbol_b": "MSFT",
  "avg_spread": 123.88,
  "z_score": 2.61,
  "confidence": "high",
  "timestamp": "2025-05-18T14:32:00Z"
}
```

---

## 🛠️ Installation

```bash
git clone https://github.com/YOUR_ORG/stock-quant-arbitrage.git
cd stock-quant-arbitrage

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Set the following via environment or Vault:

```bash
QUEUE_TYPE=rabbitmq
RABBITMQ_HOST=localhost
RABBITMQ_EXCHANGE=stock_arbitrage
RABBITMQ_ROUTING_KEY=arbitrage_opportunity
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

LOOKBACK_PERIOD=30
SPREAD_THRESHOLD=0.01
```

---

## 🧪 Running Locally

Start the service:

```bash
python -m app.main
```

---

## 🧪 Running Tests

```bash
make test      # Run pytest
make lint      # Check formatting
make coverage  # Run coverage report (if configured)
```

---

## 🐳 Docker (Optional)

```bash
docker build -t stock-quant-arbitrage .
docker run -e QUEUE_TYPE=rabbitmq stock-quant-arbitrage
```

---

## 📚 Documentation

If using MkDocs:

```bash
mkdocs serve
```

Edit documentation under the `docs/` directory.

---

## 👤 Authors

- **Mark Quinn** - [Mobious999](https://github.com/mobious999)
- **Jason Qualkenbush** - [CosmicQ](https://github.com/CosmicQ)

---

## 📄 License

Apache 2.0 License – see the `LICENSE` file.

---

## 🙏 Acknowledgments

- Thanks to upstream `stock-data-poller` and `stock-tech-*` contributors
- Inspired by real-world arbitrage use cases in equities, crypto, and ETFs
