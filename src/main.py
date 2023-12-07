import GA_core as ga_opt
import supply_chain as sc

if __name__=='__main__':

    skus = []
    # generate some random SKUs
    for i in range(5):
        sku = sc.SKU(name= "sku_" + str(i), 
                     quantity= i)
        skus.append(sku)

    # initialise the GA
    optimizer = ga_opt.Genetic_Algorithm()
    # initialise the population
    optimizer.create_population(size= 100,
                                skus= skus)
    
    print(len(optimizer.population))
    parentA = optimizer.population[10:20]
    parentB = optimizer.population[20:30]


    next_gen = optimizer.crossover(parentsA=parentA, parentsB=parentB)
    print(len(next_gen))

"""
    0) Initialise the SKU objects

    1) Initialise the initial population (for i in population_size):
        1.1) Initialise an individual solution:
            1.1.1) Generate random splits of random length of the skus 
            1.2.1) Per sku split:
                1.2.1.1) Generate a random split of SKUs and assign demnad type for each split - the solution will need to be aware of the demand types?
                1.2.1.2) Generate a policy (smart initiation of the policy?)

            1.3.1) Combine the policies into 
        1.2) Add the individual solution to the list of solutions (i.e., the population)
    

        
    Fitness Function: 
        FF = Order Costs + Holding Costs + Stockout Costs 

    
"""