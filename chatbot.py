import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="LenaChatbot")

def load_generator():
    text_generator = pipeline("text-generation", model="gpt2")
    text_generator.tokenizer.pad_token = text_generator.tokenizer.eos_token
    return text_generator

SYSTEM_INSTRUCTION = (
    "You are a helpful assistant for software engineer. "
    "You will answer precisely and concisely. "
    "Use markdown to format your answers. "
    "Use emojis to make your responses more engaging. "
    "Use code blocks to format your answers."

)
# Build the convo prompt
def build_conversation_prompt(chat_history, user_question):
    formated_conversation = []
    for previous_question, previous_answer in chat_history:
        formated_conversation.append(f"User: {previous_question}\nAssistant: {previous_answer}")

    formated_conversation.append(f"User: {user_question}\nAssistant:")   
    return SYSTEM_INSTRUCTION + "\n".join(formated_conversation)

st.title("LenaChatbot UI🤖")
st.caption("Ask me anything about software engineering!")

# Sidebar for config
with st.sidebar:
    st.header("Model Controls/Config")
    max_new_tokens = st.slider("Max New Tokens", min_value=10, max_value=100, value=50, step=10)
    temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=0.5, step=0.1)

    if st.button("clear chat history"):
        st.session_state['chat_history'] = []
        st.success("Chat history cleared!")

# Initialize chat history
if 'chat_history' not in st.session_state:
     st.session_state.chat_history = []
    
#  Dispaly chat history
for user_message, ai_reply in st.session_state.get('chat_history', []):
    st.chat_message("user").markdown(user_message)                  
    st.chat_message("assistant").markdown(ai_reply)

# User input
user_input = st.chat_input("Ask Lena anything about software engineering!")
if user_input:
    st.chat_message("user").markdown(user_input)

    with st.spinner("Thinking..."):
        text_generator = load_generator()
        prompt = build_conversation_prompt(st.session_state.get('chat_history', []), user_input)

    generation_output = text_generator(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        pad_token_id=text_generator.tokenizer.eos_token_id,
        eos_token_id=text_generator.tokenizer.eos_token_id
)[0]['generated_text']


    # Extracting the model's answer from the generated text
    if "Assistant:" in generation_output:
            generated_answer = generation_output.split("Assistant:")[-1].strip()
    else:
            generated_answer = generation_output.strip()

    # ✅ Move these inside the block
    st.chat_message("assistant").markdown(generated_answer)
    st.session_state.setdefault('chat_history', []).append((user_input, generated_answer))

          # Displaying and storing chatbot response  
    st.chat_message("assistant").markdown(generated_answer)
    st.session_state.setdefault('chat_history', []).append((user_input, generated_answer))
        


