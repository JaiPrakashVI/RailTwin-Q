# RailTwin-Q forensic code audit

**Audit date:** 2026-07-28. **Method:** source-level trace of the repository and attempted execution in the supplied Python environment. Existing README, HTML reports, JSON output, and dashboards were treated as claims unless a producing call path was found. The supplied environment cannot import NumPy, Qiskit, or pytest, so no claim below is upgraded on the basis of a successful local run.

## A. Executive verdict

RailTwin-Q is a substantial **hackathon/research prototype**, not a production digital twin or a demonstration of quantum advantage. `main.py` contains a genuine 121-tick discrete simulation and calls prediction, decision-space, optimization, counterfactual, and control code. QAOA is genuinely coded as a parameterized Qiskit/Aer circuit with COBYLA optimization, subject to dependency availability. There is no IBM hardware implementation.

The central scientific limitation is fidelity and integration: it models a small hand-authored network with heuristic movement and synthetic-model inference. Actions are only partially executable; `REROUTE` is generated/optimized but cannot be executed by `ActionExecutor`. The counterfactual applies a different, stronger action policy than the live executor. Candidate benefits, passenger values, congestion hierarchy inputs, and much frontend content are deterministic/hard-coded. Thus the project supports the defensible claim **“a hybrid quantum-classical railway-dispatch prototype evaluated on a synthetic discrete simulation”**, not real railway optimization, validated AI, a physical digital twin, or quantum advantage.

## B. Actual execution path (`python main.py`)

```text
main.main
  -> DataLoader.load_network(data/) [stations, tracks, routes, trains only]
  -> GraphBuilder.build_graph [undirected NetworkX graph]
  -> constructs HeavyRainEvent(t=15) and SignalFailureEvent(station_id=2,t=45)
  -> Delay PredictionService / Congestion PredictionService / DelayPropagationPredictor
  -> ControlOrchestrator + QuantumOrchestrator
  -> for tick 0..120:
       MovementEngine.tick -> StateEngine.update_occupancies -> record_snapshot
       delay predictor -> congestion predictor -> propagation predictor
       -> CandidateActionGenerator -> DecisionBuilder -> optimization_search_space.json
       ControlOrchestrator.orchestrate_tick
       -> QuantumOrchestrator.optimize_network when a trigger fires
       -> benchmark suite -> SimulatorValidator counterfactual -> ActionExecutor
       -> HTML/JSON/CSV generation
  -> evaluation and Layer-6 reports; simulation history JSON
```

Configuration is embedded in code; there is no configuration loader. `signals.json` and `disruptions.json` are never loaded by `DataLoader`. The scheduled signal event says “Arakkonam” in comments/logging but passes station ID 2, which is Tambaram; actual Arakkonam is 4. The input `disruptions.json` instead describes events at 15/20/25 and is unused.

## C. Code-verified feature status

| Feature | Status | Evidence and qualification |
|---|---|---|
| 1-minute discrete network simulation | ACTUALLY IMPLEMENTED & EXECUTED path | `main.py:971`, `MovementEngine.tick`; unrun locally because dependencies missing. |
| stations/tracks/routes/trains loading | ACTUALLY IMPLEMENTED & EXECUTED path | `services/data_loader.py`; 10 stations, 10 tracks, 18 trains in JSON. |
| signals/disruptions JSON inputs | DOCUMENTED BUT NOT IMPLEMENTED | files exist, no loader/use site. |
| delay prediction inference | IMPLEMENTED BUT NOT VERIFIED | live path calls it; models/artifacts required, no local execution. Training source uses synthetic datasets. |
| hierarchical congestion inference | IMPLEMENTED BUT NOT VERIFIED | live path calls it, but uses fixed station-ID topology maps. |
| candidate-action generation | ACTUALLY IMPLEMENTED & EXECUTED path | Layer 4 calls `CandidateActionGenerator`; heuristic benefits. |
| QUBO / Ising conversion | IMPLEMENTED BUT NOT VERIFIED | formulas and exhaustive N<=10 checker in `qubo_builder.py`; Qiskit unavailable locally. |
| Aer QAOA | IMPLEMENTED BUT NOT VERIFIED | parameterized circuit, shot expectation and COBYLA in `qaoa_optimizer.py`. |
| IBM quantum hardware | MISSING | `_solve_ibm_quantum` always returns `UNAVAILABLE`; no auth/provider/job code. |
| hybrid refinement | ACTUALLY IMPLEMENTED & EXECUTED path | top-K, 1/2-bit enumeration and 100-step SA; five, not eight, recorded stages. |
| action application | PARTIALLY IMPLEMENTED | speed/platform/hold mutate twin; reroute and maintenance fail as “Physical execution failed”. |
| counterfactual simulation | PARTIALLY IMPLEMENTED | deep-copies and advances twin; action semantics differ from live path. |
| Layer-6 controller | PARTIALLY IMPLEMENTED | state/trigger/gate lifecycle executes; does not use imported `RecedingHorizonManager`; feedback is synthetic. |
| dashboard | PARTIALLY IMPLEMENTED | generated/embedded snapshots exist, but many fixed presentation values remain. |
| scalability / advantage studies | IMPLEMENTED BUT NOT INTEGRATED | standalone experiment modules, not invoked from `main.py`. |

