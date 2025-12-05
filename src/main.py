from data.loadData import LoadData
from ga.geneticAlgorithm import GeneticAlgorithm
from tqdm import tqdm


loadDataObj = LoadData()
teams = loadDataObj.load_teams()
venues = loadDataObj.load_venues()
timeslots = loadDataObj.load_timeslots()


genaticalgorithmObj = GeneticAlgorithm()
best_schedule = genaticalgorithmObj.runAlgorithm(teams, venues, timeslots)

best_schedule.display()
print("Best Schedule Fitness Score:", best_schedule.fitness_score)



