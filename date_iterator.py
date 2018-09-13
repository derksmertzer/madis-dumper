class DateConstructor:

    def __init__(self, year, month, day, hour):

        self.year = year
        self.month_start = month[0]
        self.month_end = month[1]
        self.day_start = day[0]
        self.day_end = day[1]
        self.hour = hour
        self.leap = False
        self.check_year()
        self.validate_elements()

    def check_year(self):

        from datetime import date
        if self.year in range(2000, date.today().year + 1):
            if self.year in range(2000, date.today().year + 1, 4):
                self.leap = True
        else:
            raise ValueError('input year not in MADIS data range')

    def validate_elements(self):

        if self.month_start in range(1, 13) and self.month_end in range(1, 13) and self.day_start in range(1, 32) \
                and self.day_end in range(1, 32) and self.hour in range(0, 24):
            pass
        else:
            raise ValueError('input month/day/hour not in valid data range')

    def year_format(self):
        return str(self.year)

    @staticmethod
    def element_format(element):

        if element < 10:
            return '0' + str(element)
        else:
            return str(element)

    def hour_format(self, cur_hour):

        if self.hour not in range(0, 24):
            raise ValueError("input not in valid hour range")
        if cur_hour < 10:
            return '_0' + str(cur_hour) + '00'
        else:
            return '_' + str(cur_hour) + '00'

    def __iter__(self):

        for i in range(self.month_start, self.month_end + 1):
            # loop into days
            # leap years -> 29 days
            if self.leap and i == 2:
                for j in range(self.day_start, self.day_end + 1):
                    for k in range(self.hour, 24):
                        yield self.year_format(), self.element_format(i), self.element_format(j), self.hour_format(k)
            # non leap years -> 28 days
            elif i == 2:
                for j in range(self.day_start, self.day_end + 1):
                    for k in range(self.hour, 24):
                        yield self.year_format(), self.element_format(i), self.element_format(j), self.hour_format(k)
            # months with 30 days
            elif i in [4, 6, 9, 11]:
                for j in range(self.day_start, self.day_end + 1):
                    for k in range(self.hour, 24):
                        yield self.year_format(), self.element_format(i), self.element_format(j), self.hour_format(k)
                        # months with 31 days
            else:
                for j in range(self.day_start, self.day_end + 1):
                    for k in range(self.hour, 24):
                        yield self.year_format(), self.element_format(i), self.element_format(j), self.hour_format(k)

