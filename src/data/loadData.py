import pandas as pd

class LoadData:
    def __init__(self):
        self.filepath = "E:\\Projects\\GA-Tournament-Scheduler\\src\\data\\dataset.csv"  
    
    def load_teams(self):
        dataset = pd.read_csv(self.filepath)
        df = pd.DataFrame(dataset)
        return df.iloc[:, 2].astype(str).tolist()  


    def load_venues(self):
        dataset = pd.read_csv(self.filepath)
        df = pd.DataFrame(dataset)
        return df.iloc[:, 3].astype(str).tolist() 


    def load_timeslots(self):
        dataset = pd.read_csv(self.filepath)
        df = pd.DataFrame(dataset)
        return df.iloc[:, 0].astype(str).tolist()