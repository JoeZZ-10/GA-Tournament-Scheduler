from Create_Plots import PlotManager

def run_prediction(mutatetype, slctype, crovertype):
    from ga.population import Population 
    from data.loadData import LoadData
    from ga.geneticAlgorithm import GeneticAlgorithm
    from ScheduleViewer import ScheduleViewer
    
    loadDataObj = LoadData()
    teams = loadDataObj.load_teams()
    venues = loadDataObj.load_venues()
    timeslots = loadDataObj.load_timeslots()
    times = loadDataObj.load_times_from_csv()
    
    gaObj = GeneticAlgorithm()
    print(f"\nRunning GA with:")
    print(f"  Crossover: {crovertype}")
    print(f"  Selection: {slctype}")
    print(f"  Mutation: {mutatetype}")
    print("-" * 50)
    
    # Run the genetic algorithm and get fitness data
    best_schedule, best_fitness_per_gen, avg_fitness_per_gen = gaObj.runAlgorithm(
        teams, venues, timeslots, times, crovertype, slctype, mutatetype
    )
    
    print(f"\nFinal Best Fitness: {best_schedule.fitness_score}")
    
    if best_schedule.fitness_score < 0:
        print("No feasible solution found.")
        print(f"Fitness Score: {best_schedule.fitness_score}")
    else:
        # Display schedule in console
        best_schedule.display()
        
        # Create plots
        plot_manager = PlotManager()
        config_name = f"{crovertype}_{slctype}_{mutatetype}"
        
        # Create fitness evolution plot
        plot_manager.create_fitness_plot(
            best_fitness_per_gen,
            avg_fitness_per_gen,
            crovertype,
            slctype,
            mutatetype
        )
        
        # Create penalty breakdown plot if penalties exist
        if hasattr(best_schedule, 'penalties') and best_schedule.penalties:
            plot_manager.create_penalty_breakdown_plot(
                best_schedule.penalties,
                config_name
            )
        
        # Open schedule viewer GUI
        viewer = ScheduleViewer(best_schedule)
    
    return viewer, best_fitness_per_gen, avg_fitness_per_gen