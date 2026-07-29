import os
import json
import numpy as np
from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.compiler import transpile
from qiskit_aer import AerSimulator

def main():
    # 1. Exact QUBO Matrix from tick 60 live run
    Q = {
        (0, 0): 0.1185,
        (1, 1): 0.1185,
        (2, 2): -0.1815,
        (3, 3): 0.1185,
        (4, 4): 0.1185,
        (5, 5): 0.1185,
        (6, 6): 0.1185,
        (7, 7): -0.1815,
        (8, 8): -0.1815,
        (9, 9): 0.1285,
        (0, 9): 6.0
    }
    
    num_vars = 10
    p = 2
    shots = 1024
    delta = 0.3927  # warm start bias angle
    initial_state = [0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
    
    # 2. Derive Ising Hamiltonian coefficients
    h_linear = {}
    for i in range(num_vars):
        h_val = -Q.get((i, i), 0.0) / 2.0
        for j in range(num_vars):
            if i != j:
                pair = (min(i, j), max(i, j))
                if pair in Q:
                    h_val -= Q[pair] / 4.0
        h_linear[i] = h_val
        
    J_quadratic = {}
    for (i, j), val in Q.items():
        if i != j:
            u, v = min(i, j), max(i, j)
            J_quadratic[(u, v)] = J_quadratic.get((u, v), 0.0) + (val / 4.0)
            
    # 3. Construct parameterized circuit
    gammas = ParameterVector('gamma', p)
    betas = ParameterVector('beta', p)
    
    qc = QuantumCircuit(num_vars)
    
    # Apply warm-start initialization
    for idx, val in enumerate(initial_state):
        if val == 1:
            qc.ry(2 * delta, idx)
        else:
            qc.ry(-2 * delta, idx)
            
    # Apply p QAOA layers (Cost Unitary + Mixer Unitary)
    for k in range(p):
        # Cost Unitary
        for i, h in h_linear.items():
            if abs(h) > 1e-10:
                qc.rz(2 * gammas[k] * h, i)
                
        for (i, j), J in J_quadratic.items():
            if abs(J) > 1e-10:
                qc.cx(i, j)
                qc.rz(2 * gammas[k] * J, j)
                qc.cx(i, j)
                
        # Mixer Unitary
        for i in range(num_vars):
            qc.rx(2 * betas[k], i)
            
    # Add measurements
    qc.measure_all()
    
    # 4. Transpile circuit matching standard AerSimulator settings
    # basis gates & coupling map matching live generator
    coupling_map = [[i, i+1] for i in range(num_vars - 1)] + [[i+1, i] for i in range(num_vars - 1)]
    basis_gates = ['id', 'rz', 'sx', 'x', 'cx']
    transpiled_qc = transpile(qc, basis_gates=basis_gates, coupling_map=coupling_map, optimization_level=1)
    
    # Calculate stats
    ops = transpiled_qc.count_ops()
    circuit_depth = transpiled_qc.depth()
    total_gates = sum(v for k, v in ops.items() if k not in ['measure', 'barrier'])
    one_qubit_gates = sum(v for k, v in ops.items() if k in ['id', 'rz', 'sx', 'x'])
    two_qubit_gates = ops.get('cx', 0)
    
    # Print formatted stats to console
    print(f"Number of Qubits: {num_vars}")
    print(f"QAOA Depth: {p}")
    print(f"Circuit Depth: {circuit_depth}")
    print(f"Total Gates: {total_gates} (Single: {one_qubit_gates}, 2-Qubit: {two_qubit_gates})")
    print(f"CX Gates: {two_qubit_gates}")
    print(f"Shots: {shots}")
    print(f"Backend: AerSimulator")
    print("\n--- TEXT CIRCUIT DIAGRAM (UNTRANSPILED) ---")
    try:
        print(qc.draw(output="text"))
    except UnicodeEncodeError:
        print("[WARNING] Console encoding cannot render Qiskit box characters. Writing representation directly to files instead.")
    
    # 5. Save outputs in project-root reports folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Parent of tools/
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Save text diagram
    txt_path = os.path.join(reports_dir, "actual_qaoa_circuit.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=== RailTwin-Q Actual QAOA Quantum Circuit Diagram ===\n\n")
        f.write(f"Qubits: {num_vars}\n")
        f.write(f"QAOA reps (p): {p}\n")
        f.write(f"Transpiled Circuit Depth: {circuit_depth}\n")
        f.write(f"Transpiled Gate Count: {total_gates} (Single-qubit: {one_qubit_gates}, Two-qubit: {two_qubit_gates})\n")
        f.write(f"CX Gates count: {two_qubit_gates}\n\n")
        f.write(qc.draw(output="text").__str__())
        
    print(f"[SUCCESS] Saved text circuit diagram to: {txt_path}")
    
    # Save image diagram if matplotlib is installed
    img_path = os.path.join(reports_dir, "actual_qaoa_circuit.png")
    try:
        qc.draw(output="mpl", filename=img_path)
        print(f"[SUCCESS] Saved image circuit diagram to: {img_path}")
    except Exception as ex:
        print(f"[WARNING] Could not save image diagram via matplotlib: {ex}")
        
    # Save OpenQASM representation
    qasm_path = os.path.join(reports_dir, "actual_qaoa_circuit.qasm")
    try:
        # Load optimal parameters if available to write a realistic QASM circuit
        optimal_gamma = [0.5] * p
        optimal_beta = [0.25] * p
        opt_path = os.path.join(project_root, "datasets", "optimization_result.json")
        if os.path.exists(opt_path):
            try:
                with open(opt_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                q_stats = payload.get("qaoa", {})
                gamma_vals = q_stats.get("optimal_gamma", [])
                beta_vals = q_stats.get("optimal_beta", [])
                if len(gamma_vals) == p:
                    optimal_gamma = [float(g) for g in gamma_vals]
                if len(beta_vals) == p:
                    optimal_beta = [float(b) for b in beta_vals]
            except Exception:
                pass

        # Bind parameters to make the circuit concrete for QASM 2.0 export
        param_dict = {}
        for idx in range(p):
            param_dict[gammas[idx]] = optimal_gamma[idx]
            param_dict[betas[idx]] = optimal_beta[idx]
        bound_qc = qc.assign_parameters(param_dict)

        from qiskit.qasm2 import dumps
        qasm_str = dumps(bound_qc)
        with open(qasm_path, "w", encoding="utf-8") as f:
            f.write(qasm_str)
        print(f"[SUCCESS] Saved OpenQASM representation to: {qasm_path}")
    except Exception as ex:
        print(f"[ERROR] Could not export to OpenQASM: {ex}")

if __name__ == "__main__":
    main()
