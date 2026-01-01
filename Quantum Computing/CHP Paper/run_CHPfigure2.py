import os, math, random, subprocess, statistics
import matplotlib.pyplot as plt

CHP_EXEC = "./chp"     # adjust if needed
TRIALS = 5             # 5 is usually enough; use 10 for smoother curves

betas = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
qubits = list(range(200, 3201, 200))

def gen_circuit(filename: str, n: int, beta: float, seed: int):
    m = int(beta * n * math.log2(n))
    rng = random.Random(seed)
    with open(filename, "w") as f:
        f.write("#\n")
        for _ in range(m):
            gate = rng.choice(["c", "h", "p"])
            if gate == "c":
                a, b = rng.sample(range(n), 2)
                f.write(f"c {a} {b}\n")
            elif gate == "h":
                f.write(f"h {rng.randrange(n)}\n")
            else:
                f.write(f"p {rng.randrange(n)}\n")
        for i in range(n):
            f.write(f"m {i}\n")

def run_chp_measure_time(filename: str) -> float:
    # CHP prints banner + last line is the float. So parse last line.
    out = subprocess.check_output([CHP_EXEC, "-f", filename], text=True)
    last = out.strip().splitlines()[-1]
    return float(last)

def main():
    os.makedirs("results", exist_ok=True)

    results = {beta: [] for beta in betas}  # beta -> list of mean sec/measurement for each n

    for beta in betas:
        print(f"\n=== beta={beta} ===")
        for n in qubits:
            sec_per_meas_trials = []
            for trial in range(TRIALS):
                fname = f"results/tmp_n{n}_b{beta}_t{trial}.chp"
                seed = 1000003 * trial + 1009 * n + int(beta * 1000)
                gen_circuit(fname, n, beta, seed)
                meas_time = run_chp_measure_time(fname)
                sec_per_meas_trials.append(meas_time / n)
                os.remove(fname)

            mean_val = statistics.mean(sec_per_meas_trials)
            results[beta].append(mean_val)
            print(f"n={n:4d}  mean(sec/meas)={mean_val:.6e}")

    # Plot
    plt.figure(figsize=(10, 6))
    for beta in betas:
        plt.plot(qubits, results[beta], marker='o', linewidth=1.8, label=f"β={beta}")
    plt.xlabel("Number of Qubits (n)")
    plt.ylabel("Seconds per Measurement")
    plt.title("Reproduction of Figure 2 (CHP, measurement-only timing)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/figure2_reproduction.png", dpi=200)
    print("\nSaved: results/figure2_reproduction.png")

if __name__ == "__main__":
    main()
