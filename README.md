# RailTwin-Q

### A Hybrid Quantum-AI Digital Twin for Intelligent Railway Traffic Optimization

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Qiskit](https://img.shields.io/badge/Qiskit-Quantum-6929C4)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

**RailTwin-Q** is a Hybrid Quantum-AI Digital Twin platform for intelligent railway traffic management.

It combines **Digital Twin technology, Artificial Intelligence, Machine Learning, Graph Analytics, and Hybrid Quantum Optimization** to monitor railway operations, predict delays and congestion, optimize train dispatching, and provide decision support to railway operators.

The system operates as a **closed-loop framework**, continuously updating decisions as railway conditions change.

---

## Key Features

- Railway Digital Twin Simulation
- AI-based Train Delay Prediction
- Hierarchical Congestion Forecasting
- Graph-based Railway Network Analysis
- QUBO-based Optimization
- QAOA-based Quantum Optimization
- Receding-Horizon Adaptive Control
- Intelligent Train Dispatch Recommendations
- Dynamic Railway State Monitoring
- Interactive Operations Dashboard

---

## Problem Statement

Railway networks are dynamic systems where a single disruption can propagate across multiple trains, stations, and tracks.

For example, a signal failure can cause train delays, increase station and track occupancy, create congestion, and affect subsequent trains.

RailTwin-Q addresses this challenge through an integrated **predict → optimize → simulate → adapt** approach.

---

## System Architecture

```text
                  Railway Network
                         │
                         ▼
                ┌─────────────────┐
                │   Digital Twin  │
                │    Simulator    │
                └────────┬────────┘
                         │
                         ▼
                Current Network State
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Delay Prediction      Congestion Prediction
              │                     │
              └──────────┬──────────┘
                         ▼
                 Candidate Actions
                         │
                         ▼
                Hybrid Optimization
                   ┌─────┴─────┐
                   ▼           ▼
              Classical      Quantum
              Optimizer      QAOA
                   └─────┬─────┘
                         ▼
                Dispatch Recommendation
                         │
                         ▼
                  Digital Twin Update
                         │
                         └──────► Next Cycle
```

---

## Core Components

### 1. Digital Twin

Maintains a virtual representation of the railway network, including:

- Stations
- Tracks
- Trains
- Routes
- Train positions
- Train speeds
- Delays
- Station occupancy
- Track occupancy
- Network conditions

The simulator updates the railway state at each simulation step.

### 2. AI Delay Prediction

Machine Learning models predict future train delays using operational and environmental features such as:

- Current delay
- Train speed and progress
- Station and track occupancy
- Active train count
- Congestion
- Weather conditions
- Signal failures
- Time-based features

Predictions can be generated for +15, +30, and +60 minute horizons.

### 3. Hierarchical Congestion Prediction

Congestion is predicted at three levels:

```text
Station
   ↓
Track
   ↓
Network
```

Station-level predictions provide information to the track-level model, while station and track predictions contribute to network-level forecasting.

### 4. Dispatch Optimization

The system generates possible dispatch actions such as:

- Holding a train
- Prioritizing a train
- Changing train order
- Adjusting dispatch timing
- Managing conflicting movements

The feasible actions are passed to the optimization layer.

---

## Hybrid Quantum Optimization

RailTwin-Q formulates selected railway dispatch decisions as a **Quadratic Unconstrained Binary Optimization (QUBO)** problem.

A simplified objective is:

```text
Minimize:

Delay Cost
+ Congestion Cost
+ Conflict Penalty
+ Constraint Penalty
+ Priority Cost
```

The QUBO can be represented as:

```text
minimize: xᵀ Q x
```

where:

- `x` = binary decision variables
- `Q` = QUBO coefficient matrix

### QAOA Workflow

```text
Railway State
     ↓
Generate Candidate Actions
     ↓
Construct QUBO
     ↓
QUBO → Quantum Representation
     ↓
QAOA Circuit
     ↓
Quantum / Simulator Execution
     ↓
Candidate Solutions
     ↓
Best Feasible Solution
     ↓
Dispatch Recommendation
```

The architecture is hybrid because classical computing handles simulation, data processing, Machine Learning, and decision preparation, while quantum optimization is explored for the combinatorial optimization component.

---

## Adaptive Control

Railway conditions continuously change, so a decision that is optimal now may not remain optimal later.

RailTwin-Q uses a **receding-horizon control strategy**:

```text
Observe
   ↓
Predict
   ↓
Generate Actions
   ↓
Optimize
   ↓
Apply Decision
   ↓
Update Digital Twin
   ↓
Repeat
```

This enables continuous adaptation to changing railway conditions.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python 3.12 |
| AI / ML | XGBoost, LightGBM, Scikit-learn |
| Quantum Computing | Qiskit, QUBO, QAOA |
| Graph Analytics | NetworkX |
| Data Processing | Pandas, NumPy |
| Backend | FastAPI |
| Frontend | HTML5, CSS3, JavaScript |
| Simulation | Python-based Digital Twin |

---

## Project Structure

```text
RailTwin-Q/
│
├── data/
│   ├── train_dataset.csv
│   ├── station_dataset.csv
│   ├── track_dataset.csv
│   ├── network_state_dataset.csv
│   └── delay_propagation_dataset.csv
│
├── models/
│   ├── delay_prediction/
│   └── congestion_prediction/
│
├── src/
│   ├── digital_twin/
│   ├── prediction/
│   ├── optimization/
│   └── control/
│
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Advantages

- Integrates Digital Twin, AI, and optimization into one platform.
- Provides predictive rather than purely reactive decision support.
- Models congestion at multiple levels.
- Supports classical and quantum-assisted optimization.
- Continuously adapts to changing railway conditions.
- Enables safe experimentation through simulation.
- Provides a foundation for future intelligent railway research.

---

## Limitations

RailTwin-Q is currently a research and simulation platform, not a production railway control system.

Current limitations include:

- Simulation data may not fully represent real railway operations.
- Real railway networks contain additional operational and safety constraints.
- ML performance depends on training-data quality.
- Current quantum hardware has scalability and noise limitations.
- QAOA does not inherently guarantee an advantage over classical optimization.
- Real-world deployment would require extensive validation, safety certification, cybersecurity assessment, and regulatory approval.

---

## Future Enhancements

- Real-time railway data integration
- Real-world railway topology and signaling constraints
- Graph Neural Networks and Temporal GNNs
- Reinforcement Learning for dispatching
- Transformer-based delay forecasting
- Larger QUBO formulations
- Quantum annealing experiments
- Quantum hardware benchmarking
- Advanced explainable AI
- Real-time railway operations center
- Benchmarking against classical optimization algorithms

---

## Disclaimer

RailTwin-Q is intended for research, simulation, experimentation, and educational purposes.

It is **not** designed to directly control real railway infrastructure or safety-critical railway systems.

Any real-world deployment would require appropriate testing, validation, cybersecurity assessment, safety certification, regulatory approval, and integration with railway standards.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE.md) file for details.
