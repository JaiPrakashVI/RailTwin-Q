# RailTwin-Q — source-forensic audit (superseding report)

**Date:** 2026-07-28. **Scope:** repository source/data plus a fresh end-to-end execution in a prepared alternate Conda environment. **Evidence standard:** existing reports/dashboards/JSON were not accepted as proof; runtime evidence below is explicitly identified. The default interpreter lacked scientific dependencies, but the alternate environment was prepared and successfully executed tests and `main.py`. Model binaries are present locally but ignored by the initial `rg --files` inventory, so source-control inventory alone is not a complete artifact inventory.

## 1. Executive Verdict

RailTwin-Q is a broad **synthetic hackathon research prototype** with a reachable simulation → ML-service → decision-space → QUBO → QAOA/heuristic → control pipeline. It is not currently a reproducible runnable system from this checkout, a calibrated railway digital twin, genuine MPC, IBM-hardware quantum computing, or evidence of quantum advantage.

The strongest implemented technical component is a parameterized Qiskit Aer QAOA circuit with a classical COBYLA loop and a clearly classical post-processing heuristic. The largest integrity risks are unconsumed signal/disruption inputs, fixed/hard-coded action benefits and UI figures, slow tick execution, model-version compatibility warnings, and action semantics that disagree between selected action, live executor, and counterfactual. Judge-safe claim: *a synthetic discrete railway-dispatch demonstrator that formulates selected heuristic interventions as a QUBO and executes it on Aer, a classical simulation of a quantum circuit.*

Status terminology used below: **IMPLEMENTED** (source exists), **EXECUTED PATH** (reachable from `main.py`), **VERIFIED** (successfully executed in this audit—none of the dependency-sensitive claims), **CLAIMED** (artifact/document only), **MISSING**.

## 2. Repository Inventory

| Files | Role | Imported/reached by | Status |
|---|---|---|---|
| `main.py` | real entry point; 121-tick orchestrator and inline dashboard | `python main.py` | EXECUTED PATH |
| `models/*.py` | mutable Station/Track/Train/RailwayNetwork records | services | EXECUTED PATH |
| `services/data_loader.py`, `graph_builder.py`, `movement_engine.py`, `state_engine.py`, `event_system.py` | input/load/topology/simulation/events | main | EXECUTED PATH |
| `services/frontend_generator.py` | writes operations page/updates embedded state | main | PARTIAL, mixed static/live |
| `services/synthetic_data/*.py`, `generate_synthetic_data.py` | synthetic dataset generation | prediction services/training, not main generator | IMPLEMENTED, not directly executed as generator |
| `ai/delay_prediction/*.py` | synthetic delay ML train/infer | predictor imported by main | INFERENCE PATH BROKEN in checkout (missing `.pkl`) |
| `ai/congestion_prediction/*.py` | hierarchical synthetic ML train/infer | predictor imported by main | EXECUTED PATH; model artifacts present locally but version-sensitive |
| `ai/delay_propagation/*.py` | graph/cascade/candidates | main | EXECUTED PATH |
| `ai/decision_space/*.py` | heuristic action artifacts/search-space JSON | propagation predictor | EXECUTED PATH |
| `ai/quantum_optimization/{quantum_orchestrator,qubo_builder,qaoa_optimizer,benchmark,hybrid_optimizer}.py` | Layer 5 | control orchestrator, conditional | IMPLEMENTED; runtime unverified |
| other `ai/quantum_optimization/*experiment*.py`, `validation_scenario.py` | standalone benchmark/report generators | no main import | IMPLEMENTED BUT NOT EXECUTED |
| `ai/adaptive_control/*.py` | reactive state machine/controller | main | EXECUTED PATH; `receding_horizon.py` unused |
| `data/*.json` | stations/tracks/routes/trains/signals/disruptions | loader reads first four only | signals/disruptions DEAD INPUTS |
| `datasets/*.json`, `reports/*.html`, `frontend/reports/*.html` | generated/demo artifacts | frontend/report output | CLAIMED/STATIC until regenerated |
| `frontend/*.html` | demo/presentation pages | browser only | mixed static presentation |
| `tests/*.py` | narrow component checks | manual/pytest | 13 passed; no full-system E2E test |
| `README.md`, `walkthrough.md`, `architecture.md`, `task.md` | documentation | none | CLAIMS ONLY |
| `requirements.txt` | declared dependencies | user install | INCOMPLETE: misses SciPy, LightGBM, joblib, Qiskit Aer, pytest |

