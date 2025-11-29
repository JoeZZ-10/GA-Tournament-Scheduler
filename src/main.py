#just for testing

#import class
from ga.individual import ScheduleIndividual

#test for even number of teams
teams1 = ["A","B","C","D"]
schedule1 = ScheduleIndividual(teams1)
schedule1.display()
print("----------------------------------------------")


teams1 = ["A","B","C","D"]
schedule3 = ScheduleIndividual(teams1)
schedule3.display()
print("----------------------------------------------")

teams1 = ["A","B","C","D"]
schedule2 = ScheduleIndividual(teams1)
schedule2.display()
 

#test for odd number of teams
# teams2 = ["A","B","C","D","E"]
# schedule2 = ScheduleIndividual(teams2)
# schedule2.display()
