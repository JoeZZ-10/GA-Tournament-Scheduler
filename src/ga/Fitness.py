from ga.Constrains import Constraints
from ga.individual import ScheduleIndividual

class Fitness:

    def fitness(self,individual):
        constraintsObj = Constraints()

        penalty1 = constraintsObj.TwoMatchesPerTeamatSameTime(individual) # Constraint 1
        penalty2 = constraintsObj.VenueConfliictConstraint(individual) # Constraint 2
        penalty3 = constraintsObj.RestDayConstraint(individual) # Constraint 3

        total_penalty = penalty1 + penalty2 + penalty3 # Sum of all penalties

        individual.fitness_score -= total_penalty # Subtract penalties from fitness score