There are no notebooks, Dockerfiles, environment files, CSS/JS source files separate from HTML, or serialized model artifacts (`.pkl`, `.joblib`) in the checkout. HTML reports are duplicated in `reports/` and `frontend/reports/`; they are generated artifacts, not source-of-truth.

Dependency graph:

```text
data/{stations,tracks,routes,trains}.json
  -> services.DataLoader.load_network -> models.RailwayNetwork
  -> GraphBuilder / MovementEngine / StateEngine
  -> delay PredictionService + congestion PredictionService
  -> DelayPropagationPredictor -> CandidateActionGenerator -> DecisionBuilder
  -> datasets/optimization_search_space.json -> QuantumOrchestrator
  -> OptimizationBenchmark {exact, greedy, local, SA, QAOA, hybrid}
  -> SolutionDecoder -> SimulatorValidator + ActionExecutor
  -> ControlOrchestrator -> datasets/reports/frontend
```

## 3. Actual Runtime Execution Path

`main.main` (`main.py:971`) calls `DataLoader.load_network("data")`, then `GraphBuilder.build_graph`. It creates two **code-defined** events: rain at tick 15 and signal failure station 2 at tick 45. At each 0..120 tick it runs:

```text
MovementEngine.tick(network, active_events, tick)
 -> StateEngine.update_occupancies -> StateEngine.record_snapshot
 -> DelayPredictionService.get_predictions_for_tick
 -> CongestionPredictionService.get_predictions_for_tick
 -> DelayPropagationPredictor.get_predictions_for_tick
      -> CandidateActionGenerator.generate_candidate_actions
      -> DecisionBuilder.build_decision_space -> optimization_search_space.json
 -> ControlOrchestrator.orchestrate_tick
      -> QuantumOrchestrator.optimize_network [only on trigger]
      -> ActionExecutor.execute_plan [only accepted nonzero plan]
 -> dashboard/CSV/JSON writes
```

At completion it requests propagation/decision evaluation reports, control reports and saves playback JSON. `signals.json` and `disruptions.json` are never read. A fresh prepared run completed 121 ticks in 161.7 seconds and successfully loaded locally present model artifacts. It emitted scikit-learn/XGBoost serialized-model version compatibility warnings, which make results environment-sensitive. The run is therefore verified as executable, but not reproducibly pinned by the repository.

## 4. Architecture Diagram

```text
Synthetic JSON state -> discrete movement/occupancy -> synthetic ML inference* 
  -> propagation heuristics -> heuristic actions/cost artifacts -> capped action variables
  -> upper-triangular QUBO -> Ising coefficients -> Aer QAOA* -> sampled bitstrings
  -> classical 1/2-bit search + SA -> decoder -> inconsistent executor/counterfactual
  -> reactive state machine -> JSON/HTML presentation

* unavailable from this checkout without dependencies and serialized models
```

## 5. Layer 1 Audit — Digital Twin

Inputs read: station/track/route/train JSON. `DataLoader` ignores input occupancy/signal/disruption fields. `GraphBuilder.build_graph` creates an **undirected** `nx.Graph`; route movement independently scans for any matching edge and accepts either orientation.

Per moving train, `MovementEngine.tick` uses `speed=min(base_speed*(1-0.5*rain_intensity), track.max_speed)`. If another same-track train is ahead within 15 percentage points, speed is capped at `0.7*lead.speed`; if preceding-tick `track.current_trains>2`, speed is multiplied by `max(.5,1-.15*(current_trains-1))`. Position increases by `(speed/60/track.distance)*100`; delay adds `(base_speed-speed)/base_speed`. Dwell is a fixed two minutes. `StateEngine` recomputes platform and track counts after movement.

