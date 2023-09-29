class Round:

    def __init__ (self, number, start_timestamp, end_timestamp, match_lst = []):
        self.number = number
        self.match_lst = match_lst
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp


    def get_start_timestamp(self):
        return self.start_timestamp
