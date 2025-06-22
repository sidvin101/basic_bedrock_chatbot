import streamlit as st
import os
import json
import boto3

# Initialize Bedrock client using st.secrets
client = boto3.client(
    'bedrock-runtime',
    region_name=st.secrets["aws"]["region"],
    aws_access_key_id=st.secrets["aws"]["access_key_id"],
    aws_secret_access_key=st.secrets["aws"]["secret_access_key"]
)

MODEL_NAME = st.secrets["aws"].get("model_name", "meta.llama-3-8b-instruct-v1:0")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "chat"  # other: "view"

# Function to call Bedrock
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
        if "AccessDenied" in str(e):
            return "Access Denied: You do not have permission to access this resource."
        if "Throttling" in str(e):
            return "Throttling: You have exceeded the allowed request rate."
        return f"An unknown error occurred. Please try again later.\nDetails: {str(e)}"

# Construct full prompt from history
def get_full_context():
    context = ""
    for turn in st.session_state.history:
        context += f"User: {turn['user']}\nBot: {turn['bot']}\n\n"
    return context

# UI
st.set_page_config(page_title="Llama Chat", layout="centered")
st.title("Llama Chatbot")

if st.session_state.view_mode == "chat":
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Ask me anything...", key="user_input", height=100)
        submitted = st.form_submit_button("Send")
        if submitted and user_input.strip():
            prompt = get_full_context() + f"User: {user_input}\nBot:"
            bot_response = call_bedrock(prompt)
            st.session_state.history.append({"user": user_input, "bot": bot_response})
            st.markdown(f"**Response:** {bot_response}")

elif st.session_state.view_mode == "view":
    st.subheader("Conversation History")
    if st.session_state.history:
        for turn in st.session_state.history:
            st.markdown(f"**User:** {turn['user']}")
            st.markdown(f"**Bot:** {turn['bot']}")
            st.markdown("---")
    else:
        st.info("No conversation history yet.")

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("View Full History"):
        st.session_state.view_mode = "view"
with col2:
    if st.button("Back to Chat"):
        st.session_state.view_mode = "chat"
with col3:
    if st.button("Reset History"):
        st.session_state.history.clear()
        st.success("History cleared!")
