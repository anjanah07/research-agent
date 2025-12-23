from dotenv import load_dotenv
from rich.console import Console
import os

from rich.panel import Panel

from research_agent.core import Agent
load_dotenv()
console = Console()
SYSTEM_PROMPT = """
You are a deeply skeptical but helpful Research Engineer.
1. When asked a question, perform ONE web search.
2. Based on the results, provide an answer immediately.
3. Do not keep searching if the first search yields any relevant results.
"""

def main():
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]Error: OPENAI_API_KEY not found in .env file[/bold red]")
        return
    
    agent = Agent(system_prompt=SYSTEM_PROMPT)
    console.print(Panel.fit("[bold green]Agent Initialized. Type 'quit' to exit.[/bold green]"))

    while True:
        try:
            user_input =input("\n You: ")
            if user_input.lower() in ["quit", "Quit"]:
                break

            console.print("[dim]Thinking...[/dim]")
            response = agent.run(user_input)

            if response != None:
                console.print(Panel(response, title="Agent", border_style="blue"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")



if __name__ == "__main__":
    main()