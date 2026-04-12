import random


class RandomAgent:
    def act(self, state):
        return random.randint(0, 19), "Random action selected"


class RuleBasedAgent:
    def act(self, state):
        injured = state.get("injured", 0)
        food = state.get("food_needed", False)
        rescue = state.get("rescue_needed", False)
        power = state.get("power_outage", False)
        infra = state.get("infrastructure_damage", False)
        disease = state.get("disease_outbreak", False)
        people = state.get("people", 0)

        if disease:
            action = random.choice([10, 11, 12, 13])
            return action, "Disease outbreak → containment action"
        if injured > 25:
            action = random.choice([0, 4, 5, 8])
            return action, "Critical injuries → heavy medical response"
        if injured > 0:
            action = random.choice([0, 4, 7])
            return action, "Injuries present → medical response"
        if food:
            action = random.choice([1, 6])
            return action, "Food shortage → supply action"
        if rescue:
            action = random.choice([2, 8, 9])
            return action, "Rescue needed → rescue action"
        if power:
            action = random.choice([16, 17])
            return action, "Power outage → restore electricity"
        if infra:
            action = random.choice([17, 19])
            return action, "Infrastructure damage → repair action"
        if people > 100:
            return 18, "Large population → temporary shelter"
        return 15, "Situation stable → monitoring"


class GreedyAgent:
    def act(self, state):
        injured = state.get("injured", 0)
        food = state.get("food_needed", False)
        rescue = state.get("rescue_needed", False)
        power = state.get("power_outage", False)
        infra = state.get("infrastructure_damage", False)
        disease = state.get("disease_outbreak", False)
        people = state.get("people", 0)

        scores = {
            8: 9.0 if (rescue or injured > 20) else -2.0,
            0: 8.0 if injured > 0 else -1.0,
            10: 7.0 if disease else 0.5,
            13: 6.0 if disease else 1.0,
            4: 6.0 if injured > 10 else 1.0,
            16: 6.0 if power else -1.0,
            2: 6.0 if rescue else -1.0,
            5: 5.0 if (injured > 5 or disease) else 0.5,
            1: 5.0 if food else -1.0,
            9: 5.0 if (rescue or people > 100) else 0.5,
            19: 5.0 if infra else -1.0,
            7: 4.0 if (injured > 0 or disease) else 0.5,
            17: 4.0 if (power or infra) else 0.5,
            18: 4.0 if (people > 80 or rescue) else 0.5,
            14: 3.0 if (injured > 20 or rescue) else 0.5,
            11: 3.0 if (disease or injured > 10) else 0.5,
            6: 3.0 if food else 0.5,
            12: 3.0 if disease else 0.5,
            15: 0.5,
            3: 1.0 if (injured == 0 and not food and not rescue) else -2.0,
        }
        best = max(scores, key=scores.get)
        return best, f"Greedy → best expected reward: {scores[best]:.1f}"