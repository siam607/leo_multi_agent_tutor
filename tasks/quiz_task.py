
from crewai import Task


# ==========================================
# QUIZ MASTER TASK
# ==========================================

def create_quiz_task(
    agent,
    topic,
    student_level,
    explanation_task
):

    return Task(
        description=(
            f"Create a quiz about '{topic}' for a "
            f"'{student_level}' level student.\n\n"

            "Carefully review the complete explanation "
            "provided by the Explainer Agent.\n\n"

            "Create exactly 5 questions based on the "
            "learning explanation.\n\n"

            "Question requirements:\n"
            "1. Include both multiple-choice and short-answer questions.\n"
            "2. Every question must have a unique question number.\n"
            "3. MCQ questions must contain exactly 4 options.\n"
            "4. Short-answer questions must not contain options.\n"
            "5. Questions must match the student's learning level.\n\n"

            "OUTPUT FORMAT:\n"
            "Return one valid JSON object using exactly this structure:\n\n"

            "{\n"
            '  "questions": [\n'
            "    {\n"
            '      "question_number": 1,\n'
            '      "type": "multiple-choice",\n'
            '      "question": "Question text",\n'
            '      "options": ["Option A", "Option B", '
            '"Option C", "Option D"]\n'
            "    },\n"
            "    {\n"
            '      "question_number": 2,\n'
            '      "type": "short-answer",\n'
            '      "question": "Question text",\n'
            '      "options": []\n'
            "    }\n"
            "  ],\n"
            '  "answer_key": {\n'
            '    "1": {\n'
            '      "correct_answer": "Correct answer",\n'
            '      "explanation": "Explanation"\n'
            "    },\n"
            '    "2": {\n'
            '      "correct_answer": "Correct answer",\n'
            '      "explanation": "Explanation"\n'
            "    }\n"
            "  }\n"
            "}\n\n"

            "IMPORTANT RULES:\n"
            "- Include exactly 5 questions.\n"
            "- Include answer details for all 5 questions "
            "inside the answer_key object.\n"
            "- The questions array must NOT contain correct answers.\n"
            "- The answer_key must remain separate from questions.\n"
            "- Use question_number, type, question, and options "
            "as the exact field names.\n"
            "- Return valid JSON only.\n"
            "- Do not include Markdown code fences.\n"
            "- Do not add any text outside the JSON object."
        ),

        expected_output=(
            "A valid JSON object containing exactly 5 questions "
            "inside the questions array and a separate answer_key "
            "object containing the correct answer and explanation "
            "for every question. The questions must not reveal "
            "their correct answers."
        ),

        agent=agent,

        context=[explanation_task]
    )
