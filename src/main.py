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
    populationObj = Population()
    gaObj = GeneticAlgorithm()
    best_schedule = gaObj.runAlgorithm(teams, venues, timeslots,times, crovertype, slctype, mutatetype)
    best_schedule.display()
    
    
    populationList = populationObj.generate_population(teams,venues,timeslots,times, 30)
    populationObj.display_population(populationList)

    for i,individual in enumerate(populationList,start=1):
        print(f"Fitness Score of Sch[{i}]:", individual.fitness_score)
