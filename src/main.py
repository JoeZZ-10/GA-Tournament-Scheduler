#just for testing

#import class
from ga.population import Population
from data.loadData import LoadData
from ga.Fitness import Fitness
from ga.Selection import Selection
from ga.crossover import Crossover

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

selectionObj = Selection()
selectedIndividuals = selectionObj.select_population(populationList, selection_size=10)
print("\nSelected Individuals after Tournament Selection:")
for i,individual in enumerate(selectedIndividuals,start=1):
    print(f"Selected Sch[{i}] Fitness Score:", individual.fitness_score)

CrossoverObj = Crossover()
parent1 = selectedIndividuals[0]
parent2 = selectedIndividuals[1]
print("\nPerforming Single Point Crossover between two selected individuals:")
child1, child2 = CrossoverObj.single_point_crossover(parent1, parent2)
fitnessObj.fitness(child1)
fitnessObj.fitness(child2)
print("Child 1 Fitness Score after evaluation:", child1.fitness_score)
print("Child 2 Fitness Score after evaluation:", child2.fitness_score)

