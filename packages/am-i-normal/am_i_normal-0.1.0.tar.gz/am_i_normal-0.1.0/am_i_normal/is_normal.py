# am_i_normal/is_normal.py

import random

def is_normal():
    result = random.choice(["yes", "no"])
    motivation = random.choice([
        "Keep going, you're doing great!",
        "Believe in yourself!",
        "You can achieve anything!",
        "Stay positive and strong!",
        "Great things take time, be patient."
    ])
    return f"{result}. {motivation}"
