class Course:
    def __init__(self, quarter, year):
        self._quarter = quarter
        self._year = year

    def __eq__(self, other):
        return self.quarter() == other.quarter() and self.year() == other.year()

    def quarter(self):
        return self._quarter

    def year(self):
        return self._year

