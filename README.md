# basic_bedrock_chatbot
A basic repo to test and work with aws bedrock and conversational ai. This includes features to manage errors memory.

## Architecture
```
|- templates
|  - index.html: Index UI for Flask application
|- app.py: Main Flask Application
|- handle_errors.py: helper function to identify and address errors
|- manage_context.py: helper function to deal with chat history
|- requirements.txt: a list of installations
|- streamlit_app.py: Main Streamlit applictaion
```

## Process
- The User asks a question
- The app will use that question and the previous history as context for the response
- The question and response will be added into the history
- The user has the option to view the full history, as well as to reset the history for a fresh session state.

## How to Run Locally
- Clone the repo
- Install packages from requirements.txt
- Create a .env file with these specifications
AWS_REGION = your-aws-region
AWS_ACCESS_KEY_ID = your-aws-access-key
AWS_SECRET_ACCESS_KEY = your-aws-secret-access-key
MODEL_NAME = your-aws-model-name #best results are the arn inference profiles
- run app.py

Alternatively, you can use the Streamlit application instead: https://basicbedrockchatbot.streamlit.app/

## Big O
- get_history(): O(n), where n is the number of User Bot messages
- String concatentation for the prompt: O(k) where k is the total length of the prompt
- call_bedrock(): O(1) algorithmicly
- update_history(): O(1) For appending
- clear_history(): O(1)
- view int the history: O(n) since we are calling get_history()
- back: O(1) for a boolean flip
- render_template(): O(1)
