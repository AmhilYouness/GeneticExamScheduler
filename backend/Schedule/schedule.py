class Schedule:
    def __init__(self, days=dict(), fitness=0, total_days=[]):
        self.days = days
        self.fitness = fitness

        for day in total_days:
            self.days[day] = []