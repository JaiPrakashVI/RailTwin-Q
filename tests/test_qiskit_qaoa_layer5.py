import os
import numpy as np
from ai.quantum_optimization.qubo_builder import QUBOBuilder
from ai.quantum_optimization.qaoa_optimizer import QAOAOptimizer
from ai.quantum_optimization.hybrid_optimizer import HybridOptimizer
from ai.quantum_optimization.benchmark import OptimizationBenchmark
from ai.quantum_optimization.solution_decoder import SolutionDecoder
from ai.quantum_optimization.solution_validator import SolutionValidator
from ai.quantum_optimization.classical_baselines import ClassicalBaselines
from services.data_loader import DataLoader
from services.graph_builder import GraphBuilder
from services.state_engine import StateEngine
from ai.quantum_optimization.simulator_validator import SimulatorValidator

def get_sample_qubo(num_vars=3):
    qubo_matrix = {}
    reduced_vars = {}
    for i in range(num_vars):
        qubo_matrix[(i, i)] = -1.2 + 0.3 * i
        reduced_vars[101 + i] = {
            "action_id": 101 + i,
            "index": i,
            "action": "REROUTE" if i % 2 == 0 else "HOLD",
            "target": f"Train {i+1}"
        }
        for j in range(i + 1, num_vars):
            qubo_matrix[(i, j)] = 0.5 * (i + j + 1)
    return num_vars, qubo_matrix, reduced_vars

def test_qubo_to_ising_conversion():
    num_vars, qubo_matrix, _ = get_sample_qubo(3)
    hamiltonian, offset, h_linear, J_quadratic, meta = QUBOBuilder.qubo_to_ising(num_vars, qubo_matrix)
    
    assert hamiltonian is not None
    assert isinstance(offset, float)
    assert meta["num_variables"] == 3
    assert len(h_linear) == 3

def test_exhaustive_qubo_ising_energy_equivalence():
    for N in [3, 5, 6, 8]:
        num_vars, qubo_matrix, _ = get_sample_qubo(N)
        res = QUBOBuilder.validate_qubo_ising_equivalence(num_vars, qubo_matrix)
        assert res["status"] == "PASSED"
        assert res["num_tested_bitstrings"] == 2**N
        assert res["max_absolute_error"] < 1e-12

def test_qubit_count_matches_qubo_variables():
    for N in [4, 6, 8]:
        num_vars, qubo_matrix, _ = get_sample_qubo(N)
        opt = QAOAOptimizer(reps=2, shots=256, seed=42)
        res = opt.solve(num_vars, qubo_matrix, mode="AER")
        assert res["qubits"] == N

def test_bitstring_length_matches_qubit_count():
    for N in [4, 6, 8]:
        num_vars, qubo_matrix, _ = get_sample_qubo(N)
        opt = QAOAOptimizer(reps=2, shots=256, seed=42)
        res = opt.solve(num_vars, qubo_matrix, mode="AER")
        bitstring = res["bitstring"]
        assert len(bitstring) == N
        for b in res["top_k_bitstrings"]:
            assert len(b) == N

def test_action_mapping_matches_bitstring():
    num_vars, qubo_matrix, reduced_vars = get_sample_qubo(6)
    bitstring = [1, 0, 1, 0, 1, 0]
    actions = SolutionDecoder.decode_solution(bitstring, reduced_vars)
    assert len(actions) == 3
    for act in actions:
        assert "action_id" in act
        assert "action" in act
        assert "target" in act

def test_qiskit_endianness_is_consistent():
    # Verify bit at position i maps to variable index i
    num_vars = 3
    qubo_matrix = {(0,0): -10.0, (1,1): 0.0, (2,2): 0.0}
    opt = QAOAOptimizer(reps=1, shots=512, seed=42)
    res = opt.solve(num_vars, qubo_matrix, mode="AER")
    best_bit = res["bitstring"]
    assert best_bit[0] == 1, "Variable x_0 should be 1 because Q_00 = -10.0"

def test_qiskit_qaoa_circuit_execution_and_metadata():
    num_vars, qubo_matrix, _ = get_sample_qubo(3)
    opt = QAOAOptimizer(reps=2, shots=512, seed=42)
    res = opt.solve(num_vars, qubo_matrix, mode="AER")
    
    assert res["status"] == "SUCCESS"
    assert res["framework"] == "Qiskit"
    assert res["backend"] == "AerSimulator"
    assert res["qubits"] == 3
    assert res["qaoa_depth"] == 2
    assert res["circuit_depth"] > 0
    assert res["gate_count"] > 0
    assert res["two_qubit_gates"] > 0
    assert res["shots"] == 512
    assert len(res["bitstring"]) == 3
    assert res["fallback_used"] == False

def test_qaoa_solver_comparison_on_identical_qubo():
    num_vars, qubo_matrix, reduced_vars = get_sample_qubo(3)
    bench = OptimizationBenchmark.run_benchmark(
        num_vars, qubo_matrix, reduced_vars, [], {}, {}, {}, mode="AER"
    )
    comp = bench["comparison"]
    
    assert "exact" in comp
    assert "greedy" in comp
    assert "local_search" in comp
    assert "simulated_annealing" in comp
    assert "qaoa" in comp
    assert "qaoa_local_search" in comp
    assert "qaoa_simulated_annealing" in comp
    assert "hybrid_qaoa" in comp
    assert comp["exact"]["optimality_gap_percent"] == 0.0

def test_ablation_pipeline_and_separation():
    num_vars, qubo_matrix, _ = get_sample_qubo(3)
    opt = QAOAOptimizer(reps=2, shots=512, seed=42)
    qaoa_res = opt.solve(num_vars, qubo_matrix, mode="AER")
    hyb_res = HybridOptimizer.solve_hybrid(num_vars, qubo_matrix, qaoa_res)
    
    assert "qaoa_energy" in hyb_res
    assert "refined_energy" in hyb_res
    assert len(hyb_res["ablation_stages"]) == 5
    assert hyb_res["refined_energy"] <= hyb_res["qaoa_energy"]

def test_ibm_quantum_mode_honesty():
    num_vars, qubo_matrix, _ = get_sample_qubo(3)
    opt = QAOAOptimizer(reps=2, shots=512, seed=42)
    res = opt.solve(num_vars, qubo_matrix, mode="IBM_QUANTUM")
    
    assert res["status"] == "UNAVAILABLE"
    assert res["requested_mode"] == "IBM_QUANTUM"
    assert res["hardware_executed"] == False
    assert "NOT EXECUTED" in res["reason"]

def test_numpy_fallback_mode():
    num_vars, qubo_matrix, _ = get_sample_qubo(3)
    opt = QAOAOptimizer(reps=2, shots=512, seed=42)
    res = opt.solve(num_vars, qubo_matrix, mode="NUMPY")
    
    assert res["status"] == "SUCCESS"
    assert res["backend"] == "NumPyVectorSimulator"
    assert res["actual_mode"] == "NUMPY"
    assert res["fallback_used"] == False

def test_digital_twin_counterfactual_integration():
    network = DataLoader.load_network("data")
    graph = GraphBuilder.build_graph(network)
    StateEngine.update_occupancies(network)
    
    actions = [{"action_id": 101, "action": "SPEED_ADJUST", "target": network.trains[0].name}]
    cf = SimulatorValidator.run_counterfactual_simulation(network, [], 10, actions, horizon_mins=15)
    
    assert "baseline_delay" in cf
    assert "optimized_delay" in cf
    assert "delay_reduction_percent" in cf
