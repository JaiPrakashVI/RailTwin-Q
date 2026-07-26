class QUBOBuilder:
    def __init__(self, penalty_strength=100.0):
        self.penalty_strength = penalty_strength

    def build_qubo(self, num_vars: int, linear_costs: dict, linear_penalties: dict, quadratic_penalties: dict) -> dict:
        """
        Merges linear costs and quadratic constraint penalties to construct the QUBO matrix representation.
        Returns:
            qubo_dict (dict): Map of (idx_u, idx_v) -> coefficient (float).
            result_payload (dict): Structured diagnostic format containing num_variables, qubo_matrix, etc.
        """
        qubo_matrix = {}

        # 1. Add linear coefficients on diagonal Q_{ii}
        for idx in range(num_vars):
            cost_val = linear_costs.get(idx, 0.0)
            penalty_val = linear_penalties.get(idx, 0.0)
            val = cost_val + penalty_val
            if val != 0.0:
                qubo_matrix[(idx, idx)] = val

        # 2. Add quadratic coefficients off-diagonal Q_{ij} (i < j)
        for (idx_u, idx_v), val in quadratic_penalties.items():
            if val != 0.0:
                # Ensure ordered index pair (min, max)
                pair = (min(idx_u, idx_v), max(idx_u, idx_v))
                qubo_matrix[pair] = qubo_matrix.get(pair, 0.0) + val

        # 3. Compile serializable payload for logs & diagnostics
        serializable_matrix = {f"{k[0]},{k[1]}": float(v) for k, v in qubo_matrix.items()}

        payload = {
            "num_variables": num_vars,
            "qubo_matrix": serializable_matrix,
            "objective_terms": {str(k): float(v) for k, v in linear_costs.items()},
            "constraint_penalties": {
                "linear": {str(k): float(v) for k, v in linear_penalties.items()},
                "quadratic": {f"{k[0]},{k[1]}": float(v) for k, v in quadratic_penalties.items()}
            },
            "penalty_strength": float(self.penalty_strength)
        }

        return qubo_matrix, payload

    @staticmethod
    def qubo_to_ising(num_vars: int, qubo_matrix: dict):
        """
        Converts a QUBO matrix Q (x_i in {0, 1}) into an Ising Hamiltonian H (Z_i in {-1, +1})
        using binary transformation: x_i = (1 - Z_i) / 2.
        
        Returns:
            hamiltonian (SparsePauliOp): Qiskit operator representation.
            offset (float): Constant energy offset.
            h_linear (dict): Single-qubit Pauli Z coefficients {i: h_i}.
            J_quadratic (dict): Two-qubit Pauli ZZ coefficients {(i, j): J_ij}.
        """
        from qiskit.quantum_info import SparsePauliOp

        # 1. Compute Constant Offset C_offset
        offset = 0.0
        for i in range(num_vars):
            offset += qubo_matrix.get((i, i), 0.0) / 2.0

        for (i, j), val in qubo_matrix.items():
            if i != j:
                u, v = min(i, j), max(i, j)
                offset += val / 4.0

        # 2. Compute Linear Z_i coefficients h_i
        h_linear = {}
        for i in range(num_vars):
            h_val = -qubo_matrix.get((i, i), 0.0) / 2.0
            for j in range(num_vars):
                if i != j:
                    pair = (min(i, j), max(i, j))
                    if pair in qubo_matrix:
                        h_val -= qubo_matrix[pair] / 4.0
            h_linear[i] = h_val

        # 3. Compute Quadratic Z_i Z_j coefficients J_ij (i < j)
        J_quadratic = {}
        for (i, j), val in qubo_matrix.items():
            if i != j:
                u, v = min(i, j), max(i, j)
                J_quadratic[(u, v)] = J_quadratic.get((u, v), 0.0) + (val / 4.0)

        # 4. Build Qiskit SparsePauliOp
        pauli_list = []
        
        # Linear terms: h_i * Z_i
        for i, coeff in h_linear.items():
            if abs(coeff) > 1e-12:
                p_str = list("I" * num_vars)
                p_str[num_vars - 1 - i] = "Z"
                pauli_list.append(("".join(p_str), float(coeff)))

        # Quadratic terms: J_ij * Z_i Z_j
        for (i, j), coeff in J_quadratic.items():
            if abs(coeff) > 1e-12:
                p_str = list("I" * num_vars)
                p_str[num_vars - 1 - i] = "Z"
                p_str[num_vars - 1 - j] = "Z"
                pauli_list.append(("".join(p_str), float(coeff)))

        if not pauli_list:
            pauli_list.append(("I" * max(1, num_vars), 0.0))

        hamiltonian = SparsePauliOp.from_list(pauli_list)

        metadata = {
            "num_variables": num_vars,
            "constant_offset": offset,
            "h_linear": {str(k): float(v) for k, v in h_linear.items()},
            "J_quadratic": {f"{k[0]},{k[1]}": float(v) for k, v in J_quadratic.items()},
            "pauli_terms_count": len(pauli_list)
        }

        return hamiltonian, offset, h_linear, J_quadratic, metadata

    @staticmethod
    def validate_qubo_ising_equivalence(num_vars: int, qubo_matrix: dict, max_tol: float = 1e-8) -> dict:
        """
        Exhaustively tests QUBO <-> Ising energy equivalence for N <= 8 bitstrings.
        Verifies E_QUBO(x) == E_Ising(Z) + C_offset for all 2^N state configurations.
        """
        if num_vars > 10:
            return {"status": "SKIPPED", "reason": "N > 10 exceeds exhaustive check limits"}

        hamiltonian, offset, h_linear, J_quadratic, metadata = QUBOBuilder.qubo_to_ising(num_vars, qubo_matrix)

        num_states = 2 ** num_vars
        max_error = 0.0
        sum_error = 0.0

        for state_int in range(num_states):
            # Binary string x
            x = [(state_int >> (num_vars - 1 - i)) & 1 for i in range(num_vars)]
            # Spin string Z: Z_i = 1 - 2*x_i
            Z = [1 - 2 * bit for bit in x]

            # 1. QUBO Energy
            e_qubo = 0.0
            for i in range(num_vars):
                e_qubo += qubo_matrix.get((i, i), 0.0) * x[i]
            for (i, j), val in qubo_matrix.items():
                if i != j:
                    e_qubo += val * x[i] * x[j]

            # 2. Ising Energy + Offset
            e_ising = 0.0
            for i, h in h_linear.items():
                e_ising += h * Z[i]
            for (i, j), J in J_quadratic.items():
                e_ising += J * Z[i] * Z[j]
            e_total_ising = e_ising + offset

            err = abs(e_qubo - e_total_ising)
            sum_error += err
            if err > max_error:
                max_error = err

        passed = max_error <= max_tol
        return {
            "status": "PASSED" if passed else "FAILED",
            "num_variables": num_vars,
            "num_tested_bitstrings": num_states,
            "max_absolute_error": float(max_error),
            "mean_absolute_error": float(sum_error / num_states),
            "tolerance": max_tol,
            "constant_offset": float(offset)
        }

