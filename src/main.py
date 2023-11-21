import GA_core as ga_opt
import supply_chain as sc

if __name__=='__main__':

    optimizer = ga_opt.Genetic_Algorithm()
    
    optimizer.run_genetic(generations=10, population=None)

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