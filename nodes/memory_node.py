class Memory:
    def __init__(self):
        self.log = []
        self.history = set()

    def add_argument(self, speaker, argument, round_num):
        if argument in self.history:
            raise ValueError("Repeated argument")
        self.history.add(argument)
        log_entry = f"[Round {round_num+1}] {speaker}: {argument}"
        self.log.append(log_entry)
        return log_entry

    def get_log(self):
        return self.log
