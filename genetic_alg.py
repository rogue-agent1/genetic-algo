#!/usr/bin/env python3
"""genetic_alg - GA optimizer."""
import sys,argparse,json,random,math
def onemax(individual):return sum(individual)
def sphere(individual):return -sum(x**2 for x in individual)
def rastrigin(individual):n=len(individual);return -(10*n+sum(x**2-10*math.cos(2*math.pi*x) for x in individual))
class GA:
    def __init__(self,pop_size,gene_len,fitness_fn,gene_type="binary"):
        self.pop_size=pop_size;self.gene_len=gene_len;self.fitness=fitness_fn;self.gene_type=gene_type
        if gene_type=="binary":self.pop=[[random.randint(0,1) for _ in range(gene_len)] for _ in range(pop_size)]
        else:self.pop=[[random.uniform(-5,5) for _ in range(gene_len)] for _ in range(pop_size)]
    def evolve(self,generations=100,mutation_rate=0.01):
        history=[]
        for gen in range(generations):
            scored=[(self.fitness(ind),ind) for ind in self.pop]
            scored.sort(reverse=True);best=scored[0]
            history.append({"gen":gen,"best_fitness":round(best[0],4)})
            parents=[ind for _,ind in scored[:self.pop_size//2]]
            children=[]
            while len(children)<self.pop_size:
                p1,p2=random.sample(parents,2)
                cx=random.randint(1,self.gene_len-1)
                child=p1[:cx]+p2[cx:]
                for i in range(len(child)):
                    if random.random()<mutation_rate:
                        if self.gene_type=="binary":child[i]=1-child[i]
                        else:child[i]+=random.gauss(0,0.5)
                children.append(child)
            self.pop=children
        return best,history
def main():
    p=argparse.ArgumentParser(description="Genetic algorithm")
    p.add_argument("--problem",choices=["onemax","sphere","rastrigin"],default="onemax")
    p.add_argument("--pop",type=int,default=50);p.add_argument("--genes",type=int,default=20)
    p.add_argument("--gens",type=int,default=100);p.add_argument("--mutation",type=float,default=0.02)
    args=p.parse_args()
    fns={"onemax":(onemax,"binary"),"sphere":(sphere,"real"),"rastrigin":(rastrigin,"real")}
    fn,gtype=fns[args.problem]
    ga=GA(args.pop,args.genes,fn,gtype)
    best,history=ga.evolve(args.gens,args.mutation)
    print(json.dumps({"problem":args.problem,"best_fitness":round(best[0],4),"generations":args.gens,"history":history[::max(1,args.gens//10)]},indent=2))
if __name__=="__main__":main()
