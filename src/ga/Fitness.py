from ga.Constrains import Constraints
from ga.individual import ScheduleIndividual

class Fitness:
    def __init__(self):
        self.constraintsObj = Constraints()

    def fitness(self,individual):
        self.constraintsObj.Team_Played = {}
        self.constraintsObj.venue_usage = {}
        self.constraintsObj.team_last_match_day = {}
        self.constraintsObj.team_times = {}
        individual.fitness_score = 10000  # Reset fitness score to a base value

        c = self.constraintsObj
        penalty1 = c.TwoMatchesPerTeamatSameDay(individual) 
        penalty2 = c.VenueConfliictConstraint(individual) 
        penalty3 = c.RestDayConstraint(individual) 
        penalty4 = c.FairTimeDistributionConstraint(individual)

        total_penalty = penalty1 + penalty2 + penalty3 + penalty4  # Sum of all penalties

        individual.fitness_score -= total_penalty # Subtract penalties from fitness score

        individual.penalties = {
           'TwoMatchesPerTeamatSameDay': penalty1,
           'VenueConfliictConstraint': penalty2,
           'RestDayConstraint': penalty3,
           'FairTimeDistributionConstraint': penalty4
       }