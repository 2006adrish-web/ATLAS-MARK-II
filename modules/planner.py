import json
from modules.ai import ask_ai


def create_plan(goal, memory):

    prompt = f"""
You are Atlas Project Planner.

Convert the user's goal into JSON.

Goal:
{goal}

Return format:

{{
    "project":"name",
    "tasks":[
        "task1",
        "task2",
        "task3"
    ]
}}

Return ONLY JSON.
"""

    result = ask_ai(prompt, memory)

    try:
        plan = json.loads(result)
        return plan

    except:
        return {
            "project": goal,
            "tasks": [goal]
        }