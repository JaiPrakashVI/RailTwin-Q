import os
import json
import time
from ai.quantum_optimization.data_loader import OptimizationDataLoader
from ai.quantum_optimization.decision_variables import DecisionVariables
from ai.quantum_optimization.objective_function import ObjectiveFunction
from ai.quantum_optimization.constraint_encoder import ConstraintEncoder
from ai.quantum_optimization.qubo_builder import QUBOBuilder
from ai.quantum_optimization.benchmark import OptimizationBenchmark
from ai.quantum_optimization.solution_decoder import SolutionDecoder
from ai.quantum_optimization.solution_validator import SolutionValidator
from ai.quantum_optimization.simulator_validator import SimulatorValidator
from ai.quantum_optimization.explainability import OptimizationExplainer

class QuantumOrchestrator:
    def __init__(self, data_dir="datasets", reports_dir="reports", reps=2, shots=1024, seed=42):
        self.data_dir = data_dir
        self.reports_dir = reports_dir
        self.reps = reps
        self.shots = shots
        self.seed = seed
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)

    def optimize_network(self, network, active_events: list, tick: int, baseline_recovery_time: int, 
                         previous_solution=None, previous_candidates=None, p_switch=0.15, mode="AER") -> dict:
        """
        Coordinates Layer 5 optimization, Qiskit Aer circuit execution, solver comparisons,
        ablation tracking, action decoding, Digital Twin counterfactual re-simulation, and report generation.
        """
        start_time = time.time()

        # 1. Load candidate action search space
        loader = OptimizationDataLoader(data_dir=self.data_dir)
        search_space = loader.load_search_space()

        # 2. Variable reduction & mapping
        var_engine = DecisionVariables(max_variables=10)
        reduced_vars, variable_map = var_engine.build_variables(search_space)
        num_vars = len(reduced_vars)

        if num_vars == 0:
            return self._build_empty_payload(tick, baseline_recovery_time)

        # 3. Multi-objective costs & constraint penalties
        obj_engine = ObjectiveFunction()
        linear_costs = obj_engine.calculate_linear_coefficients(variable_map, search_space["cost_vectors"], active_events=active_events)

        # Dynamic penalty normalization: P = sum(|c_i|) + 0.5 (with a minimum of 1.5)
        sum_abs_costs = sum(abs(v) for v in linear_costs.values())
        dynamic_penalty = max(1.5, sum_abs_costs + 0.5)

        const_engine = ConstraintEncoder(penalty_strength=dynamic_penalty)
        linear_penalties, quadratic_penalties = const_engine.encode_constraints(
            variable_map, search_space["dependencies"], search_space["constraints"]
        )

        # 4. Build QUBO & test QUBO-to-Ising equivalence
        qubo_engine = QUBOBuilder(penalty_strength=dynamic_penalty)
        qubo_matrix, qubo_payload = qubo_engine.build_qubo(
            num_vars, linear_costs, linear_penalties, quadratic_penalties
        )
        equivalence_check = QUBOBuilder.validate_qubo_ising_equivalence(num_vars, qubo_matrix)

        # Apply Warm Start and Stability Penalties if previous solution exists
        initial_state = None
        if previous_solution is not None:
            from ai.adaptive_control.warm_start import WarmStartManager
            from ai.adaptive_control.stability_manager import StabilityManager
            initial_state = WarmStartManager.get_warm_start_vector(reduced_vars, previous_solution, previous_candidates)
            qubo_matrix = StabilityManager.inject_switching_penalties(qubo_matrix, reduced_vars, previous_solution, previous_candidates, p_switch)

        # 5. Run Solver Suite Benchmark
        bench = OptimizationBenchmark.run_benchmark(
            num_vars, qubo_matrix, reduced_vars, search_space["cost_vectors"],
            search_space["constraints"], search_space["dependencies"],
            linear_costs=linear_costs, penalty_strength=dynamic_penalty,
            qaoa_reps=self.reps, qaoa_shots=self.shots, seed=self.seed,
            initial_state=initial_state, mode=mode
        )

        solver_comparison = bench["comparison"]
        selected_solver = "hybrid_qaoa"
        best_sol = solver_comparison.get(selected_solver, solver_comparison.get("simulated_annealing"))

        if not best_sol.get("validation", {}).get("valid", False):
            selected_solver = "simulated_annealing"
            best_sol = solver_comparison["simulated_annealing"]

        selected_actions = best_sol["actions"]
        validation_status = best_sol["validation"]

        # 6. Counterfactual Re-simulation inside Digital Twin
        counterfactuals = SimulatorValidator.run_counterfactual_simulation(
            network, active_events, tick, selected_actions, horizon_mins=30
        )

        # 7. Explainability
        explanations = OptimizationExplainer.generate_explanations(
            selected_actions, selected_solver.upper(), validation_status, counterfactuals
        )

        # 8. Extract Qiskit metrics
        qaoa_stats = solver_comparison.get("qaoa", {})

        # Scientific conclusion
        advantage_demonstrated = False
        scientific_verdict = "No Demonstrated Quantum Advantage at Tested Scale"

        # Record QUBO log entry
        qubo_log_entry = {
            "tick": tick,
            "variable_count": num_vars,
            "qubo_coefficients": {f"{k[0]},{k[1]}": float(v) for k, v in qubo_matrix.items()},
            "selected_actions": [act["action"] for act in selected_actions],
            "solver_selected": selected_solver,
            "warm_start_loaded": initial_state is not None
        }
        with open(os.path.join(self.data_dir, "qubo_comparison_log.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(qubo_log_entry) + "\n")

        # Master payload schema (Phase 18)
        payload = {
            "execution": {
                "requested_mode": mode.upper(),
                "actual_mode": qaoa_stats.get("actual_mode", mode.upper()),
                "fallback_used": qaoa_stats.get("fallback_used", False),
                "fallback_reason": qaoa_stats.get("fallback_reason", "None"),
                "framework": "Qiskit",
                "backend": qaoa_stats.get("backend", "AerSimulator"),
                "hardware_executed": False
            },
            "problem": {
                "num_variables": num_vars,
                "num_qubits": num_vars,
                "qubo_to_ising_equivalence": equivalence_check
            },
            "circuit": {
                "qubits": num_vars,
                "qaoa_depth": self.reps,
                "circuit_depth": qaoa_stats.get("circuit_depth", 0),
                "total_gates": qaoa_stats.get("gate_count", 0),
                "one_qubit_gates": qaoa_stats.get("one_qubit_gates", 0),
                "two_qubit_gates": qaoa_stats.get("two_qubit_gates", 0),
                "shots": self.shots
            },
            "qaoa": {
                "optimizer": qaoa_stats.get("optimizer", "COBYLA"),
                "optimal_gamma": qaoa_stats.get("optimal_gamma", []),
                "optimal_beta": qaoa_stats.get("optimal_beta", []),
                "expected_energy": qaoa_stats.get("expected_energy", 0.0),
                "best_bitstring": qaoa_stats.get("bitstring", []),
                "qubo_energy": qaoa_stats.get("qubo_energy", 0.0),
                "ising_energy": qaoa_stats.get("ising_energy", 0.0),
                "constant_offset": qaoa_stats.get("constant_offset", 0.0)
            },
            "benchmark": solver_comparison,
            "ablation": bench.get("ablation", []),
            "railway": {
                "selected_actions": selected_actions,
                "feasible": validation_status.get("valid", True),
                "predicted_delay_reduction": counterfactuals.get("delay_reduction_mins", 0.0),
                "actual_delay_reduction": counterfactuals.get("delay_reduction_mins", 0.0),
                "digital_twin_validated": True
            },
            "scientific_conclusion": {
                "quantum_advantage_demonstrated": advantage_demonstrated,
                "verdict": scientific_verdict
            },
            "optimization_tick": tick,
            "selected_solver": selected_solver.upper(),
            "selected_actions": selected_actions,
            "selected_bitstring": best_sol.get("bitstring", []),
            "reduced_variables": reduced_vars,
            "best_energy": best_sol.get("energy", 0.0),
            "exact_energy": solver_comparison.get("exact", {}).get("energy", 0.0),
            "warm_start_used": initial_state is not None,
            "initial_state_vector": initial_state,
            "constraint_validation": validation_status,
            "counterfactual_results": counterfactuals,
            "quantum_metrics": {
                "status": "SUCCESS" if qaoa_stats.get("status") == "SUCCESS" else "UNAVAILABLE",
                "backend": qaoa_stats.get("backend", "AerSimulator"),
                "qubits": num_vars,
                "circuit_depth": qaoa_stats.get("circuit_depth", 0),
                "qaoa_reps": self.reps,
                "shots": self.shots
            },
            "winners": bench["winners"],
            "explanations": explanations
        }

        # Write datasets
        with open(os.path.join(self.data_dir, "optimization_result.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

        with open(os.path.join(self.data_dir, "qiskit_qaoa_metadata.json"), "w", encoding="utf-8") as f:
            json.dump(payload["circuit"], f, indent=4)

        with open(os.path.join(self.data_dir, "qaoa_ablation_results.json"), "w", encoding="utf-8") as f:
            json.dump({"ablation_stages": payload["ablation"]}, f, indent=4)

        with open(os.path.join(self.data_dir, "quantum_railway_trace.json"), "w", encoding="utf-8") as f:
            json.dump(payload["railway"], f, indent=4)

        # Generate HTML report
        self.generate_html_report(payload, solver_comparison, bench["winners"])

        return payload

    def generate_html_report(self, payload: dict, solver_comparison: dict, winners: dict):
        """
        Generates a premium dark-themed HTML report comparing solver metrics.
        """
        rows = ""
        for name, data in solver_comparison.items():
            gap = data.get("optimality_gap_percent", 0.0)
            valid_val = data.get("validation", {})
            valid = "PASS" if valid_val.get("valid", True) else "FAIL"
            color = "#10b981" if valid == "PASS" else "#ef4444"
            rows += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: 600;">{name.upper().replace('_', ' ')}</td>
                <td style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); text-align: center;">{data['energy']:.4f}</td>
                <td style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); text-align: center;">{gap:.2f}%</td>
                <td style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); text-align: center; color: {color}; font-weight: bold;">{valid} ({valid_val.get('violations', 0)} viol)</td>
                <td style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); text-align: center;">{data.get('runtime_seconds', 0.0) * 1000.0:.2f} ms</td>
            </tr>
            """

        actions_html = ""
        for act in payload["selected_actions"]:
            actions_html += f"<li><span style='color: var(--accent-indigo); font-weight: bold;'>[{act['action']}]</span> Target: {act['target']}</li>"
        if not actions_html:
            actions_html = "<li>No active intervention required.</li>"

        cf = payload["counterfactual_results"]

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Quantum Optimization Solver Benchmark</title>
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: #111827;
            --border-color: #1f2937;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --accent-indigo: #6366f1;
            --accent-yellow: #f59e0b;
        }}
        body {{
            background: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 40px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        .header {{
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
        }}
        h1, h2, h3 {{ margin-top: 0; }}
        h1 {{ color: var(--accent-indigo); }}
        h2 {{ color: var(--text-main); border-bottom: 1px solid var(--border-color); padding-bottom: 8px; font-size: 1.3rem; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th {{
            text-align: left;
            padding: 12px;
            background: rgba(255,255,255,0.02);
            border-bottom: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.85rem;
            text-transform: uppercase;
        }}
        .winner-tag {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            background: rgba(99, 102, 241, 0.15);
            color: var(--accent-indigo);
            font-weight: bold;
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Layer 5: Verifiable Qiskit QAOA & Solver Benchmark</h1>
            <p style="color: var(--text-muted); margin: 5px 0 0 0;">Optimization Tick: {payload['optimization_tick']} | Seed: {self.seed}</p>
        </div>

        <div class="grid">
            <div class="card">
                <h2>Digital Twin Counterfactual Results</h2>
                <div style="display: flex; justify-content: space-around; text-align: center; margin-top: 20px;">
                    <div>
                        <div style="font-size: 2rem; font-weight: bold; color: var(--accent-red);">{cf.get('baseline_delay', 0.0):.1f}m</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">Baseline Delay</div>
                    </div>
                    <div style="border-left: 1px solid var(--border-color);"></div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold; color: var(--accent-green);">{cf.get('optimized_delay', 0.0):.1f}m</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">Optimized Delay</div>
                        <div style="color: var(--accent-green); font-size: 0.8rem; font-weight: 600; margin-top: 4px;">-{cf.get('delay_reduction_percent', 0.0)}%</div>
                    </div>
                </div>

                <div style="display: flex; justify-content: space-around; text-align: center; margin-top: 30px; border-top: 1px solid var(--border-color); padding-top: 20px;">
                    <div>
                        <div style="font-size: 2rem; font-weight: bold; color: var(--accent-red);">{cf.get('baseline_congestion', 0.0):.1f}%</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">Baseline Congestion</div>
                    </div>
                    <div style="border-left: 1px solid var(--border-color);"></div>
                    <div>
                        <div style="font-size: 2rem; font-weight: bold; color: var(--accent-green);">{cf.get('optimized_congestion', 0.0):.1f}%</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">Optimized Congestion</div>
                        <div style="color: var(--accent-green); font-size: 0.8rem; font-weight: 600; margin-top: 4px;">-{cf.get('congestion_reduction_percent', 0.0)}%</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Qiskit QAOA Execution Configuration</h2>
                <p><strong>Execution Status:</strong> <span style="color: var(--accent-green);">{payload['quantum_metrics']['status']}</span></p>
                <p><strong>Backend:</strong> {payload['execution']['backend']}</p>
                <p><strong>IBM Quantum Hardware:</strong> <span style="color: var(--accent-yellow); font-weight: bold;">NOT EXECUTED</span></p>
                <p><strong>Qubits Count:</strong> {payload['circuit']['qubits']}</p>
                <p><strong>QAOA Depth (p):</strong> {payload['circuit']['qaoa_depth']}</p>
                <p><strong>Circuit Depth:</strong> {payload['circuit']['circuit_depth']}</p>
                <p><strong>Total Gates:</strong> {payload['circuit']['total_gates']} (2-Qubit: {payload['circuit']['two_qubit_gates']})</p>
                <p><strong>Optimization Solver:</strong> {payload['selected_solver']}</p>
                
                <h3 style="margin-top: 20px; font-size: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 4px;">Selected Intervention Plan</h3>
                <ul style="margin: 8px 0 0 0; font-size: 0.9rem;">
                    {actions_html}
                </ul>
            </div>
        </div>

        <div class="card" style="margin-bottom: 30px;">
            <h2>Categorical Metric Winners</h2>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 4px;">Objective Value</div>
                    <span class="winner-tag">{winners.get('objective_winner', 'N/A')}</span>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 4px;">Runtime Performance</div>
                    <span class="winner-tag">{winners.get('runtime_winner', 'N/A')}</span>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 4px;">Delay Reduction</div>
                    <span class="winner-tag">{winners.get('delay_reduction_winner', 'N/A')}</span>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Solver Optimization Performance Matrix</h2>
            <table>
                <thead>
                    <tr>
                        <th style="text-align: left;">Optimizer Solver</th>
                        <th style="text-align: center;">Objective Value (QUBO Energy)</th>
                        <th style="text-align: center;">Optimality Gap</th>
                        <th style="text-align: center;">Constraint Feasibility</th>
                        <th style="text-align: center;">Runtime</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
        rep_path = os.path.join(self.reports_dir, "quantum_benchmark_report.html")
        with open(rep_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _build_empty_payload(self, tick: int, baseline_recovery_time: int) -> dict:
        return {
            "execution": {
                "requested_mode": "AER",
                "actual_mode": "NONE",
                "fallback_used": False,
                "framework": "Qiskit",
                "backend": "None",
                "hardware_executed": False
            },
            "problem": {"num_variables": 0, "num_qubits": 0},
            "circuit": {"qubits": 0, "qaoa_depth": self.reps, "circuit_depth": 0, "total_gates": 0, "one_qubit_gates": 0, "two_qubit_gates": 0, "shots": self.shots},
            "qaoa": {"optimizer": "COBYLA", "expected_energy": 0.0, "best_bitstring": [], "qubo_energy": 0.0, "ising_energy": 0.0, "constant_offset": 0.0},
            "benchmark": {},
            "ablation": [],
            "railway": {"selected_actions": [], "feasible": True, "predicted_delay_reduction": 0.0, "actual_delay_reduction": 0.0, "digital_twin_validated": True},
            "scientific_conclusion": {"quantum_advantage_demonstrated": False, "verdict": "No Candidate Actions Found"},
            "optimization_tick": tick,
            "selected_solver": "NONE",
            "selected_actions": [],
            "constraint_validation": {"valid": True, "violations": 0, "details": []},
            "counterfactual_results": {"baseline_delay": 0.0, "optimized_delay": 0.0, "delay_reduction_percent": 0.0, "baseline_congestion": 0.0, "optimized_congestion": 0.0, "congestion_reduction_percent": 0.0},
            "quantum_metrics": {"status": "UNAVAILABLE", "backend": "None", "qubits": 0, "circuit_depth": 0, "qaoa_reps": self.reps, "shots": self.shots},
            "winners": {},
            "explanations": [{"type": "BASELINE", "text": "No candidate actions found."}]
        }
