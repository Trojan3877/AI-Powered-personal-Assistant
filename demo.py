# demo.py
from assistant.main import process_user_input

print("🤖 AI Assistant (type 'exit' to quit)")
print("--------------------------------------")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break
    response = process_user_input(user_input)
    print(f"Assistant: {response}")