| Railway feature | Status | Code evidence |
|---|---|---|
| topology/routing | PARTIAL | fixed route lists; graph not used to find alternatives |
| directed/bidirectional/double track | MISSING | labels only; undirected graph and bidirectional movement |
| block sections/headway/interlocking/junction conflict | MISSING | only 15% same-track slowdown |
| platform constraint | PARTIAL | display count and non-priority departure stop when full |
| hard track capacity | MISSING | occupancy can exceed 100%; no entry denial |
| speed limits/weather/dwell | IMPLEMENTED | movement formulas above |
| acceleration/braking/train length | MISSING | no data or equations |
| schedules | PARTIAL | arrival estimated from route distance; no departures/timetable enforcement |
| signal aspect JSON | MISSING | never loaded |
| code-created signal failure | PARTIAL | holds departures at event station, no signal/interlocking model |
| maintenance/blockage events | IMPLEMENTED but not scheduled by main | movement flags exist; JSON disruption unused |
| coordinates | VISUAL ONLY | graph/frontend attributes, not physics/optimization |
| priority/freight | PARTIAL | priority bypasses platform wait; no dispatch priority model |

It is a discrete synthetic simulation, not a real-network digital twin.

## 6. Layer 2 Audit — AI Delay Prediction

`ModelTrainer.run_training_pipeline` reads synthetic `datasets` data, engineers features, and splits scenarios <=80/train, 81–90/validation, >90/test. Targets are `future_delay_15`, `_30`, `_60`. It fits dummy, linear regression, RF, LightGBM and XGBoost and writes model/preprocessor artifacts when training is run. `InferenceEngine` loads only the saved ensemble `.pkl` files; it does not dynamically select all models. The registry JSON records claims/metadata but is not an estimator.

Live feature flow is: current model state -> synthetic dataset generators -> merged dataframe -> `FeatureEngineer.engineer_features` -> persisted preprocessor -> ensemble mean prediction -> 15/30/60 values. Output is used by congestion features and propagation CSI. Confidence is `clip(exp(-std_30/6), .40, .98)`, an ensemble-spread heuristic, not calibrated uncertainty. Metrics have calculation code in `model_evaluation.py`, but no artifact can be accepted as verified here; data are synthetic and the time/scenario split alone does not prove no simulated-scenario leakage.

## 7. Layer 3 Audit — Congestion Prediction

`HierarchicalInferenceEngine` invokes station models, injects horizon-30 station predictions into track features, aggregates station/track predictions into network features, then emits 15/30/60 future-state dictionaries. Layer 4 uses horizon-30 station/track outputs for CSI and candidate triggers. It initialized and ran in the prepared end-to-end execution, but emitted serialized-model library-version compatibility warnings.

It is not topology-general: `ai/congestion_prediction/predictor.py` contains literal `hops_map` and `route_pressure_map` for station IDs 1–4 and also derives “downstream” as `station_id+1`. Candidate thresholds are literals (40/50/10/5). These invalidate claims of arbitrary network hierarchy. Main records network predicted congestion against average delay, a target mismatch.

## 8. Layer 4 Audit — Decision Space

| Action | Generation | benefit | QUBO/decode | live executor | counterfactual |
|---|---|---|---|---|---|
| `PLATFORM_SWAP` | station congestion >=40 | fixed 8.5 | selectable | set priority | set priority |
| `REROUTE` | track >=50%/blocked, moving train | fixed 14.2 | selectable | **fails** (unimplemented) | +10% speed, no route change |
| `HOLD` | train delay >10 | fixed 6.0 | selectable | dwell >=1 | dwell >=10 / speed override |
| `SPEED_ADJUST` | moving and delay >5 | fixed 4.5 | selectable | base speed +2% | base speed +25% |
| `SCHEDULE_MAINTENANCE` | fallback | 0 | selectable | fails | no action |
| `PRIORITY_CHANGE` | no generator | — | none | none | none |

`DecisionBuilder` calls validation, costs, passenger impact, robustness, Pareto and graph generators; these consume action dictionaries and fixed heuristic estimates rather than measured operational impacts. `DecisionVariables.build_variables` filters feasible actions, Pareto/ranks them and caps to 10. One variable means **one retained candidate intervention**, so N is neither train count nor time-expanded railway state.

Critical mismatch: selected QAOA action != reliably executed action != counterfactual action. In particular `REROUTE` is a QUBO variable that is neither route-planned nor live-executed. This invalidates the optimization-to-railway claim.

## 9. Layer 5 QUBO Audit

