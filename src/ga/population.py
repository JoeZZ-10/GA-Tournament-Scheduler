from ga.individual import ScheduleIndividual

class Population:

    def __init__(self):
        self.population = []

    def generate_population(self, teams, venues, timeslots,population_size):
        for _ in range(population_size):
            individual = ScheduleIndividual(teams, venues, timeslots,"2025-12-01",randomize=True)
            self.population.append(individual)
        return self.population
    
    def display_population(self, population):
        for i, individual in enumerate(population, start=1):
            print(f"\n=== Schedule Individual {i} ===")
            individual.display()