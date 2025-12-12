def run_prediction(mutatetype, slctype, crovertype):
    from ga.population import Population 
    from data.loadData import LoadData
    from ga.geneticAlgorithm import GeneticAlgorithm
    from PIL import ImageTk, Image
    loadDataObj = LoadData()
    teams = loadDataObj.load_teams()
    venues = loadDataObj.load_venues()
    timeslots = loadDataObj.load_timeslots()
    times = loadDataObj.load_times_from_csv()
    gaObj = GeneticAlgorithm()
    best_schedule = gaObj.runAlgorithm(teams, venues, timeslots,times, crovertype, slctype, mutatetype)
    if best_schedule.NoSolution:
        print("No feasible solution found.")
    else:
        best_schedule.display()
        print(best_schedule.fitness_score)
