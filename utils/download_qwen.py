"""
download_qwen.py
================
One‑time helper script that pre‑downloads the Qwen‑1.5‑0.5B model so the
debate application can run fully offline.

Usage
-----
    python utils/download_qwen.py

This pulls the tokenizer and weights into your Hugging Face cache directory
(~/.cache/huggingface), so subsequent runs of the debate app start instantly.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen1.5-0.5B"


def download_qwen() -> None:
    print(f" Downloading {MODEL_ID} …")
    AutoTokenizer.from_pretrained(MODEL_ID)
    AutoModelForCausalLM.from_pretrained(MODEL_ID)
    print(" Qwen‑1.5‑0.5B is now cached locally.")


if __name__ == "__main__":
    download_qwen()
