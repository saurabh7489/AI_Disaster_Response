import os
from flask import Flask, render_template, jsonify, request
from disaster_env import DisasterEnv
from agent import RuleBasedAgent, RandomAgent, GreedyAgent

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

env = DisasterEnv(difficulty="medium")
agents = {
    "rule":   RuleBasedAgent(),
    "random": RandomAgent(),
    "greedy": GreedyAgent(),
}
active_agent = "rule"


def get_priority(state):
    if state.get("disease_outbreak"):
        return "Critical"
    if state.get("injured", 0) > 20:
        return "Critical"
    if state.get("injured", 0) > 0 or state.get("rescue_needed"):
        return "High"
    if state.get("food_needed") or state.get("power_outage"):
        return "Medium"
    return "Low"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/state", methods=["GET"])
def get_state():
    return jsonify({"state": env.get_state()})


@app.route("/step", methods=["POST"])
def step():
    data = request.get_json(silent=True) or {}
    agent_name = data.get("agent", active_agent)
    agent = agents.get(agent_name, agents["rule"])
    state = env.get_state()
    action, reason = agent.act(state)
    new_state, reward, done, info = env.step(action)
    return jsonify({
        "state": new_state,
        "action": action,
        "reason": reason,
        "reward": reward,
        "done": done,
        "priority": get_priority(new_state),
        "info": info,
    })


@app.route("/reset", methods=["POST"])
def reset():
    data = request.get_json(silent=True) or {}
    difficulty = data.get("difficulty", "medium")
    new_state = env.reset(difficulty=difficulty)
    return jsonify({
        "msg": "Environment reset!",
        "state": new_state,
        "difficulty": difficulty,
    })


@app.route("/agents", methods=["GET"])
def list_agents():
    return jsonify({"agents": list(agents.keys()), "active": active_agent})


def main():
    port = int(os.getenv("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()