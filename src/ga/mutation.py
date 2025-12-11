import random
import copy
import pandas as pd


class Mutation:

    def __init__(self, teams=None, venues=None, date=None, Times=None):
        self.teams = teams if teams is not None else []
        self.venues = venues if venues is not None else []
        self.date = date if date is not None else []
        self.Times = Times if Times is not None else []

    def mutate(self, individual, mutate_type, mutation_rate=0.01):
        new_individual = copy.deepcopy(individual)

        for r in range(len(new_individual.schedule)):
            if random.random() < mutation_rate:

                match mutate_type:
                    case "Random_Resetting":
                        self.mutate_round(new_individual.schedule[r])

                    case "Inversion_Mutation":
                        self.inversion_mutation(new_individual.schedule[r])
                    case _:
                        pass
        return new_individual

    def mutate_round(self, round_matches):
        if len(round_matches) < 2:
            self.modify_single_match(round_matches[0])
            return

        mutation_type = random.choice(
            [
                "swap_matches",
                "swap_teams",
                "change_date",
                "change_team",
                "change_timeslot",
            ]
        )

        if mutation_type == "swap_matches":
            i, j = random.sample(range(len(round_matches)), 2)
            round_matches[i], round_matches[j] = round_matches[j], round_matches[i]

        elif mutation_type == "swap_teams":
            m = random.choice(round_matches)
            m["home"], m["away"] = m["away"], m["home"]

        elif mutation_type == "change_date":
            self.modify_single_match(random.choice(round_matches))

        elif mutation_type == "change_team":
            self.change_team(random.choice(round_matches))

        elif mutation_type == "change_timeslot":
            self.modify_single_match(random.choice(round_matches))

    def modify_single_match(self, match):
        change = random.choice(["venue", "timeslot", "date"])
        if change == "venue":
            match["venue"] = random.choice(self.venues)
        elif change == "timeslot":
            match["Times"] = random.choice(self.Times)
        else:
            match["date"] = random.choice(self.date)

    def change_team(self, match):
        team_choice = random.choice(self.teams)
        if random.random() < 0.5:
            match["home"] = team_choice
        else:
            match["away"] = team_choice

    def inversion_mutation(self, round_matches):
        if len(round_matches) < 3:
            return  # nothing useful to invert

        i, j = sorted(random.sample(range(len(round_matches)), 2))

        # Reverse the sublist between i and j
        round_matches[i : j + 1] = reversed(round_matches[i : j + 1])
