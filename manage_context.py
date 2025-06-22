history = []

# Update the chat history with user input and bot response
def update_history(user_input, bot_response):
    history.append({
        'user_input': user_input,
        'bot_response': bot_response
    })

# Get the chat history, optionally limiting to the last n turns
def get_history(n=None):
    context = ''
    for turn in history:
        context += f"User: {turn['user_input']}\n"
        context += f"Bot: {turn['bot_response']}\n\n"
    if n is not None:
        context_blocks = context.strip().split('\n\n')[-n:]
        return '\n\n'.join(context_blocks)
    return context

# Clear the chat history
def clear_history():
    history.clear()
