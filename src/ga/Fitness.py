from ga.Constrains import Constraints
from ga.individual import ScheduleIndividual

class Fitness:

    def fitness(self,individual):
        constraintsObj = Constraints()

        penalty1 = constraintsObj.TwoMatchesPerTeamatSameTime(individual)
        penalty2 = constraintsObj.VenueConfliictConstraint(individual)
        penalty3 = constraintsObj.RestDayConstraint(individual)

        total_penalty = penalty1 + penalty2 + penalty3

        individual.fitness_score -= total_penalty