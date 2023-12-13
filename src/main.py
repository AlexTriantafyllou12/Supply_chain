import GA_core as ga_opt
import supply_chain as sc
import utilities as util

if __name__=='__main__':

    nr_skus = 5
    time_periods = 30

    skus = []
    # generate some random SKUs
    for i in range(nr_skus):
        sku = sc.SKU(name= "sku_" + str(i), 
                     quantity= i*80,
                     per_item_cost=10*i+10)
        skus.append(sku)

    demand_factory = util.Demand_Factory(time_periods)

    # generate demand
    demand = demand_factory.generate(nr_skus=nr_skus, split=[1, 2, 2], type=['random', 'trend', 'seasonal'])
    demand.to_csv('demand.csv', index=False)

    # initialise the GA
    optimizer = ga_opt.Genetic_Algorithm()
    # initialise the population
    optimizer.create_population(size= 100,
                                skus= skus)
    
    # create some parents
    print(len(optimizer.population))
    parentA = optimizer.population[10:20]
    parentB = optimizer.population[20:30]

    # crossover
    next_gen = optimizer.crossover(parentsA=parentA, parentsB=parentB)
    print(len(next_gen))

    # mutate
    optimizer.mutate()

    # evaluate a policy
    rand_policy = optimizer.population[2]
    print(rand_policy.solution)
    fitness = rand_policy.solution_evaluation(demand=demand, time_periods=time_periods)
    print('Fitness: ' + str(fitness))

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