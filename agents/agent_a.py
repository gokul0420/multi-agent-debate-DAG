# agents/agent_a.py  – Scientist persona (local Qwen 0.5B)
from functools import lru_cache

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

_MODEL_ID = "Qwen/Qwen1.5-0.5B"


@lru_cache(maxsize=1)
def _load_model():
    """Load model & tokenizer exactly once (cached)."""
    tokenizer = AutoTokenizer.from_pretrained(_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        _MODEL_ID, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    model.eval()
    return tokenizer, model


def _generate(messages, max_new_tokens=120, temperature=0.7):
    tokenizer, model = _load_model()
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
        model.cuda()
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = output_ids[0][inputs["input_ids"].shape[1] :]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def agent_a_logic(memory, round_num, topic):
    """Scientist’s dynamic argument (2‑3 sentences)."""
    argument_idx = round_num // 2 + 1
    prior = "\n".join(memory.get_log()) or "None so far."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a pragmatic SCIENTIST debating a Philosopher. "
                "Respond with a single concise argument (max 3 sentences) using empirical or risk‑based reasoning."
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
    return _generate(messages)
