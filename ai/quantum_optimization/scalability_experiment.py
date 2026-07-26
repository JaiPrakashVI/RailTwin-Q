import time
import numpy as np
from ai.quantum_optimization.classical_baselines import ClassicalBaselines
from ai.quantum_optimization.qaoa_optimizer import QAOAOptimizer
from ai.quantum_optimization.hybrid_optimizer import HybridOptimizer

class ScalabilityExperiment:
    @staticmethod
    def generate_railway_qubo(num_vars: int, family="medium_density", seed=42) -> dict:
        """
        Generates railway-inspired QUBO problem instances across different density & constraint families.
        """
        np.random.seed(seed + num_vars)
        qubo = {}
        
        density_map = {
            "low_density": 0.15,
            "medium_density": 0.35,
            "high_density": 0.65,
            "constraint_heavy": 0.40,
            "conflict_heavy": 0.50,
            "dynamic_disruption": 0.45
        }
        prob = density_map.get(family, 0.35)

        # Linear diagonal cost terms (delay savings, energy, safety)
        for i in range(num_vars):
            qubo[(i, i)] = float(np.random.uniform(-3.5, 1.5))

        # Quadratic off-diagonal coupling terms (track/platform conflict penalties)
        penalty = 100.0 if "constraint" in family or "conflict" in family else 25.0
        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                if np.random.rand() < prob:
                    qubo[(i, j)] = float(np.random.uniform(2.0, penalty))

        return qubo

    @classmethod
    def run_scalability_suite(cls, sizes=None, families=None, seed=42) -> dict:
        """
        Executes problem scaling benchmark across N = 4 to N = 100.
        Fairly separates algorithm runtime, optimization, execution, and post-processing.
        """
        if sizes is None:
            sizes = [4, 6, 8, 10, 12, 16, 20, 30, 40, 50, 75, 100]
        if families is None:
            families = ["medium_density", "conflict_heavy"]

        results = {}
        qaoa_solver = QAOAOptimizer(reps=2, shots=512, seed=seed)

        for N in sizes:
            results[N] = {}
            for fam in families:
                qubo = cls.generate_railway_qubo(N, family=fam, seed=seed)
                
                # Solvers evaluation
                # 1. Exact (Feasible for N <= 20)
                if N <= 20:
                    bit_e, energy_e, time_e = ClassicalBaselines.solve_exact(N, qubo)
                else:
                    bit_e, energy_e, time_e = [0] * N, 0.0, 0.0

                # 2. Greedy
                bit_g, energy_g, time_g = ClassicalBaselines.solve_greedy(N, qubo)

                # 3. Local Search
                bit_ls, energy_ls, time_ls = ClassicalBaselines.solve_local_search(N, qubo)

                # 4. Simulated Annealing
                bit_sa, energy_sa, time_sa = ClassicalBaselines.solve_simulated_annealing(N, qubo, seed=seed)

                # 5. Qiskit Aer QAOA (For N <= 12 using Qiskit Aer, or NumPy fallback for N > 12)
                mode = "AER" if N <= 12 else "NUMPY"
                qaoa_res = qaoa_solver.solve(N, qubo, mode=mode)
                
                # 6. Hybrid QAOA
                hybrid_res = HybridOptimizer.solve_hybrid(N, qubo, qaoa_res)

                # Reference exact energy for gap computation
                ref_energy = energy_e if N <= 20 else min(energy_g, energy_ls, energy_sa, hybrid_res["refined_energy"])
                def calc_gap(e):
                    if abs(ref_energy) < 1e-9: return 0.0
                    return round((abs(e - ref_energy) / abs(ref_energy)) * 100.0, 2)

                results[N][fam] = {
                    "num_variables": N,
                    "qubits": N,
                    "exact": {"energy": round(energy_e, 4), "runtime_seconds": round(time_e, 5), "gap": 0.0},
                    "greedy": {"energy": round(energy_g, 4), "runtime_seconds": round(time_g, 5), "gap": calc_gap(energy_g)},
                    "local_search": {"energy": round(energy_ls, 4), "runtime_seconds": round(time_ls, 5), "gap": calc_gap(energy_ls)},
                    "simulated_annealing": {"energy": round(energy_sa, 4), "runtime_seconds": round(time_sa, 5), "gap": calc_gap(energy_sa)},
                    "qaoa": {
                        "energy": round(qaoa_res["energy"], 4),
                        "runtime_seconds": round(qaoa_res["runtime_seconds"], 5),
                        "gap": calc_gap(qaoa_res["energy"]),
                        "circuit_depth": qaoa_res.get("circuit_depth", 0),
                        "two_qubit_gates": qaoa_res.get("two_qubit_gates", 0),
                        "backend": qaoa_res.get("backend", "AerSimulator")
                    },
                    "hybrid_qaoa": {
                        "energy": round(hybrid_res["refined_energy"], 4),
                        "quantum_runtime": round(hybrid_res["quantum_runtime_seconds"], 5),
                        "classical_postprocessing_runtime": round(hybrid_res["classical_postprocessing_runtime_seconds"], 5),
                        "total_runtime_seconds": round(hybrid_res["runtime_seconds"], 5),
                        "gap": calc_gap(hybrid_res["refined_energy"])
                    }
                }

        return results

def generate_random_railway_qubo(num_vars: int, seed=42):
    qubo = ScalabilityExperiment.generate_railway_qubo(num_vars, family="medium_density", seed=seed)
    return qubo, None, None

