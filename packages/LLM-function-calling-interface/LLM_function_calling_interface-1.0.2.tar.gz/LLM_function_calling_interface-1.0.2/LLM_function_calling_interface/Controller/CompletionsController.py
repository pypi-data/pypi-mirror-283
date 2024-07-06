import json
from typing import List, Optional

from Model import CompletionModel, Tool, Message, FunctionCall


class GenerateArgs:
    instruction: Optional[str]
    messages: List[Message]
    tools: Optional[List[Tool]]


def parse_content_to_function_call(content, **args: GenerateArgs):
    tools = args.get('tools')
    if tools is None:
        return True, content
    if 'function_response' in content:
        return False, 'This is a function response, not a function call. Please provide a function call.'
    try:
        function_call_str = content.split('<function_call>')[1].split('</function_call>')[0].replace("'", '')
    except Exception as e:
        return True, content
    try:
        function_calls = json.loads(function_call_str)
        if not isinstance(function_calls, list):
            return False, 'The function call must be a list in JSON format between <function_call> and </function_call>. Example:<function_call> [{"name": "function_name", "arguments": {"arg_1": "value_1", "arg_2": "value_2"}}]</function_call>'
        function_calls_validate = [FunctionCall(**function_call) for function_call in function_calls]
        for function in function_calls_validate:
            function.validate()
            function.validate_arguments(tools)
        print('function_calls', function_calls)
        return True, function_calls
    except Exception as e:
        print('Error', e)
        return False, 'The function call must be a list in JSON format between <function_call> and </function_call>. Example:<function_call> [{"name": "function_name", "arguments": {"arg_1": "value_1", "arg_2": "value_2"}}]</function_call>'


def generate_function_call_prompt(functions_metadata):
    return f"""
    Available tools:
    {str(functions_metadata)}
    
    Analyze the user's input to determine which tool (if any) should be invoked.
    
    If a tool is relevant, provide its name and the necessary parameters in JSON format between <function_call> and </function_call>:
    <function_call>
     [{{ "name": "function_name1", "arguments": {{ "arg_1": "value_1", "arg_1": "value_1", ... }} }},
    {{ "name": "function_name2", "arguments": {{ "arg_2": "value_2", "arg_2": "value_2", ... }} }}] 
    </function_call>
    It is important to provide the correct tool name and parameters to ensure the tool is invoked correctly.
    Remember, you can find the list of tools here: {str(functions_metadata)}
    If no tool is relevant, respond with an empty JSON object:
    {{}}
    """


def format_message(**args: GenerateArgs):
    messages = args.get('messages', [])
    instruction = args.get('instruction')
    tools = args.get('tools')
    messages_result = []
    if tools is not None:
        messages_result.append({
            'role': 'system',
            'content': generate_function_call_prompt(tools)
        })
    if instruction is not None:
        messages_result.append({
            'role': 'system',
            'content': instruction
        })
    for message in messages:
        if message['role'] == 'user':
            messages_result.append({
                'role': 'user',
                'content': message['content']
            })
        elif message['role'] == 'assistant':
            messages_result.append({
                'role': 'assistant',
                'content': message['content']
            })
        elif message['role'] == 'function_call':
            messages_result.append({
                'role': 'assistant',
                'content': f"<function_call> {message['content']} </function_call>"
            })
        elif message['role'] == 'function_response':
            messages_result.append({
                'role': 'user',
                # 'content': f"<function_response> {message['content']} </function_response>"
                'content': f"Based on the data retrieved from the following tool invocations, provide an appropriate response to the user's question(s). \n **** \n The result of invoking {message['content']['function_name']} is {message['content']['response']}."
            })
    return messages_result


class CompletionController(CompletionModel):
    def generate(self, **args: GenerateArgs):
        args = {
            'instruction': args.get('instruction') or self.instruction,
            'messages': args.get('messages') or [],
            'tools': args.get('tools') or self.tools
        }
        response = 'No response'
        retry = 3
        valid = False
        while retry > 0:
            messages = format_message(**args)
            response = self.generate_function(messages)
            valid, response = parse_content_to_function_call(response, **args)
            if valid:
                break
            retry -= 1
        return {
            'role': 'fuction_call',
            'content': response
        } if valid \
            else {
            'role': 'assistant',
            'content': response
        }
