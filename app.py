from flask import Flask, render_template, request, jsonify, session
import os
import json
import boto3
from dotenv import load_dotenv
from manage_context import update_history, get_history, clear_history
from handle_errors import handle_error

#Load the environment variables
load_dotenv()

#Create the Flask app
app = Flask(__name__)

#Create the bedrock client
client = boto3.client(
    'bedrock-runtime',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

MODEL_NAME = os.getenv('MODEL_NAME', 'meta.llama-3-8b-instruct-v1:0')

# Function that calls the Bedrock API
def call_bedrock(prompt):
    try:
        response = client.invoke_model(
            modelId=MODEL_NAME,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'prompt': prompt,
                'max_gen_len': 100,
                'temperature': 0.1,
            })
        )
        result = json.loads(response['body'].read())
        model_output = result.get("generation", "No response from model.")
        
        if "User:" in model_output:
            model_output = model_output.split("User:")[0].strip()
        return model_output
    
    except Exception as e:
        return handle_error(e)

#Main app route
@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize variables
    response = None
    history = None
    history_view = False

    if request.method == 'POST':
        # Get the action from the form
        action = request.form.get('action')

        # Handle different actions
        if action == 'send':
            user_input = request.form.get('user_input')
            try:
                context = get_history() or ""
                prompt = context + f"User: {user_input}\nBot:"
                response = call_bedrock(prompt)
                update_history(user_input, response)
            except Exception as e:
                response = handle_error(e)

        elif action == 'reset':
            clear_history()
            response = "Chat history cleared."

        elif action == 'view':
            history = get_history()
            history_view = True

        elif action == 'back':
            history_view = False

    return render_template(
        'index.html',
        response=response,
        history=get_history() if history_view else None,
        history_view=history_view
    )

# Route to clear chat history
@app.route('/reset', methods=['POST'])
def reset():
    clear_history()
    return render_template('index.html', response="History has been cleared!", history="")

# Route to get chat history
@app.route('/view', methods=['GET'])
def view():
    return render_template('index.html', response=None, history=get_history())

if __name__ == '__main__':
    app.run(debug=True)
