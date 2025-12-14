from ga.individualV2 import ScheduleIndividualV2

class Population:

    def __init__(self):
        self.population = []

    def generate_population(self, teams, venues, timeslots,times,population_size):
        for _ in range(population_size):
            individual = ScheduleIndividualV2(teams, venues, timeslots,times,"2025-12-01",randomize=True)
            self.population.append(individual)
        return self.population
    
    def display_population(self, population):
        for i, individual in enumerate(population, start=1):
            print(f"\n=== Schedule Individual {i} ===")
            individual.display()