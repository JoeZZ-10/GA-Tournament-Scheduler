from tkinter import *
from main import run_prediction
from tkinter import filedialog, messagebox
import pandas as pd

window_GA = Tk()
window_GA.title("Genetic Algorithms For The Sport Tournament Schedule")

window_width = 1200
window_height = 700
screen_width = window_GA.winfo_screenwidth()
screen_height = window_GA.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window_GA.geometry(f"{window_width}x{window_height}+{x}+{y}")

welcome_label = Label(window_GA,
                      text="WELCOME!\nSport Tournament Schedule Prediction",
                      font=("Arial", 18, "bold"),
                      justify="center")
welcome_label.pack(pady=20)

teams_path = None
venue_path = None
timeslot_path = None

frame_buttons = Frame(window_GA)
frame_buttons.pack(pady=10)

frame_texts = Frame(window_GA)
frame_texts.pack(pady=30)

frame_save = Frame(window_GA)
frame_save.pack(pady=20)

txt_width = 23
txt_height = 20

txt_teams = Text(frame_texts, width=txt_width, height=txt_height)
txt_venue = Text(frame_texts, width=txt_width, height=txt_height)
txt_timeslot = Text(frame_texts, width=txt_width, height=txt_height)

txt_teams.pack(side=LEFT, padx=20)
txt_venue.pack(side=LEFT, padx=20)
txt_timeslot.pack(side=LEFT, padx=20)

def load_csv(txt_area, file_type):
    global teams_path, venue_path, timeslot_path

    path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not path:
        return

    if file_type == "teams":
        teams_path = path
    elif file_type == "venue":
        venue_path = path
    elif file_type == "timeslot":
        timeslot_path = path

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

button1 = Button(frame_buttons, text="Upload Teams", width=20,
                 command=lambda: load_csv(txt_teams, "teams"))
button2 = Button(frame_buttons, text="Upload Venue", width=20,
                 command=lambda: load_csv(txt_venue, "venue"))
button3 = Button(frame_buttons, text="Upload TimeSlot", width=20,
                 command=lambda: load_csv(txt_timeslot, "timeslot"))

button1.pack(side=LEFT, padx=20)
button2.pack(side=LEFT, padx=20)
button3.pack(side=LEFT, padx=20)

save1 = Button(frame_save, text="Save Teams", width=20,
               command=lambda: save_csv(txt_teams, teams_path))
save2 = Button(frame_save, text="Save Venue", width=20,
               command=lambda: save_csv(txt_venue, venue_path))
save3 = Button(frame_save, text="Save TimeSlot", width=20,
               command=lambda: save_csv(txt_timeslot, timeslot_path))

save1.pack(side=LEFT, padx=20)
save2.pack(side=LEFT, padx=20)
save3.pack(side=LEFT, padx=20)

frame_run = Frame(window_GA)
frame_run.pack(pady=20)

msg2 = Label(frame_run,
                    text="whenever you are ready ;)",
                    font=("Arial", 18, "bold"),
                    justify="center")

predict_btn = Button(frame_run,
                     text="Predict",
                     font=("Arial", 14, "bold"),
                     width=12,
                     bg="#4CAF50",
                     fg="white",
                     command=run_prediction)


msg2.pack(side=LEFT, padx=20)
predict_btn.pack(side=LEFT, padx=20)


window_GA.mainloop()
