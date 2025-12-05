import random
import copy
import pandas as pd

class Mutation:

    def __init__(self, teams=None, venues=None, timeslots=None):
        self.teams = teams if teams is not None else []
        self.venues = venues if venues is not None else []
        self.timeslots = timeslots if timeslots is not None else []

    def mutate(self, individual, mutation_rate=0.01):
        new_individual = copy.deepcopy(individual)
        for r in range(len(new_individual.schedule)):
            if random.random() < mutation_rate:
                self.mutate_round(new_individual.schedule[r])
        return new_individual

    def mutate_round(self, round_matches):
        if len(round_matches) < 2:
            self.modify_single_match(round_matches[0])
            return
        
        mutation_type = random.choice(["swap_matches", "swap_teams", "change_slot", "change_team"])
        
        if mutation_type == "swap_matches":
            i, j = random.sample(range(len(round_matches)), 2)
            round_matches[i], round_matches[j] = round_matches[j], round_matches[i]

        elif mutation_type == "swap_teams":
            m = random.choice(round_matches)
            m["home"], m["away"] = m["away"], m["home"]

        elif mutation_type == "change_slot":
            self.modify_single_match(random.choice(round_matches))

        elif mutation_type == "change_team":
            self.change_team(random.choice(round_matches))

    def modify_single_match(self, match):
        change = random.choice(["venue", "timeslot"])
        if change == "venue":
            match["venue"] = random.choice(self.venues)
        elif change == "timeslot":
            match["timeslot"] = random.choice(self.timeslots)

    def change_team(self, match):
        team_choice = random.choice(self.teams)
        if random.random() < 0.5:
            match["home"] = team_choice
        else:
            match["away"] = team_choice
