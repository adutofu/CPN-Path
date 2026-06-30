"""Creating helper functions that would help to manage conversation better.
in the context of multi-turn conversation"""


"""This following lines of code are for if one want to make use of Anthropic_API_key...
from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()
client = Anthropic()
model = "name of anthropic model that u would like to use"
reponse = client.messages.create(
    model=model
    max_tokens=1000
    messages=[
    {
    "role": "user",
    "content": "what is devops?"
    }
]
)

print(response.content[0].text)
"""

# import neccessary packages

from dotenv import load_dotenv

import os # this is because we want to make use of another API key
#which is a function for you to read the other API key in the .env file

import json

from anthropic import Anthropic # Import the Anthropic client for interacting with Anthropic models.

from statistics import mean

# Import re module stands for Regular Expressions. 
# It is used to search, match, and manipulate text based on specific, highly flexible patterns.
import re

# The ast module stands for Abstract Syntax Tree. 
# It allows a Python program to look at, analyze, or safely execute Python code as a structured tree data object.
import ast

# Load the API KEY from the .env file
load_dotenv()

# Create the Anthropic client - it automatically reads ANTHROPIC_API_KEY from the environment.
# Ensure you have ANTHROPIC_API_KEY set in your .env file.
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"), # Anthropic client automatically looks for ANTHROPIC_API_KEY.
)


# select the claude model you would like to use
# Using a specific Anthropic model identifier.
# Examples: "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
# For the latest models, check Anthropic's documentation.
model = "claude-haiku-20231024-5" # Using Claude Haiku 4.5 as a capable and cost-effective option.



# ADD USER MESSAGE FUNCTION THIS CAN ALSO WORK FOR ANTHROPIC AND OTHER AI
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)



# ADD ASSISTANT(AI) MESSAGE FUNCTION THIS CAN ALSO WORK FOR ANTHROPIC AND OTHE AI
def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


# NOW CREATING THE CHAT FUNCTION THAT WOULD MAKE USE OF THE ADD_MSG and ADD_ASSISTANT MSG..

# THIS IS THE ADAPTED CHAT FUNCTION FOR ANTHROPIC SDK
def chat(messages, system=None, temperature=1.0, stop_sequences=None):
    # Anthropic's messages API expects a 'system' parameter for system prompts,
    # separate from the 'messages' list which contains user/assistant turns.
    # If a system prompt is provided, it will be passed directly to the 'system' parameter.
    
    # Anthropic uses 'max_tokens' to limit the length of the generated response.
    # The 'stop_sequences' parameter is directly supported by Anthropic.
    
    # Create the parameters dictionary for the Anthropic API call.
    params = {
        "model": model, # The specific Anthropic model to use.
        "max_tokens": 1000, # Maximum number of tokens to generate in the response.
        "messages": messages, # The conversation history, a list of message dictionaries.
        "temperature": temperature, # Controls the randomness of the model's output. Higher values mean more random.
        "stop_sequences": stop_sequences,
         
    }

    # If a system prompt is provided, add it to the parameters.
    if system:
        params["system"] = system # Anthropic's API takes a dedicated 'system' parameter.

    # If stop sequences are provided, add them to the parameters.
    if stop_sequences:
        params["stop_sequences"] = stop_sequences # Anthropic uses 'stop_sequences' parameter.

    try:
        # Make the API call to Anthropic.
        message = client.messages.create(**params)
        # Anthropic returns a list of content blocks. 
        # We need to access the text field of the first block.
        return message.content[0].text
    
    except Exception as e:
        print(f"Error during Anthropic API call: {e}")
        # Return None so calling functions know the generation failed.
        return None


