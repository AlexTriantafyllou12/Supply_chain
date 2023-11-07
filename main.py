import GA_core.ga_classes as ga_opt



if __name__=='__main__':

    optimizer = ga_opt.Genetic_Algorithm()
    
    optimizer.run_genetic(generations=10)