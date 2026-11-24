
from crewai import Crew, Process

from agents.coordinator import create_coordinator
from agents.explainer import create_explainer
from agents.quiz_master import create_quiz_master
from agents.evaluator import create_evaluator

from tasks.coordinator_task import create_coordinator_task
from tasks.explanation_task import create_explanation_task
from tasks.quiz_task import create_quiz_task
from tasks.evaluation_task import create_evaluation_task


# ==========================================
# PHASE 1: LEARNING SESSION
# ==========================================

def run_learning_session(
    topic,
    student_level,
    previous_memory=None
):

    coordinator = create_coordinator()
    explainer = create_explainer()
    quiz_master = create_quiz_master()

    # Coordinator creates a personalized learning plan
    coordinator_task = create_coordinator_task(
        coordinator,
        topic,
        student_level,
        previous_memory
    )

    # Explainer follows the Coordinator's learning plan
    explanation_task = create_explanation_task(
        explainer,
        topic,
        student_level,
        coordinator_task
    )

    # Quiz Master creates questions from the explanation
    quiz_task = create_quiz_task(
        quiz_master,
        topic,
        student_level,
        explanation_task
    )

    # Sequential multi-agent orchestration
    learning_crew = Crew(
        agents=[
            coordinator,
            explainer,
            quiz_master
        ],
        tasks=[
            coordinator_task,
            explanation_task,
            quiz_task
        ],
        process=Process.sequential,
        verbose=True
    )

    learning_crew.kickoff(
        inputs={
            "topic": topic,
            "student_level": student_level
        }
    )

    # Extract individual task outputs
    explanation_output = (
        explanation_task.output.raw
        if explanation_task.output else ""
    )

    quiz_output = (
        quiz_task.output.raw
        if quiz_task.output else ""
    )

    return explanation_output, quiz_output, quiz_task


# ==========================================
# PHASE 2: STUDENT EVALUATION
# ==========================================

def evaluate_student(quiz_task, student_answers):

    evaluator = create_evaluator()

    evaluation_task = create_evaluation_task(
        evaluator,
        quiz_task,
        student_answers
    )

    evaluation_crew = Crew(
        agents=[evaluator],
        tasks=[evaluation_task],
        process=Process.sequential,
        verbose=True
    )

    evaluation_result = evaluation_crew.kickoff()

    return evaluation_result
