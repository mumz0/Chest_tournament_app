class Round:

    def __init__(self, number, start_timestamp, end_timestamp=None, match_lst=[]):
        self.number = number
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.match_lst = match_lst

    def serialize(self):
        return {
            "number": self.number,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "match_lst": self.match_lst
            }

    @classmethod
    def deserialize(cls, data):
        return cls(
            number=data['number'],
            start_timestamp=data['start_timestamp'],
            end_timestamp=data['end_timestamp'],
            match_lst=data['match_lst'],
            )
