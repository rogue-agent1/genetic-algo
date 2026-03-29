import argparse, random, math

def onemax(bits):
    return sum(bits)

def sphere(vals):
    return -sum(x**2 for x in vals)

def rastrigin(vals):
    n = len(vals)
    return -(10*n + sum(x**2 - 10*math.cos(2*math.pi*x) for x in vals))

PROBLEMS = {"onemax": (onemax, "binary"), "sphere": (sphere, "real"), "rastrigin": (rastrigin, "real")}

def run_ga(problem, pop_size=50, gens=100, mut_rate=0.01, dim=20, seed=None):
    if seed: random.seed(seed)
    fitness_fn, kind = PROBLEMS[problem]
    if kind == "binary":
        pop = [[random.randint(0,1) for _ in range(dim)] for _ in range(pop_size)]
    else:
        pop = [[random.uniform(-5.12, 5.12) for _ in range(dim)] for _ in range(pop_size)]
    best_ever = None
    for gen in range(gens):
        fits = [fitness_fn(ind) for ind in pop]
        best_idx = max(range(len(fits)), key=lambda i: fits[i])
        if best_ever is None or fits[best_idx] > fitness_fn(best_ever):
            best_ever = pop[best_idx][:]
        # Selection (tournament)
        new_pop = []
        for _ in range(pop_size):
            i, j = random.sample(range(pop_size), 2)
            new_pop.append(pop[i][:] if fits[i] > fits[j] else pop[j][:])
        # Crossover
        for i in range(0, pop_size-1, 2):
            pt = random.randint(1, dim-1)
            new_pop[i][pt:], new_pop[i+1][pt:] = new_pop[i+1][pt:], new_pop[i][pt:]
        # Mutation
        for ind in new_pop:
            for k in range(dim):
                if random.random() < mut_rate:
                    if kind == "binary": ind[k] = 1 - ind[k]
                    else: ind[k] += random.gauss(0, 0.5)
        pop = new_pop
        if gen % 20 == 0:
            print(f"Gen {gen:4d}: best={fitness_fn(best_ever):.4f}")
    print(f"Final:    best={fitness_fn(best_ever):.4f}")
    return best_ever

def main():
    p = argparse.ArgumentParser(description="Genetic algorithm")
    p.add_argument("problem", choices=PROBLEMS.keys())
    p.add_argument("-p", "--pop-size", type=int, default=50)
    p.add_argument("-g", "--generations", type=int, default=100)
    p.add_argument("-m", "--mutation-rate", type=float, default=0.01)
    p.add_argument("-d", "--dimensions", type=int, default=20)
    p.add_argument("--seed", type=int)
    args = p.parse_args()
    run_ga(args.problem, args.pop_size, args.generations, args.mutation_rate, args.dimensions, args.seed)

if __name__ == "__main__":
    main()
