import random

class ScheduleIndividual:
    # constructor
    def __init__(self, teams, venues, timeslots, randomize=False):
        self.teams = teams[:]
        self.venues = venues[:]
        self.timeslots = timeslots[:]
        self.randomize = randomize
        pair_rounds = self.generate_pair_rounds()
        self.schedule = self.assign_slots(pair_rounds)
        self.fitness_score = 10000 # default high fitness score
    
    def generate_pair_rounds(self):
        teams = self.teams[:] # copy of team list to avoid modifying original list
        if len(teams) % 2 != 0: # handling odd number of teams
            teams.append("BYE")
        
        num_rounds = len(teams) - 1 # number of rounds = number of teams - 1
        num_matches_per_round = len(teams) // 2 # num of matches per round = number of teams / 2
        rounds = [] # list to store all rounds

        for _ in range(num_rounds):
            round_matches = [] # list to store all matches for current round
            for i in range(num_matches_per_round):
                t1 = teams[i] # team 1 from the start
                t2 = teams[-i-1] # teams 2 from the end
                if t1 != "BYE" and t2 != "BYE": # if 1 team is BYE, dont add the match
                    round_matches.append((t1,t2)) # add match
            rounds.append(round_matches) # add the round to schedule
            teams = [teams[0]] + [teams[-1]] + teams[1:-1] # rotate the teams
        
        return rounds
    
    def assign_slots(self, pair_rounds):
        rounds_with_slots = [] # list to store the schedule
        combos = [(v,t) for v in self.venues for t in self.timeslots] # lis to store all possible (venues,timeslots) pairings

        for round_pairs in pair_rounds:
            if self.randomize: # shuffle if randomize = true
                random.shuffle(combos)
            if len(combos) < len(round_pairs): # handle not enough venues,timslots error
                raise ValueError("Not enough (venue,timeslots) combinations to schedule this round. " f"matches: {len(round_pairs)}, slots: {len(combos)}")
            round_matches = [] # list to store matches of every round
            for pair, (venue,timeslot) in zip(round_pairs, combos):
                # match dict
                match = {
                    "home": pair[0],
                    "away": pair[1],
                    "venue": venue,
                    "timeslot": timeslot
                }
                round_matches.append(match) # add match to the round
            rounds_with_slots.append(round_matches) # add round to the schedule
        
        return rounds_with_slots

    
    # function for displaying the schedule
    def display(self):
        for i, round_matches in enumerate(self.schedule, start=1):
            print(f"Round {i}: ")
            for m in round_matches:
                print(f"{m['home']} vs {m['away']} @ {m['venue']} at {m['timeslot']}")
                print()

    


    


