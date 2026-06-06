"""Main entry point for the deep research virtual files agent."""

import sys

from agent.core import create_agent, run_agent
from agent.export_hook import export_virtual_files
from config.settings import get_export_dir, get_thread_id


def main():
    """Run the deep research agent interactively."""
    print("=" * 60)
    print("Deep Research Virtual Files Agent")
    print("=" * 60)
    print("Type your query or command. Type '/exit' to finish.")
    print("The agent will search the internet and create virtual files.")
    print("Virtual files will be exported on exit.\n")

    # Initialize agent
    try:
        agent = create_agent()
    except Exception as e:
        print(f"Error creating agent: {e}")
        print("Make sure you have configured your LLM API key in .env")
        sys.exit(1)

    thread_id = get_thread_id()
    print(f"Session thread_id: {thread_id}\n")

    all_states: list[dict] = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession interrupted.")
            break

        if not user_input:
            continue

        if user_input.lower() == "/exit":
            print("\nEnding session...")
            break

        try:
            state = run_agent(agent, user_input, thread_id)
            all_states.append(state)

            # Print the last assistant message as response
            messages = state.get("messages", [])
            if messages:
                last_msg = messages[-1]
                content = getattr(last_msg, "content", str(last_msg))
                print(f"\nAgent: {content}\n")
        except Exception as e:
            print(f"\nError during agent execution: {e}\n")

    # Export virtual files from all states
    if all_states:
        export_dir = get_export_dir()
        print(f"\nExporting virtual files to: {export_dir}")

        try:
            # Use the last state (most complete)
            exported = export_virtual_files(all_states[-1], export_dir)
            if exported:
                print(f"Exported {len(exported)} file(s):")
                for f in exported:
                    print(f"  - {f}")
            else:
                print("No virtual files to export.")
        except Exception as e:
            print(f"Error during export: {e}")

    print("\nSession ended.")


if __name__ == "__main__":
    main()
