Perfect — here’s the regenerated and expanded `TODO.md` for
`stock-quant-arbitrage`, now reflecting the extended engine logic and **future
enhancements** you may want to explore later.

---

### ✅ `TODO.md` — `stock-quant-arbitrage`

```markdown
# 🧠 TODO – stock-quant-arbitrage

This module detects arbitrage opportunities between correlated instruments using
spread-based and statistical methods. It consumes market data via RabbitMQ or
SQS and emits actionable signals for downstream systems.

---

## 📦 Core Features

- [x] Vault-integrated configuration (`config.py`)
- [x] Message consumption from RabbitMQ or SQS
- [x] Rule-based and statistical arbitrage engine (`arbitrage_engine.py`)
- [x] Confidence scoring using z-score logic
- [x] Signal output via queue publisher (`queue_sender.py`)
- [x] Logging, exception handling, and retry-ready

---

## 🛠️ Implementation Tasks

### ⬜ Engine Enhancements

- [x] Z-score based mean reversion detection
- [x] Absolute spread threshold detection
- [x] Configurable lookback and thresholds
- [ ] Add support for multi-pair or batched analysis
- [ ] Add cross-instrument normalization (e.g., percent spread or log spread)
- [ ] Add `confidence` weighting factors to output schema
- [ ] Refactor engine for plug-and-play strategy modules

### ⬜ Input Handling

- [x] `queue_handler.py` integration
- [ ] Retry mechanism for transient errors (e.g., DLQ support)
- [ ] Batch polling or streaming input mode (optional)

### ⬜ Output Handling

- [x] Forward signals to downstream via RabbitMQ/SQS
- [ ] Write signals to a backing store (PostgreSQL, DynamoDB, S3)
- [ ] Forward high-confidence signals to notification or trade execution service

---

## 🧪 Testing & Validation

- [ ] Add unit tests for `arbitrage_engine.py`
- [ ] Add test harness for input/output queue simulation
- [ ] Add mock SQS and RabbitMQ fixtures
- [ ] Add validation for malformed payloads

---

## 🚀 Deployment & Ops

- [ ] Create `Dockerfile`
- [ ] Create `docker-compose.yml` for local queue testbed
- [ ] Add `Makefile` with common targets (run, test, format)
- [ ] Optional: Add ArgoCD manifests or Helm chart for Kubernetes deployment

---

## 📈 Observability

- [x] Info and debug-level logging
- [ ] Convert logs to structured JSON for ingestion into ELK/Loki/CloudWatch
- [ ] Emit basic metrics (signals per hour, error rate, confidence distribution)
- [ ] Add `/health` check endpoint if converted to API service

---

## 🔐 Security & Compliance

- [x] Uses Vault for secret management
- [ ] Validate all loaded Vault keys and fallbacks
- [ ] IAM roles with read-only secret access
- [ ] Add SLSA provenance + SBOM via CI/CD
- [ ] Add `safety`, `bandit`, `checkov` to dev dependencies

---

## 📚 Documentation

- [ ] Add usage example to `README.md`
- [ ] Document input and output JSON payload format
- [ ] Update `mkdocs.yml` and generate `docs/usage.md`

---

## 🧹 Code Quality

- [x] Pre-commit hooks configured (`ruff`, `black`, `pyright`)
- [ ] Add `deptry`, `safety`, `bandit` to `requirements-dev.in`
- [ ] Enable docstring validation and enforce function typing
- [ ] Add `check-pyproject` to validate metadata

---

## 🧩 Future Enhancements

### 🧪 Advanced Strategy Support

- [ ] Add Engle-Granger cointegration testing
- [ ] Add Johansen test support for multi-asset analysis
- [ ] Integrate ML-based arbitrage classifier (e.g., XGBoost, LSTM)

### 💡 Multi-leg Arbitrage

- [ ] Support triangular arbitrage across three instruments
- [ ] NAV-based arbitrage (ETF/crypto premium detection)

### ⏱️ Real-time Execution

- [ ] Add latency tracking and ingestion delay metrics
- [ ] Integrate with live WebSocket feeds or FIX gateway

---

_Last updated: {{ date }}_
```

---
