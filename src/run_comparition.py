"""
Script to run multiple GA configurations and compare results
"""
from ga.geneticAlgorithm import GeneticAlgorithm
from data.loadData import LoadData
from Create_Plots import PlotManager

def run_comparison():
    """
    Run GA with different configurations and create comparison plots
    """
    # Load data
    loadDataObj = LoadData()
    teams = loadDataObj.load_teams()
    venues = loadDataObj.load_venues()
    timeslots = loadDataObj.load_timeslots()
    times = loadDataObj.load_times_from_csv()
    
    # Define configurations to test
    configurations = [
        # Crossover variations
        {"crossover": "one_point", "selection": "rank", "mutation": "Random_Resetting"},
        {"crossover": "two_point", "selection": "rank", "mutation": "Random_Resetting"},
        {"crossover": "uniform", "selection": "rank", "mutation": "Random_Resetting"},
        
        # Selection variations
        {"crossover": "one_point", "selection": "tournament", "mutation": "Random_Resetting"},
        {"crossover": "one_point", "selection": "rank", "mutation": "Random_Resetting"},
        
        # Mutation variations
        {"crossover": "one_point", "selection": "rank", "mutation": "Random_Resetting"},
        {"crossover": "one_point", "selection": "rank", "mutation": "Inversion_Mutation"},
    ]
    
    results = {}
    plot_manager = PlotManager()
    
    print("=" * 80)
    print("RUNNING GENETIC ALGORITHM COMPARISON")
    print("=" * 80)
    
    for idx, config in enumerate(configurations, 1):
        config_name = f"{config['crossover']}_{config['selection']}_{config['mutation']}"
        
        # Skip duplicate configurations
        if config_name in results:
            print(f"\n[{idx}/{len(configurations)}] Skipping duplicate: {config_name}")
            continue
        
        print(f"\n[{idx}/{len(configurations)}] Running configuration: {config_name}")
        print("-" * 80)
        
        # Run GA
        gaObj = GeneticAlgorithm()
        best_schedule, best_fitness, avg_fitness = gaObj.runAlgorithm(
            teams, venues, timeslots, times,
            config['crossover'],
            config['selection'],
            config['mutation']
        )
        
        # Store results
        results[config_name] = {
            'best_fitness': best_fitness,
            'avg_fitness': avg_fitness,
            'final_fitness': best_schedule.fitness_score,
            'crossover': config['crossover'],
            'selection': config['selection'],
            'mutation': config['mutation']
        }
        
        print(f"Final Fitness: {best_schedule.fitness_score}")
        
        # Create individual plot
        plot_manager.create_fitness_plot(
            best_fitness,
            avg_fitness,
            config['crossover'],
            config['selection'],
            config['mutation']
        )
        
        # Create penalty plot if applicable
        if hasattr(best_schedule, 'penalties') and best_schedule.penalties:
            plot_manager.create_penalty_breakdown_plot(
                best_schedule.penalties,
                config_name
            )
    
    # Create comparison plot for all configurations
    print("\n" + "=" * 80)
    print("Creating comparison plot...")
    print("=" * 80)
    plot_manager.create_comparison_plot(results)
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY OF RESULTS")
    print("=" * 80)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['final_fitness'], reverse=True)
    
    print(f"\n{'Rank':<6} {'Configuration':<50} {'Final Fitness':<15}")
    print("-" * 80)
    
    for rank, (config_name, data) in enumerate(sorted_results, 1):
        print(f"{rank:<6} {config_name:<50} {data['final_fitness']:<15}")
    
    print("\n" + "=" * 80)
    print(f"Best configuration: {sorted_results[0][0]}")
    print(f"Best fitness achieved: {sorted_results[0][1]['final_fitness']}")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    results = run_comparison()