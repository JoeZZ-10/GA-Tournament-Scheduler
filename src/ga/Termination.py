from ga.individual import ScheduleIndividual

class terminationConditions:

    def checkForSolution(self,populationList):
        self.perfectScore = 10000

        if not hasattr(self, "bestSolution"):
            self.bestSolution = populationList[0]

        for individual in populationList:
            if individual.fitness_score == self.perfectScore:
                self.bestSolution = individual
                return individual
            
            elif individual.fitness_score > self.bestSolution.fitness_score:
                self.bestSolution = individual
        
        return self.bestSolution