`ObjectiveFunction.calculate_linear_coefficients` makes each diagonal objective coefficient from normalized heuristic delay/congestion/passenger/risk/energy/operation/stability values (active-event weights favor delay 0.85). `ConstraintEncoder` adds pairwise conflict, require, and some platform-swap penalties. `QUBOBuilder.build_qubo` makes the upper-triangular form:

`E(x) = Σ_i (c_i + l_i)x_i + Σ_{i<j} q_ij x_i x_j`, `x_i∈{0,1}`.

This is equivalent to `x^T Q x` only if Q is understood as the stored upper-triangular coefficient convention, not a symmetric matrix. Constraints are partial: dependency/conflict relationships from action artifacts and pairwise platform swaps only. There are no track capacity, junction, route, time-window, minimum/maximum action, or at-least-one constraints. All-zero is intentionally feasible.

Penalty is `max(1.5, sum(abs(c_i))+.5)`. It is **not formally guaranteed** to exceed aggregate benefits or multiple competing terms, so feasibility is not proven by construction. A `SolutionValidator` exists as a post hoc filter; that cannot repair a QUBO whose best feasible state was excluded by inadequate penalties.

## 10. QUBO-to-Ising Mathematical Audit

For stored diagonal `a_i` and off-diagonal `b_ij`, substitution `x_i=(1-Z_i)/2` gives:

`C = Σ_i a_i/2 + Σ_i<j b_ij/4`

`h_i = -a_i/2 - Σ_{j!=i} b_min(i,j),max(i,j)/4`

`J_ij=b_ij/4`, hence `E_QUBO = C + Σh_iZ_i + ΣJ_ijZ_iZ_j`.

`QUBOBuilder.qubo_to_ising` implements these signs/factors and reverses Pauli-string indexes for Qiskit little-endian ordering. `validate_qubo_ising_equivalence` enumerates all states only when N<=10 and reports max/mean error. In the verified live N=10 run it tested 1,024 states and returned `PASSED`, maximum absolute error `1.7763568394002505e-15`, mean `2.991584844430628e-16`, offset `2.5005`. This verifies numerical equivalence for that emitted QUBO, not for arbitrary inputs above N=10.

## 11. Qiskit/QAOA Audit

Qiskit use sites: `qubo_builder.py` imports `SparsePauliOp`; `qaoa_optimizer.py` imports `QuantumCircuit`, `ParameterVector`, `AerSimulator`, and `qiskit.compiler.transpile`; SciPy `minimize(..., COBYLA)` optimizes parameters. No `Sampler`, `Estimator`, IBM provider, authentication, or submitted hardware job exists.

`QAOAOptimizer.solve_qiskit_qaoa` uses a `|+>` initial state (or biased `RY` warm start), then for p layers applies `RZ(2γh_i)` and `CX-RZ(2γJ_ij)-CX` costs, `RX(2β)` mixers, measures, and minimizes sampled expected QUBO energy. Defaults in live `QuantumOrchestrator`: p=2, shots=1024, three starts, up to 100 COBYLA iterations/start. Circuit depth/gate/CX/iteration counts are runtime-dependent outputs, hence **unknown for a real live run**. On Aer failure `solve` silently invokes NumPy; for N>12 NumPy returns simulated annealing rather than statevector QAOA. `qiskit-aer` is not declared in requirements.

## 12. Exact Qubit/N Analysis

At Layer 4 N = number of candidates retained by `DecisionVariables`, capped to 10 in the live orchestrator. `num_vars=len(reduced_vars)` is passed unmodified to QUBO, `QuantumCircuit(num_vars)`, simulator output parser, and `SolutionDecoder`. Thus intended invariant is `N_QUBO=N_qubits=N_circuit=N_bitstring=N_retained_actions`, not N trains/tracks/junctions/time slots. It is logged in payload metadata but dynamically **unverified** in this checkout. A candidate count of zero produces an empty payload; 1–10 produces a circuit of that many qubits if Aer is actually used.

## 13. Hybrid Optimization Audit

`HybridOptimizer.solve_hybrid` has **five** recorded algorithmic stages:

1. QAOA most-probable sample (quantum-simulator output).
2. Top-K candidate deduplication and best direct QUBO scoring (classical).
3. Exhaustive 1-bit neighbors of top-K (classical).
4. Exhaustive 2-bit neighbors of top-K (classical).
5. 100-step local simulated annealing (classical).

