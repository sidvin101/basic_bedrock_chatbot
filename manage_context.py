
# A variable to store the context
history = []

'''
This function will update the user input and bot response and append it to the history
'''
def update_history(user_input, bot_response):
    history.append(
        {
            'user_input': user_input,
            'bot_response': bot_response
        }
    )

'''
This function will retrieve the context from the history. If n is not defined, it will get all of the history
'''
def get_history(n=None):
    context = ''
    for turn in history:
        context += f"User: {turn['user_input']}\n"
        context += f"Bot: {turn['bot_response']}\n\n"
    if n is not None:
        context = context.split('\n\n')[-n-1:]