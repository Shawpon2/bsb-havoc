<p align="center">
  <img src="https://github.com/Shawpon2/bsb-havoc/blob/main/1770169913749.png" width="180" style="border-radius:50%; border:5px solid #0EA5E9;" />
</p>
<p align="center">
  <img src="https://img.shields.io/badge/BSB-HAVOC-ff1a1a?style=for-the-badge&logo=apachekafka&logoColor=white" />
  <img src="https://img.shields.io/badge/ENGINE-Asynchronous-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PERFORMANCE-High_Throughput-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/PYTHON-3.7+-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/STATUS-Stable-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">⚡ BSB HAVOC</h1>
<h3 align="center">Professional Asynchronous Load Testing Framework</h3>

<p align="center">
  Built for Engineers • Designed for Scale • Optimized for Performance
</p>

---

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-performance-engine">Engine</a> •
  <a href="#-real-time-metrics">Metrics</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-cli-reference">CLI</a> •
  <a href="#-reports">Reports</a> •
  <a href="#-safety--legal">Legal</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## 🎯 Overview

**BSB Havoc** is a modern **asynchronous load testing engine** built to simulate real-world traffic patterns and measure system performance under pressure.

It provides **high concurrency**, **low resource overhead**, and **accurate performance analytics** — making it ideal for:

- API performance testing  
- Backend stress testing  
- Infrastructure benchmarking  
- CI/CD performance validation  

---

## ✨ Key Features

| Category | Capability | Benefit |
|---------|------------|---------|
| ⚡ Performance | Massive async concurrency | Realistic traffic simulation |
| 📊 Monitoring | Live RPS & latency tracking | Instant performance insight |
| 📈 Analytics | Percentiles & distributions | Deep performance visibility |
| 🛡 Control | Safe ramp-up & stop controls | Prevent accidental overload |
| 📁 Reporting | JSON export support | Easy integration with tools |

---

## ⚙ Performance Engine

BSB Havoc is powered by a **non-blocking async architecture**:

- Built using **asyncio** + **aiohttp**
- Efficient connection pooling  
- Persistent sessions for realistic load  
- Minimal CPU & memory footprint  

This allows high request throughput while keeping the testing environment stable.

---

## 📊 Real-Time Metrics

During a test run, the CLI dashboard displays:

- **Requests Per Second (RPS)**
- **Average / Min / Max Latency**
- **P50 / P90 / P95 / P99 Percentiles**
- **Success vs Failure Counts**
- **HTTP Status Code Distribution**

All metrics update live in the terminal.

---

## 📦 Installation

### Install from PyPI
```bash
pip install bsb-havoc --upgrade
```

### Install from Source
```bash
git clone https://github.com/Shawpon2/bsb-havoc.git
cd bsb-havoc
pip install -r requirements.txt
python setup.py install
```

### Verify Installation
```bash
bsb-havoc --version
```

---

## ⚡ Quick Start

Run a simple performance test against your **own test server**:

```bash
bsb-havoc https://your-server.com -c 500 -d 60
```

This will:
- Launch 500 concurrent virtual users  
- Run for 60 seconds  
- Show live performance metrics  

---

## 🛠 CLI Reference

| Option | Description |
|-------|-------------|
| `-c, --connections` | Number of concurrent users |
| `-d, --duration` | Test duration in seconds |
| `-t, --timeout` | Request timeout value |
| `--ramp` | Gradually increase load |
| `--output` | Export results to JSON |

---

## 🧪 Example Commands

### Standard Test
```bash
bsb-havoc https://staging.example.com -c 1000 -d 120
```

### Ramp-Up Mode
```bash
bsb-havoc https://api.example.com -c 3000 -d 180 --ramp
