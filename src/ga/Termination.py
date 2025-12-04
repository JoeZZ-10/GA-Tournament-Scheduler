from ga.individual import ScheduleIndividual

class terminationConditions:

    def checkForSolution(self,populationList):
        self.perfectScore = 10000
        self.bestSolution = populationList[0].fitness_score
        for individual in populationList:
            if individual.fitness_score == self.perfectScore:
                return individual
            elif individual.fitness_score > self.bestSolution:
                self.bestSolution = individual
        
        return self.bestSolution
