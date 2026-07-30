# RailTwin-Q

> **A Hybrid Quantum-AI Digital Twin for Intelligent Railway Traffic Optimization**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![HTML5/CSS3](https://img.shields.io/badge/HTML5/CSS3-Presentation-orange)
![Qiskit](https://img.shields.io/badge/Qiskit-Quantum-6929C4)
![License](https://img.shields.io/badge/License-MIT-yellow)

RailTwin-Q is a **Hybrid Quantum-AI Digital Twin** platform designed to support intelligent railway traffic management. It integrates **Digital Twin technology, Artificial Intelligence, Machine Learning, Graph Analytics, and Hybrid Quantum Optimization** to predict delays, forecast congestion, optimize train dispatching, and provide explainable decision support for railway operators.

---

# Overview

RailTwin-Q maintains a real-time digital representation of a railway network, continuously monitoring operational conditions and simulating future system states.

The platform:

- Predicts train delays using AI.
- Forecasts network congestion.
- Generates candidate dispatch actions.
- Optimizes scheduling using Hybrid Quantum Optimization (QUBO + QAOA).
- Continuously re-optimizes through a closed-loop adaptive controller.
- Provides an interactive operations dashboard for railway controllers.

The project demonstrates how **Digital Twins, AI, and Quantum Computing** can be integrated into an intelligent railway traffic management system.

---

# Key Features

- 🚆 Railway Digital Twin Simulation
- 🤖 AI-Based Train Delay Prediction
- 📈 Hierarchical Congestion Forecasting
- ⚛️ Hybrid Quantum Optimization (QUBO + QAOA)
- 🔄 Receding-Horizon Adaptive Control
- 🚦 Intelligent Dispatch Recommendation Engine
- 🗺️ Railway Network Simulation
- 📊 Interactive Operations Dashboard
- 📉 Benchmark & Performance Analytics

---

# System Architecture

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
                 (QUBO + Hybrid QAOA)
                            │
                            ▼
             Decision Recommendation Engine
                            │
                            ▼
                Operations Dashboard
```

---

# Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python 3.12 |
| Machine Learning | XGBoost, Scikit-learn |
| Graph Analytics | NetworkX |
| Data Processing | Pandas, NumPy |
| Quantum Computing | Qiskit, QAOA, COBYLA |
| Digital Twin | Custom Railway Simulation Engine |
| Control System | Receding-Horizon Adaptive Control |
| Frontend | HTML5, CSS3, Vanilla JavaScript |

---

# Project Structure

```text
RailTwin-Q/
│
├── ai/
│   ├── delay_prediction/          # Layer 2: AI delay prediction
│   ├── delay_propagation/         # Layer 3: Delay propagation & graph analysis
│   ├── decision_space/            # Layer 4: Candidate dispatch generation
│   ├── quantum_optimization/      # Layer 5: QUBO & QAOA optimization
│   └── adaptive_control/          # Layer 6: Receding-horizon adaptive controller
│
├── data/                          # Railway topology & infrastructure
├── datasets/                      # Generated datasets & simulation snapshots
├── reports/                       # Benchmark & experiment reports
├── tests/                         # Automated validation tests
├── requirements.txt
├── main.py                        # Simulation entry point
└── README.md
```

---

# Workflow

1. Load the railway network topology and timetable.
2. Initialize the Digital Twin simulation.
3. Predict train delays using AI.
4. Forecast congestion using graph analytics.
5. Generate candidate dispatch actions.
6. Convert the optimization problem into a QUBO formulation.
7. Solve the QUBO using Hybrid QAOA and classical baselines.
8. Select the optimal dispatch strategy.
9. Apply the decision to the Digital Twin.
10. Monitor outcomes and continuously repeat the optimization cycle.

---

# Development Roadmap

- ✅ Layer 1 — Railway Digital Twin
- ✅ Layer 2 — AI Delay Prediction
- ✅ Layer 3 — Hierarchical Congestion Prediction
- ✅ Layer 4 — Decision Intelligence Engine
- ✅ Layer 5 — Hybrid Quantum Optimization
- ✅ Layer 6 — Receding-Horizon Adaptive Control (Simulation Validated)
- ⬜ Physical Railway Hardware Integration
- ⬜ Real-Time Railway Data Streaming

---

# Six-Layer Architecture

RailTwin-Q follows a hierarchical closed-loop architecture consisting of six computational layers.

| Layer | Description |
|--------|-------------|
| **Layer 1** | Railway Digital Twin |
| **Layer 2** | AI Delay Prediction |
| **Layer 3** | Hierarchical Congestion Prediction |
| **Layer 4** | Decision Intelligence Engine (Candidate Dispatch Generation) |
| **Layer 5** | Hybrid Quantum Optimization (QUBO + QAOA) |
| **Layer 6** | Receding-Horizon Adaptive Control & Continuous Re-Optimization |

---

## Overall Pipeline

```text
Railway Network
       │
       ▼
Digital Twin
       │
       ▼
Delay Prediction
       │
       ▼
Congestion Prediction
       │
       ▼
Candidate Dispatch Actions
       │
       ▼
QUBO Formulation
       │
       ▼
Hybrid QAOA Optimization
       │
       ▼
Optimal Dispatch Plan
       │
       ▼
Adaptive Controller
       │
       ▼
Digital Twin Feedback
       │
       └──────────────► Repeat
```

---

# Layer 6: Receding-Horizon Adaptive Control

Layer 6 implements an MPC-inspired receding-horizon adaptive controller that continuously monitors railway conditions and autonomously re-optimizes operations within the Digital Twin.

---

## 1. State Monitoring & Event Detection

The controller continuously monitors:

- Train positions
- Current delays
- Platform occupancy
- Track utilization
- Signal failures
- Weather events
- Infrastructure disruptions

Whenever an abnormal condition is detected, the optimization engine is triggered.

---

## 2. Trigger Engine

The controller categorizes disruptions into four severity levels:

- LOW
- MEDIUM
- HIGH
- CRITICAL

To prevent unnecessary optimization, a cooldown mechanism is applied.

Critical disruptions bypass the cooldown and trigger immediate optimization.

---

## 3. Intervention Lifecycle

Every dispatch recommendation follows a complete lifecycle.

```text
PROPOSED
    │
    ▼
VALIDATED
    │
    ▼
APPLIED
    │
    ▼
ACTIVE
    │
    ▼
COMPLETED
```

Additional terminal states include:

- FAILED
- EXPIRED
- REVOKED

This prevents duplicate or conflicting dispatch actions.

---

## 4. Warm-Start Optimization

Instead of restarting optimization from a random state, RailTwin-Q initializes the solver using the previous optimal solution.

Benefits include:

- Faster convergence
- Reduced optimization oscillation
- Greater schedule stability

A switching-cost penalty discourages unnecessary schedule changes.

\[
C_{switch}=P_{switch}\times|x_i-x_i^{previous}|
\]

---

## 5. Decision Quality Gate

A new dispatch strategy is accepted only if it provides a meaningful operational improvement.

\[
\Delta Utility>\epsilon
\]

where

\[
\epsilon \approx 0.05
\]

This prevents unnecessary switching between similar schedules.

---

## 6. Closed-Loop Feedback

After applying the optimized dispatch plan, RailTwin-Q evaluates:

- Delay reduction
- Congestion reduction
- Prediction accuracy
- Optimization quality
- Dispatch effectiveness

These metrics update the Digital Twin for the next optimization cycle.

---

# Candidate Dispatch Actions

When congestion or delays are detected, the Decision Intelligence Engine generates a set of candidate dispatch actions, including:

- Hold Train
- Platform Swap
- Speed Adjustment
- Route Diversion
- Schedule Maintenance (Fallback)

Each action is evaluated based on:

- Expected delay reduction
- Congestion impact
- Passenger impact
- Operational risk

These actions become binary decision variables in the QUBO optimization problem.

---

# Hybrid Quantum Optimization

The optimization engine transforms candidate dispatch actions into a **Quadratic Unconstrained Binary Optimization (QUBO)** problem.

Each action corresponds to a binary decision variable:

```text
x₁ = Hold Train A
x₂ = Speed Adjustment
x₃ = Platform Swap
...
```

The QUBO objective is optimized using:

- Hybrid QAOA
- Classical Optimization
- Simulated Annealing
- Greedy Search
- Local Search

The selected dispatch plan is then returned to the adaptive controller.

---

# Research Focus

RailTwin-Q investigates the integration of:

- Digital Twin Technology
- Artificial Intelligence
- Graph Analytics
- Hybrid Quantum Optimization

for intelligent railway scheduling and traffic optimization.

The project demonstrates a complete pipeline from prediction through optimization to autonomous closed-loop control.

---

# Quantum Evaluation

## Research Verdict

**Quantum Potential — No Demonstrated Quantum Advantage (Current Scale)**

RailTwin-Q converts railway dispatch decisions into constrained binary optimization problems using **QUBO**, solved by:

- Classical Optimization
- Simulated Annealing
- Ideal QAOA
- Hybrid QAOA

Experimental evaluation shows:

- Hybrid QAOA consistently recovers the same optimal solution as classical methods.
- Classical solvers execute significantly faster for the evaluated problem sizes (N ≤ 100).
- No measurable quantum advantage was observed at the tested scale.
- The architecture provides a scalable foundation for evaluating future fault-tolerant quantum hardware.

---

# Future Work

- Real-time railway sensor integration
- IoT-enabled Digital Twin synchronization
- Hardware execution on IBM Quantum devices
- Larger-scale railway optimization
- Multi-objective passenger-centric scheduling
- Reinforcement Learning-assisted dispatch optimization

---

# License

This project is released under the **MIT License**.
