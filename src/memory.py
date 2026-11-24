
import json
from pathlib import Path


# ==========================================
# STUDENT MEMORY CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MEMORY_FILE = PROJECT_ROOT / "data" / "student_memory.json"


# ==========================================
# LOAD STUDENT MEMORY
# ==========================================

def load_memory():

    if not MEMORY_FILE.exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


# ==========================================
# SAVE STUDENT LEARNING HISTORY
# ==========================================

def save_memory(student_name, topic, student_level, result=None):

    memory = load_memory()

    if student_name not in memory:
        memory[student_name] = {
            "learning_history": []
        }

    session = {
        "topic": topic,
        "student_level": student_level,
        "result": str(result) if result is not None else None
    }

    memory[student_name]["learning_history"].append(session)

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            memory,
            file,
            ensure_ascii=False,
            indent=4
        )

    return memory


# ==========================================
# GET STUDENT MEMORY
# ==========================================

def get_student_memory(student_name):

    memory = load_memory()

    return memory.get(
        student_name,
        {"learning_history": []}
    )
