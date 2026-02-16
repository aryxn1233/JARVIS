def get_user_input():
    try:
        return input("You: ").strip()
    except KeyboardInterrupt:
        return "exit"