## D. Layer review

### Layer 1 — digital twin (PARTIAL)

Inputs: `stations.json`, `tracks.json`, `routes.json`, `trains.json`; not signals/disruptions. `GraphBuilder` produces an **undirected** `nx.Graph`, disregarding the declared track direction. `MovementEngine` routes by the next fixed route node and treats any connecting track as bidirectional. It implements speed cap, rain factor, a 15%-of-track following slowdown, a simple occupancy slowdown, dwell, a destination platform check, and blockade/maintenance flags. Occupancy is recomputed after movement, so the movement check sees the preceding tick's counts.

This is a small synthetic, deterministic, discrete-time traffic simulation—not a real-time calibrated railway digital twin. Coordinates are visual metadata (no movement/routing calculation uses them). Track types are data labels only; single/double behavior is not enforced. Capacity is a percent metric; there is no hard track admission capacity. Platforms are counted/capped for display and only non-priority departure blocks when already full. There are no train lengths, braking/acceleration, block sections, routing interlocking, junction conflict reservations, timetable adherence constraints, signal aspects, or causal network delay propagation. A signal *event* delays departure at its station, but signal JSON state/failure is ignored. Rain reduces speed. Freight breakdown input is ignored.

### Layer 2 — delay prediction (PARTIAL / UNVERIFIED)

`ai/delay_prediction/model_training.py` loads dataset files, engineers features, and splits **synthetic scenarios** 1–80/81–90/91–100 for train/validation/test. It trains dummy, linear, RF, LightGBM and XGBoost candidates per 15/30/60-minute targets and persists selected artifacts. The production service loads an inference engine, builds a one-tick synthetic-data-generator dataframe, and predicts each tick. XGBoost/LightGBM are both trained; the registry determines production selection, not a hard-coded report claim. No raw real railway data, robust temporal backtest, leakage audit, or local metric rerun was available. The main loop does align predicted values with later simulator values, but the “actual” data is from the same synthetic simulator.

### Layer 3 — congestion prediction (PARTIAL / UNVERIFIED)

The service constructs station/track/network frames, rolling windows, delay-feature joins, then calls stacked inference models. It is connected into Layer 4: propagation CSI consumes horizon-30 station/track predictions; resulting candidates become QUBO costs. However `predictor.py` uses literal `hops_map` and `route_pressure_map` for IDs 1–4, rather than deriving topology, which breaks generality and makes the hierarchy partly hand-authored. Network “actual” evaluation in `main.py` is average delay, not the predicted network-congestion target, invalidating that comparison.

### Layer 4 — decision space (PARTIAL)

`CandidateActionGenerator` dynamically scans current state, but action effect estimates are constants: platform 8.5, reroute 14.2, hold 6.0, speed 4.5. REROUTE requires >=50% occupancy/blocked and moving train; HOLD requires delay >10; SPEED_ADJUST requires moving and delay >5; platform swap requires congestion >=40. Fallback is a no-benefit `SCHEDULE_MAINTENANCE`. `DecisionBuilder` calls validation, cost, Pareto, dependency and report generators; `DecisionVariables` filters `feasible`, ranks Pareto then expected saving, and retains at most **10**. Thus N is the selected actions, not the number of trains, tracks, junctions, or time windows. There is no true route feasibility search, conflict-reservation model, or Pareto optimization over measured outcomes.

### Layer 5 — QUBO/QAOA/hybrid (PARTIAL / UNVERIFIED)

For selected action bit vector `x`, code minimizes:

`E(x) = Σ_i (c_i + l_i)x_i + Σ_(i<j) q_ij x_i x_j`.

`c_i` is a weighted normalized heuristic score (`ObjectiveFunction`); under active events the delay weight is 0.85. `l_i,q_ij` encode conflicts, requires relations, and pairwise platform conflicts. Dynamic penalty `P=max(1.5, Σ|c_i|+0.5)` is not proven sufficient to dominate all reward terms. No equality/at-least-one constraint is encoded, so all-zero is valid.

