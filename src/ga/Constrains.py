from datetime import datetime

class Constraints:

    def TwoMatchesPerTeamatSameTime(self,individual):
        Team_Played = {}
        penalty = 0
        conflict_found = 0
        for round_matches in individual.schedule:
            for m in round_matches:
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
        if conflict_found > 0:
                    penalty += conflict_found * 200
        return penalty

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


    def RestDayConstraint(self,individual):
        penalty = 0
        rest_violations = 0
        team_last_match_day = {}
        for round_matches in individual.schedule:
             for m in round_matches:
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
        if rest_violations > 0:
            penalty += rest_violations * 50
        return penalty
    
    


