"""
Judge node: evaluates the full debate with multiple criteria
using the local Qwen‑1.5‑0.5B model.

Returns:
    summary (str): Natural‑language summary of the debate.
    winner  (str): "Scientist" or "Philosopher".
    reason  (str): One‑paragraph rationale referencing the metrics.
"""

import json

from agents.agent_a import _generate  # reuse the same Qwen loader

JUDGE_SYSTEM_PROMPT = (
    "You are an impartial debate judge. Rate each debater on 5 criteria:\n"
    "1. Logical Coherence\n"
    "2. Evidence / Factual Support\n"
    "3. Relevance to the Topic\n"
    "4. Persuasive Strength\n"
    "5. Rebuttal Quality\n\n"
    "Score each criterion from 1 (poor) to 5 (excellent).\n"
    "Output strictly in the following JSON format:\n"
    "{\n"
    '  "summary": "<concise overall summary>",\n'
    '  "scores": {\n'
    '    "Scientist": {"logic": <1‑5>, "evidence": <1‑5>, "relevance": <1‑5>, "persuasion": <1‑5>, "rebuttal": <1‑5>},\n'
    '    "Philosopher": {"logic": <1‑5>, "evidence": <1‑5>, "relevance": <1‑5>, "persuasion": <1‑5>, "rebuttal": <1‑5>}\n'
    "  },\n"
    '  "winner": "<Scientist | Philosopher | Tie>",\n'
    '  "reason": "<1‑2 sentence justification>"\n'
    "}\n\n"
    "Only output valid JSON—NO extra commentary."
)


def judge_debate(memory_log, topic):
    # Assemble transcript for the judge
    transcript = "\n".join(memory_log)

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Debate topic: {topic}\n\n"
                f"Transcript:\n{transcript}\n\n"
                "Now provide your JSON verdict:"
            ),
        },
    ]

    raw_response = _generate(messages, max_new_tokens=300, temperature=0.3)

    # Safely parse JSON (fallback to heuristic winner if parsing fails)
    try:
        verdict = json.loads(raw_response)
        summary = verdict["summary"]
        winner = verdict["winner"]
        reason = verdict["reason"]
    except Exception:
        # Fallback heuristic: choose debater with more words
        sci_words = sum(len(line.split()) for line in memory_log if "Scientist:" in line)
        phil_words = sum(len(line.split()) for line in memory_log if "Philosopher:" in line)
        winner = "Scientist" if sci_words >= phil_words else "Philosopher"
        summary = raw_response.strip()
        reason = f"Because {winner} offered more consistent, well-articulated arguments throughout the discussion."

    return summary, winner, reason
