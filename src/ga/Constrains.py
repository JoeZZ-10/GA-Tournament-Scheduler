from datetime import datetime

class Constraints:

    # Constraint: No team should have more than one match at the same time slot

    def TwoMatchesPerTeamatSameTime(self,individual):
        Team_Played = {} # Dictionary to track team and their timeslots
        penalty = 0
        conflict_found = 0
        for round_matches in individual.schedule:
            for m in round_matches:
                conflict_found = self.count_team_conflicts(Team_Played, m) # Check for conflicts
        if conflict_found > 0:
                    penalty += conflict_found * 200 # High penalty for this constraint
        return penalty

    def count_team_conflicts(self, Team_Played, m):
        conflict_found = 0
        Team_timeslot1 = (m['home'],m['timeslot'])
        Team_timeslot2 = (m['away'],m['timeslot'])
        if Team_timeslot1 in Team_Played: # Check if team has already played at this timeslot for home team
            conflict_found += 1 
        else: # if not, mark team as played at this timeslot for home team
            Team_Played[Team_timeslot1] = 1 # Mark team as played at this timeslot for home team
        if Team_timeslot2 in Team_Played: # Check if team has already played at this timeslot for away team
            conflict_found += 1
        else: # if not, mark team as played at this timeslot for away team
            Team_Played[Team_timeslot2] = 1 # Mark team as played at this timeslot for away team
        return conflict_found
    
# -----------------------------------------------------------------------------------------
    
    # Constraint: No venue should host more than one match at the same time slot

    def VenueConfliictConstraint(self,individual):
        venue_usage = {} # Dictionary to track venue and their timeslots
        penalty = 0
        conflict_found = 0
        for i,round_matches in enumerate(individual.schedule,start= 1):
            for m in round_matches:
                venue_timeslot = (m['venue'],m['timeslot'],i)
                if venue_timeslot in venue_usage: # Check if venue is already used at this timeslot
                    conflict_found += 1
                venue_usage[venue_timeslot] = 1 # Mark venue as used at this timeslot
        if conflict_found > 0:
            penalty += conflict_found * 100
        return penalty
    
# -----------------------------------------------------------------------------------------

    # Constraint: Each team should have at least 2 rest days between matches

    def RestDayConstraint(self,individual): 
        penalty = 0
        rest_violations = 0
        team_last_match_day = {} # Dictionary to track last match day of each team
        for round_matches in individual.schedule:
             for m in round_matches:
                  rest_violations = self.calculate_rest_violations(team_last_match_day, m) # Calculate rest day violations
        if rest_violations > 0:
            penalty += rest_violations * 50 # Penalty for rest day violations
        return penalty

    def calculate_rest_violations(self, team_last_match_day, m):
        rest_violations = 0
        date1 = datetime.strptime(m['timeslot'], "%Y-%m-%d") 
        if m['home'] in team_last_match_day:
              date2 = datetime.strptime(team_last_match_day[m['home']], "%Y-%m-%d") 
              diff = (date1 - date2).days # Calculate difference in days
              if diff < 2: # If less than 2 days, it's a violation
                  rest_violations += 1
        team_last_match_day[m['home']] = m['timeslot'] # Update last match day for home team
        if m['away'] in team_last_match_day:
          date2 = datetime.strptime(team_last_match_day[m['away']], "%Y-%m-%d")
          diff = (date1 - date2).days # Calculate difference in days
          if diff < 2: # Violation for away team
              rest_violations += 1
        team_last_match_day[m['away']] = m['timeslot'] # Update last match day for away team
        return rest_violations


