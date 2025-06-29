# agents/agent_b.py  – Philosopher persona (local Qwen 0.5B)
from agents.agent_a import _generate  # reuse loader & generate helper


def agent_b_logic(memory, round_num, topic):
    argument_idx = round_num // 2 + 1
    prior = "\n".join(memory.get_log()) or "None so far."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a thoughtful PHILOSOPHER debating a Scientist. "
                "Respond with a single reflective argument (max 3 sentences) citing ethics, history, or logic."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Debate topic: {topic}\n"
                f"This is your argument #{argument_idx} of 4.\n"
                f"Previous arguments:\n{prior}\n\n"
                f"Provide the next argument now:"
            ),
        },
    ]
    return _generate(messages, temperature=0.8)
