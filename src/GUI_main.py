from tkinter import *
from main import run_prediction
from tkinter import filedialog, messagebox
import pandas as pd
import threading

window_GA = Tk()
window_GA.title("Genetic Algorithms For The Sport Tournament Schedule")

window_width = 1400
window_height = 900
screen_width = window_GA.winfo_screenwidth()
screen_height = window_GA.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window_GA.geometry(f"{window_width}x{window_height}+{x}+{y}")

welcome_label = Label(window_GA, text="WELCOME!\nSport Tournament Schedule Prediction", font=("Arial", 18, "bold"), justify="center")
welcome_label.pack(pady=20)

frame_ga = Frame(window_GA)
frame_ga.pack(pady=20)

frame_inner = Frame(frame_ga)
frame_inner.pack()

frame_selection = Frame(frame_inner)
frame_crossover = Frame(frame_inner)
frame_mutation = Frame(frame_inner)

frame_selection.grid(row=0, column=0, padx=50)
frame_crossover.grid(row=0, column=1, padx=50)
frame_mutation.grid(row=0, column=2, padx=50)

Label(frame_selection, text="Selection Type:", font=("Arial", 12, "bold")).pack(anchor="w")
selection_type = StringVar(value="rank")
Radiobutton(frame_selection, text="Rank", variable=selection_type, value="rank").pack(anchor="w")
Radiobutton(frame_selection, text="Tournament", variable=selection_type, value="tournament").pack(anchor="w")

Label(frame_crossover, text="Crossover Type:", font=("Arial", 12, "bold")).pack(anchor="w")
crossover_type = StringVar(value="one_point")
Radiobutton(frame_crossover, text="One Point", variable=crossover_type, value="one_point").pack(anchor="w")
Radiobutton(frame_crossover, text="Two Point", variable=crossover_type, value="two_point").pack(anchor="w")
Radiobutton(frame_crossover, text="Uniform", variable=crossover_type, value="uniform").pack(anchor="w")

Label(frame_mutation, text="Mutation Type:", font=("Arial", 12, "bold")).pack(anchor="w")
mutation_type = StringVar(value="Random_Resetting")
Radiobutton(frame_mutation, text="Random Resetting", variable=mutation_type, value="Random_Resetting").pack(anchor="w")
Radiobutton(frame_mutation, text="Inversion Mutation", variable=mutation_type, value="Inversion_Mutation").pack(anchor="w")

frame_buttons = Frame(window_GA)
frame_buttons.pack(pady=10)

frame_texts = Frame(window_GA)
frame_texts.pack(pady=10)

frame_save = Frame(window_GA)
frame_save.pack(pady=10)

txt_width = 23
txt_height = 20

txt_teams = Text(frame_texts, width=txt_width, height=txt_height)
txt_venue = Text(frame_texts, width=txt_width, height=txt_height)
txt_timeslot = Text(frame_texts, width=txt_width, height=txt_height)
txt_times = Text(frame_texts, width=txt_width, height=txt_height)

txt_teams.pack(side=LEFT, padx=15)
txt_venue.pack(side=LEFT, padx=15)
txt_timeslot.pack(side=LEFT, padx=15)
txt_times.pack(side=LEFT, padx=15)

teams_path = None
venue_path = None
timeslot_path = None
times_path = None

def load_csv(txt_area, file_type):
    global teams_path, venue_path, timeslot_path, times_path
    path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not path:
        return
    if file_type == "teams":
        teams_path = path
    elif file_type == "venue":
        venue_path = path
    elif file_type == "timeslot":
        timeslot_path = path
    elif file_type == "times":
        times_path = path
    df = pd.read_csv(path)
    text = df.to_string(index=False)
    txt_area.delete("1.0", "end")
    txt_area.insert("1.0", text)

def save_csv(txt_area, file_path):
    if not file_path:
        messagebox.showerror("Error", "No file loaded to save!")
        return
    text = txt_area.get("1.0", "end").strip()
    df = pd.DataFrame([line.split() for line in text.split("\n")])
    df.to_csv(file_path, index=False)
    messagebox.showinfo("Success", f"File saved successfully:\n{file_path}")

Button(frame_buttons, text="Upload Teams", width=20, command=lambda: load_csv(txt_teams, "teams")).pack(side=LEFT, padx=15)
Button(frame_buttons, text="Upload Venue", width=20, command=lambda: load_csv(txt_venue, "venue")).pack(side=LEFT, padx=15)
Button(frame_buttons, text="Upload TimeSlot", width=20, command=lambda: load_csv(txt_timeslot, "timeslot")).pack(side=LEFT, padx=15)
Button(frame_buttons, text="Upload Times", width=20, command=lambda: load_csv(txt_times, "times")).pack(side=LEFT, padx=15)

Button(frame_save, text="Save Teams", width=20, command=lambda: save_csv(txt_teams, teams_path)).pack(side=LEFT, padx=15)
Button(frame_save, text="Save Venue", width=20, command=lambda: save_csv(txt_venue, venue_path)).pack(side=LEFT, padx=15)
Button(frame_save, text="Save TimeSlot", width=20, command=lambda: save_csv(txt_timeslot, timeslot_path)).pack(side=LEFT, padx=15)
Button(frame_save, text="Save Times", width=20, command=lambda: save_csv(txt_times, times_path)).pack(side=LEFT, padx=15)

frame_run = Frame(window_GA)
frame_run.pack(pady=20)

# Status label for showing progress
status_label = Label(frame_run, text="", font=("Arial", 12), justify="center", fg="blue")
status_label.pack(side=TOP, pady=5)

msg2 = Label(frame_run, text="whenever you are ready ;)", font=("Arial", 18, "bold"), justify="center")
msg2.pack(side=LEFT, padx=20)

def prediction():
    mutatetype = mutation_type.get()
    slctype = selection_type.get()
    crovertype = crossover_type.get()
    
    # Update status
    status_label.config(text="Running Genetic Algorithm... Please wait.", fg="blue")
    predict_btn.config(state=DISABLED)
    window_GA.update()
    
    try:
        # Run prediction in a separate thread to keep GUI responsive
        def run_thread():
            try:
                run_prediction(mutatetype=mutatetype, slctype=slctype, crovertype=crovertype)
                status_label.config(text="Prediction completed successfully! Check the results window.", fg="green")
            except Exception as e:
                status_label.config(text=f"Error: {str(e)}", fg="red")
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            finally:
                predict_btn.config(state=NORMAL)
        
        thread = threading.Thread(target=run_thread)
        thread.daemon = True
        thread.start()
        
    except Exception as e:
        status_label.config(text="Error occurred!", fg="red")
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        predict_btn.config(state=NORMAL)

predict_btn = Button(frame_run, text="Predict", font=("Arial", 14, "bold"), width=12, bg="#4CAF50", fg="white", command=prediction)
predict_btn.pack(side=LEFT, padx=20)

window_GA.mainloop()