import pandas as pd

class LoadData:
    def __init__(self):
        self.Teams = "E:\\Projects\\GA-Tournament-Scheduler\\src\\data\\Teams.csv"
        self.Venues = "E:\\Projects\\GA-Tournament-Scheduler\\src\\data\\Venues.csv"
        self.TimeSlots = "E:\\Projects\\GA-Tournament-Scheduler\\src\\data\\TimeSlots.csv"
    
    def load_teams(self):
        dataset = pd.read_csv(self.Teams)
        df = pd.DataFrame(dataset)
        return df.iloc[:, -1].astype(str).tolist()  


    def load_venues(self):
        dataset = pd.read_csv(self.Venues)
        df = pd.DataFrame(dataset)
        return df.iloc[:, -1].astype(str).tolist() 


    def load_timeslots(self):
        dataset = pd.read_csv(self.TimeSlots)
        df = pd.DataFrame(dataset)
        return df.iloc[:, -1].astype(str).tolist()
