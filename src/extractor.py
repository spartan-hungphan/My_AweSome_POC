import re
from typing import List

def extract_common_steps(common_steps : str) -> List[str]:
    common_steps_regex = r"(Given|Then|When)\('(.+?)'"
    steps = re.findall(common_steps_regex, common_steps)
    return steps

def feature2scenario(feature : str) -> List[str]:
    scenarios = feature.split("Scenario")
    scenarios = ["Scenario" + scenario for scenario in scenarios[1:]]
    return scenarios

def scenario2steps(scenario : str) -> List[str]:
    steps = "\n".join(scenario).split("\n")
    steps = [step.strip() for step in steps]
    return steps
