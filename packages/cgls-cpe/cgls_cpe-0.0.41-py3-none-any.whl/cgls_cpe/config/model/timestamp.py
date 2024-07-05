from cgls_cpe.common.helper import pad_two_digits
class Timestamp(object):

    def __init__(self, year:int, month:int, day:int, hour:int=-1, minutes:int=-1, seconds:int=-1):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hour)
        self.minutes = int(minutes)
        self.seconds = int(seconds)
        
    # Define getter methods for each attribute
    def get_year(self) -> int:
        return self.year

    def get_month(self) -> int:
        return self.month

    def get_day(self) -> int:
        return self.day

    def get_hour(self) -> int:
        return self.hour

    def get_minutes(self) -> int:
        return self.minutes

    def get_seconds(self) -> int:
        return self.seconds
    
    def __str__(self):
        return self.get_value()
    
    def get_date_short(self):
        return  ''.join([str(self.year) , pad_two_digits(self.month) , pad_two_digits(self.day)]) 
    
    def get_value(self):
        result = self.get_date_short()
        if self.hour >= 0:
            result += pad_two_digits(self.hour)
        if self.minutes>= 0:
            result += pad_two_digits(self.minutes)
        if self.seconds >= 0:
            result += pad_two_digits(self.seconds)
        return result 
            