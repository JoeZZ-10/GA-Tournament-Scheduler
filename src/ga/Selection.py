import random
import copy
from ga.individual import ScheduleIndividual

class Selection:     

    def tournament_selection(self, population):
        tournament = random.sample(population, 2)
        return max(tournament, key=lambda ind: ind.fitness_score)

    def rank_selection(self, population):
        sorted_pop = sorted(population, key=lambda ind: ind.fitness_score)
        ranks = list(range(1, len(sorted_pop) + 1))
        total = sum(ranks)
        pick = random.uniform(0, total)
        current = 0
        for ind, r in zip(sorted_pop, ranks):
            current += r
            if current >= pick:
                return ind

    def select_population(self, population, selection_size, method):
        selected = []
        for _ in range(selection_size):
            if method == "rank":
                winner = self.rank_selection(population)
            else:
                winner = self.tournament_selection(population)
            
            new_individual = ScheduleIndividual(
                winner.teams,
                winner.venues,
                winner.timeslots,
                winner.times,
                winner.start_date,
                randomize=False
            )
            new_individual.schedule = copy.deepcopy(winner.schedule)
            new_individual.fitness_score = winner.fitness_score
            selected.append(new_individual)
        return selected
