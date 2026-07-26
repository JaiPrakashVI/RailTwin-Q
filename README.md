# RailTwin-Q

> A Hybrid Quantum-AI Digital Twin for Intelligent Railway Traffic Optimization

![Python](https://img.shields.io/badge/Python-3.12-blue)
![HTML5/CSS3](https://img.shields.io/badge/HTML5/CSS3-Presentation-orange)
![Qiskit](https://img.shields.io/badge/Qiskit-Quantum-6929C4)
![License](https://img.shields.io/badge/License-MIT-yellow)

RailTwin-Q is a hybrid Quantum-AI platform that combines Digital Twin technology, Artificial Intelligence, and Quantum Optimization to improve railway traffic management. The system predicts delays, identifies congestion, optimizes train scheduling, and assists railway operators through intelligent decision support.

---

## Overview

RailTwin-Q provides a virtual representation of railway operations that continuously analyzes network conditions, predicts disruptions, and recommends optimized routing strategies. The platform combines machine learning models with hybrid quantum optimization techniques to address complex scheduling and routing challenges.

---

## Features

- Railway Digital Twin
- Train Delay Prediction
- Congestion Forecasting
- Receding-Horizon MPC Adaptive Control
- Hybrid Quantum Optimization (QAOA/QUBO)
- Intelligent Signal Recommendation
- Interactive Operations Dashboard
- Railway Network Simulation
- Performance Analytics

---

## Architecture

```text
                  Railway Operational Data
                            │
                            ▼
                  Data Processing Pipeline
                            │
                            ▼
                   Railway Digital Twin
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
Delay Prediction   Congestion Prediction   Decision Space
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
            Hybrid Quantum Optimization Engine
                  (QAOA / QUBO Scheduler)
                            │
                            ▼
              Decision Recommendation Engine
                            │
                            ▼
                 Operations Dashboard
```

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Core Simulation | Python 3.10 |
| AI Forecasting | XGBoost, NetworkX, Scikit-learn, Pandas, NumPy |
| Quantum Engine | Qiskit, QAOA Simulation, COBYLA Optimization |
| Closed-Loop Control | Receding-Horizon Control State Machine |
| Presentation | Static HTML5 / CSS3 / Vanilla JS Web Dashboards |

---

## Project Structure

```text
RailTwin-Q/
│
├── ai/
│   ├── delay_prediction/             # Layer 2: XGBoost delay models
│   ├── delay_propagation/            # Layer 3: NetworkX critical path & propagation graphs
│   ├── decision_space/               # Layer 4: Candidate action search spaces
│   ├── quantum_optimization/         # Layer 5: QUBO formulations & QAOA solvers
│   └── adaptive_control/             # Layer 6: Receding-horizon adaptive control loop
│
├── data/                             # Railway topology configuration and station layout parameters
├── datasets/                         # State snapshots, database files, and dashboard state logs
├── reports/                          # Generated HTML benchmark and timeline control reports
├── tests/                            # Automated closed-loop acceptance tests
├── requirements.txt                  # Python dependencies
├── main.py                           # Simulation execution orchestrator
└── README.md                         # Project documentation
```

---

## Workflow

1. Model railway network topology and timetable parameters.
2. Initialize the Digital Twin simulation state.
3. Formulate XGBoost delay projections and NetworkX propagation paths.
4. Dynamically compile candidate scheduling intervention actions.
5. Solve multi-objective QUBO matrices using classical baselines and simulated QAOA.
6. Actuate validated plans and evaluate real-time feedback loops.

---

## Project Roadmap

- [x] Layer 1: Digital Twin Simulator
- [x] Layer 2: AI Delay Prediction
- [x] Layer 3: AI Congestion Forecasting
- [x] Layer 4: Decision Intelligence Engine
- [x] Layer 5: Hybrid Quantum Optimization Engine
- [x] Layer 6: Receding-Horizon Adaptive Control (Validated in simulated environment)
- [ ] Real-world actuator hardware integration (Future Research Goal)
- [ ] Real-time physical system data streaming (Future Research Goal)

---

## Architecture Layers

RailTwin-Q operates as a hierarchical, closed-loop 6-layer system:
* **Layer 1**: Digital Twin Simulator
* **Layer 2**: Predict Delay (AI Prediction)
* **Layer 3**: Predict Congestion (Hierarchical Forecasts)
* **Layer 4**: Decision Intelligence Engine (Candidate Action Generation)
* **Layer 5**: Hybrid Quantum Optimization Engine (QUBO/QAOA Scheduler)
* **Layer 6**: **Receding-Horizon Adaptive Control & Autonomous Simulation Re-Optimization**

```text
Digital Twin State → Delay & Congestion Predictions → Decision Space Generation
       ▲                                                           │
       │                                                           ▼
Actuate Decisions ← Decision Quality Gate ← Warm-Started Optimization (QUBO)
```

---

## Layer 6: Receding-Horizon Adaptive Control

Layer 6 is implemented as an MPC-inspired receding-horizon adaptive control dispatcher demonstrating autonomous closed-loop control in a simulated Digital Twin environment:
- **State Monitor & Event Detector**: Evaluates active train status, average delays, platform utilization, and triggers alerts upon detecting disruptions (e.g. Weather Change, Signal Failure).
- **Trigger Engine**: Manages re-optimization cooldown boundaries (minimum 5 ticks) and maps severity-aware triggers (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), where high-severity alerts bypass cooldowns immediately.
- **Intervention Lifecycle Manager**: Enforces action statuses (`PROPOSED`, `VALIDATED`, `APPLIED`, `ACTIVE`, `FAILED`, `COMPLETED`, `EXPIRED`, `REVOKED`) to prevent duplicate actuator commands.
- **Warm-Start & Stability Manager**: Biases QAOA and SA solvers towards the previous optimal solution vector and applies switching cost penalties ($C_{\text{switch}} = P_{\text{switch}} \times |x_i - x_i^{\text{prev}}|$) to suppress optimization oscillations.
- **Decision Quality Gate**: Compares plan utility improvements against switching costs to only switch schedules when $\Delta \text{Utility} > \epsilon \approx 0.05$.
- **Outcome Feedback & Calibration Engine**: Tracks actual delay reduction errors and passes outcomes to closed-loop statistics.

---

## Research Focus & Verdict
RailTwin-Q investigates the integration of Digital Twin technology, Artificial Intelligence, and Hybrid Quantum Optimization to solve large-scale railway scheduling.
* **Quantum Verdict**: `Quantum Potential / No Demonstrated Quantum Advantage`. The architecture converts real railway intervention decisions into constrained binary variables (QUBO) solved by classical methods, Ideal QAOA, and Hybrid QAOA. While Hybrid QAOA recovers the exact classical optimum under noise, classical baselines yield lower execution runtimes at tested dimensions ($N \le 100$). RailTwin-Q demonstrates that Hybrid QAOA provides reliable optimum recovery and robustness against QAOA local minima, while quantum advantage was not observed at the tested problem sizes. Autonomous closed-loop control is demonstrated in a simulated Digital Twin environment; real-world deployment requires physical hardware actuator validation.

