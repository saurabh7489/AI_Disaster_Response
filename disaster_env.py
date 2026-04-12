import random

DIFFICULTY_CONFIGS = {
    "easy": {
        "people_range": (20, 50),
        "injured_range": (0, 10),
        "food_prob": 0.3,
        "rescue_prob": 0.2,
        "power_prob": 0.1,
        "infra_prob": 0.1,
        "max_steps": 30,
        "injury_growth": (-3, 2),
        "crisis_prob": 0.15,
    },
    "medium": {
        "people_range": (50, 120),
        "injured_range": (10, 30),
        "food_prob": 0.5,
        "rescue_prob": 0.4,
        "power_prob": 0.3,
        "infra_prob": 0.3,
        "max_steps": 25,
        "injury_growth": (-2, 4),
        "crisis_prob": 0.25,
    },
    "hard": {
        "people_range": (120, 300),
        "injured_range": (30, 80),
        "food_prob": 0.7,
        "rescue_prob": 0.6,
        "power_prob": 0.5,
        "infra_prob": 0.5,
        "max_steps": 20,
        "injury_growth": (-1, 6),
        "crisis_prob": 0.40,
    },
}

ZONES = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E"]


class DisasterEnv:
    def __init__(self, difficulty: str = "medium"):
        assert difficulty in DIFFICULTY_CONFIGS
        self.difficulty = difficulty
        self.cfg = DIFFICULTY_CONFIGS[difficulty]
        self.step_count = 0
        self.total_reward = 0.0
        self.state = {}
        self.reset()

    def reset(self, difficulty: str = None):
        if difficulty and difficulty in DIFFICULTY_CONFIGS:
            self.difficulty = difficulty
            self.cfg = DIFFICULTY_CONFIGS[difficulty]
        cfg = self.cfg
        self.step_count = 0
        self.total_reward = 0.0
        self.state = {
            "zone": random.choice(ZONES),
            "people": random.randint(*cfg["people_range"]),
            "injured": random.randint(*cfg["injured_range"]),
            "food_needed": random.random() < cfg["food_prob"],
            "rescue_needed": random.random() < cfg["rescue_prob"],
            "power_outage": random.random() < cfg["power_prob"],
            "infrastructure_damage": random.random() < cfg["infra_prob"],
            "disease_outbreak": False,
            "step": 0,
            "max_steps": cfg["max_steps"],
            "difficulty": self.difficulty,
        }
        return self.state

    def get_state(self):
        return self.state

    def step(self, action: int):
        assert isinstance(action, int) and 0 <= action <= 19
        reward = 0.0
        s = self.state
        cfg = self.cfg

        if action == 0:
            if s["injured"] > 0:
                s["injured"] = max(0, s["injured"] - random.randint(5, 15))
                reward += 8.0
            else:
                reward -= 1.0
        elif action == 1:
            if s["food_needed"]:
                s["food_needed"] = False
                reward += 5.0
            else:
                reward -= 1.0
        elif action == 2:
            if s["rescue_needed"]:
                s["rescue_needed"] = False
                reward += 6.0
            else:
                reward -= 1.0
        elif action == 3:
            stable = (s["injured"] == 0 and not s["food_needed"]
                      and not s["rescue_needed"] and not s["disease_outbreak"])
            reward += 1.0 if stable else -2.0
        elif action == 4:
            if s["injured"] > 10:
                s["injured"] = max(0, s["injured"] - random.randint(3, 10))
                reward += 6.0
            else:
                reward += 1.0
        elif action == 5:
            if s["injured"] > 5 or s["disease_outbreak"]:
                s["injured"] = max(0, s["injured"] - random.randint(2, 8))
                reward += 5.0
            else:
                reward += 0.5
        elif action == 6:
            reward += 3.0 if s["food_needed"] else 0.5
        elif action == 7:
            if s["injured"] > 0 or s["disease_outbreak"]:
                s["injured"] = max(0, s["injured"] - random.randint(1, 5))
                reward += 4.0
            else:
                reward += 0.5
        elif action == 8:
            if s["rescue_needed"] or s["injured"] > 20:
                s["rescue_needed"] = False
                s["injured"] = max(0, s["injured"] - random.randint(5, 12))
                reward += 9.0
            else:
                reward -= 2.0
        elif action == 9:
            if s["rescue_needed"] or s["people"] > 100:
                s["rescue_needed"] = False
                reward += 5.0
            else:
                reward += 0.5
        elif action == 10:
            if s["disease_outbreak"]:
                s["disease_outbreak"] = False
                reward += 7.0
            else:
                reward += 0.5
        elif action == 11:
            reward += 3.0 if (s["disease_outbreak"] or s["injured"] > 10) else 0.5
        elif action == 12:
            reward += 3.0 if s["disease_outbreak"] else 0.5
        elif action == 13:
            if s["disease_outbreak"]:
                s["disease_outbreak"] = False
                reward += 6.0
            else:
                reward += 1.0
        elif action == 14:
            reward += 3.0 if (s["injured"] > 20 or s["rescue_needed"]) else 0.5
        elif action == 15:
            reward += 0.5
        elif action == 16:
            if s["power_outage"]:
                s["power_outage"] = False
                reward += 6.0
            else:
                reward -= 1.0
        elif action == 17:
            reward += 4.0 if (s["power_outage"] or s["infrastructure_damage"]) else 0.5
        elif action == 18:
            reward += 4.0 if (s["people"] > 80 or s["rescue_needed"]) else 0.5
        elif action == 19:
            if s["infrastructure_damage"]:
                s["infrastructure_damage"] = False
                reward += 5.0
            else:
                reward -= 1.0

        s["injured"] = max(0, s["injured"] + random.randint(*cfg["injury_growth"]))
        cp = cfg["crisis_prob"]
        if random.random() < cp:
            s["food_needed"] = True
        if random.random() < cp:
            s["rescue_needed"] = True
        if random.random() < cp * 0.4:
            s["disease_outbreak"] = True
        if s["injured"] == 0:
            s["rescue_needed"] = False

        self.step_count += 1
        self.total_reward += reward
        s["step"] = self.step_count

        done = (
            s["injured"] <= 0
            and not s["food_needed"]
            and not s["rescue_needed"]
            and not s["power_outage"]
            and not s["disease_outbreak"]
        ) or self.step_count >= cfg["max_steps"]

        info = {
            "total_reward": round(self.total_reward, 2),
            "step": self.step_count,
            "difficulty": self.difficulty,
        }
        return s, round(reward, 2), bool(done), info