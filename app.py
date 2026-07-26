import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-3.5-flash")

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="centered"
)
with st.sidebar:
    st.title("📧 AI Email Generator")

    st.markdown("---")

    st.markdown("""
### Features
- ✉️ Generate Professional Emails
- 🎯 Multiple Email Types
- 🎨 Tone Selection
- 📄 Adjustable Email Length
   """ )

    st.info(
    "This application uses a Large Language Model (LLM) to generate professional emails based on user inputs.")
    st.markdown("---")
    st.markdown("""
    Developed by **Hardik Chaturvedi**

""")

st.title("📧 AI EMAIL GENERATOR")
st.markdown("""
Generate professional, well-structured, and context-aware emails using an advanced Large Language Model (LLM).

Simply enter the required details, choose the email type, tone, and length, and let AI generate a polished email ready to send.
""")

st.divider()

email_type = st.selectbox(
    "Email Type",
    [
        "Formal",
        "Leave Application",
        "Complaint",
        "Apology",
        "Thank You",
        "Job Application"
    ]
)

recipient = st.text_input("Recipient Email")
subject = st.text_input("Subject")
sender_name = st.text_input("Sender Name")

email_length = st.selectbox(
    "Email Length",
    ["Short", "Medium", "Detailed"]
)

details = st.text_area("Additional Details", height=150)

tone = st.radio(
    "Select Tone",
    ["Professional", "Formal", "Informal"],
    horizontal=True
)

generate = st.button("✨ Generate Email", use_container_width=True)

if generate:

    if not recipient or not subject or not sender_name or not details:
        st.warning("Please fill all the fields.")

    else:

        if email_length == "Short":
            length_instruction = "Write a concise email of approximately 100-150 words."
        elif email_length == "Medium":
            length_instruction = "Write a well-structured email of approximately 180-250 words."
        else:
            length_instruction = "Write a detailed and professional email of approximately 300-450 words."

        prompt = f"""
Generate a complete {tone} {email_type} email using the information provided below.

Email Details:
- Recipient: {recipient}
- Subject: {subject}
- Sender Name: {sender_name}
- Tone: {tone}
- Email Length: {email_length}

Additional Information:
{details}

Instructions:
{length_instruction}

1. Write a complete and well-structured email.
2. Begin with an appropriate greeting.
3. Clearly explain the purpose of the email.
4. Expand the provided information naturally where appropriate.
5. Use professional, natural and grammatically correct English.
6. Organize the email into multiple paragraphs.
7. Maintain the selected tone throughout the email.
8. End the email with a professional closing.
9. Sign the email using:
{sender_name}
10. Return only the final email.
"""

        try:
            with st.spinner("Generating Email..."):
                response = model.generate_content(prompt)

            st.success("✅ Email generated successfully!")

            st.subheader("📧 Generated Email")

            st.text_area(
                "Email",
                value=response.text,
                height=350
            )

            st.download_button(
                label="📥 Download Email",
                data=response.text,
                file_name="generated_email.txt",
                mime="text/plain"
            )

            word_count = len(response.text.split())
            st.caption(f"📄 Word Count: {word_count}")

        except Exception as e:
            st.error(f"Error generating email: {e}")

st.divider()

st.caption(
    "© 2026 AI Email Generator | Developed by Hardik Chaturvedi | Powered by Google Gemini"
)