import os
import streamlit as st
import openai

st.title("Interview Preparation Bot 🎯")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found! Please set it in Streamlit Secrets.")
    st.stop()

openai.api_key = openai_api_key

role = st.selectbox("Select your target role:", ["Software Engineer", "Product Manager", "Data Analyst"])
mode = st.selectbox("Select interview mode:", ["Technical Interview", "Behavioral Interview"])

if st.button("Start Interview"):
    if mode == "Technical Interview":
        prompt = f"Ask me a technical interview question for the role of {role}."
    else:
        prompt = f"Ask me a behavioral interview question for the role of {role}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert interviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    question = response['choices'][0]['message']['content']
    st.write("**Interview Question:**")
    st.info(question)

    answer = st.text_area("Your Answer:", height=200)

    if st.button("Submit Answer"):
        feedback_prompt = f"Evaluate this answer for the interview question in terms of clarity, correctness, and examples. Provide feedback and a score out of 10.\\n\\nAnswer: {answer}"
        
        feedback_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert interviewer."},
                {"role": "user", "content": feedback_prompt}
            ]
        )

        feedback = feedback_response['choices'][0]['message']['content']
        st.success("Feedback:")
        st.write(feedback)
