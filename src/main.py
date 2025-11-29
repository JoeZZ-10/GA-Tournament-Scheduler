#just for testing

#import class
from ga.individual import ScheduleIndividual


teams = ["A","B","C","D","E"]
venues = ["V1","V2","V3"]
timeslots = ["09:00", "13:00"]
schedule = ScheduleIndividual(teams, venues, timeslots, randomize=True)
schedule.display()
 

