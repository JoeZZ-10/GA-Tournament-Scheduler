import matplotlib.pyplot as plt
import os

class PlotManager:
    def __init__(self):
        self.plots_dir = "plots"
        if not os.path.exists(self.plots_dir):
            os.makedirs(self.plots_dir)
    
    def create_fitness_plot(self, best_fitness_per_gen, avg_fitness_per_gen, 
                           crossover_type, selection_type, mutation_type):
        """
        Create a plot showing best and average fitness over generations
        
        Args:
            best_fitness_per_gen: List of best fitness values per generation
            avg_fitness_per_gen: List of average fitness values per generation
            crossover_type: Type of crossover used
            selection_type: Type of selection used
            mutation_type: Type of mutation used
        """
        plt.figure(figsize=(12, 6))
        
        generations = range(1, len(best_fitness_per_gen) + 1)
        
        # Plot best fitness
        plt.plot(generations, best_fitness_per_gen, 'b-', linewidth=2, 
                label='Best Fitness', marker='o', markersize=4)
        
        # Plot average fitness
        plt.plot(generations, avg_fitness_per_gen, 'r--', linewidth=2, 
                label='Average Fitness', marker='s', markersize=4)
        
        plt.xlabel('Generation', fontsize=12, fontweight='bold')
        plt.ylabel('Fitness Score', fontsize=12, fontweight='bold')
        plt.title(f'Fitness Evolution\nCrossover: {crossover_type} | Selection: {selection_type} | Mutation: {mutation_type}',
                 fontsize=14, fontweight='bold')
        plt.legend(loc='lower right', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Add horizontal line at perfect score
        plt.axhline(y=10000, color='g', linestyle=':', linewidth=2, 
                   label='Perfect Score (10000)', alpha=0.7)
        
        plt.tight_layout()
        
        # Save the plot
        filename = f"{self.plots_dir}/fitness_{crossover_type}_{selection_type}_{mutation_type}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved: {filename}")
        
        plt.show()
        plt.close()
    
    def create_comparison_plot(self, results_dict):
        """
        Create a comparison plot for different GA configurations
        
        Args:
            results_dict: Dictionary with format:
                {
                    'config_name': {
                        'best_fitness': [...],
                        'avg_fitness': [...],
                        'crossover': str,
                        'selection': str,
                        'mutation': str
                    }
                }
        """
        plt.figure(figsize=(14, 7))
        
        colors = ['b', 'r', 'g', 'm', 'c', 'y', 'orange', 'purple']
        
        for idx, (config_name, data) in enumerate(results_dict.items()):
            generations = range(1, len(data['best_fitness']) + 1)
            color = colors[idx % len(colors)]
            
            plt.plot(generations, data['best_fitness'], 
                    color=color, linewidth=2, label=config_name, 
                    marker='o', markersize=3)
        
        plt.xlabel('Generation', fontsize=12, fontweight='bold')
        plt.ylabel('Best Fitness Score', fontsize=12, fontweight='bold')
        plt.title('Comparison of Different GA Configurations', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='lower right', fontsize=9)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=10000, color='black', linestyle=':', linewidth=2, alpha=0.5)
        
        plt.tight_layout()
        filename = f"{self.plots_dir}/comparison_all_configs.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Comparison plot saved: {filename}")
        
        plt.show()
        plt.close()
    
    def create_penalty_breakdown_plot(self, penalties_dict, config_name):
        """
        Create a bar plot showing penalty breakdown
        
        Args:
            penalties_dict: Dictionary of penalty types and their values
            config_name: Name of the configuration
        """
        plt.figure(figsize=(10, 6))
        
        penalty_names = list(penalties_dict.keys())
        penalty_values = list(penalties_dict.values())
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        bars = plt.bar(penalty_names, penalty_values, color=colors, alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Constraint Type', fontsize=12, fontweight='bold')
        plt.ylabel('Penalty Value', fontsize=12, fontweight='bold')
        plt.title(f'Penalty Breakdown - {config_name}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        filename = f"{self.plots_dir}/penalties_{config_name}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Penalty plot saved: {filename}")
        
        plt.show()
        plt.close()