from ga.Constrains import Constraints
from ga.individual import ScheduleIndividual

class Fitness:

    def fitness(self,individual):
        constraintsObj = Constraints()

        penalty1 = constraintsObj.TwoMatchesPerTeamatSameDay(individual) # Constraint 1
        penalty2 = constraintsObj.VenueConfliictConstraint(individual) # Constraint 2
        penalty3 = constraintsObj.RestDayConstraint(individual) # Constraint 3
        penalty4 = constraintsObj.FairTimeDistributionConstraint(individual) # Constraint 4

        total_penalty = penalty1 + penalty2 + penalty3 + penalty4  # Sum of all penalties

        individual.fitness_score -= total_penalty # Subtract penalties from fitness score

        if individual.fitness_score < 0:
            individual.penalties = {
                'TwoMatchesPerTeamatSameDay': penalty1,
                'VenueConfliictConstraint': penalty2,
                'RestDayConstraint': penalty3,
                'FairTimeDistributionConstraint': penalty4
            }