It reports raw QAOA and refined energy separately. Any refinement improvement is classical by definition. The effect of removing QAOA is **not measured by a controlled ablation**; fallback candidates can themselves come from SA, so it cannot be inferred from reports.

## 14. Counterfactual Validation

`SimulatorValidator.run_counterfactual_simulation` deep-copies state/events and advances baseline/optimized copies for 30 minutes, so its output formula is dynamic. It reports percentage `(baseline-opt)/baseline*100`, not the static 42.5→28.2. However its modifications disagree with `ActionExecutor` as detailed in section 8. It neither changes a reroute path nor invokes the live executor. Therefore counterfactual results are **not valid validation of deployed actions**.

`42.5`, `28.2`, `14.3`, and `33.6%` occur in `frontend/judge_demo.html` as literal display text; `services/frontend_generator.py` also defaults to 28.2/33.6. They are STATIC PRESENTATION ONLY, not traceable to the counterfactual function.

## 15. Layer 6/MPC Audit

`ControlOrchestrator.orchestrate_tick` performs observation (`StateMonitor`), event detection, cooldown/critical trigger, conditional optimization, switching-cost/quality gate, execution/lifecycle, then dashboard state. Warm-start and a diagonal switching-penalty injector exist. This is **reactive event-triggered control**. It does not formulate a multi-step horizon, optimize a sequence, apply only the first time-indexed action, or shift/re-solve a horizon. `RecedingHorizonManager` is imported but unused. Feedback is formulaic (`expected*(1-network_delay/120)`) rather than measured outcome. Also when warm-started it uses exact solver energy as “current plan” energy, not evaluated prior plan energy under new QUBO, undermining the quality gate.

## 16. Frontend Audit

`FrontendGenerator` embeds snapshot state and tries regex replacement in existing pages, so selected fields can become generated. Static/misleading values include 18 trains, 28.2 min, “33.6% after QAOA”, 18,320 passengers, CSI 68, 12-minute recovery, 94% confidence, map incident/train positions and candidate actions in `services/frontend_generator.py`. It substitutes `(state.network_delay || 28.2)`, making genuine zero display as 28.2. `frontend/judge_demo.html` literals include N=6–25, XGBoost 94%, 42.5→28.2, 42% bar. `frontend/optimization.html` contains a prior embedded state; that is an artifact, not a live API. No backend server/API is used. The judge dashboard must label all static values as demo data or derive them from a run artifact that exposes `actual_mode` and input hash.

## 17. Testing Audit

| Layer | Tests | What they prove | Gap |
|---|---|---|---|
| 1 | counterfactual key check inside Layer 5 test | keys exist | no physical railway constraints |
| 2/3 | none | — | model training/inference absent |
| 4 | decoder only | bit-to-action fields | action semantics absent |
| 5 | QUBO equivalence/QAOA metadata/benchmark-key functions | limited unit intent | requires absent deps; no full live QUBO |
| 6 | manual `test_all()` assertions | isolated trigger/state helpers | no full controller+sim integration |
| frontend | none | — | no provenance/render test |

`test_qiskit_qaoa_layer5.py` is pytest-discoverable; `test_layer6_closed_loop.py` only runs its `test_all` under `__main__`. Local test command could not start because pytest/NumPy are absent. No full system E2E, model artifact, fixture, or frontend test is present.

## 18. Quantum Advantage Audit

No quantum advantage/speedup/utility has been demonstrated. Aer is classical simulation and IBM mode always returns `UNAVAILABLE`. The live problem is capped N<=10. `ScalabilityExperiment` uses Aer only N<=12, NumPy thereafter, and NumPy switches to SA N>12; “exact” for N>20 is a padded placeholder, not exact. There are no MILP, CP-SAT/OR-Tools, Gurobi/CPLEX, genetic algorithm, or optimized native-QUBO baselines. A fair experiment requires fixed QUBO instances, identical constraints/objective, repeated seeds/shots, wall-clock accounting including compilation, and time-matched strong classical baselines. Present work is best described as simulated quantum candidate sampling plus classical refinement.

## 19. Complete Input → Processing → Output Table

