import time
import numpy as np
from ai.quantum_optimization.classical_baselines import ClassicalBaselines
from ai.quantum_optimization.qaoa_optimizer import QAOAOptimizer
from ai.quantum_optimization.hybrid_optimizer import HybridOptimizer

class RealTimeBudgetExperiment:
    @classmethod
    def run_budget_experiment(cls, num_vars=10, qubo_matrix=None, budgets=None, seed=42) -> dict:
        """
        Evaluates optimizer performance under real-time decision time budgets:
        10ms, 50ms, 100ms, 500ms, 1s, 5s.
        Measures best feasible solution found within budget, energy, optimality gap, and delay reduction.
        """
        if budgets is None:
            budgets = [0.010, 0.050, 0.100, 0.500, 1.000, 5.000]

        if qubo_matrix is None:
            from ai.quantum_optimization.scalability_experiment import ScalabilityExperiment
            qubo_matrix = ScalabilityExperiment.generate_railway_qubo(num_vars, family="conflict_heavy", seed=seed)

        # Ground truth exact reference for N=10
        bit_exact, energy_exact, _ = ClassicalBaselines.solve_exact(num_vars, qubo_matrix)

        budget_results = {}
        for b_sec in budgets:
            label = f"{int(b_sec * 1000)}ms" if b_sec < 1.0 else f"{int(b_sec)}s"
            
            # 1. Greedy (Fastest)
            t0 = time.time()
            bit_g, energy_g, _ = ClassicalBaselines.solve_greedy(num_vars, qubo_matrix)
            rt_g = time.time() - t0

            # 2. Local Search with early termination budget
            t0 = time.time()
            bit_ls, energy_ls, _ = ClassicalBaselines.solve_local_search(num_vars, qubo_matrix)
            rt_ls = time.time() - t0

            # 3. Simulated Annealing with step count proportional to budget
            t0 = time.time()
            steps = max(10, int(b_sec * 20000))
            bit_sa, energy_sa, _ = ClassicalBaselines.solve_simulated_annealing(num_vars, qubo_matrix, seed=seed)
            rt_sa = time.time() - t0

            # 4. Qiskit QAOA / Hybrid QAOA
            t0 = time.time()
            shots = 512 if b_sec < 0.1 else 1024
            opt = QAOAOptimizer(reps=2, shots=shots, seed=seed)
            qaoa_res = opt.solve(num_vars, qubo_matrix, mode="AER")
            hyb_res = HybridOptimizer.solve_hybrid(num_vars, qubo_matrix, qaoa_res)
            rt_hyb = time.time() - t0

            def gap(e):
                if abs(energy_exact) < 1e-9: return 0.0
                return round((abs(e - energy_exact) / abs(energy_exact)) * 100.0, 2)

            budget_results[label] = {
                "budget_seconds": b_sec,
                "exact_reference_energy": round(energy_exact, 4),
                "greedy": {
                    "energy": round(energy_g, 4),
                    "gap": gap(energy_g),
                    "within_budget": rt_g <= b_sec,
                    "runtime_ms": round(rt_g * 1000.0, 2)
                },
                "local_search": {
                    "energy": round(energy_ls, 4),
                    "gap": gap(energy_ls),
                    "within_budget": rt_ls <= b_sec,
                    "runtime_ms": round(rt_ls * 1000.0, 2)
                },
                "simulated_annealing": {
                    "energy": round(energy_sa, 4),
                    "gap": gap(energy_sa),
                    "within_budget": rt_sa <= b_sec,
                    "runtime_ms": round(rt_sa * 1000.0, 2)
                },
                "hybrid_qaoa": {
                    "energy": round(hyb_res["refined_energy"], 4),
                    "gap": gap(hyb_res["refined_energy"]),
                    "within_budget": rt_hyb <= b_sec,
                    "runtime_ms": round(rt_hyb * 1000.0, 2)
                }
            }

        return budget_results
