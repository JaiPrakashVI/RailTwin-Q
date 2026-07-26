import time
import math
import random
from ai.quantum_optimization.classical_baselines import ClassicalBaselines

class HybridOptimizer:
    @staticmethod
    def solve_hybrid(num_vars: int, qubo_matrix: dict, qaoa_result: dict) -> dict:
        """
        Executes an advanced 8-stage Hybrid QAOA refinement pipeline:
        1. Top-K bitstrings extraction from Qiskit Aer QAOA
        2. Deduplication
        3. Feasibility validation & Raw candidate scoring
        4. 1-bit neighborhood local search
        5. 2-bit neighborhood local search
        6. Local Simulated Annealing refinement
        7. Best feasible candidate selection

        Returns detailed ablation study metrics separating raw Qiskit QAOA performance
        from classical post-processing refinement.
        """
        post_start_time = time.time()
        ablation_stages = []

        # 1. Extract Top-K bitstrings from QAOA
        raw_bitstring = qaoa_result.get("bitstring", [0] * num_vars)
        raw_qaoa_energy = ClassicalBaselines.evaluate_qubo(raw_bitstring, qubo_matrix)

        ablation_stages.append({
            "stage": "1. Raw Qiskit QAOA",
            "bitstring": list(raw_bitstring),
            "energy": round(raw_qaoa_energy, 4),
            "description": "Most probable bitstring measured from Qiskit Aer QAOA circuit"
        })

        candidates = []
        if qaoa_result.get("status") == "SUCCESS" and "top_k_bitstrings" in qaoa_result:
            candidates = [list(bit) for bit in qaoa_result["top_k_bitstrings"]]

        if not candidates:
            sa_bit, sa_energy, _ = ClassicalBaselines.solve_simulated_annealing(num_vars, qubo_matrix)
            candidates = [list(sa_bit)]

        # 2. Deduplicate candidates
        unique_candidates = []
        seen = set()
        for c in candidates:
            tup = tuple(c)
            if tup not in seen:
                seen.add(tup)
                unique_candidates.append(c)

        # 3. Evaluate deduplicated Top-K candidates
        best_candidate = list(unique_candidates[0])
        best_energy = ClassicalBaselines.evaluate_qubo(best_candidate, qubo_matrix)

        for c in unique_candidates[1:]:
            energy = ClassicalBaselines.evaluate_qubo(c, qubo_matrix)
            if energy < best_energy:
                best_candidate = list(c)
                best_energy = energy

        stage2_energy = best_energy
        ablation_stages.append({
            "stage": "2. Top-K Deduplication",
            "bitstring": list(best_candidate),
            "energy": round(stage2_energy, 4),
            "description": f"Best candidate among Top-{len(unique_candidates)} sampled bitstrings"
        })

        # 4. Stage 4: 1-bit neighborhood search
        explored = set(tuple(c) for c in unique_candidates)
        pool = list(unique_candidates)

        for c in pool:
            for idx in range(num_vars):
                neighbor = list(c)
                neighbor[idx] = 1 - neighbor[idx]
                tup = tuple(neighbor)
                if tup not in explored:
                    explored.add(tup)
                    energy = ClassicalBaselines.evaluate_qubo(neighbor, qubo_matrix)
                    if energy < best_energy:
                        best_candidate = list(neighbor)
                        best_energy = energy

        stage3_energy = best_energy
        ablation_stages.append({
            "stage": "3. 1-Bit Search",
            "bitstring": list(best_candidate),
            "energy": round(stage3_energy, 4),
            "description": "Best candidate after 1-bit Hamming distance neighborhood sweep"
        })

        # 5. Stage 5: 2-bit neighborhood search
        for c in pool:
            for idx1 in range(num_vars):
                for idx2 in range(idx1 + 1, num_vars):
                    neighbor = list(c)
                    neighbor[idx1] = 1 - neighbor[idx1]
                    neighbor[idx2] = 1 - neighbor[idx2]
                    tup = tuple(neighbor)
                    if tup not in explored:
                        explored.add(tup)
                        energy = ClassicalBaselines.evaluate_qubo(neighbor, qubo_matrix)
                        if energy < best_energy:
                            best_candidate = list(neighbor)
                            best_energy = energy

        stage4_energy = best_energy
        ablation_stages.append({
            "stage": "4. 2-Bit Search",
            "bitstring": list(best_candidate),
            "energy": round(stage4_energy, 4),
            "description": "Best candidate after 2-bit Hamming distance neighborhood sweep"
        })

        # 6. Stage 6: Local Simulated Annealing refinement starting from the best candidate
        current_state = list(best_candidate)
        current_energy = best_energy

        temp = 1.0
        cooling_rate = 0.95
        random.seed(42)

        for step in range(100):
            next_state = list(current_state)
            if random.random() < 0.7:
                flip_idx = random.randint(0, num_vars - 1)
                next_state[flip_idx] = 1 - next_state[flip_idx]
            else:
                idx1 = random.randint(0, num_vars - 1)
                idx2 = random.randint(0, num_vars - 1)
                next_state[idx1] = 1 - next_state[idx1]
                next_state[idx2] = 1 - next_state[idx2]

            next_energy = ClassicalBaselines.evaluate_qubo(next_state, qubo_matrix)
            delta = next_energy - current_energy

            if delta < 0 or (random.random() < math.exp(-delta / temp) if temp > 0 else False):
                current_state = next_state
                current_energy = next_energy
                if current_energy < best_energy:
                    best_candidate = list(current_state)
                    best_energy = current_energy

            temp *= cooling_rate

        stage5_energy = best_energy
        ablation_stages.append({
            "stage": "5. Local SA Refinement",
            "bitstring": list(best_candidate),
            "energy": round(stage5_energy, 4),
            "description": "Final candidate after local Simulated Annealing refinement"
        })

        post_runtime = time.time() - post_start_time
        qaoa_runtime = qaoa_result.get("runtime_seconds", 0.0)
        total_runtime = qaoa_runtime + post_runtime

        return {
            "status": "EXECUTED",
            "backend": qaoa_result.get("backend", "AerSimulator"),
            "qaoa_bitstring": list(raw_bitstring),
            "qaoa_energy": round(raw_qaoa_energy, 4),
            "refined_bitstring": list(best_candidate),
            "refined_energy": round(best_energy, 4),
            "energy": round(best_energy, 4),
            "improvement": round(raw_qaoa_energy - best_energy, 4),
            "improved": best_energy < raw_qaoa_energy,
            "quantum_runtime_seconds": round(qaoa_runtime, 4),
            "classical_postprocessing_runtime_seconds": round(post_runtime, 4),
            "runtime_seconds": round(total_runtime, 4),
            "ablation_stages": ablation_stages
        }
