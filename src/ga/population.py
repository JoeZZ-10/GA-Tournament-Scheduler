from ga.individual import ScheduleIndividual

class Population:

    def generate_population(self, teams, population_size):
        population = []
        for _ in range(population_size):
            individual = ScheduleIndividual(teams)
            population.append(individual)
        return population