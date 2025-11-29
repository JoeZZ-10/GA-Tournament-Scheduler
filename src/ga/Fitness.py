from ga.Constrains import Constraints
from ga.individual import ScheduleIndividual

class Fitness:
    def __init__(self, populationList):
        self.populationList = populationList

    def fitness(self):
        for individual in self.populationList:
            constraintsObj = Constraints()

            penalty1 = constraintsObj.TwoMatchesPerTeamatSameTime(individual)
            penalty2 = constraintsObj.VenueConfliictConstraint(individual)

            total_penalty = penalty1 + penalty2

            individual.fitness_score -= total_penalty