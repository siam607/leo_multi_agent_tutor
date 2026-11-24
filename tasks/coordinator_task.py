
from crewai import Task


# ==========================================
# COORDINATOR TASK
# ==========================================

def create_coordinator_task(
    agent,
    topic,
    student_level,
    previous_memory=None
):

    return Task(
        description=(
            f"Manage a personalized tutoring session "
            f"for the topic: {topic}.\n\n"

            f"Student's current level: {student_level}.\n\n"

            f"Previous Learning History:\n"
            f"{previous_memory}\n\n"

            "Review the student's previous learning history. "
            "Identify previously studied topics and any available "
            "evaluation feedback.\n\n"

            "Use the previous learning history to personalize "
            "the current tutoring session. If the student "
            "struggled with a related topic, provide additional "
            "learning support.\n\n"

            "Identify clear learning objectives and create "
            "a structured learning plan.\n\n"

            "The learning plan should guide the Explainer Agent "
            "and Quiz Master Agent during the next stages."
        ),

        expected_output=(
            "A personalized and structured learning plan containing:\n"
            "1. Learning topic\n"
            "2. Student's current level\n"
            "3. Learning objectives\n"
            "4. Recommended learning sequence\n"
            "5. Relevant recommendations based on previous "
            "learning history"
        ),

        agent=agent
    )
