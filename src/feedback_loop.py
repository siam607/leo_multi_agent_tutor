
from src.crew import run_learning_session, evaluate_student
from src.memory import save_memory, get_student_memory


# ==========================================
# LEO AI TUTOR FEEDBACK LOOP
# ==========================================

def start_tutoring_session():

    print("\n===================================")
    print("       LEO AI TUTOR")
    print("===================================\n")

    student_name = input("Enter Student Name: ").strip()

    if not student_name:
        print("Student name cannot be empty.")
        return

    while True:

        print("\n===================================")
        print("       NEW LEARNING SESSION")
        print("===================================\n")

        topic = input("Enter Learning Topic: ").strip()

        if not topic:
            print("Topic cannot be empty.")
            continue

        print("\nSelect Learning Level:")
        print("1. Beginner")
        print("2. Intermediate")
        print("3. Advanced")

        level_options = {
            "1": "Beginner",
            "2": "Intermediate",
            "3": "Advanced"
        }

        level_choice = input(
            "\nEnter your choice (1-3): "
        ).strip()

        if level_choice not in level_options:
            print("Invalid learning level.")
            continue

        student_level = level_options[level_choice]

        # Retrieve previous learning history
        previous_memory = get_student_memory(student_name)

        print("\nCoordinator Agent is preparing your learning plan...")

        try:

            # PHASE 1: LEARNING SESSION
            explanation, quiz_output, quiz_task = (
                run_learning_session(
                    topic,
                    student_level,
                    previous_memory
                )
            )

            print("\n========== LEARNING EXPLANATION ==========\n")
            print(explanation)

            print("\n========== YOUR QUIZ ==========\n")
            print(quiz_output)

            # PHASE 2: STUDENT ANSWERS
            print("\n========== SUBMIT YOUR ANSWERS ==========\n")

            student_answers = input(
                "Enter your answers:\n"
            ).strip()

            if not student_answers:
                print("No answers submitted. Evaluation skipped.")
                continue

            # PHASE 3: EVALUATION
            print("\nEvaluator Agent is checking your answers...")

            evaluation_result = evaluate_student(
                quiz_task,
                student_answers
            )

            print("\n========== EVALUATION REPORT ==========\n")
            print(evaluation_result)

            # PHASE 4: SAVE STUDENT MEMORY
            save_memory(
                student_name,
                topic,
                student_level,
                evaluation_result
            )

            print("\nYour learning history has been saved!")

        except Exception as error:

            print(f"\nLearning session failed: {error}")

        # FEEDBACK LOOP
        continue_choice = input(
            "\nWould you like to start another learning session? (yes/no): "
        ).strip().lower()

        if continue_choice not in ["yes", "y"]:
            print("\nThank you for learning with LEO AI Tutor!")
            break


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    start_tutoring_session()