`QUBOBuilder.qubo_to_ising` correctly implements for its upper-triangular convention `x_i=(1-Z_i)/2`: `C=ΣQii/2+ΣQij/4`, `h_i=-Qii/2-Σ_j Qij/4`, `Jij=Qij/4`. It exhaustively tests `E_QUBO=E_Ising+C` only at N<=10; maximum error is unavailable without Qiskit. The Qiskit operator is constructed but the circuit directly uses the returned h/J coefficients. Bit ordering reverses Qiskit's count string consistently. The invariant is coded: `num_vars == num_qubits == circuit qubits == decoded bitstring length == reduced actions`; it is runtime metadata, not guaranteed for externally malformed files.

`QAOAOptimizer` builds `H`/warm-start `RY`, then p cost RZ/CX-RZ-CX layers and RX mixers; default p=2, 1024 shots, three random starts, COBYLA maxiter=100. It measures shot distributions and optimizes expected **QUBO** energy. This is genuine parameterized QAOA-like circuit construction, not fixed parameters. Aer is imported at runtime from `qiskit_aer`, but that package is absent from requirements. On failure it silently reports a NumPy fallback (and for N>12 NumPy fallback returns a simulated-annealing solution labelled NumPyVectorSimulator). Any “Aer QAOA” metric must therefore check `actual_mode` and `fallback_used`.

Hybrid has five recorded stages: raw top-K, dedup/best scoring, 1-bit, 2-bit, 100-step local SA—not the advertised eight. Improvement is classical post-processing, not QAOA. Exact/greedy/local/SA/QAOA/hybrid comparisons are generated on the same QUBO in `benchmark.py`, but only unverified local code exists.

### Counterfactual and Layer 6 (PARTIAL)

`SimulatorValidator` performs baseline and optimized 30-minute copies, so numbers are dynamically calculated, not literal 42.5/28.2. Yet its actions are semantic shortcuts: speed +25%, reroute +10% base speed (without changing route), priority platform bypass, and hold 10 minutes. Live `ActionExecutor` only does speed +2%, platform priority, and hold >=1; it does not execute REROUTE. The result is not a physically meaningful reroute counterfactual and is not consistent with enacted actions.

The Layer-6 control sequence is observe -> detect -> cooldown/critical trigger -> QUBO -> gate -> execute -> lifecycle/feedback -> state JSON. Warm-start and switching penalties are coded. `current_energy` is erroneously set to exact energy whenever warm start exists, not energy of the actual current plan under the new QUBO. Feedback computes `expected*(1-network_delay/120)` rather than measuring intervention outcome. `RecedingHorizonManager` is imported but never used; there is no explicit moving-horizon model. It is a reactive loop, not genuine MPC.

## E. Quantum advantage and scalability verdict

**No quantum speedup, advantage, or hardware utility has been demonstrated.** Aer/NumPy are classical simulations; p=2, N<=10 on the live path. The standalone scalability suite labels N<=12 as Aer and N>12 as NumPy; the NumPy solver changes to simulated annealing at N>12. Exact is actually enumerated to N=20; at N>20 it reports a placeholder all-zero “exact” row and computes reference gap against the best heuristic. Therefore N>12 is neither quantum execution nor quantum scalability, and N>20 “exact” is not exact. Report any QAOA contribution only as exploratory hybrid candidate generation, compared against strong time-matched classical baselines on identical fixed instances.

## F. Frontend and test audit

`FrontendGenerator` writes live embedded state, but `operations.html` contains fixed values such as 28.2 min, 33.6%, 18 trains, 18,320 passengers, CSI 68, recovery 12, map statuses and train positions. It uses `(state.network_delay || 28.2)`, so zero is incorrectly replaced with 28.2. `judge_demo.html`, `network.html`, and `optimization.html` are static/generated presentation artifacts unless an embedded payload is demonstrably refreshed. Do not claim their circuit metrics or improvement values are live without inspecting the specific generated `optimization_result.json` and its execution flags.

Tests: `test_qiskit_qaoa_layer5.py` has pytest-style functions and exercises conversion, metadata, benchmark keys, IBM honesty and counterfactual key presence; it does not assert physical action effects, model quality, exactness of the full pipeline, or frontend fidelity. `test_layer6_closed_loop.py` is a manually run `test_all()` of isolated objects and writes reports; it does not execute `ControlOrchestrator` against the live simulation. `pytest` is absent and both scripts fail to import NumPy in this environment. Thus **tests are UNABLE TO VERIFY here** and would still be insufficient scientific validation if they passed.

## G. Repository inventory and dependency graph

