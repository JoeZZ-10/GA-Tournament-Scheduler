from tkinter import *
from tkinter import ttk

class ScheduleViewer:
    def __init__(self, best_schedule):
        self.best_schedule = best_schedule
        self.current_round = 0
        self.total_rounds = len(best_schedule.schedule)
        
        # Create the window
        self.window = Toplevel()
        self.window.title("Tournament Schedule Viewer")
        
        # Set window size and center it
        window_width = 1000
        window_height = 700
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header Frame
        header_frame = Frame(self.window, bg="#2C3E50", height=100)
        header_frame.pack(fill=X, pady=(0, 10))
        
        # Fitness Score Display
        fitness_label = Label(header_frame, 
                             text=f"Best Schedule Fitness Score: {self.best_schedule.fitness_score}",
                             font=("Arial", 18, "bold"),
                             bg="#2C3E50",
                             fg="#ECF0F1")
        fitness_label.pack(pady=10)
        
        # Penalty breakdown
        if hasattr(self.best_schedule, 'penalties') and self.best_schedule.penalties:
            penalty_text = "Penalties: "
            for penalty_name, value in self.best_schedule.penalties.items():
                if value > 0:
                    short_name = penalty_name.replace('Constraint', '').replace('TwoMatchesPerTeamatSameDay', 'SameDay')
                    penalty_text += f"{short_name}={value}  "
            
            penalty_label = Label(header_frame,
                                 text=penalty_text,
                                 font=("Arial", 10),
                                 bg="#2C3E50",
                                 fg="#E74C3C")
            penalty_label.pack()
        
        # Round info frame
        info_frame = Frame(self.window, bg="#34495E")
        info_frame.pack(fill=X, pady=5)
        
        self.round_label = Label(info_frame,
                                text=f"Round {self.current_round + 1} of {self.total_rounds}",
                                font=("Arial", 16, "bold"),
                                bg="#34495E",
                                fg="#ECF0F1")
        self.round_label.pack(pady=10)
        
        # Matches display frame with scrollbar
        matches_container = Frame(self.window)
        matches_container.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Create canvas and scrollbar
        canvas = Canvas(matches_container, bg="white")
        scrollbar = Scrollbar(matches_container, orient=VERTICAL, command=canvas.yview)
        self.matches_frame = Frame(canvas, bg="white")
        
        self.matches_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.matches_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Navigation buttons frame
        nav_frame = Frame(self.window, bg="#ECF0F1")
        nav_frame.pack(fill=X, pady=10)
        
        self.prev_button = Button(nav_frame,
                                  text="← Previous Round",
                                  font=("Arial", 12, "bold"),
                                  bg="#3498DB",
                                  fg="white",
                                  width=20,
                                  height=2,
                                  command=self.previous_round,
                                  state=DISABLED)
        self.prev_button.pack(side=LEFT, padx=20)
        
        self.next_button = Button(nav_frame,
                                  text="Next Round →",
                                  font=("Arial", 12, "bold"),
                                  bg="#2ECC71",
                                  fg="white",
                                  width=20,
                                  height=2,
                                  command=self.next_round)
        self.next_button.pack(side=RIGHT, padx=20)
        
        close_button = Button(nav_frame,
                             text="Close",
                             font=("Arial", 12, "bold"),
                             bg="#E74C3C",
                             fg="white",
                             width=15,
                             height=2,
                             command=self.window.destroy)
        close_button.pack(side=BOTTOM, pady=10)
        
        # Display first round
        self.display_round()
    
    def display_round(self):
        """Display matches for the current round"""
        # Clear previous matches
        for widget in self.matches_frame.winfo_children():
            widget.destroy()
        
        # Update round label
        self.round_label.config(text=f"Round {self.current_round + 1} of {self.total_rounds}")
        
        # Get matches for current round
        round_matches = self.best_schedule.schedule[self.current_round]
        
        # Create header
        header_frame = Frame(self.matches_frame, bg="#34495E", height=40)
        header_frame.pack(fill=X, pady=(0, 10))
        
        Label(header_frame, text="Home Team", font=("Arial", 11, "bold"), 
              bg="#34495E", fg="white", width=15).grid(row=0, column=0, padx=5, pady=5)
        Label(header_frame, text="VS", font=("Arial", 11, "bold"), 
              bg="#34495E", fg="white", width=5).grid(row=0, column=1, padx=5, pady=5)
        Label(header_frame, text="Away Team", font=("Arial", 11, "bold"), 
              bg="#34495E", fg="white", width=15).grid(row=0, column=2, padx=5, pady=5)
        Label(header_frame, text="Venue", font=("Arial", 11, "bold"), 
              bg="#34495E", fg="white", width=18).grid(row=0, column=3, padx=5, pady=5)
        Label(header_frame, text="Date", font=("Arial", 11, "bold"), 
              bg="#34495E", fg="white", width=12).grid(row=0, column=4, padx=5, pady=5)
        Label(header_frame, text="Time", font=("Arial", 11, "bold"), 
              bg="#34495E", fg="white", width=10).grid(row=0, column=5, padx=5, pady=5)
        
        # Display each match
        for idx, match in enumerate(round_matches):
            bg_color = "#ECF0F1" if idx % 2 == 0 else "#BDC3C7"
            
            match_frame = Frame(self.matches_frame, bg=bg_color, relief=RIDGE, borderwidth=2)
            match_frame.pack(fill=X, pady=5, padx=10)
            
            Label(match_frame, text=match['home'], font=("Arial", 10), 
                  bg=bg_color, width=15, anchor=E).grid(row=0, column=0, padx=5, pady=8)
            Label(match_frame, text="VS", font=("Arial", 10, "bold"), 
                  bg=bg_color, fg="#E74C3C", width=5).grid(row=0, column=1, padx=5, pady=8)
            Label(match_frame, text=match['away'], font=("Arial", 10), 
                  bg=bg_color, width=15, anchor=W).grid(row=0, column=2, padx=5, pady=8)
            Label(match_frame, text=match['venue'], font=("Arial", 10), 
                  bg=bg_color, width=18).grid(row=0, column=3, padx=5, pady=8)
            Label(match_frame, text=match['timeslot'], font=("Arial", 10), 
                  bg=bg_color, width=12).grid(row=0, column=4, padx=5, pady=8)
            
            # Handle time format (could be string or time object)
            time_str = match['time'] if isinstance(match['time'], str) else match['time'].strftime("%H:%M")
            Label(match_frame, text=time_str, font=("Arial", 10), 
                  bg=bg_color, width=10).grid(row=0, column=5, padx=5, pady=8)
        
        # Update button states
        self.prev_button.config(state=NORMAL if self.current_round > 0 else DISABLED)
        self.next_button.config(state=NORMAL if self.current_round < self.total_rounds - 1 else DISABLED)
    
    def next_round(self):
        """Show next round"""
        if self.current_round < self.total_rounds - 1:
            self.current_round += 1
            self.display_round()
    
    def previous_round(self):
        """Show previous round"""
        if self.current_round > 0:
            self.current_round -= 1
            self.display_round()