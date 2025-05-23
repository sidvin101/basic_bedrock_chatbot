import boto3
import json
import os
from manage_context import update_history, get_history
from handle_errors import handle_error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the AWS Bedrock client
client = boto3.client(
    'bedrock',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Get the model name
MODEL_NAME = os.getenv('MODEL_NAME', 'anthropic.claude-v2')

'''
This function will call the Bedrock API and return the response
'''
def call_bedrock(prompt):
    response = client.invoke_model(
        modelId=MODEL_NAME,
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            'prompt': prompt,
            'maxTokens': 1000,
            'temperature': 0.7
        })
    )

    result = json.loads(response['body'].read())
    return result.get("completion", "No response from model.")

'''
This is the main chat function
'''
def chat_with_bedrock(user_input):
    print("Welcome User! You can ask a question to the chatbot, or type 'exit' to quit. \n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        try:
            #Get the history and combine with the user input
            context_prompt = get_history() + f"User: {user_input}\nBot:"
            # Call the Bedrock API
            response = call_bedrock(context_prompt)
            # Update the history with the user input and bot response
            update_history(user_input, response)
            # Print the bot response
            print(f"Bot: {response}")
        except Exception as e:
            # Handle the error
            error_message = handle_error(e)
            print(f"Error: {error_message}")

if __name__ == "__main__":
    chat_with_bedrock()