| Layer | Input | Processing/calculation | Tool | Output | Next |
|---|---|---|---|---|---|
| 1 | 4 loaded JSON files + code events | movement/occupancy formulas | Python/NetworkX | mutable network/snapshots | 2/3/6 |
| 2 | current synthetic snapshot | feature merge → model ensembles | pandas/sklearn/etc. | delays +15/30/60 | 3/propagation |
| 3 | state + delay outputs | stacked station→track→network models | pandas/NumPy | future state maps | propagation |
| 4 | propagation/current state | thresholds, fixed effects, Pareto rank | Python | search-space JSON | 5 |
| 5 | selected candidates/costs/dependencies | QUBO→Ising→QAOA/heuristics | Qiskit Aer/SciPy | bitstrings/actions | executor/counterfactual |
| 6 | state/event/solution | reactive gate/lifecycle | Python | applied action/state JSON | next tick/UI |

## 20. Critical Bugs

1. Missing model `.pkl`/preprocessor artifacts break prediction initialization; main assumes congestion key 30 afterwards.
2. Dependencies required by imports are absent from environment and incomplete in `requirements.txt`.
3. Signal event says Arakkonam but station ID 2 is Tambaram; JSON disruptions/signals are ignored.
4. REROUTE is optimized but not live-executable; counterfactual fakes it as speed increase.
5. Counterfactual/live speed and hold effects conflict.
6. Track capacity is not enforced; generated artifacts show >100% occupancy.
7. UI treats zero delay as fallback 28.2.

## 21. Scientific Weaknesses

Synthetic uncalibrated data; heuristic benefits/confidence/passenger impact; no railway interlocking/time-expanded conflicts; invalid network-congestion evaluation target; no numerical QUBO-Ising verification in this audit; no hardware; solver substitution under quantum labels; and no controlled ablation demonstrating QAOA contribution.

## 22. What Is Actually Good

Clear module boundaries, a real reachable orchestration design, honest IBM-unavailable response, explicit bit ordering and Ising-offset code, raw-versus-refined hybrid energy separation, and an accessible visual narrative. These are valuable foundations once reproducibility and semantics are fixed.

## 23. What Is Actually Bad

The software creates a compelling end-to-end appearance while several inputs are unused, models are missing, numbers are static, and optimizer actions are not consistently applied. Report files can therefore overstate runtime reality.

## 24. What Is Missing

Reproducible environment/model release; config/schema validation; directed/multitrack time-expanded constraints; real rerouting; one action contract; end-to-end test/CI; strong classical baseline suite; true MPC horizon; hardware integration/experiments; real/calibrated data.

## 25. P0/P1/P2/P3 Roadmap

**P0:** supply lockfile/model artifacts or fail fast; load/validate all declared inputs; correct station event; unify executor/counterfactual semantics; remove or badge every static KPI; never call fallback SA QAOA.

**P1:** derive graph features from topology; implement directed routing and feasible reroute; enforce capacity/headway/junction constraints; add one deterministic E2E fixture that validates N/action/energy/artifact provenance.

**P2:** real/calibrated datasets and leakage-resistant temporal evaluation; time-expanded conflict graph/MWIS or MILP formulation; penalty proof/feasibility repair; CP-SAT/MILP/SA baselines and controlled QAOA ablation.

**P3:** IBM Runtime/provider integration, transpilation to selected backend, calibration/noise/mitigation logging, queue versus execution accounting, hardware shots/repetitions, and no speedup claim absent end-to-end comparative evidence.

## 26. Objective Scorecard

| Category | /10 |
|---|---:|
| Digital Twin Fidelity | 3 |
| Railway Realism | 2 |
| AI/ML | 3 |
| Data Quality | 2 |
| Decision Space | 4 |
| QUBO Correctness | 5 |
| QAOA Implementation | 5 |
| Quantum Authenticity | 3 |
| Hybrid Optimization | 6 |
| Quantum Advantage Evidence | 0 |
| Closed-Loop Control | 4 |
| MPC Correctness | 2 |
| Software Architecture | 4 |
| Testing | 3 |
| Scalability | 2 |
| Frontend | 4 |
| Scientific Rigor | 3 |
| Hackathon Readiness | 5 |

## 27. Final Judge-Safe Technical Explanation

