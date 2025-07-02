from celery import Celery
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, nutrition_analysis, exercise_planning, verification
import os

load_dotenv()

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/1"
)

celery_app.conf.update(
    task_track_started=True,
)

@celery_app.task(name="run_crew_task")
def run_crew_task(query: str, file_path: str):
    """
    This function defines the background task that will run the CrewAI analysis.
    It takes a user query and the path to the uploaded file as arguments.
    """

    medical_crew = Crew(
        agents=[doctor],
        tasks=[help_patients],
        process=Process.sequential,
    )

    result = medical_crew.kickoff({'query': query})

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")

    return str(result) 