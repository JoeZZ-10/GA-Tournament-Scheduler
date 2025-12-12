import pandas as pd
import datetime


class LoadData:
    def __init__(self):
        self.Teams = "src/data/Teams.csv"
        self.Venues = "src/data/Venues.csv"
        self.TimeSlots = "src/data/TimeSlots.csv"
        self.Times = "src/data/Times.csv"

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

    def load_times_from_csv(self):
        times = []
        dataset = pd.read_csv(self.Times)
        df = pd.DataFrame(dataset)
        reader = df.values.tolist()

        for row in reader:
            if not row:
                continue

            time_str = str(row[0]).strip()

            # Skip empty cells
            if time_str == "" or time_str.lower() == "nan":
                print("Skipping empty time entry.")
                continue

            # Check correct format
            if ":" not in time_str:
                raise ValueError(f"Invalid time format (missing ':'): {time_str}")

            parts = time_str.split(":")

            if len(parts) < 2:
                raise ValueError(f"Invalid time format (not HH:MM): {time_str}")

            # Handle cases like HH:MM:SS → ignore seconds
            hour = int(parts[0])
            minute = int(parts[1])

            times.append(datetime.time(hour, minute))

        return times
