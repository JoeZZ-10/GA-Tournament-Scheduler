from datetime import datetime

class Constraints:

    def __init__(self):
        self.Team_Played = {} # Dictionary to track team and their timeslots
        self.venue_usage = {} # Dictionary to track venue and their timeslots
        self.team_last_match_day = {} # Dictionary to track last match day of each team
        self.team_times = {} # Dictionary to track time slots for each team


    # Constraint 1: No team should have more than one match at the same time slot

    def TwoMatchesPerTeamatSameDay(self,individual):
        penalty = 0
        conflict_found = 0  
        for round_matches in individual.schedule:
            for m in round_matches:
                conflict_found += self.count_team_conflicts(m) # Check for conflicts
        if conflict_found > 0:
            penalty += conflict_found * 500 # High penalty for this constraint
        return penalty

    def count_team_conflicts(self, m):
        conflict_found = 0
        time_slot = m['date']
        # Initialize set for this timeslot if not exist
        if time_slot not in self.Team_Played:
            self.Team_Played[time_slot] = set()

        played = self.Team_Played[time_slot]
        home = m['home']
        away = m['away']

        if home in played and away in played:
            conflict_found += 2
        elif home in played or away in played:
            conflict_found += 1
        else:
            # Register teams as played
            played.add(home)
            played.add(away)

        return conflict_found

    
# -----------------------------------------------------------------------------------------
    
    # Constraint 2: No venue should host more than one match at the same time slot

    def VenueConfliictConstraint(self,individual):
        penalty = 0
        conflict_found = 0
        for round_matches in individual.schedule:
            for m in round_matches:
                timeandtime_slot_usage = (m['timeslot'],m['date'])
                venue = m['venue']
                if venue in self.venue_usage: # Check if venue is already used at this timeslot
                    if  timeandtime_slot_usage in self.venue_usage[venue]:
                        conflict_found += 1
                    else:
                        self.venue_usage[venue].add(timeandtime_slot_usage) # Mark venue as used at this timeslot
                else:
                    self.venue_usage[venue] = set() # Initialize set for venue
                    self.venue_usage[venue].add(timeandtime_slot_usage) 
        if conflict_found > 0:
            penalty += conflict_found * 200
        return penalty
    
# -----------------------------------------------------------------------------------------

    # Constraint 3: Each team should have at least 2 rest days between matches

    def RestDayConstraint(self,individual): 
        penalty = 0
        rest_violations = 0
        for round_matches in individual.schedule:
             for m in round_matches:
                  rest_violations += self.calculate_rest_violations(m) # Calculate rest day violations
        if rest_violations > 0:
            penalty += rest_violations * 100 # Penalty for rest day violations
        return penalty

    def calculate_rest_violations(self,m):
        rest_violations = 0
        date1 = datetime.strptime(m['date'], "%Y-%m-%d") 
        if m['home'] in self.team_last_match_day:
              date2 = datetime.strptime(self.team_last_match_day[m['home']], "%Y-%m-%d") 
              diff = (date1 - date2).days # Calculate difference in days
              if diff < 2: # If less than 2 days, it's a violation
                  rest_violations += 1
        self.team_last_match_day[m['home']] = m['date'] # Update last match day for home team
        if m['away'] in self.team_last_match_day:
          date2 = datetime.strptime(self.team_last_match_day[m['away']], "%Y-%m-%d")
          diff = (date1 - date2).days # Calculate difference in days
          if diff < 2: # Violation for away team
              rest_violations += 1
        self.team_last_match_day[m['away']] = m['date'] # Update last match day for away team
        return rest_violations
    
# -----------------------------------------------------------------------------------------
    
    # Constraint 4: fair time distribution of matches for each team

    def FairTimeDistributionConstraint(self,individual):
        penalty = 0
        time_distribution_violations = 0
        for round_matches in individual.schedule:
                for m in round_matches:
                    time_distribution_violations += self.calculate_time_distribution_violations(m) # Calculate time distribution violations
        if time_distribution_violations > 0:
            penalty += time_distribution_violations * 50 # Penalty for time distribution violations
        return penalty
    
    def calculate_time_distribution_violations(self, m):
        time_distribution_violations = 0
        if m['home'] in self.team_times: # Check if home team has played before
            if self.team_times[m['home']] == m['timeslot']: # Check if home team has played at this time
                time_distribution_violations += 1
        else:
            self.team_times[m['home']] = m['timeslot'] # Mark home team as played at this time
        if m['away'] in self.team_times: # Check if home team has played before
            if self.team_times[m['away']] == m['timeslot']: # Check if away team has played at this time
                time_distribution_violations += 1 
        else:
            self.team_times[m['away']] = m['timeslot'] # Mark away team as played at this time
        return time_distribution_violations




