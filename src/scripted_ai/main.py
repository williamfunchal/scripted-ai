#!/usr/bin/env python
import sys
import warnings

from scripted_ai.crew import ScriptedAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

PROMPT = "What is a crew in CrewAI? A complete guide to understanding crews."
MAIN_FONT = "https://docs.crewai.com/concepts/crews"

def run():
    """
    Run the crew.
    """
    
    inputs = {
        "topic": f"{PROMPT}",
        "main_font": f"{MAIN_FONT}"
    }
    ScriptedAi().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": f"{PROMPT}",
        "main_font": f"{MAIN_FONT}"
        
    }
    try:
        ScriptedAi().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ScriptedAi().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": f"{PROMPT}",
        "main_font": f"{MAIN_FONT}"
        
    }
    try:
        ScriptedAi().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