# Report Builder function for buildeing a report from the prompt evaluation and grading process
def generate_prompt_evaluation_report(evaluation_results):
    """
    Generates a structured, self-contained HTML report document detailing 
    the summary metrics and fine-grained results of a prompt evaluation run.
    """
    # -------------------------------------------------------------------------
    # 1. SUMMARY METRICS CALCULATION
    # -------------------------------------------------------------------------
    
    # Capture the total count of test cases evaluated to determine dataset scale.
    total_tests = len(evaluation_results)
    
    # Extract just the raw numerical score integers from every evaluation dictionary.
    scores = [result["score"] for result in evaluation_results]
    
    # Calculate the mathematical mean score across all items; default to 0 if the list is completely empty.
    avg_score = mean(scores) if scores else 0
    
    # Establish a constant upper boundary for the grading scale to contextualize scores (e.g., /10).
    max_possible_score = 10
    
    # Determine the project's quality pass rate by filtering for scores >= 7,
    # converting it into a percentage, and safeguarding against division-by-zero errors.
    pass_rate = (
        100 * len([s for s in scores if s >= 7]) / total_tests if total_tests else 0
    )

    # -------------------------------------------------------------------------
    # 2. HTML STRUCTURE AND INLINE CSS STYLING LAYOUT
    # -------------------------------------------------------------------------
    
    # Initialize a multi-line HTML string buffer, embedding standard responsive CSS
    # layouts to handle styling, flexbox grids, table structures, and code coloring.
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Prompt Evaluation Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .header {{
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .summary-stats {{
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 10px;
            }}
            .stat-box {{
                background-color: #fff;
                border-radius: 5px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                flex-basis: 30%;
                min-width: 200px;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: bold;
                margin-top: 5px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th {{
                background-color: #4a4a4a;
                color: white;
                text-align: left;
                padding: 12px;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                vertical-align: top;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .output-cell {{
                white-space: pre-wrap;
            }}
            .score {{
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 3px;
                display: inline-block;
            }}
            .score-high {{
                background-color: #c8e6c9;
                color: #2e7d32;
            }}
            .score-medium {{
                background-color: #fff9c4;
                color: #f57f17;
            }}
            .score-low {{
                background-color: #ffcdd2;
                color: #c62828;
            }}
            .output {{
                overflow: auto;
                white-space: pre-wrap;
            }}

            .output pre {{
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                margin: 0;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.4;
                color: #333;
                box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
                overflow-x: auto;
                white-space: pre-wrap; 
                word-wrap: break-word; 
            }}

            td {{
                width: 20%;
            }}
            .score-col {{
                width: 80px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Prompt Evaluation Report</h1>
            <div class="summary-stats">
                <div class="stat-box">
                    <div>Total Test Cases</div>
                    <div class="stat-value">{total_tests}</div>
                </div>
                <div class="stat-box">
                    <div>Average Score</div>
                    <div class="stat-value">{avg_score:.1f} / {max_possible_score}</div>
                </div>
                <div class="stat-box">
                    <div>Pass Rate (≥7)</div>
                    <div class="stat-value">{pass_rate:.1f}%</div>
                </div>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Scenario</th>
                    <th>Prompt Inputs</th>
                    <th>Solution Criteria</th>
                    <th>Output</th>
                    <th>Score</th>
                    <th>Reasoning</th>
                </tr>
            </thead>
            <tbody>
    """

    # -------------------------------------------------------------------------
    # 3. DYNAMIC ROW PROCESSING & CONTENT GENERATION LOOP
    # -------------------------------------------------------------------------
    
    # Iterate through each structured evaluation dictionary inside our input results array.
    for result in evaluation_results:
        
        # Unpack the prompt_inputs nested dictionary. We use a list comprehension to transform
        # each key-value attribute map into a bold tag string segment, then join them with HTML line breaks.
        prompt_inputs = result["test_case"].get("prompt_inputs")
+        if prompt_inputs and isinstance(prompt_inputs, dict):
+            prompt_inputs_html = "<br>".join(
+                [f"<strong>{key}:</strong> {value}" for key, value in prompt_inputs.items()]
+            )
+        else:
+            prompt_inputs_html = "N/A"

        # Process the solution_criteria list. It joins the criteria array strings with an internal line break
        # accompanied by a structural list bullet marker (•) to display the evaluation rules neatly.
        
        criteria = result["test_case"].get("solution_criteria")
        if criteria and isinstance(criteria, list) and len(criteria) > 0:
            # Add bullet marker to the first item for clean formatting
            criteria_string = "<br>• ".join([str(c) for c in criteria])
        else:
            criteria_string = "N/A"


        # Determine semantic color thresholds: Check the test item score to assign the appropriate CSS class.
        score = result["score"]
        if score >= 8:
            score_class = "score-high"     # High quality threshold match -> Applies a solid green accent badge.
        elif score <= 5:
            score_class = "score-low"      # Syntax fail/Severe risk deviation -> Applies a warning red accent badge.
        else:
            score_class = "score-medium"   # Intermediate / Partial completion -> Applies a warning yellow accent badge.

        # Append a populated HTML table row string template block directly to our main data table container body.
        # Uses the pre-formatted variables and extracts raw string variables like scenario and output parameters.
        html += f"""
            <tr>
                <td>{result["test_case"]["scenario"]}</td>
                <td class="prompt-inputs">{prompt_inputs_html}</td>
                <td class="criteria">• {criteria_string}</td>
                <td class="output"><pre>{result["output"]}</pre></td>
                <td class="score-col"><span class="score {score_class}">{score}</span></td>
                <td class="reasoning">{result["reasoning"]}</td>
            </tr>
        """

    # -------------------------------------------------------------------------
    # 4. STRUCTURAL CONCATENATION AND RETURN
    # -------------------------------------------------------------------------
    
    # Close out the remaining open structural table container body tags and end the HTML string stream.
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    # Return the completely processed, monolithic HTML string buffer back to the calling function module.
    return html

# Dataset generating function for prompt evaluation
def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
        "format": "json" or "python" or "regex"
        "solution_criteria" "Key criteria for evaluating the solution"
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages = []

    # Append the structured instructions (the prompt variable) to the messages list as a 'user' role input.
    add_user_message(messages, prompt)

    # Inject a pre-filled assistant response to guide the model's generation.
    # By forcing the model to start with "```json", it ensures the AI begins outputting the raw data array directly
    # instead of wasting tokens on conversational text like "Sure, here is your dataset:".
    add_assistant_message(messages, "```json") # Standardizing to triple backticks for JSON block.

    # Send the messages payload to the LLM. The 'stop_sequences' parameter tells the model to stop generating
    # immediately when it outputs the closing triple backticks ("```"), preventing extra text trailing at the end.
    text = chat(messages, stop_sequences=["```"]) # Corrected stop sequence to triple backticks.

    if text is None:
        print("Failed to generate dataset due to API error.")
        return []
    
    # Strip away any leading or trailing whitespace or hidden newline characters from the model's string response.
    text = text.strip()
    
    if text.endswith('```'):
        text = text[:-3].strip()

    # Print the final cleaned-up JSON string to the console/terminal.
    print(text)

    # Convert the generated text into a json file and rename it to the variable data
    # then return the valrable data to the function
    return json.loads(text)


class PromptEvaluator():
    """
    The master blueprint for our evaluation engine. It wraps together string 
    rendering, prompt execution, model judging, and algorithmic code syntax 
    verification inside a single unified namespace.
    """

    def __init__(self):
        """
        The Class Constructor.
        Initializes an isolated worker copy of our evaluator engine. Currently 
        stateless, providing an open slot to append configuration keys later.
        """
        pass
    

    def render(self, template_text, content_dict):
        """
        The Safe Template Rendering Engine.
        
        Purpose:
            Prevents raw f-strings from accidentally confusing JSON/XML syntax 
            brackets with active Python variables. Loops over context dictionaries 
            and replaces exact target keywords enclosed in matching braces.
        """
        # Step 1: Copy the incoming text template into a mutable variable
        rendered_text = template_text

        # Step 2: Loop through every isolated key-value element inside our target map
        for key, value in content_dict.items():
            
            # Step 3: Piece together the exact string sequence to find (e.g., "{task}")
            placeholder = "{" + key + "}"

            # Step 4: Swap every single placeholder match with our text-casted runtime variable
            rendered_text = rendered_text.replace(placeholder, str(value))
        
        # Step 5: Return the fully compiled prompt text string back to the executor
        return rendered_text

# CREATING OF THE GRADER FUNCTION & we are making use of a model grader, THAT WOULD BE USED IN THE run_eval function
    def grade_by_model(self, test_case, output):
        # This function implements the 'LLM-as-a-judge' pattern.
        # It leverages a highly capable model to act as an expert reviewer,
        # providing structured feedback and a numerical score for the AI's output.
    
        # 1. Define a detailed evaluation prompt using XML-like tags to clearly 
        # delineate the original task from the AI-generated solution.
        eval_template = """
        You are and expert AWS code reviewr. your task is to evaluate the following AI_generated solution.

        Original Task:
        <task>
        {test_case["task"]}
        </task>

        AI Generated Solution:
        <solution>
        {output}
        </solution>

        Solution Criteria to be used to evaluate it:
        <criteria>
        {test_case["solution_criteria"]}
        </criteria>


        Output Format
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key strengths
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1-10

        Respond with JSON. Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}
        """

        # Establish the context blueprint dict mapping our inputs to the customer template keys

        content = {
            'test_case["task"]': test_case["task"],
            "output": output,
            'test_case["solution_criteria"]': test_case["solution_criteria"],
        }

        eval_prompt = self.render(eval_template, content)


            # 2. Build the message history for the evaluation request.
        messages = []

        add_user_message(messages, eval_prompt)
    
            # 3. Use 'pre-filling' to force the assistant to start with a JSON block.
            # This significantly improves reliability by ensuring the response begins with data.
        add_assistant_message(messages, "```json")
    
            # 4. Call the LLM and use a stop sequence to halt generation at the end of the JSON block.
        eval_text = chat(messages, stop_sequences=["```"]) # Corrected stop sequence to triple backticks.
    
        if eval_text is None:
            print("Failed to get model grade due to API error.")
            return None # Return None if chat failed
    
        # 5. Deserialize the JSON string into a structured Python dictionary.
        try:
            return json.loads(eval_text)
        except json.JSONDecodeError as e:
            print(f"Failed to parse model grade JSON: {e}")
            print(f"Raw response: {eval_text}")
            return None # Return None if JSON parsing failed


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
        # Iterate through each test case in the provided dataset.
        for test_case in dataset:
            # Execute the test case and get its result (output and score).
            result = self.run_test_case(test_case)
            # Append the result of the current test case to the results list.
            results.append(result)

        # Calculate the mathematical average (mean) of the scores extracted from all results
        average_score = mean([result["score"] for result in results])
        # Step 6: Log a clean telemetry overview onto the console terminal pipeline
        print(f"\n==========================================")
        print(f"EVALUATION COMPLETE | Dataset Average Score: {average_score}")
        print(f"==========================================\n")
        return results


# Syntax Validation Function in line with CODE BASED GRADING: To check if
# generated code has valid syntax, you can create three helper functions that attempts to parse the output.
    def validate_json(self, text):
        try:
            # Attempt to parse the stripped text string into a valid Python dictionary/list.
            json.loads(text.strip())
            # Return a perfect score of 10 if the JSON syntax is entirely valid.
            return 10
        except json.JSONDecodeError:
            # Return a score of 0 if a parsing error occurs due to invalid JSON formatting.
            return 0
    
    def validate_python(self, text):
        try:
            # Parse the stripped string into an Abstract Syntax Tree to check for valid Python syntax.
            ast.parse(text.strip())
            # Return a perfect score of 10 if the string compiles as valid, executable Python code.
            return 10
        except SyntaxError:
            # Return a score of 0 if the code contains syntax violations or formatting errors.
            return 0

    def validate_regex(self, text):
        try:
            # Attempt to compile the stripped string into a regular expression pattern object.
            re.compile(text.strip())
            # Return a perfect score of 10 if the string forms a valid regular expression pattern.
            return 10
        except re.error:
            # Return a score of 0 if the string contains a malformed or invalid regular expression.
            return 0

    def grade_syntax(self, response, test_case):
        """
        The Code-Based Syntax Validator routing hook.
        Evaluates structural formatting benchmarks using concrete syntax checks instead of an LLM.
        """
        # Extract the expected target format constraints from the specific evaluation test case.
        target_format = test_case.get("format", "regex")

        # Check if the required output structure should be validated as JSON
        if target_format == "json":
            return self.validate_json(response)
    
        # Check if the required output structure should be validated as standard Python code
        elif target_format == "python":
            return self.validate_python(response)
    
        # Default to verifying the string against regular expression rules if no other formats match.
        else:
            return self.validate_regex(response)
    


# FUNCTION TO EXECUTE A SINGLE TEST CASE AND GRADE THE OUTPUT
    def run_test_case(self, test_case):
        """
        The Single Test Case Coordinator.
        Combines task rendering, baseline chat generation, text verification, 
        and deep LLM judging into an integrated pipeline output report.
        """
        # Step 1: Set up the raw execution template string layout.
        # FIXED: Variable updated from raw expressions to a clean placeholder matching the dict key
        template = """
        please solve the following task:
        {task}
        """
        
        # Step 2: Render out variables to establish our model instruction prompt
        prompt = self.render(template, test_case)

        # Step 3: Pack history array buffers and send them down to the target baseline chat client
        messages = []
        add_user_message(messages, prompt)
        output = chat(messages)
        
        # Step 4: Run our object-oriented LLM-as-a-judge evaluator method using the 'self' keyword.
        # This executes the handshake, passing our test parameters and fresh text responses.
        model_grade = self.grade_by_model(test_case, output)

        # Step 5: Establish runtime safety defaults in case our model grader runs into API failures
        score = 0
        reasoning = "Grading sequence aborted: target judge response payload was malformed."
        strengths = []
        weaknesses = []

        # Step 6: Safely unpack our rich JSON data dictionary elements if our judge executed successfully
        if model_grade is not None:
            try:
                score = model_grade.get("score", 0)
                reasoning = model_grade.get("reasoning", "No summary provided.")
                strengths = model_grade.get("strengths", [])
                weaknesses = model_grade.get("weaknesses", [])
            except AttributeError:
                # Triggers defensive fallback flags if json.loads yielded unmappable data structures
                reasoning = "Grading failure: judge output returned unparsable object types."

        # Step 7: Map all analytical logs cleanly into an executive validation report summary map
        return {
            "output": output,
            "test_case": test_case,
            "score": score,
            "reasoning": reasoning,
            "strengths": strengths,
            "weaknesses": weaknesses
        }

# Defines the `run_prompt` function, which merges a generic prompt with a specific test case.
# This function is designed to send a task to the AI and retrieve its solution.
def run_prompt(test_case):
    """
    Constructs a prompt for the AI based on a given test case and retrieves the AI's response.

    Args:
        test_case (dict): A dictionary containing details of the task, typically with a "task" key.

    Returns:
        str: The AI's generated response to the task.
    """
    # Formulate the prompt by embedding the test case's task description.
    prompt = f"""
please solve the following task:

{test_case["task"]}
"""
    # Initialize an empty list to hold the conversation messages for this specific interaction.
    messages = []
    # Add the constructed prompt as a user message to the conversation history.
    add_user_message(messages, prompt)
    # Send the messages to the AI model and get its response.
    output = chat(messages)
    # Return the AI's output.
    return output
