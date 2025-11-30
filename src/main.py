#just for testing

#import class
from ga.population import Population
from data.loadData import LoadData
from ga.Fitness import Fitness

# teams = ["A","B","C","D"]
# venues = ["V1","V2","V3"]
# timeslots = ["01-12-2025T12:00", "05-12-2025T12:00", "07-12-2025T12:00"]



loadDataObj = LoadData()
teams = loadDataObj.load_teams()
venues = loadDataObj.load_venues()
timeslots = loadDataObj.load_timeslots()
# print("Teams:", teams)
# print("Venues:", venues)
# print("TimeSlots:", timeslots)


populationObj = Population()
populationList = populationObj.generate_population(teams, venues, timeslots, 10)

fitnessObj = Fitness()

# populationObj.display_population(populationList)

for i,individual in enumerate(populationList,start=1):
    fitnessObj.fitness(individual)
    print(f"Fitness Score of Sch[{i}]:", individual.fitness_score)