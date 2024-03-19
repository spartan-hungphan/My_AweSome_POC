from langchain.prompts import PromptTemplate
import openai
import re
from typing import List
from .retriever import Retriever
from .extractor import feature2scenario, scenario2steps

class ModelPredictor:
    def __init__(self, 
                 retrieve_method : str = "faiss", 
                 top_k : int = 3, 
                 threshold : int = 0.7):
        with(open("./dataset/system_prompt.txt", "r")) as INFILE:
            self.system_message = INFILE.read()
        
        with(open("./dataset/user_prompt.txt", "r")) as INFILE:
            user_prompt = INFILE.read()
            self.user_prompt = PromptTemplate(
                input_variables = ["related_steps", "given_step"],
                template = user_prompt
            )

        self.top_k = top_k
        self.threshold = threshold
        self.retriever = Retriever()

    def _retrieve(self, steps : List[str]) -> List[str]:
        for step in steps:
            structure = step.split(" ")
            step_type = structure[0]
            step = " ".join(structure[1:])
            ### If step startswith Then, replace Then into I expect that
            step = "I expect that" + step if "Then" in step_type else step 
            ### Replace "string" into {string}
            step = re.sub(r'"[^"]+"', '{string}', step) 

        related_steps = [self.retriever.faiss_retrieve(step) for step in steps]
        return related_steps
    
    def _ignore_step(self, step : str) -> bool:
        ignore_patterns = ["Scenario", "Example", "|"]
        for pattern in ignore_patterns:
            if pattern in step:
                return True
        if step == "": 
            return True
        if step.startswith("@"): 
            return True
        return False

    async def predict(self, feature_content : str) -> str:
        ### Extract
        scenarios = feature2scenario(feature_content)
        steps = scenario2steps(scenarios)
        ### Retrieve
        related_steps = self._retrieve(steps)
        
        ### LLM
        client = openai.Client()

        ### User Calling
        step_responses = []
        for index, step in enumerate(steps):
            if self._ignore_step(step):
                step_responses.append(step) 
                continue

            step_temp = step.split(" ")
            step_type = step_temp[0]
            step = " ".join(step_temp[1:])

            user_message = self.user_prompt.format(
                related_steps = "\n".join(related_steps[index]),
                given_step = step
            )
        
            step_response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": user_message}]
            )       
            step_responses.append(step_type + " " + step_response.choices[0].message.content)

        return "\n".join(step_responses)