“RailTwin-Q is a synthetic railway-dispatch prototype. Its simulator creates train, track and disruption state; prediction services estimate short-horizon delay and congestion when trained artifacts are available. The system turns a capped set of candidate interventions into binary QUBO variables, and its Qiskit Aer implementation uses p=2 QAOA to sample candidate bitstrings. Classical local search and simulated annealing then refine those samples before actions are decoded. The digital twin can compare intervention scenarios, but this is a simulated evaluation, not a deployed railway result. We do not claim quantum advantage: the next experiment is a controlled, time-budgeted comparison against strong classical solvers on identical constrained instances, followed by hardware-quality evaluation.”

## 28. Final Recommendation

Do not add more algorithms or report pages before repairing the executable backbone. Ship a reproducible minimal demo with the model artifacts, input-driven events, one consistent action implementation, run-proven QAOA metadata, and static UI values removed or labelled. That makes the project credible and competitive as a transparent hybrid-optimization prototype; only after those fixes should it pursue real railway data, time-expanded constraints, and hardware research.

---

# Addendum — performance, reliability, and status evidence

## Performance Benchmark Analysis

`OptimizationBenchmark.run_benchmark` builds comparisons for exact, greedy, local search, simulated annealing, raw QAOA, QAOA+local search, QAOA+SA and hybrid on one supplied QUBO. This is the correct *code intent* for same-instance comparison, but no fresh benchmark result was produced in this audit. Existing JSON/HTML benchmark numbers are **UNVERIFIED generated artifacts**. The exact solver enumerates `2^min(N,20)` states, so it is not exact above 20; QAOA wall time includes parameter optimization/sampling on a classical simulator and must not be compared as a quantum-hardware runtime.

## Scalability Analysis

Architecture limit: Layer 5's live `DecisionVariables(max_variables=10)` caps retained actions and hence intended Qiskit qubits at ten. Standalone `ScalabilityExperiment` accepts sizes through 100, but it uses Aer only at N<=12, NumPy at N>12, and `solve_numpy_qaoa` calls classical SA for N>12. Thus:

| N range | Claimed code path | Actual quantum status |
|---|---|---|
| 0–10 live | Aer requested | classical simulation of a quantum circuit if Aer installed |
| 11–12 standalone | Aer requested | classical simulation of a quantum circuit if Aer installed |
| 13–100 standalone | NumPy requested | **NOT A QUANTUM EXECUTION AT THAT SCALE**; N>12 is SA fallback |
| >20 exact column | padded/placeholder reference | **not exact** |

No supported architecture actually runs a 100-qubit Qiskit circuit in the live pipeline.

## Security / Reliability Issues

There is no authentication/API surface in the current offline script, so the principal risks are reliability and provenance rather than network attack surface. Critical reliability issues are unchecked JSON schemas/missing fields, process-global mutable `StateEngine.history`, repeated overwrites of shared datasets/report paths, mutable action dictionaries, broad `except Exception` blocks that permit degraded state, missing reproducible dependency lock, absent models, and no deterministic run manifest (commit, input hash, seed, package versions, fallback state). `main.py` deletes generated logs at start, which destroys comparison provenance. Reports render dynamic strings into HTML without a clear escaping policy; if inputs become external this becomes an injection risk.

## Green–Yellow–Red Status Matrix

| Component | Status | Evidence | Problem | Priority |
|---|---|---|---|---|
| Core tick simulator | YELLOW | `main.py`, movement/state services | simplistic constraints | P1 |
| JSON input loading | RED | data loader reads only 4/6 input types | signals/disruptions ignored | P0 |
| ML live inference | RED | inference loaders require absent `.pkl` | fresh run fails/degrades | P0 |
| Candidate generation | YELLOW | propagation predictor calls generator | rule-based fixed benefits | P1 |
| QUBO/Ising source | YELLOW | explicit upper-triangular formulas | numerical runtime unverified | P1 |
| Aer QAOA source | YELLOW | parameterized circuit/COBYLA | dependencies unavailable; no hardware | P0/P2 |
| Hybrid refinement | GREEN (code only) | five explicit stages | not eight; no contribution ablation | P2 |
| Action execution | RED | executor lacks REROUTE/maintenance | semantic mismatch | P0 |
| Counterfactual | RED | different intervention effects | invalid causal validation | P0 |
| MPC claim | RED | reactive orchestrator, unused horizon manager | no horizon optimization | P1 |
| Frontend | RED | literal KPIs/demo values | can misrepresent execution | P0 |
| Quantum advantage | RED | Aer/fallback study only | no evidence | P0 wording |

