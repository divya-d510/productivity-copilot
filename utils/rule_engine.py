import re
from datetime import datetime, timedelta


def detect_intents(text: str):
    text = text.lower()
    intents = []

    if any(w in text for w in ["meeting", "schedule", "event"]):
        intents.append("calendar")

    if any(w in text for w in ["task", "todo", "remind"]):
        intents.append("task")

    if any(w in text for w in ["note", "write", "save"]):
        intents.append("note")

    if any(w in text for w in ["search", "find", "recall"]):
        intents.append("memory")

    return list(set(intents))


def extract_priority(text):
    if "high" in text:
        return "high"
    if "low" in text:
        return "low"
    return "medium"


def extract_date(text):
    if "tomorrow" in text:
        return (datetime.utcnow() + timedelta(days=1)).isoformat()
    if "today" in text:
        return datetime.utcnow().isoformat()
    return None


def extract_time(text):
    match = re.search(r"\d{1,2}(am|pm)", text.lower())
    return match.group() if match else None


def extract_title(text: str):
    text = text.lower()

    for word in [
        "create", "task", "todo",
        "high priority", "low priority",
        "tomorrow", "today"
    ]:
        text = text.replace(word, "")

    # remove filler words
    words = text.split()
    words = [w for w in words if w not in ["a", "an", "the"]]

    cleaned = " ".join(words)

    return cleaned.strip()