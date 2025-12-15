import random
import datetime

class ScheduleIndividualV2:
    """
    Represents a tournament schedule individual for genetic algorithm.
    Uses Round Robin for pairing teams and completely random assignment 
    for venues, dates, and timeslots to ensure initial constraint violations.
    """
    
    def __init__(self, teams, venues, timeslots, times, randomize=False):
        # Initialize a schedule individual.
        self.teams = teams[:]
        self.venues = venues[:]
        self.timeslots = timeslots[:]
        self.times = times[:]
        self.randomize = randomize
        
        # Generate the schedule
        pair_rounds = self.generate_pair_rounds()
        self.schedule = self.assign_slots_randomly(pair_rounds)
        
        # Initialize fitness and tracking attributes
        self.fitness_score = 10000  # Default high fitness score
        self.penalties = {}  # Dictionary to store penalties for each constraint
        self.Nosolution = False  # Flag to indicate if no valid solution found
    
    def generate_pair_rounds(self):
        """
        Generate team pairings using Round Robin algorithm.
        Each team plays every other team exactly once.
        
        Returns:
            List of rounds, where each round contains match tuples (home, away)
        """
        teams = self.teams[:]
        
        # Handle odd number of teams by adding a "BYE"
        if len(teams) % 2 != 0:
            teams.append("BYE")
        
        num_rounds = len(teams) - 1  # Number of rounds = number of teams - 1
        num_matches_per_round = len(teams) // 2  # Matches per round = teams / 2
        rounds = []
        
        for round_num in range(num_rounds):
            round_matches = []
            
            # Generate matches for this round
            for i in range(num_matches_per_round):
                t1 = teams[i]  # Team from start
                t2 = teams[-i-1]  # Team from end
                
                # Skip matches with BYE team
                if t1 != "BYE" and t2 != "BYE":
                    round_matches.append((t1, t2))
            
            rounds.append(round_matches)
            
            # Rotate teams for next round (keep first team fixed)
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        
        return rounds
    
    def assign_slots_randomly(self, pair_rounds):
        """
        Assign venues, dates, and timeslots completely randomly to matches.
        This ensures constraint violations in initial population for GA to optimize.
        
        Args:
            pair_rounds: List of rounds with team pairings
            
        Returns:
            Complete schedule with all match details
        """
        rounds_with_slots = []
        
        for round_index, matches in enumerate(pair_rounds):
            round_matches = []
            
            for home, away in matches:
                # Completely random assignment of all attributes
                venue = random.choice(self.venues)
                time = random.choice(self.times)
                timeslot = random.choice(self.timeslots)
                
                # Optionally swap home/away randomly for more variation
                if self.randomize and random.random() < 0.3:
                    home, away = away, home
                
                # Create match dictionary
                match = {
                    "round": round_index + 1,
                    "home": home,
                    "away": away,
                    "venue": venue,
                    "timeslot": timeslot,
                    "time": time
                }
                
                round_matches.append(match)
            
            # Optionally shuffle match order within round
            if self.randomize:
                random.shuffle(round_matches)
            
            rounds_with_slots.append(round_matches)
        
        return rounds_with_slots
    
    def display(self):
        """
        Display the complete schedule in a readable format.
        Shows round number, teams, venue, time, and date for each match.
        """
        print(f"\n{'='*70}")
        print(f"TOURNAMENT SCHEDULE (Fitness: {self.fitness_score})")
        print(f"{'='*70}\n")
        
        for i, round_matches in enumerate(self.schedule, start=1):
            print(f"+-- Round {i} {'-'*60}")
            for m in round_matches:
                print(f"|  {m['home']:12} vs {m['away']:12} @ {m['venue']:18} "
                      f"| {m['timeslot']} {m['time']}")
            print(f"+{'-'*69}\n")
        
        # Display penalties if available
        if self.penalties:
            print(f"\n{'='*70}")
            print("CONSTRAINT VIOLATIONS:")
            print(f"{'='*70}")
            total_penalty = sum(self.penalties.values())
            for penalty_name, penalty_value in self.penalties.items():
                if penalty_value > 0:
                    print(f"  [!] {penalty_name:35} : {penalty_value:6}")
            print(f"{'-'*70}")
            print(f"  Total Penalty: {total_penalty}")
            print(f"{'='*70}\n")