## File-Specific P0/P1/P2/P3 Plan

| Priority | Problem and exact change site | Expected result | Verification |
|---|---|---|---|
| P0 | Add pinned dependencies (`requirements.txt`/lockfile); ship or generate model artifacts used by `ai/delay_prediction/inference.py:initialize` and congestion `Station/Track/Network*Model.load_model` | `main.py` either runs reproducibly or fails before simulation with a precise prerequisite error | clean-environment install and E2E smoke test |
| P0 | Extend `services/data_loader.py:load_network` and replace code literals in `main.py:main` with validated signal/disruption objects | all declared JSON inputs affect the same run; correct Arakkonam station 4 | test source JSON event appears in snapshot |
| P0 | Define action semantics once; implement route mutation in `action_executor.py:execute_plan` and reuse it in `simulator_validator.py:run_counterfactual_simulation` | selected=decoded=executed=counterfactual action | action-contract integration test per type |
| P0 | Remove/badge literals in `services/frontend_generator.py` and `frontend/judge_demo.html`; expose run ID, actual mode and fallback | judge values trace to an artifact | frontend provenance test with zero state |
| P1 | Replace hardcoded maps in `ai/congestion_prediction/predictor.py` with NetworkX-derived neighborhoods; make `GraphBuilder` directed/multigraph where data requires it | topology works beyond IDs 1–4 | alternate topology fixture |
| P1 | Implement time-indexed headway/platform/junction/track constraints in `constraint_encoder.py` and action feasibility | operationally feasible QUBO | independent constraint checker against adversarial cases |
| P1 | Evaluate current plan energy correctly in `control_orchestrator.py:orchestrate_tick`; use `receding_horizon.py` or remove MPC claim | valid gate and honest controller terminology | repeated-tick controller test |
| P2 | Add MILP/CP-SAT and strong heuristic baselines around `benchmark.py`; store fixed instances/seeds | fair same-instance quality/TTS study | repeated statistical benchmark |
| P2 | Add an explicit raw-QAOA-vs-classical-ablation in `hybrid_optimizer.py` | quantified quantum contribution or honest absence | confidence intervals over independent seeds |
| P3 | Replace `_solve_ibm_quantum` with explicit opt-in provider/runtime execution and calibration manifest | real job status, not simulated claim | backend job ID, transpiled circuit, shots/results |

## Runtime Verification Performed After the Initial Audit

An alternate local Conda environment was prepared with the declared packages plus `lightgbm`, `joblib`, `qiskit-aer`, SciPy, and pytest. First, a direct in-memory Layer-1 smoke test loaded `data/`, enabled rain plus a signal event, and executed 30 `MovementEngine.tick` / `StateEngine.update_occupancies` cycles. It produced 10 stations, 10 tracks, 18 trains, 7 routes, 30 snapshots, 17 moving trains, mean delay 23.87, and maximum track occupancy **133.33%**. `compileall` passed for `ai`, `models`, `services`, `main.py`, and `tests`.

Then `pytest -q` passed **13 tests in 15.05 seconds** (39 deprecation warnings). A complete `main.py` execution completed in **161.7 seconds** (121 ticks) with actual Qiskit Aer execution: requested/actual mode `AER`, fallback false, p=2, N=10, 1,024 shots, circuit depth 23, 172 gates and 8 CX gates. Its QUBO–Ising check passed exhaustively at N=10 (1,024 states; error as recorded in section 10). This is **CLASSICAL SIMULATION OF A QUANTUM CIRCUIT**, not hardware execution.

The same actual run exposes major integration defects: it selected eight `REROUTE` actions, but `ActionExecutor` has no REROUTE implementation; the recorded counterfactual was only 878.80 → 877.76 total delay (0.12%) with 0% congestion reduction, while the `railway` payload reports 0.0 delay reduction and sets `digital_twin_validated: true`. Run end-state was tick 120, mean network delay 61.5, one control cycle and ten qubits. Runtime averages about 1.34 seconds/tick before considering external hardware/queueing, which contradicts a strong real-time claim. Model loading emitted scikit-learn/XGBoost serialized-version compatibility warnings. The >100% occupancy directly corroborates that capacity is measured but not enforced.
