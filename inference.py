import os
import json
import sys
from disaster_env import DisasterEnv

# ── Required environment variables (as per OpenEnv submission checklist) ──
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN     = os.getenv("HF_TOKEN")

# Optional – used when deploying via from_docker_image()
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# ── OpenAI client (all LLM calls use this) ──


# ── Global environment instance ──
env = DisasterEnv()


def reset(difficulty: str = "medium") -> dict:
    """Reset the environment and return initial state."""
    state = env.reset(difficulty=difficulty)
    if not isinstance(state, dict):
        raise TypeError("Reset must return a dictionary")
    return state


def step(action: int) -> dict:
    """Take an integer action (0–19) and return result dict."""
    if not isinstance(action, int):
        raise TypeError("Action must be an integer")
    if not (0 <= action <= 19):
        raise ValueError("Action must be between 0 and 19")

    state, reward, done, info = env.step(action)

    if not isinstance(state, dict):
        raise TypeError("State must be a dictionary")
    if not isinstance(reward, (int, float)):
        raise TypeError("Reward must be a number")
    if not isinstance(done, bool):
        raise TypeError("Done must be boolean")
    if not isinstance(info, dict):
        raise TypeError("Info must be a dictionary")

    return {
        "state": state,
        "reward": float(reward),
        "done": done,
        "info": info,
    }

def run_episode(difficulty: str = "medium", max_steps: int = 25):

    # START log
    print(f"[START] difficulty={difficulty} max_steps={max_steps}", flush=True)

    state = reset(difficulty=difficulty)
    total_reward = 0.0
    step_num = 0

    while step_num < max_steps:
        action = _greedy_action(state)

        result = step(action)
        total_reward += result["reward"]
        step_num += 1

        # STEP log
        print(
            f"[STEP] step={step_num} action={action} reward={result['reward']} done={result['done']}",
            flush=True
        )

        if result["done"]:
            break

        state = result["state"]

    # END log
    print(
        f"[END] total_reward={round(total_reward,2)} steps={step_num} difficulty={difficulty}",
        flush=True
    )

    return total_reward



def _greedy_action(state: dict) -> int:
    """Simple greedy action picker for inference runs."""
    injured = state.get("injured", 0)
    food    = state.get("food_needed", False)
    rescue  = state.get("rescue_needed", False)
    power   = state.get("power_outage", False)
    infra   = state.get("infrastructure_damage", False)
    disease = state.get("disease_outbreak", False)
    people  = state.get("people", 0)

    if disease:
        return 10
    if injured > 20:
        return 8
    if injured > 0:
        return 0
    if food:
        return 1
    if rescue:
        return 2
    if power:
        return 16
    if infra:
        return 19
    return 15


if __name__ == "__main__":
    difficulty = sys.argv[1] if len(sys.argv) > 1 else "medium"
    run_episode(difficulty=difficulty)