| Group / important files | Purpose / status |
|---|---|
| `main.py` | Actual entry point and a second, large inline HTML dashboard. EXECUTED path. |
| `models/{station,track,train,railway_network}.py` | mutable in-memory domain records; no validation/persistence. |
| `services/{data_loader,graph_builder,movement_engine,state_engine,event_system}.py` | core simulator; no signals object model. |
| `services/frontend_generator.py` | pages and embedded state; MIXED live/static. |
| `services/synthetic_data/*.py`, `generate_synthetic_data.py` | synthetic dataset generation; training support, not live simulation. |
| `ai/delay_prediction/*.py` | synthetic ML train/infer/evaluate pipeline; only `predictor` and inference chain invoked live. |
| `ai/congestion_prediction/*.py` | hierarchical ML train/infer; predictor invoked live, model training standalone. |
| `ai/delay_propagation/*.py` | graph/cascade/criticality/candidates; predictor invoked live. |
| `ai/decision_space/*.py` | heuristic decision artifacts/search space; `DecisionBuilder` invoked from propagation. |
| `ai/quantum_optimization/{quantum_orchestrator,qubo_builder,qaoa_optimizer,benchmark,hybrid_optimizer,...}.py` | Layer 5; orchestrator invoked conditionally. Experiment modules are standalone. |
| `ai/adaptive_control/*.py` | state machine/control; orchestrator invoked per tick; `receding_horizon.py` unused. |
| `tests/*.py` | limited unit/acceptance scripts, no full E2E test. |
| `data/*.json` | inputs; signals/disruptions unused. |
| `datasets/*.json`, `reports/*.html`, `frontend/reports/*.html` | generated/demo artifacts; do not count as proof. Duplicated reports exist. |
| `frontend/*.html` | static/demo shells with partial state injection. |
| `README.md`, `walkthrough.md`, `architecture.md`, `task.md` | documentation claims only. |

```text
JSON -> DataLoader -> RailwayNetwork -> Movement/State
                              -> Delay + Congestion -> Propagation
                              -> CandidateAction -> DecisionBuilder -> search-space JSON
                              -> ControlOrchestrator -> QuantumOrchestrator
                              -> benchmark/QAOA/hybrid -> decoder -> counterfactual/executor
                              -> datasets/reports/frontend
```

## H. Critical defects and immediate roadmap

1. Make dependencies reproducible: pin Python and add `scipy`, `joblib`, `lightgbm`, `qiskit-aer`, `pytest` (and SHAP if used); create a clean test environment and CI.
2. Load/validate signals and disruptions, eliminate embedded events, correct station 2/4 mismatch, and use directed/multi-edge topology.
3. Define one action contract; implement true rerouting and use exactly the live executor semantics in counterfactuals.
4. Replace fixed candidate benefits/passenger estimates/front-end figures with explicit provenance or label them demo values.
5. Enforce track/platform/junction/headway constraints in a time-expanded or conflict-graph formulation; validate feasibility independently.
6. Make the QUBO penalty derivation explicit, test QUBO–Ising equality independently without Qiskit, and fail rather than silently call SA under a quantum label.
7. Separate experiment outputs from production UI; record seed, versions, instance ID, `actual_mode`, and raw counts.
8. For research: compare time-budgeted QAOA versus optimized CPLEX/MILP/CP-SAT, SA, local search and decomposition on identical instances; use hardware only with calibration, queue and error mitigation recorded. A legitimate advantage claim needs statistically sound performance superiority beyond end-to-end classical costs—none is present.

## I. Scorecard

| Category | /10 | Evidence-based verdict |
|---|---:|---|
| Digital twin | 3 | executable simulator, low operational fidelity |
| Railway realism | 2 | no direction/interlocking/headway/physics |
| AI/ML | 4 | real training/inference code, synthetic and unverified |
| QUBO formulation | 5 | coherent binary objective, heuristic/weak constraints |
| Quantum computing | 5 | genuine Aer circuit code; unavailable here/no hardware |
| QAOA correctness | 5 | mapping/circuit plausible, execution unverified |
| Hybrid optimization | 6 | clear classical refinement and baseline suite |
| Closed-loop control | 4 | reactive state loop, not MPC |
| Software architecture | 4 | modules exist but file coupling/artifact overwrite is high |
| Testing | 3 | narrow tests; unavailable environment |
| Scalability | 2 | solver substitution beyond N=12 |
| Frontend | 4 | polished but materially static |
| Scientific rigor | 3 | synthetic data, unverified metrics, semantic mismatch |
| Hackathon readiness | 6 | compelling demonstrator if claims are narrowed |

## J. Judge-safe conclusion

Impressive: the repository contains a broad, connected simulator-to-QUBO-to-QAOA-to-hybrid-control story, with explicit Aer metadata and an honest code path that refuses IBM execution. Weak: most railway semantics and business impacts are heuristic; artifacts can overstate liveness; and QAOA is simulated. Before a hackathon, fix action/counterfactual consistency and clearly annotate synthetic, simulated, and static elements. Preserve the modular QUBO/QAOA, hybrid baseline comparison, and UI narrative. The single highest-impact improvement is a unified, validated dispatch action model shared by candidate generation, constraints, executor, and counterfactual simulation.
