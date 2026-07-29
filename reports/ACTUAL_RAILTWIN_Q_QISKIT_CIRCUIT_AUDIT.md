# RailTwin-Q — Actual Implemented Qiskit QAOA Circuit Audit

## 1. Executive Summary

This audit report presents a forensic investigation of the Qiskit Quantum Approximate Optimization Algorithm (QAOA) circuit as implemented and executed in the **RailTwin-Q** digital twin workspace. Rather than describing an idealized or theoretical algorithm, this report documents the exact parameters, qubit mappings, mathematical operators, gate-level decompositions, and classical post-processing steps found in the active source code.

**Key Findings:**
1. The codebase generates a **10-qubit parameterized QAOA circuit** with a variational depth of $p = 2$.
2. Qubits represent binary decision variables representing station-hold and speed-adjustment interventions.
3. The circuit is executed on Qiskit's **`AerSimulator`** (a classical CPU-based simulation backend), not physical quantum hardware.
4. The raw QAOA circuit outputs an all-zeros state `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]` with energy `0.0`. 
5. The final feasible plan `[0, 0, 1, 0, 0, 0, 0, 1, 1, 0]` (energy `-0.5445`) is found through **classical refinement** (1-bit/2-bit neighborhood search and Simulated Annealing) applied to the quantum candidate pool. No quantum advantage is demonstrated.

---

## 2. Exact Runtime Configuration

The active digital twin runs with the following configurations during a re-optimization trigger:
* **Number of Decision Variables:** 10
* **QAOA Depth ($p$):** 2
* **Backend:** `AerSimulator` (Local Simulator)
* **Optimization Method:** COBYLA (constrained optimization by linear approximation)
* **Number of Optimization Restarts (Multi-start):** 3
* **Aer Shots per Step:** 1024
* **Warm-Start Status:** Enabled (uses classical warm-start initial state bias)
* **Switching Penalty (Stability):** Injecting Switching Penalties with $p_{switch} = 0.15$

---

## 3. Actual Qubit Count

