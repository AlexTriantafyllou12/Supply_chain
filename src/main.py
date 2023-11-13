import GA_core as ga_opt
import supply_chain as sc



if __name__=='__main__':

    optimizer = ga_opt.Genetic_Algorithm()
    
    optimizer.run_genetic(generations=10, population=None)

