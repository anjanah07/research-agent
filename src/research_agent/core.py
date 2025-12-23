from typing import cast
import json
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam, ChatCompletionMessageToolCall, ChatCompletionToolMessageParam
from rich.console import Console
from research_agent.tools import AVAILABLE_TOOLS

class Agent:
    def __init__(self, system_prompt: str):
        self.client = OpenAI()
        self.model = "gpt-5-nano"
        self.messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": system_prompt}]
        self.tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the internet for current events, facts, or news.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            },
                        },
                        "required": ["query"]
                    }
                }
            }
        ]
    
    def run(self, user_input: str):
        loop_count = 0
        MAX_LOOPS = 3

        self.messages.append({"role": "user", "content": user_input})
        while True:
            if loop_count >= MAX_LOOPS:
                return "I searched multiple times but couldn't find a clear answer. Please refine your question."

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=cast(list[ChatCompletionToolParam], self.tool_definitions),
                tool_choice="auto"
            )
            message = response.choices[0].message
            self.messages.append(cast(ChatCompletionMessageParam, message.model_dump(exclude_none=True))) 
            
            if message.tool_calls:
                console = Console()
                console.print(f"[bold yellow]Agent decided to use tools ... [/bold yellow]")

                for tool_call in message.tool_calls:
                    if isinstance(tool_call, ChatCompletionMessageToolCall):
                        func_name = tool_call.function.name
                        func_args = json.loads(tool_call.function.arguments)

                        console.print(f"[cyan]Executing: {func_name}({func_args})[/cyan]")
            
                        if func_name in AVAILABLE_TOOLS:
                            tool_output = AVAILABLE_TOOLS[func_name](**func_args)
                        else:
                            tool_output = f"Error : Tool {func_name} not found"

                        tool_message: ChatCompletionToolMessageParam = {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "content": tool_output
                        }
                        self.messages.append(tool_message)
                        return tool_output
            else:
                return message.content


