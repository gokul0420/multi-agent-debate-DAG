# nodes/logger.py
def log_to_file(text, file_path: str = "debate_log.txt") -> None:
    
    with open(file_path, "a", encoding="utf-8", errors="replace") as f:
        f.write(text + "\n")
