---
title: AI Disaster Response
emoji: 🚨
colorFrom: red
colorTo: red
sdk: docker
pinned: false
---

# 🚨 AI Disaster Response Environment

An AI agent that responds to disasters by allocating emergency resources like ambulances, food, rescue boats, and more.

Built for the **Meta × PyTorch × Hugging Face × Scaler OpenEnv Hackathon 2025**.

---

## What does it do?

The AI agent looks at a disaster zone and decides what action to take — send an ambulance, drop food supplies, dispatch a helicopter, contain a disease outbreak, and 16 more actions. The goal is to save as many lives as possible with the right resources at the right time.

---

## Folder Structure

```
ai-disaster-response-env/
│
├── disaster_env.py              # Core RL environment
├── agent.py                     # Rule-Based, Greedy, Random agents
├── inference.py                 # OpenEnv reset() and step() interface
├── openenv.yaml                 # OpenEnv specification file
├── pyproject.toml               # Project config and entry points
├── requirements.txt             # Python dependencies
├── uv.lock                      # Locked dependency versions
├── Dockerfile                   # Docker container setup
├── .dockerignore                # Files excluded from Docker build
├── README.md                    # Project documentation
│
├── server/
│   └── app.py                   # Flask API server
│
├── templates/
│   └── index.html               # Dashboard UI
│
└── static/
    ├── style.css                # Dashboard styles
    └── script.js                # Dashboard logic
```

---

## How to use the dashboard

1. Select a **difficulty** (Easy / Medium / Hard)
2. Select an **agent** (Rule-Based / Greedy / Random)
3. Click **Run Step** to see one decision
4. Click **Auto Run** to watch a full episode automatically
5. Click **Reset** to start a new episode

---

## Difficulty levels

| Level  | People    | Injured  | Max Steps |
|--------|-----------|----------|-----------|
| Easy   | 20 – 50   | 0 – 10   | 30        |
| Medium | 50 – 120  | 10 – 30  | 25        |
| Hard   | 120 – 300 | 30 – 80  | 20        |

---

## Actions available (20 total)

| ID | Action               |
|----|----------------------|
| 0  | Ambulance Dispatch   |
| 1  | Food Supply          |
| 2  | Rescue Boat          |
| 3  | Wait / Monitor       |
| 4  | Deploy Doctors       |
| 5  | Setup Medical Camp   |
| 6  | Water Supply         |
| 7  | Distribute Medicines |
| 8  | Helicopter Rescue    |
| 9  | Evacuation Bus       |
| 10 | Quarantine Zone      |
| 11 | Sanitize Area        |
| 12 | Distribute Masks     |
| 13 | Vaccination Drive    |
| 14 | Alert Authorities    |
| 15 | Monitor Situation    |
| 16 | Restore Electricity  |
| 17 | Setup Comms Network  |
| 18 | Temporary Shelter    |
| 19 | Clear Road Blockages |

---

## Agents

- **Rule-Based** — follows a priority chain (disease → injuries → food → rescue → power)
- **Greedy** — picks the action with highest expected reward each step
- **Random** — picks a random action (baseline for comparison)

---

## API Endpoints

| Method | Endpoint | Description                   |
|--------|----------|-------------------------------|
| GET    | `/state` | Get current environment state |
| POST   | `/reset` | Reset to a new episode        |
| POST   | `/step`  | Run one step with agent       |

---
## License

[MIT LICENSE](LICENSE)

---
## Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-disaster-response-env
cd ai-disaster-response-env

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac / Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server/app.py
```

Then open `http://localhost:7860` in your browser.

---

## Run with Docker

```bash
docker build -t ai-disaster-env .
docker run -p 7860:7860 ai-disaster-env
```

Then open `http://localhost:7860`

---

## Tech Stack

- Python 3.11 · Flask · OpenEnv Core · OpenAI SDK · Docker · Hugging Face Spaces

---
