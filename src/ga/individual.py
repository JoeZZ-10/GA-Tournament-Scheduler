class ScheduleIndividual:
    # constructor
    def __init__(self, teams):
        self.teams = teams 
        self.schedule = self.generate_round_robin()
    
    def generate_round_robin(self):
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
    
    # function for displaying the rounds
    def display(self):
        for i, round_matches in enumerate(self.schedule, start=1):
            print(f"Round {i}: {round_matches}")
    


    


