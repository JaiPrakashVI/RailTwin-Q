import time
from ai.quantum_optimization.classical_baselines import ClassicalBaselines
from ai.quantum_optimization.qaoa_optimizer import QAOAOptimizer
from ai.quantum_optimization.hybrid_optimizer import HybridOptimizer
from ai.quantum_optimization.solution_decoder import SolutionDecoder
from ai.quantum_optimization.solution_validator import SolutionValidator

class OptimizationBenchmark:
    @staticmethod
    def run_benchmark(num_vars: int, qubo_matrix: dict, reduced_vars: dict, cost_vectors: list, 
                      constraints: dict, dependencies: dict, linear_costs: dict, penalty_strength: float = 100.0, 
                      qaoa_reps=2, qaoa_shots=1024, seed=42, initial_state=None, mode="AER") -> dict:
        """
        Runs solver suite on the EXACT SAME QUBO matrix instance:
        1. Exact (Ground Truth reference optimum for N <= 20)
        2. Greedy
        3. Local Search
        4. Simulated Annealing
        5. Raw Qiskit QAOA (Qiskit Aer)
        6. Qiskit QAOA + Local Search
        7. Qiskit QAOA + Simulated Annealing
        8. Full Hybrid QAOA
        """
        results = {}

        # 1. Exact Solver (Ground Truth for N <= 20)
        if num_vars <= 20:
            bit_exact, energy_exact, time_exact = ClassicalBaselines.solve_exact(num_vars, qubo_matrix)
            act_exact = SolutionDecoder.decode_solution(bit_exact, reduced_vars)
            val_exact = SolutionValidator.validate_plan(act_exact, constraints, dependencies)
            exact_found = True
        else:
            bit_exact = [0] * num_vars
            energy_exact = 0.0
            time_exact = 0.0
            act_exact = []
            val_exact = {"valid": False, "violations": 0, "details": ["Skipped Exact for N > 20"]}
            exact_found = False

        results["exact"] = {
            "status": "SUCCESS" if exact_found else "SKIPPED",
            "bitstring": bit_exact,
            "energy": round(energy_exact, 4),
            "runtime_seconds": round(time_exact, 4),
            "actions": act_exact,
            "validation": val_exact,
            "optimality_gap_percent": 0.0,
            "approximation_ratio": 1.0
        }

        # Run safety audit on exact solution if available
        if exact_found:
            SolutionValidator.audit_pipeline(
                qubo_matrix, linear_costs, bit_exact, reduced_vars,
                cost_vectors, constraints, dependencies, penalty_strength
            )

        # Helper to compute optimality gap and approximation ratio
        def calc_metrics(energy):
            if not exact_found:
                return 0.0, 1.0
            if abs(energy_exact) < 1e-9:
                gap = 0.0 if abs(energy - energy_exact) < 1e-9 else 100.0
                ratio = 1.0 if abs(energy - energy_exact) < 1e-9 else 0.0
            else:
                gap = round((abs(energy - energy_exact) / abs(energy_exact)) * 100.0, 2)
                ratio = round(energy / energy_exact, 4)
            return gap, ratio

        # 2. Greedy Solver
        bit_greedy, energy_greedy, time_greedy = ClassicalBaselines.solve_greedy(num_vars, qubo_matrix)
        act_greedy = SolutionDecoder.decode_solution(bit_greedy, reduced_vars)
        val_greedy = SolutionValidator.validate_plan(act_greedy, constraints, dependencies)
        gap_g, ratio_g = calc_metrics(energy_greedy)
        results["greedy"] = {
            "status": "SUCCESS",
            "bitstring": bit_greedy,
            "energy": round(energy_greedy, 4),
            "runtime_seconds": round(time_greedy, 4),
            "actions": act_greedy,
            "validation": val_greedy,
            "optimality_gap_percent": gap_g,
            "approximation_ratio": ratio_g
        }

        # 3. Local Search Solver
        bit_ls, energy_ls, time_ls = ClassicalBaselines.solve_local_search(num_vars, qubo_matrix, initial_state=initial_state)
        act_ls = SolutionDecoder.decode_solution(bit_ls, reduced_vars)
        val_ls = SolutionValidator.validate_plan(act_ls, constraints, dependencies)
        gap_ls, ratio_ls = calc_metrics(energy_ls)
        results["local_search"] = {
            "status": "SUCCESS",
            "bitstring": bit_ls,
            "energy": round(energy_ls, 4),
            "runtime_seconds": round(time_ls, 4),
            "actions": act_ls,
            "validation": val_ls,
            "optimality_gap_percent": gap_ls,
            "approximation_ratio": ratio_ls
        }

        # 4. Simulated Annealing
        bit_sa, energy_sa, time_sa = ClassicalBaselines.solve_simulated_annealing(num_vars, qubo_matrix, seed, initial_state=initial_state)
        act_sa = SolutionDecoder.decode_solution(bit_sa, reduced_vars)
        val_sa = SolutionValidator.validate_plan(act_sa, constraints, dependencies)
        gap_sa, ratio_sa = calc_metrics(energy_sa)
        results["simulated_annealing"] = {
            "status": "SUCCESS",
            "bitstring": bit_sa,
            "energy": round(energy_sa, 4),
            "runtime_seconds": round(time_sa, 4),
            "actions": act_sa,
            "validation": val_sa,
            "optimality_gap_percent": gap_sa,
            "approximation_ratio": ratio_sa
        }

        # 5. Qiskit Aer QAOA (Raw)
        qaoa_solver = QAOAOptimizer(reps=qaoa_reps, shots=qaoa_shots, seed=seed)
        qaoa_res = qaoa_solver.solve(num_vars, qubo_matrix, mode=mode, initial_state=initial_state)
        bit_qaoa = qaoa_res["bitstring"]
        energy_qaoa = qaoa_res["energy"]
        time_qaoa = qaoa_res["runtime_seconds"]
        act_qaoa = SolutionDecoder.decode_solution(bit_qaoa, reduced_vars)
        val_qaoa = SolutionValidator.validate_plan(act_qaoa, constraints, dependencies)
        gap_qaoa, ratio_qaoa = calc_metrics(energy_qaoa)
        results["qaoa"] = {
            "status": qaoa_res["status"],
            "requested_mode": qaoa_res.get("requested_mode", mode),
            "actual_mode": qaoa_res.get("actual_mode", mode),
            "fallback_used": qaoa_res.get("fallback_used", False),
            "backend": qaoa_res["backend"],
            "bitstring": bit_qaoa,
            "energy": round(energy_qaoa, 4),
            "qubo_energy": round(qaoa_res.get("qubo_energy", energy_qaoa), 4),
            "ising_energy": round(qaoa_res.get("ising_energy", energy_qaoa), 4),
            "constant_offset": round(qaoa_res.get("constant_offset", 0.0), 4),
            "runtime_seconds": round(time_qaoa, 4),
            "actions": act_qaoa,
            "validation": val_qaoa,
            "optimality_gap_percent": gap_qaoa,
            "approximation_ratio": ratio_qaoa,
            "circuit_depth": qaoa_res.get("circuit_depth", 0),
            "gate_count": qaoa_res.get("gate_count", 0),
            "one_qubit_gates": qaoa_res.get("one_qubit_gates", 0),
            "two_qubit_gates": qaoa_res.get("two_qubit_gates", 0),
            "qubits": qaoa_res.get("qubits", num_vars)
        }

        # 6. Qiskit QAOA + Local Search
        bit_qaoa_ls, energy_qaoa_ls, time_qaoa_ls = ClassicalBaselines.solve_local_search(num_vars, qubo_matrix, initial_state=bit_qaoa)
        act_qaoa_ls = SolutionDecoder.decode_solution(bit_qaoa_ls, reduced_vars)
        val_qaoa_ls = SolutionValidator.validate_plan(act_qaoa_ls, constraints, dependencies)
        gap_qls, ratio_qls = calc_metrics(energy_qaoa_ls)
        results["qaoa_local_search"] = {
            "status": "SUCCESS",
            "bitstring": bit_qaoa_ls,
            "energy": round(energy_qaoa_ls, 4),
            "runtime_seconds": round(time_qaoa + time_qaoa_ls, 4),
            "actions": act_qaoa_ls,
            "validation": val_qaoa_ls,
            "optimality_gap_percent": gap_qls,
            "approximation_ratio": ratio_qls
        }

        # 7. Qiskit QAOA + Simulated Annealing
        bit_qaoa_sa, energy_qaoa_sa, time_qaoa_sa = ClassicalBaselines.solve_simulated_annealing(num_vars, qubo_matrix, seed, initial_state=bit_qaoa)
        act_qaoa_sa = SolutionDecoder.decode_solution(bit_qaoa_sa, reduced_vars)
        val_qaoa_sa = SolutionValidator.validate_plan(act_qaoa_sa, constraints, dependencies)
        gap_qsa, ratio_qsa = calc_metrics(energy_qaoa_sa)
        results["qaoa_simulated_annealing"] = {
            "status": "SUCCESS",
            "bitstring": bit_qaoa_sa,
            "energy": round(energy_qaoa_sa, 4),
            "runtime_seconds": round(time_qaoa + time_qaoa_sa, 4),
            "actions": act_qaoa_sa,
            "validation": val_qaoa_sa,
            "optimality_gap_percent": gap_qsa,
            "approximation_ratio": ratio_qsa
        }

        # 8. Full Hybrid QAOA (8-Stage Pipeline)
        hybrid_res = HybridOptimizer.solve_hybrid(num_vars, qubo_matrix, qaoa_res)
        bit_hybrid = hybrid_res["refined_bitstring"]
        energy_hybrid = hybrid_res["refined_energy"]
        time_hybrid = hybrid_res["runtime_seconds"]
        act_hybrid = SolutionDecoder.decode_solution(bit_hybrid, reduced_vars)
        val_hybrid = SolutionValidator.validate_plan(act_hybrid, constraints, dependencies)
        gap_hyb, ratio_hyb = calc_metrics(energy_hybrid)
        results["hybrid_qaoa"] = {
            "status": hybrid_res["status"],
            "backend": hybrid_res.get("backend", "AerSimulator"),
            "bitstring": bit_hybrid,
            "energy": round(energy_hybrid, 4),
            "runtime_seconds": round(time_hybrid, 4),
            "actions": act_hybrid,
            "validation": val_hybrid,
            "optimality_gap_percent": gap_hyb,
            "approximation_ratio": ratio_hyb,
            "raw_qaoa_energy": hybrid_res["qaoa_energy"],
            "improvement": hybrid_res["improvement"],
            "quantum_runtime_seconds": hybrid_res["quantum_runtime_seconds"],
            "classical_postprocessing_runtime_seconds": hybrid_res["classical_postprocessing_runtime_seconds"],
            "ablation_stages": hybrid_res["ablation_stages"]
        }

        # Helper to compute metric totals for action sets
        cost_map = {cv["action_id"]: cv["cost_vector"] for cv in cost_vectors}
        def sum_metric(actions, metric_key):
            return sum(cost_map.get(act["action_id"], {}).get(metric_key, 0.0) for act in actions)

        # Categorical Winners
        valid_solvers = [k for k, v in results.items() if v.get("validation", {}).get("valid", True)]
        if not valid_solvers:
            valid_solvers = list(results.keys())

        obj_winner = min(valid_solvers, key=lambda k: results[k]["energy"])
        rt_winner = min(valid_solvers, key=lambda k: results[k]["runtime_seconds"])
        delay_winner = min(valid_solvers, key=lambda k: sum_metric(results[k]["actions"], "delay_saved"))
        pass_winner = min(valid_solvers, key=lambda k: sum_metric(results[k]["actions"], "passenger_delay"))
        nrg_winner = min(valid_solvers, key=lambda k: sum_metric(results[k]["actions"], "energy_consumption"))

        winners = {
            "objective_winner": obj_winner.upper(),
            "runtime_winner": rt_winner.upper(),
            "delay_reduction_winner": delay_winner.upper(),
            "passenger_impact_winner": pass_winner.upper(),
            "energy_winner": nrg_winner.upper()
        }

        return {
            "comparison": results,
            "winners": winners,
            "ablation": hybrid_res["ablation_stages"]
        }
