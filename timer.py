class timer():
    def __init__(self1):
        self1.timeron = True
        self1.seconds = 0
        self1.minutes = 0
        self1.hours = 0

    def changetime(self1):
        if self1.timeron is True:
            self1.seconds = self1.seconds + 1
        if self1.seconds == 60:
            self1.minutes = self1.minutes + 1
            self1.seconds = 0
        if self1.minutes == 60:
            self1.hours = self1.hours + 1
            self1.minutes = 0
        
        return self1.returntime()

    def pausetimer(self1):
        self1.timeron = False
    
    def returntime(self1):
        seconds = self1.seconds
        if self1.seconds < 10:
            seconds = str("0" + str(self1.seconds))
        minutes = self1.minutes
        if self1.minutes < 10:
            minutes = str("0" + str(self1.minutes))
        hours = self1.hours
        if self1.hours < 10:
            hours = str("0" + str(self1.hours))
        return str(str(hours) + ":" + str(minutes) + ":" + str(seconds))