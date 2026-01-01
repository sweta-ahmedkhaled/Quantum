import math, random

n = 200
beta = 0.6
m = int(beta * n * math.log2(n))

random.seed(1)

with open("one_point.chp", "w") as f:
    f.write("#\n")
    for _ in range(m):
        gate = random.choice(["c", "h", "p"])
        if gate == "c":
            a, b = random.sample(range(n), 2)
            f.write(f"c {a} {b}\n")
        elif gate == "h":
            f.write(f"h {random.randrange(n)}\n")
        else:
            f.write(f"p {random.randrange(n)}\n")
    for i in range(n):
        f.write(f"m {i}\n")

print("Wrote one_point.chp with", n, "qubits and", m, "unitary gates.")
