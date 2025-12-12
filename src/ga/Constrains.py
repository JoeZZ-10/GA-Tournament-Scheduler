from datetime import datetime

class Constraints:

    def __init__(self):
        self.Team_Played = {} # Dictionary to track team and their timeslots
        self.venue_usage = {} # Dictionary to track venue and their timeslots
        self.team_last_match_day = {} # Dictionary to track last match day of each team
        self.team_times = {} # Dictionary to track time slots for each team


    # Constraint 1: No team should have more than one match at the same time slot

    def TwoMatchesPerTeamatSameDay(self, m):
        conflict_found = 0
        time_slot = m['timeslot']
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
            if home in played:
                played.add(away)
            else:
                played.add(home)
        else:
            # Register teams as played
            played.add(home)
            played.add(away)

        return conflict_found

    
# -----------------------------------------------------------------------------------------
    
    # Constraint 2: No venue should host more than one match at the same time slot

    def VenueConfliictConstraint(self,m):
        penalty = 0
        conflict_found = 0
        timeandtime_slot_usage = (m['time'],m['timeslot'])
        venue = m['venue']
        if venue in self.venue_usage: # Check if venue is already used at this timeslot
            if  timeandtime_slot_usage in self.venue_usage[venue]:
                conflict_found += 1
            else:
                self.venue_usage[venue].add(timeandtime_slot_usage) # Mark venue as used at this timeslot
        else:
            self.venue_usage[venue] = set() # Initialize set for venue
            self.venue_usage[venue].add(timeandtime_slot_usage) 
        return conflict_found
    
# -----------------------------------------------------------------------------------------

    # Constraint 3: Each team should have at least 2 rest days between matches

    def RestDayConstraint(self, m):
        rest_violations = 0

        # parse date
        date1 = datetime.strptime(m['timeslot'], "%Y-%m-%d") 

        # HOME TEAM
        if m['home'] in self.team_last_match_day:
            last_date = self.team_last_match_day[m['home']]
            diff = (date1 - last_date).days
            if diff < 2:
                rest_violations += 1

        # Always update AFTER check
        self.team_last_match_day[m['home']] = date1

        # AWAY TEAM
        if m['away'] in self.team_last_match_day:
            last_date = self.team_last_match_day[m['away']]
            diff = (date1 - last_date).days
            if diff < 2:
                rest_violations += 1

        self.team_last_match_day[m['away']] = date1

        return rest_violations


# -----------------------------------------------------------------------------------------
    
    # Constraint 4: fair time distribution of matches for each team

    def FairTimeDistributionConstraint(self, m):
        time_distribution_violations = 0
        if m['home'] in self.team_times: # Check if home team has played before
            if self.team_times[m['home']] == m['time']: # Check if home team has played at this time
                time_distribution_violations += 1
        else:
            self.team_times[m['home']] = m['time'] # Mark home team as played at this time
        if m['away'] in self.team_times: # Check if home team has played before
            if self.team_times[m['away']] == m['time']: # Check if away team has played at this time
                time_distribution_violations += 1 
        else:
            self.team_times[m['away']] = m['time'] # Mark away team as played at this time
        return time_distribution_violations




