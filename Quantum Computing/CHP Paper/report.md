# Reproducing Gottesman–Knill with the CHP Simulator

From Ahmed Khaled <b>232000046</b>
To Dr. Norhan El Sayed

## Why I did this

The Gottesman–Knill theorem says something that feels counter-intuitive at first:
> even though stabilizer circuits create superposition and entanglement, they can still be simulated efficiently on a classical computer.

Instead of just accepting this as a theoretical statement, I wanted to *see it happen* in practice.  
For that reason, I reproduced **Figure 2** from Aaronson & Gottesman’s paper *“Improved Simulation of Stabilizer Circuits”* using the original **CHP** simulator.

---

## What was simulated

For each experiment:

- I fixed a number of qubits  
  \[
  n = 200, 400, \dots, 3200
  \]

- I chose a circuit depth parameter  
  \[
  \beta = 0.6 \text{ to } 1.2
  \]

- I applied  
  \[
  m = \lfloor \beta\, n \log_2 n \rfloor
  \]
  random Clifford gates (CNOT, H, and Phase).

- Finally, **all qubits were measured in the Z basis**.

The only thing I measured was **how long the measurement stage takes**.

---

## Small changes to the CHP code (important)

I used the original CHP source code, but made a **very small and controlled modification** so the experiment could be measured cleanly:

- I added a special flag (`-f`) that:
  - suppresses all printing,
  - starts timing at the *first measurement*,
  - stops timing at the *last measurement*,
  - prints **one number only**: total measurement time in seconds.

Nothing about the stabilizer algorithm itself was changed — only how timing and output are handled.

---

## What I observed

The reproduced plot (shown above) matches the behavior reported in the paper:

- For **small β (≈ 0.6)**  
  measurement time grows slowly with the number of qubits.

- As **β increases**, the curves separate clearly.

- For **β ≥ 1.0**, the cost per measurement grows much faster, close to quadratic behavior.

![Figure 1: Reproduction of Figure 2 from Aaronson–Gottesman. 
Average seconds per measurement vs number of qubits for different β values.](./results/figure2_reproduction.png)


This happens because deeper random Clifford circuits produce **dense stabilizers**, making most measurements *indeterminate* and therefore more expensive to update.

---

## What this shows about Gottesman–Knill

This experiment made the theorem much clearer to me:

- Stabilizer circuits really are **classically simulable**.
- The simulation cost is **polynomial**, not exponential.
- However, “efficient” does not mean “always fast” — circuit structure matters a lot.

Seeing this transition directly in runtime made the theorem feel concrete rather than abstract.

---
Working directly with the CHP code helped me understand *why* Clifford circuits are special, and why non-Clifford gates are essential for quantum advantage.
