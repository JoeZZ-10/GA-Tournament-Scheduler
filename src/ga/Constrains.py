from datetime import datetime

class Constraints:

    # Constraint: No team should have more than one match at the same time slot

    def TwoMatchesPerTeamatSameTime(self,individual):
        Team_Played = {}
        penalty = 0
        conflict_found = 0
        for round_matches in individual.schedule:
            for m in round_matches:
                conflict_found = self.count_team_conflicts(Team_Played, m)
        if conflict_found > 0:
                    penalty += conflict_found * 200
        return penalty

    def count_team_conflicts(self, Team_Played, m):
        conflict_found = 0
        Team_timeslot1 = (m['home'],m['timeslot'])
        Team_timeslot2 = (m['away'],m['timeslot'])
        if Team_timeslot1 in Team_Played:
            conflict_found += 1
        else:
            Team_Played[Team_timeslot1] = 1
        if Team_timeslot2 in Team_Played:
            conflict_found += 1
        else:
            Team_Played[Team_timeslot2] = 1
        return conflict_found
    
# -----------------------------------------------------------------------------------------
    
    # Constraint: No venue should host more than one match at the same time slot

    def VenueConfliictConstraint(self,individual):
        venue_usage = {}
        penalty = 0
        conflict_found = 0
        for i,round_matches in enumerate(individual.schedule,start= 1):
            for m in round_matches:
                venue_timeslot = (m['venue'],m['timeslot'],i)
                if venue_timeslot in venue_usage:
                    conflict_found += 1
                venue_usage[venue_timeslot] = 1
        if conflict_found > 0:
            penalty += conflict_found * 100
        return penalty
    
# -----------------------------------------------------------------------------------------

    # Constraint: Each team should have at least 2 rest days between matches

    def RestDayConstraint(self,individual):
        penalty = 0
        rest_violations = 0
        team_last_match_day = {}
        for round_matches in individual.schedule:
             for m in round_matches:
                  rest_violations = self.calculate_rest_violations(team_last_match_day, m)
        if rest_violations > 0:
            penalty += rest_violations * 50
        return penalty

    def calculate_rest_violations(self, team_last_match_day, m):
        rest_violations = 0
        date1 = datetime.strptime(m['timeslot'], "%Y-%m-%d")
        if m['home'] in team_last_match_day:
              date2 = datetime.strptime(team_last_match_day[m['home']], "%Y-%m-%d")
              diff = (date1 - date2).days
              if diff < 2:
                  rest_violations += 1
        team_last_match_day[m['home']] = m['timeslot']
        if m['away'] in team_last_match_day:
          date2 = datetime.strptime(team_last_match_day[m['away']], "%Y-%m-%d")
          diff = (date1 - date2).days
          if diff < 2:
              rest_violations += 1
        team_last_match_day[m['away']] = m['timeslot']
        return rest_violations


