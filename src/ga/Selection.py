import random
import copy
from ga.individual import ScheduleIndividual
class Selection:
    def tournament_selection(self,population, k=3,tournament_size=5):
        # Randomly choose k individuals from the population
        tournament = random.sample(population, tournament_size)
        # Higher fitness_score is better (10000 - penalties)
        winner = max(tournament, key=lambda ind: ind.fitness_score)
        return winner
    
    def select_population(self, population, selection_size, tournament_size=5):
        selected = []
        for _ in range(selection_size):
            winner = self.tournament_selection(population, tournament_size)
            # Create a new individual with same data
            new_individual = ScheduleIndividual(
                winner.teams,
                winner.venues,
                winner.timeslots,
                winner.start_date,
                randomize=False
            )
            new_individual.schedule = copy.deepcopy(winner.schedule)
            new_individual.fitness_score = winner.fitness_score
            selected.append(new_individual)
        return selected
