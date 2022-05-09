class Operation:
    def __init__(self, machine, duration):
        self.machine = machine
        self.duration = duration
        self.initTime = -1
        self.finishTime = -1

    def setInitTime(self, initTime):
        self.initTime = initTime
        self.finishTime = self.initTime + self.duration
