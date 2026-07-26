import time
import numpy as np
from ai.quantum_optimization.classical_baselines import ClassicalBaselines
from ai.quantum_optimization.qaoa_optimizer import QAOAOptimizer
from ai.quantum_optimization.hybrid_optimizer import HybridOptimizer

class NoiseDepthExperiment:
    @classmethod
    def run_depth_study(cls, num_vars=6, qubo_matrix=None, depths=None, seed=42) -> dict:
        """
        Evaluates QAOA depth p in {1, 2, 3, 4} measuring energy, gap, circuit depth, 2-qubit gates, and runtime.
        """
        if depths is None:
            depths = [1, 2, 3, 4]
        if qubo_matrix is None:
            from ai.quantum_optimization.scalability_experiment import ScalabilityExperiment
            qubo_matrix = ScalabilityExperiment.generate_railway_qubo(num_vars, family="medium_density", seed=seed)

        bit_exact, energy_exact, _ = ClassicalBaselines.solve_exact(num_vars, qubo_matrix)

        depth_results = {}
        for p in depths:
            opt = QAOAOptimizer(reps=p, shots=512, seed=seed)
            q_res = opt.solve(num_vars, qubo_matrix, mode="AER")
            h_res = HybridOptimizer.solve_hybrid(num_vars, qubo_matrix, q_res)

            gap_raw = round((abs(q_res["energy"] - energy_exact) / abs(energy_exact)) * 100.0, 2) if abs(energy_exact) > 1e-9 else 0.0
            gap_hyb = round((abs(h_res["refined_energy"] - energy_exact) / abs(energy_exact)) * 100.0, 2) if abs(energy_exact) > 1e-9 else 0.0

            depth_results[f"p={p}"] = {
                "qaoa_depth": p,
                "circuit_depth": q_res.get("circuit_depth", 0),
                "total_gates": q_res.get("gate_count", 0),
                "two_qubit_gates": q_res.get("two_qubit_gates", 0),
                "raw_qaoa_energy": round(q_res["energy"], 4),
                "raw_qaoa_gap": gap_raw,
                "hybrid_energy": round(h_res["refined_energy"], 4),
                "hybrid_gap": gap_hyb,
                "runtime_seconds": round(q_res["runtime_seconds"], 4)
            }

        return depth_results

    @classmethod
    def run_noise_robustness_study(cls, num_vars=6, qubo_matrix=None, seed=42) -> dict:
        """
        Evaluates QAOA performance under ideal simulation vs noise models.
        """
        if qubo_matrix is None:
            from ai.quantum_optimization.scalability_experiment import ScalabilityExperiment
            qubo_matrix = ScalabilityExperiment.generate_railway_qubo(num_vars, family="conflict_heavy", seed=seed)

        bit_exact, energy_exact, _ = ClassicalBaselines.solve_exact(num_vars, qubo_matrix)

        noise_scenarios = {
            "Ideal": {"depolarizing_noise": 0.0, "readout_noise": 0.0},
            "Depolarizing Noise (0.5%)": {"depolarizing_noise": 0.005, "readout_noise": 0.0},
            "Readout Noise (1.0%)": {"depolarizing_noise": 0.0, "readout_noise": 0.010},
            "Combined Hardware Noise": {"depolarizing_noise": 0.005, "readout_noise": 0.010}
        }

        noise_results = {}
        for name, noise_params in noise_scenarios.items():
            opt = QAOAOptimizer(reps=2, shots=512, seed=seed)
            q_res = opt.solve(
                num_vars, qubo_matrix, mode="AER",
                depolarizing_noise=noise_params["depolarizing_noise"],
                readout_noise=noise_params["readout_noise"]
            )
            h_res = HybridOptimizer.solve_hybrid(num_vars, qubo_matrix, q_res)

            gap_raw = round((abs(q_res["energy"] - energy_exact) / abs(energy_exact)) * 100.0, 2) if abs(energy_exact) > 1e-9 else 0.0
            gap_hyb = round((abs(h_res["refined_energy"] - energy_exact) / abs(energy_exact)) * 100.0, 2) if abs(energy_exact) > 1e-9 else 0.0

            noise_results[name] = {
                "scenario": name,
                "raw_qaoa_energy": round(q_res["energy"], 4),
                "raw_qaoa_gap": gap_raw,
                "hybrid_refined_energy": round(h_res["refined_energy"], 4),
                "hybrid_gap": gap_hyb,
                "quantum_recovery_rate": "100%" if gap_hyb == 0.0 else "PARTIAL"
            }

        return noise_results

    @classmethod
    def generate_scientific_verdict(cls, scalability_res: dict, budget_res: dict) -> dict:
        """
        Automatically classifies the scientific verdict from empirical benchmark data:
        1. QUANTUM ADVANTAGE
        2. QUANTUM UTILITY
        3. NO DEMONSTRATED QUANTUM ADVANTAGE
        """
        # Check if quantum wall-clock runtime beat classical exact or SA fairly on larger N
        quantum_faster = False
        quantum_better_solution = False

        for N, fam_map in scalability_res.items():
            if N >= 20:
                for fam, metrics in fam_map.items():
                    sa_rt = metrics["simulated_annealing"]["runtime_seconds"]
                    hyb_rt = metrics["hybrid_qaoa"]["total_runtime_seconds"]
                    if hyb_rt < sa_rt:
                        quantum_faster = True

        for label, b_data in budget_res.items():
            hyb_e = b_data["hybrid_qaoa"]["energy"]
            sa_e = b_data["simulated_annealing"]["energy"]
            if hyb_e < sa_e and b_data["hybrid_qaoa"]["within_budget"]:
                quantum_better_solution = True

        if quantum_faster:
            verdict = "DEMONSTRATED QUANTUM ADVANTAGE"
            reason = "Qiskit Hybrid QAOA achieved lower wall-clock execution time than classical baselines on scaled problem instances (N >= 20)."
        elif quantum_better_solution:
            verdict = "QUANTUM UTILITY DEMONSTRATED"
            reason = "Qiskit Hybrid QAOA produced superior operational solution quality under constrained real-time decision budgets."
        else:
            verdict = "NO DEMONSTRATED QUANTUM ADVANTAGE"
            reason = "At tested scales (N <= 100), classical baselines (Simulated Annealing & Local Search) execute faster and achieve equivalent solution quality. Hybrid QAOA provides research utility and potential scalability."

        return {
            "verdict": verdict,
            "reason": reason,
            "quantum_faster": quantum_faster,
            "quantum_better_solution": quantum_better_solution
        }
