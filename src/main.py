def run_prediction():
    from tkinter import Toplevel
    from tkinter import Label
    from data.loadData import LoadData
    from ga.geneticAlgorithm import GeneticAlgorithm
    from schdualeAndPlots import generate_all_round_images, merge_images_grid
    from PIL import ImageTk, Image
    loadDataObj = LoadData()
    teams = loadDataObj.load_teams()
    venues = loadDataObj.load_venues()
    timeslots = loadDataObj.load_timeslots()

    gaObj = GeneticAlgorithm()
    best_schedule = gaObj.runAlgorithm(teams, venues, timeslots)

    # Final Schedule 
    round_images = generate_all_round_images(best_schedule)
    merge_images_grid(round_images, columns=4, max_width=1200, max_height=1000, output_file="Final_Schedule.png")

    # Create new window
    img_window = Toplevel()
    img_window.title("Final Schedule")
    
    # Load the saved image
    img = Image.open("Final_Schedule.png")
    img_tk = ImageTk.PhotoImage(img)
    
    # Display in label
    label_img = Label(img_window, image=img_tk)
    label_img.image = img_tk  # Keep reference
    label_img.pack()
