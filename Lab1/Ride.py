class Ride:
    def __init__(self, date):
        self.__date = date

    @property
    def date(self):
        return self.__date

    def __str__(self):
        raise NotImplementedError()
