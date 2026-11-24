
from crewai import Task


def create_explanation_task(
    agent,
    topic,
    student_level,
    coordinator_task
):

    return Task(
        description=(
            f"Explain the topic '{topic}' to a "
            f"'{student_level}' level student. "

            "First, carefully review the learning plan "
            "and learning objectives created by the "
            "Coordinator Agent. "

            "Follow that learning plan while explaining "
            "the topic. Use simple language, step-by-step "
            "explanations, practical examples, and important "
            "key points."
        ),

        expected_output=(
            "A clear and structured explanation containing "
            "the learning objectives, key concepts, practical "
            "examples, and a short summary."
        ),

        agent=agent,

        context=[coordinator_task]
    )
