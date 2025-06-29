def validate_turn(round_num, speaker):
    return (round_num % 2 == 0 and speaker == "Scientist") or \
           (round_num % 2 == 1 and speaker == "Philosopher")
