import streamlit as st
import google.generativeai as genai

st.title("👨‍🏫 Python tutor")
st.subheader(f"What Do You Want :blue[Know?]")

# Capture Gemini API key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Initialize the Gemini Model
if gemini_api_key: 
    try: 
        # Configure Gemini with the provided API Key 
        genai.configure(api_key=gemini_api_key) 
        model = genai.GenerativeModel("gemini-pro") 
        st.success("Gemini API Key successfully configured.") 
    except Exception as e: 
        st.error(f"An error occurred while setting up the Gemini model: {e}") 

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
        st.session_state.chat_history = [] # Initialize with an emthy list

if "prompt_chain" not in st.session_state:
    st.session_state.prompt_chain = "Tell you what I can help you about Python coding. After you response, I’ll help you about what Python topic. I’d like to learn, such as loops, functions, data structures, or debugging. Based on your needs, I’ll explain the concepts and definitions about any topics clearly, provide code examples, and guide you step by step."
 
# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history:
      with st.chat_message("role", avatar="👨‍🏫" if role == "assistant" else "🧐"):
            st.markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."):
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

      # Append the new question to the prompt chain
    st.session_state.prompt_chain += f"\nCustomer: {user_input}"
   
    # Combine the predefined prompt chain with the current user input
    full_input = st.session_state.prompt_chain

     # Use Gemini AI to generate a bot response
    if model: 
        try: 
            if not st.session_state.chat_history:  # Check if chat history is empty
                introduction = "Hello! As your Python coding tutor, I'm here to help you learn about Python coding. I can help you with loops, functions, data structures, or debugging. What would you like to learn about today? Let me know and I'll help you out!"
                bot_response = introduction
            else:
                response = model.generate_content(full_input) 
                bot_response = response.text

            # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response)) 
            st.chat_message("assistant").markdown(bot_response) 
        except Exception as e: 
            st.error(f"An error occurred while generating the response: {e}")
