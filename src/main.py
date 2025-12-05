from data.loadData import LoadData


loadDataObj = LoadData()
teams = loadDataObj.load_teams()
venues = loadDataObj.load_venues()
timeslots = loadDataObj.load_timeslots()



