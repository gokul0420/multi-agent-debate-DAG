from agents.agent_a import agent_a_logic
from agents.agent_b import agent_b_logic
from agents.judge import judge_debate
from nodes.logger import log_to_file
from nodes.memory_node import Memory
from nodes.state_validation import validate_turn


def run_debate(topic: str):
    print(f"Starting debate between Scientist and Philosopher on: {topic}")
    memory = Memory()

    for round_num in range(8):
        speaker = "Scientist" if round_num % 2 == 0 else "Philosopher"

        if not validate_turn(round_num, speaker):
            raise Exception("Invalid turn")

        # ──▶ pass the topic to the agent logic functions
        if speaker == "Scientist":
            argument = agent_a_logic(memory, round_num, topic)
        else:
            argument = agent_b_logic(memory, round_num, topic)

        log_entry = memory.add_argument(speaker, argument, round_num)
        print(log_entry)
        log_to_file(log_entry)

    summary, winner, reason = judge_debate(memory.get_log(), topic)

    print("\n[Judge] Summary of debate:\n" + summary)
    print(f"\n[Judge] Winner: {winner}\nReason: {reason}")
    log_to_file("\n[Judge] Summary of debate:\n" + summary)
    log_to_file(f"\n[Judge] Winner: {winner}\nReason: {reason}")
