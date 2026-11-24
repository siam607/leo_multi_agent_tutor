
from crewai import Task


# ==========================================
# EVALUATOR TASK
# ==========================================

def create_evaluation_task(
    agent,
    quiz_task,
    student_answers
):

    return Task(
        description=(
            "Evaluate the student's answers using the quiz "
            "and answer key created by the Quiz Master Agent.\n\n"

            "The Quiz Master's complete output is provided "
            "as context. Carefully review the questions and "
            "the separate answer_key before evaluating.\n\n"

            f"Student Answers:\n{student_answers}\n\n"

            "EVALUATION INSTRUCTIONS:\n"
            "1. Evaluate all 5 questions.\n"
            "2. Compare each answer with the Quiz Master's answer key.\n"
            "3. Award 1 mark for each correct answer.\n"
            "4. Calculate the total score out of 5.\n"
            "5. Identify correct and incorrect answers.\n"
            "6. Explain mistakes in simple language.\n"
            "7. Highlight the student's strengths and weaknesses.\n"
            "8. Provide personalized recommendations for improvement.\n\n"

            "IMPORTANT RULES:\n"
            "- Use the Quiz Master's answer_key as the reference.\n"
            "- Do not invent questions or correct answers.\n"
            "- Do not award marks without checking the answer.\n"
            "- Be fair and supportive when evaluating the student.\n"
            "- If an answer is blank, award 0 marks.\n"
        ),

        expected_output=(
            "A structured evaluation report containing:\n"
            "1. Total score out of 5\n"
            "2. Question-wise evaluation\n"
            "3. Correct and incorrect answers\n"
            "4. Explanation of mistakes\n"
            "5. Student strengths\n"
            "6. Areas needing improvement\n"
            "7. Personalized learning recommendations"
        ),

        agent=agent,

        context=[quiz_task]
    )
