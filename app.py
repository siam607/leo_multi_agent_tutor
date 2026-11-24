
import json
import re
import streamlit as st

from src.crew import run_learning_session, evaluate_student
from src.memory import save_memory, get_student_memory


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="LEO AI Tutor",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# HELPER FUNCTION: PARSE QUIZ JSON
# ==========================================

def parse_quiz_output(raw_output):

    cleaned_output = str(raw_output).strip()

    # Remove Markdown code fences if present
    cleaned_output = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned_output,
        flags=re.IGNORECASE
    )

    cleaned_output = re.sub(
        r"\s*```$",
        "",
        cleaned_output
    )

    return json.loads(cleaned_output)


# ==========================================
# HEADER
# ==========================================

st.title("🎓 LEO - Multi-Agent AI Tutor")

st.write(
    "Your personal AI-powered learning assistant."
)

st.divider()


# ==========================================
# STUDENT INFORMATION
# ==========================================

st.header("👨‍🎓 Student Information")

with st.form("learning_form"):

    student_name = st.text_input("Student Name")

    topic = st.text_input(
        "Learning Topic",
        placeholder="Example: Python Programming"
    )

    student_level = st.selectbox(
        "Learning Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    start_session = st.form_submit_button(
        "🚀 Start Learning Session"
    )


# ==========================================
# START LEARNING SESSION
# ==========================================

if start_session:

    if not student_name.strip() or not topic.strip():

        st.warning("Please enter your name and topic.")

    else:

        try:

            with st.spinner("AI Agents are working..."):

                st.info(
                    "Coordinator Agent is preparing "
                    "the personalized learning plan."
                )

                # Retrieve previous student memory
                previous_memory = get_student_memory(
                    student_name.strip()
                )

                # Run the multi-agent learning session
                explanation, quiz_output, quiz_task = (
                    run_learning_session(
                        topic.strip(),
                        student_level,
                        previous_memory
                    )
                )

                # Store current session information
                st.session_state.student_name = student_name.strip()
                st.session_state.topic = topic.strip()
                st.session_state.student_level = student_level

                st.session_state.explanation = str(explanation)
                st.session_state.quiz_output = str(quiz_output)
                st.session_state.quiz_task = quiz_task

                # Clear previous session evaluation and answers
                st.session_state.pop("evaluation_result", None)
                st.session_state.pop("student_answers", None)

            st.success("Learning session completed!")

        except Exception as error:

            st.error(
                f"Learning session failed: {error}"
            )


# ==========================================
# DISPLAY LEARNING EXPLANATION
# ==========================================

if "explanation" in st.session_state:

    st.divider()

    st.header("📚 Learning Explanation")

    st.markdown(
        st.session_state.explanation
    )


# ==========================================
# DISPLAY QUIZ WITHOUT ANSWER KEY
# ==========================================

if "quiz_output" in st.session_state:

    st.divider()

    st.header("📝 Your Quiz")

    try:

        quiz_data = parse_quiz_output(
            st.session_state.quiz_output
        )

        questions = quiz_data.get("questions", [])

        if not questions:

            st.warning(
                "No questions were found in the quiz."
            )

        else:

            for question in questions:

                question_number = question.get(
                    "question_number", ""
                )

                question_text = question.get(
                    "question", ""
                )

                question_type = question.get(
                    "type", ""
                ).lower()

                options = question.get(
                    "options", []
                )

                st.markdown(
                    f"**Question {question_number}: "
                    f"{question_text}**"
                )

                if question_type in [
                    "multiple-choice",
                    "mcq"
                ] and options:

                    for option in options:

                        st.write(f"- {option}")

                st.write("")

    except (
        json.JSONDecodeError,
        AttributeError,
        TypeError
    ):

        st.error(
            "Quiz format is invalid. "
            "The Quiz Master must return valid JSON."
        )


# ==========================================
# STUDENT ANSWERS
# ==========================================

if "quiz_task" in st.session_state:

    st.divider()

    st.header("✍️ Submit Your Answers")

    student_answers = st.text_area(
        "Write your answers below:",
        placeholder=(
            "Q1: Your answer\n"
            "Q2: Your answer\n"
            "Q3: Your answer\n"
            "Q4: Your answer\n"
            "Q5: Your answer"
        ),
        height=180,
        key="student_answers"
    )

    if st.button("📊 Evaluate My Answers"):

        if not student_answers.strip():

            st.warning(
                "Please enter your answers first."
            )

        else:

            try:

                with st.spinner(
                    "Evaluator Agent is checking your answers..."
                ):

                    evaluation_result = evaluate_student(
                        st.session_state.quiz_task,
                        student_answers
                    )

                    st.session_state.evaluation_result = str(
                        evaluation_result
                    )

                    # Save evaluation and learning history
                    save_memory(
                        st.session_state.student_name,
                        st.session_state.topic,
                        st.session_state.student_level,
                        evaluation_result
                    )

                st.success(
                    "Evaluation completed!"
                )

            except Exception as error:

                st.error(
                    f"Evaluation failed: {error}"
                )


# ==========================================
# EVALUATION REPORT
# ==========================================

if "evaluation_result" in st.session_state:

    st.divider()

    st.header("🏆 Evaluation Report")

    st.markdown(
        st.session_state.evaluation_result
    )

    st.success(
        "Your learning history has been saved!"
    )


# ==========================================
# STUDENT MEMORY
# ==========================================

if "student_name" in st.session_state:

    with st.expander(
        "🧠 Previous Learning History"
    ):

        previous_memory = get_student_memory(
            st.session_state.student_name
        )

        st.json(previous_memory)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "LEO Multi-Agent AI Tutor | "
    "Powered by CrewAI and Google Gemini"
)
