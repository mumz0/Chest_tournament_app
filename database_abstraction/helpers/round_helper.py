import datetime


class RoundHelper:

    def set_round_time(self):
        time_now = datetime.datetime.now()
        return time_now.strftime("%H:%M:%S")
