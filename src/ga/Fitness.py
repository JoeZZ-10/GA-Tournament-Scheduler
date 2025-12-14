from ga.Constrains import Constraints
from ga.individualV2 import ScheduleIndividualV2

class Fitness:
    def __init__(self):
        self.constraintsObj = Constraints()

    def fitness(self,individual):
        self.constraintsObj.Team_Played = {}
        self.constraintsObj.venue_usage = {}
        self.constraintsObj.team_last_match_day = {}
        self.constraintsObj.team_times = {}
        self.round_last_date = {}
        self.TwoMatchesPerTeamatSameDay_Conflict_Found = 0
        self.Venue_Conflict_Found = 0
        self.Rest_Violations_Conflict_Found = 0
        self.Fair_Time_Distribution_Conflict_Found = 0
        self.DatesOfRoundNotSorted_Conflict_Found = 0
        individual.fitness_score = 10000  # Reset fitness score before calculation

        for round_matches in individual.schedule:
            for m in round_matches:
                self.TwoMatchesPerTeamatSameDay_Conflict_Found += self.constraintsObj.TwoMatchesPerTeamatSameDay(m) # Constraint 1
                self.Venue_Conflict_Found += self.constraintsObj.VenueConfliictConstraint(m) # Constraint 2
                self.Rest_Violations_Conflict_Found += self.constraintsObj.RestDayConstraint(m) # Constraint 3
                self.Fair_Time_Distribution_Conflict_Found += self.constraintsObj.FairTimeDistributionConstraint(m) # Constraint 4

        TwoMatchesPerTeamatSameDay_penalty = self.TwoMatchesPerTeamatSameDay_Conflict_Found * 500
        VenueConfliictConstraint_penalty = self.Venue_Conflict_Found * 200
        RestDayConstraint_penalty = self.Rest_Violations_Conflict_Found * 100
        FairTimeDistributionConstraint_penalty = self.Fair_Time_Distribution_Conflict_Found * 50

        total_penalty = TwoMatchesPerTeamatSameDay_penalty + VenueConfliictConstraint_penalty + RestDayConstraint_penalty + FairTimeDistributionConstraint_penalty  # Sum of all penalties

        individual.fitness_score -= total_penalty # Subtract penalties from fitness score
        individual.penalties = {
            'TwoMatchesPerTeamatSameDay': TwoMatchesPerTeamatSameDay_penalty,
            'VenueConfliictConstraint': VenueConfliictConstraint_penalty,
            'RestDayConstraint':   RestDayConstraint_penalty,
            'FairTimeDistributionConstraint': FairTimeDistributionConstraint_penalty,
        }