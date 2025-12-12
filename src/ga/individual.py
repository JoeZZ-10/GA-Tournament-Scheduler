import random
import datetime

#from schdualeAndPlots import create_round_image, merge_images_grid

class ScheduleIndividual:
    # constructor
    def __init__(self, teams, venues, timeslots, start_date, randomize=False):
        self.teams = teams[:]
        self.venues = venues[:]
        self.timeslots = timeslots[:]
        if isinstance(start_date, str):
            self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        elif isinstance(start_date, datetime.date):
            self.start_date = start_date
        else:
            raise TypeError("start_date must be a 'YYYY-MM-DD' string or a datetime.date object")
        self.randomize = randomize
        pair_rounds = self.generate_pair_rounds()
        self.schedule = self.assign_slots(pair_rounds)
        self.fitness_score = 10000 # default high fitness score
        self.penalties = {} # dictionary to store penalties for each constraint 
        self.Nosolution = False # flag to indicate if no valid solution
    
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

        for round_index, matches in enumerate(pair_rounds):
            base_week = self.start_date + datetime.timedelta(weeks=round_index) # base date for the current round

            matches_copy = matches[:] # copy matches to avoid modifying original list

            if self.randomize:
                random.shuffle(matches_copy) # randomly shuffle match order

            round_venues = [
                random.choice(self.venues) # randomly assign a venue
                for _ in range(len(matches_copy))
            ]

            round_matches = [] # list to store matches of current round

            for i, (home, away) in enumerate(matches_copy):
                random_day_offset = random.randint(0,6) # pick random day within the week
                date = base_week + datetime.timedelta(days=random_day_offset) # compute match date
                venue = round_venues[i] # assign venue for the match
                timeslot = random.choice(self.timeslots) # randomly assign timeslot

                # match dict
                match = {
                    "round": round_index + 1,
                    "home": home,
                    "away": away,
                    "venue": venue,
                    "date": date.strftime("%Y-%m-%d"),
                    "timeslot": timeslot.strftime("%H:%M")
                }
                round_matches.append(match) # add match to the round
            rounds_with_slots.append(round_matches) # add round to the schedule
        
        return rounds_with_slots

    
    # function for displaying the schedule
    def display(self):
        for i, round_matches in enumerate(self.schedule, start=1):
            print(f"Round {i}: ")
            for m in round_matches:
                print(f"{m['home']} vs {m['away']} @ {m['venue']} on {m['timeslot']} {m['date']}")
            print()