The number of qubits is dynamically determined by the variable reduction engine [DecisionVariables](file:///c:/Users/idhay/Desktop/RailTwin-Q/ai/quantum_optimization/decision_variables.py), capped at a maximum of **10 qubits**. Each qubit represents a single binary decision variable $x_i \in \{0, 1\}$ mapped to a feasible railway control action.

---

## 4. Qubit-to-Action Mapping

The active mapping from the latest re-optimization run at simulation tick 60 maps the 10 qubits to the following train control actions:

| Qubit | Binary Variable | Candidate Action ID | Train Name | Location / Station | Action Meaning |
|---|---|---|---|---|---|
| **q0** | $x_0$ | Action 1 | Chennai Mail | Chennai Central (MAS) | 0=Free Run, 1=Hold at station |
| **q1** | $x_1$ | Action 2 | Chennai Mail Return | Jolarpettai Junction (JTJ) | 0=Free Run, 1=Hold at station |
| **q2** | $x_2$ | Action 3 | Kerala Express | Chennai Central (MAS) | 0=Free Run, 1=Hold at station |
| **q3** | $x_3$ | Action 4 | Sapthagiri Express | Arakkonam Junction (AJJ) | 0=Free Run, 1=Hold at station |
| **q4** | $x_4$ | Action 5 | Shatabdi Express | Chennai Central (MAS) | 0=Free Run, 1=Hold at station |
| **q5** | $x_5$ | Action 6 | Grand Trunk Express | Tirupati (TPTY) | 0=Free Run, 1=Hold at station |
| **q6** | $x_6$ | Action 7 | Double Decker Express | Chennai Central (MAS) | 0=Free Run, 1=Hold at station |
| **q7** | $x_7$ | Action 8 | Tirupati Express | Chennai Central (MAS) | 0=Free Run, 1=Hold at station |
| **q8** | $x_8$ | Action 13 | Lalbagh Express | Chennai Central (MAS) | 0=Free Run, 1=Hold at station |
| **q9** | $x_9$ | Action 17 | Chennai Mail | Chennai Central (MAS) | 0=Normal Speed, 1=Speed Adjust |

---

## 5. Exact QUBO Matrix

The dynamic Quadratic Unconstrained Binary Optimization (QUBO) problem is defined as:
$$E(x) = \sum_{i} Q_{ii} x_i + \sum_{i < j} Q_{ij} x_i x_j$$

For the tick 60 run, the non-zero coefficients of the QUBO matrix $Q$ are:
* **Diagonal Coefficients ($Q_{ii}$):**
  * $Q_{00} = 0.1185$
  * $Q_{11} = 0.1185$
  * $Q_{22} = -0.1815$
  * $Q_{33} = 0.1185$
  * $Q_{44} = 0.1185$
  * $Q_{55} = 0.1185$
  * $Q_{66} = 0.1185$
  * $Q_{77} = -0.1815$
  * $Q_{88} = -0.1815$
  * $Q_{99} = 0.1285$
* **Off-Diagonal Coefficients ($Q_{ij}$):**
  * $Q_{09} = 6.0$

All other $Q_{ij} = 0.0$. The large positive quadratic term $Q_{09} = 6.0$ enforces a mutual exclusion constraint between holding the Chennai Mail ($x_0$) and adjusting its speed ($x_9$).

---

## 6. QUBO-to-Ising Transformation

The binary variables $x_i \in \{0, 1\}$ are mapped to spin variables $Z_i \in \{-1, +1\}$ using the transformation:
$$x_i = \frac{I - Z_i}{2}$$

Substituting this into $E(x)$ transforms the QUBO problem into a Hamiltonian $H_C$:
$$H_C = \sum_{i} h_i Z_i + \sum_{i < j} J_{ij} Z_i Z_j + C_{offset}$$

The parameters calculated by [QUBOBuilder.qubo_to_ising](file:///c:/Users/idhay/Desktop/RailTwin-Q/ai/quantum_optimization/qubo_builder.py#L45-L118) are:
* **Constant Energy Offset ($C_{offset}$):** $1.6475$
* **Linear Coefficients ($h_i$):**
  * $h_0 = -1.55925$
  * $h_1 = -0.05925$
  * $h_2 = 0.09075$
  * $h_3 = -0.05925$
  * $h_4 = -0.05925$
  * $h_5 = -0.05925$
  * $h_6 = -0.05925$
  * $h_7 = 0.09075$
  * $h_8 = 0.09075$
  * $h_9 = -1.56425$
* **Quadratic Coupling ($J_{ij}$):**
  * $J_{09} = 1.5$

---

## 7. Cost Hamiltonian

The Cost Hamiltonian $H_C$ acts on the 10 qubits:
$$H_C = -1.55925 Z_0 - 0.05925 Z_1 + 0.09075 Z_2 - 0.05925 Z_3 - 0.05925 Z_4 - 0.05925 Z_5 - 0.05925 Z_6 + 0.09075 Z_7 + 0.09075 Z_8 - 1.56425 Z_9 + 1.5 Z_0 Z_9$$

In the QAOA circuit, the unitary operator $U_C(\gamma) = e^{-i \gamma H_C}$ is implemented using single-qubit rotation gates ($R_Z$) and CNOT-RZ-CNOT gates:
1. **Single-Qubit Rotation Terms:**
   * $e^{-i \gamma h_i Z_i} \rightarrow R_z(2 \gamma h_i, i)$
2. **Two-Qubit Coupling Terms:**
   * $e^{-i \gamma J_{09} Z_0 Z_9} \rightarrow CX(0, 9) \rightarrow R_z(2 \gamma J_{09}, 9) \rightarrow CX(0, 9)$

---

## 8. Mixer Hamiltonian

The standard transverse-field mixer is used:
$$H_M = \sum_{i=0}^{9} X_i$$

The mixer unitary operator $U_M(\beta) = e^{-i \beta H_M}$ is implemented on each qubit using:
$$e^{-i \beta X_i} \rightarrow R_x(2 \beta, i)$$

---

## 9. Exact QAOA Circuit

The Qiskit parameterized circuit implemented in [qaoa_optimizer.py](file:///c:/Users/idhay/Desktop/RailTwin-Q/ai/quantum_optimization/qaoa_optimizer.py#L97-L294) has the following structure:

```text
                  --- Parameterized QAOA Structure (p = 2) ---

      q_0: ──[ RY ]──[ Rz(2h0*g0) ]────●────────────────────●──[ Rx(2b0) ]──[ Rz(2h0*g1) ]────●────────────────────●──[ Rx(2b1) ]──[M]
      q_1: ──[ RY ]──[ Rz(2h1*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h1*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_2: ──[ RY ]──[ Rz(2h2*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h2*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_3: ──[ RY ]──[ Rz(2h3*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h3*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_4: ──[ RY ]──[ Rz(2h4*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h4*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_5: ──[ RY ]──[ Rz(2h5*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h5*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_6: ──[ RY ]──[ Rz(2h6*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h6*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_7: ──[ RY ]──[ Rz(2h7*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h7*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_8: ──[ RY ]──[ Rz(2h8*g0) ]────┼────────────────────┼──[ Rx(2b0) ]──[ Rz(2h8*g1) ]────┼────────────────────┼──[ Rx(2b1) ]──[M]
      q_9: ──[ RY ]──[ Rz(2h9*g0) ]───[CX]──[ Rz(2J09*g0) ]──[CX]──[ Rx(2b0) ]──[ Rz(2h9*g1) ]───[CX]──[ Rz(2J09*g1) ]──[CX]──[ Rx(2b1) ]──[M]
```

---

## 10. Gate-by-Gate Explanation

* **`RY(2 * delta, idx)` / `RY(-2 * delta, idx)`**: Initial state preparation using warm-start bias. Instead of creating a uniform superposition $|+\rangle^{\otimes N}$ using Hadamard gates, the warm-start vector biases initial qubits towards promising directions found by classical pre-solvers.
* **`RZ(2 * gammas[k] * h_i, i)`**: Implements the phase rotation associated with linear Ising terms $h_i Z_i$. Rotates the qubit around the Z-axis by an angle proportional to the parameterized phase $\gamma_k$ and the coefficient $h_i$.
* **`CX(i, j) -> RZ(2 * gammas[k] * J_ij, j) -> CX(i, j)`**: Implements the entangling interaction associated with the quadratic coupling term $J_{ij} Z_i Z_j$. Evaluates the parity of $q_i$ and $q_j$, applies a phase rotation to $q_j$, and un-computes the parity.
* **`RX(2 * betas[k], i)`**: Transverse-field mixing rotation. Rotates each qubit around the X-axis by $2 \beta_k$ to drive quantum transitions between states.
* **`Measure`**: Projects the final quantum state onto the computational basis, collapsing the superposition to produce a classical 10-bit binary string.

---

## 11. Circuit Statistics

* **Qubits:** 10
* **QAOA Depth ($p$):** 2
* **Transpiled Circuit Depth:** 23 (transpiled to basis `['id', 'rz', 'sx', 'x', 'cx']` and linear layout)
* **Total Transpiled Gates:** 166 (Single-qubit: 162, Two-qubit: 4)
* **CX Gates:** 4
* **Shots:** 1024

---

## 12. Qiskit Implementation

The standalone script generating this exact circuit is stored at [tools/generate_actual_qaoa_circuit.py](file:///c:/Users/idhay/Desktop/RailTwin-Q/tools/generate_actual_qaoa_circuit.py). It reconstructs the dynamic QUBO, converts it to Ising terms, instantiates a parameterized Qiskit `QuantumCircuit`, transpiles it to basis gates, and saves the text diagram to `reports/actual_qaoa_circuit.txt` and the OpenQASM 2.0 file to `reports/actual_qaoa_circuit.qasm`.

---

## 13. AerSimulator Execution

The circuit runs on **Qiskit's `AerSimulator`** locally, which simulates quantum operations classically on CPU cores. Because the simulation runs classically:
1. No physical quantum coherence or gate noise affects the calculation.
2. The simulation runtime scales exponentially with qubit count $N$, restricting live runs to a capped $N = 10$.
3. Physical execution on IBM Quantum hardware is marked as **`NOT EXECUTED`** in the dashboard and report outputs to maintain strict scientific honesty.

---

## 14. Measurement and Bitstring Decoding

Upon circuit completion, the `AerSimulator` takes 1024 shots (measurements). 
* **Raw QAOA Output:** The most probable bitstring sampled is `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]` with a QUBO energy of `0.0`.
* **Interpretation:** This raw quantum result represents a "do-nothing" baseline plan (rejecting all interventions). This occurs because the standard transverse mixer and small $p=2$ depth under classical optimization of parameters default to a conservative, low-risk state.

---

## 15. Classical Refinement After QAOA

Because the raw quantum candidate has a high optimality gap, [HybridOptimizer.solve_hybrid](file:///c:/Users/idhay/Desktop/RailTwin-Q/ai/quantum_optimization/hybrid_optimizer.py#L8-L176) executes a **5-stage classical refinement pipeline**:
1. **Raw QAOA:** Candidate `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]` (Energy: `0.0`)
2. **Top-K Deduplication:** Candidate `[0, 0, 0, 0, 0, 0, 0, 1, 0, 0]` (Energy: `-0.1815`) — selects x7 (Hold Tirupati Express)
3. **1-Bit Neighborhood Search:** Candidate `[0, 0, 1, 0, 0, 0, 0, 1, 0, 0]` (Energy: `-0.363`) — selects x2 (Hold Kerala Express) + x7
4. **2-Bit Neighborhood Search:** Candidate `[0, 0, 1, 0, 0, 0, 0, 1, 1, 0]` (Energy: `-0.5445`) — selects x2 + x7 + x8 (Hold Lalbagh Express)
5. **Local SA Refinement:** Candidate `[0, 0, 1, 0, 0, 0, 0, 1, 1, 0]` (Energy: `-0.5445`) — converges on global optimum.

---

## 16. Quantum Contribution vs Classical Contribution

The energy levels across the stages clearly identify the contributions:

* **Quantum Contribution:** $0.0\%$ (produces the all-zeros baseline).
* **Classical Contribution:** $100.0\%$ (drives the energy from `0.0` down to the global minimum of `-0.5445`).

---

## 17. Scientific Limitations

1. **Simulation Scale:** Classical simulation of quantum circuits scales exponentially in memory and time ($O(2^N)$). Running QAOA on $N \ge 30$ is classically intractable in real-time, meaning the current simulator approach cannot scale without physical hardware access.
2. **Quantum Advantage:** No quantum advantage or speedup is demonstrated. Classical solvers (Exact, Greedy, Simulated Annealing) solve the 10-variable problem in sub-millisecond runtimes on a standard CPU, whereas the Qiskit Aer QAOA simulator requires $\sim 1.7$ seconds.
3. **Transpilation Routing Overhead:** The CNOT gate between non-adjacent qubits $q_0$ and $q_9$ requires routing. While the local simulator bypasses layout penalties, mapping this circuit to physical linear topologies would require multiple SWAP gates, expanding circuit depth and gate errors.

---

## 18. Discrepancies Between Documentation and Code

To uphold forensic audit integrity, we document the following discrepancies:
* **Documentation Claims:** Earlier drafts claimed "Quantum speedup" and "proven global optimum via QAOA".
* **Source Code Reality:** The optimization solver uses a hybrid pipeline where the actual global optimum is discovered entirely by classical neighborhood search post-processing.
* **Correction:** The frontend dashboard has been successfully updated to display **"Quantum optimization mode: QAOA-based probabilistic search + classical refinement"** and explicitly warns that **"Quantum advantage not yet demonstrated at current simulation scale."** This aligns the user interface with the reality of the codebase.

---

## 19. Judge-Ready Explanation

Here are clear, precise answers to judge questions:
1. **What does each qubit represent?** One qubit represents a binary decision variable ($x_i \in \{0,1\}$) corresponding to a recommended dispatching intervention (e.g. HOLD train at station).
2. **Why are there N qubits?** Because the search space is reduced to $N=10$ candidate actions.
3. **What is the QUBO?** It is a mathematical matrix combining dispatching benefits (delay savings) with capacity constraints (safety headway) as penalties.
4. **How is the problem converted into QUBO?** Headway violations are encoded as quadratic penalties ($Q_{ij} = 6.0$) to penalize conflicting actions.
5. **How is QUBO converted to an Ising Hamiltonian?** Via algebraic substitution $x_i = (I-Z_i)/2$.
6. **Where exactly is Qiskit used?** To define, transpile, and classically simulate the QAOA circuit.
7. **What does QAOA do?** It projects the problem space onto a quantum state and optimizes gamma/beta parameters to maximize the probability of sampling low-energy configurations.
8. **What does each layer do?** Each layer applies the Cost Hamiltonian (phase rotation) followed by the Mixer Hamiltonian (driving state transitions).
9. **What does the measurement produce?** A 10-bit binary string representing selected control actions.
10. **How is it decoded?** Qubits with value `1` are translated back to operational interventions (e.g. HOLD Kerala Express).
11. **What happens after QAOA?** The output string is passed through local searches to fix constraint violations.
12. **Is there quantum advantage?** No, classical simulation cannot outperform classical solvers on small problems.
13. **What is the genuine quantum contribution?** Demonstration of a verifiable hybrid quantum-classical optimization workflow ready for hardware deployment.

---

## 20. Final Scientific Verdict

The RailTwin-Q repository implements a genuine, mathematically correct, and parameterized Qiskit QAOA workflow. However, at its current scale, the quantum circuit acts as a probabilistic sampler classically simulated on CPU cores. The final optimal interventions are discovered and verified by classical post-processing algorithms. The project represents a **Quantum-Ready Hybrid Architecture**, but does not demonstrate quantum supremacy or advantage.
