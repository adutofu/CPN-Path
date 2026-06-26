from chat_functions import add_assistant_message, add_user_message, chat

from statistics import mean
import json


class PromtEvaluator():
    def __init__(self):
        pass

    def render(self, template_text, content_dict):
        """
        Takes a raw string templates annd replaces placeholders like {task}
        with the actual data values found inthe dictionary"""


        # 1. Create a copy of the template text to modify.
        rendered_text = template_text


        # 2. Loop through every key and value inside the context_dict.
        
        for key, value in content_dict.items():
        
            # construct the traget placeholder string like "{task}"
            placeholder = "{" + key + "}"

            # replace all occurence of {task} with the actual value

            rendered_text = rendered_text.replace(placeholder, str(value))
        
        
        # 3. For each key, search the text for '{key}' and swap it with the string value.
        
        
        return rendered_text
        
        # 4. Return the fully updated text string.


    
    def run_test_case(self, test_case):
        """
    Constructs a prompt for the AI based on a given test case and retrieves the AI's response.

    Args:
        test_case (dict): A dictionary containing details of the task, typically with a "task" key.

    Returns:
        str: The AI's generated response to the task.
    """
        #Formulate the prompt by embedding the test case's task discription.
        template = """
        solve the folowing task:
        test_case{"task"}
        """
        prompt = self.render(template, test_case)


        messages = []

        add_user_message(messages, prompt)

        output = chat(messages)
        
        model_grade = self.grade_output(test_case, output)

        return {
            "output": output,
            "test_case": test_case,
            "score": model_grade["score"],
            "reasoning": model_grade["reasoning"]
        }
    
    def grade_output(self, test_case, output):
        """
        Leverages an LLM judge to evaluate the output against the solution criteria.
        """
        # 1. Create an evaluation prompt string enclosing the task, the solution, 
        #    and test_case["solution_criteria"] inside clear labels.
        
        eval_template = """
    You are an expert AWS code reviewer, reveiew the following

        Original Task:
        <task>
        {test_case["task"]}
        </task>

        AI Generated solution:
        <solution>
        {output}
        </solution>


        Solution Criteria
        <criteria>
        {test_case["solution_criteria"]}
        </criteria>


        Output Format:
        Respond with a raw JSON object contaning a "score" integer (1-10) and a "reasoning" string.
        """

        content = {
            "task": test_case["task"],
            "solution": output,
            "criteria": test_case["solution_criteria"],
        }

        eval_prompt = self.render(eval_template, content)

        messages = []

        add_user_message(messages, eval_prompt)


        add_assistant_message(messages, "```json")

                                         


        grader_response = chat(messages, stop_sequences=["```"])
        
        

        
        

        # 2. Set up an empty messages list and append the evaluation prompt.
        
        # 3. Call chat(messages) to get the grader's response text.
        return json.loads(grader_response)
        # 4. Use json.loads() to turn that response into a dictionary and return it.






    def run_eval(self, dataset):
        """
        Evaluates a set of test cases by running each one and collecting the results.

    Args:
        dataset (list): A list of dictionaries, where each dictionary represents a test case.

    Returns:
        list: A list of dictionaries, each containing the output, original test case, and score
              for a given test case.
        """
        results = []

        for test_case in dataset:

            result = self.run_test_case(test_case)

            results.append(result)

        average_score = mean([result["score"] for result in results])

        print(f"Average score: {average_score}")

        return results
    
