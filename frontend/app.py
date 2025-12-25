import streamlit as st
import requests

st.set_page_config(page_title="AI Email Polisher", page_icon="✉️", layout="centered")

BACKEND_URL = "http://127.0.0.1:8000/rewrite"


st.title("✉️ AI-Powered Email Polisher")
st.write("Convert harsh or informal emails into calm, polite and professional ones — instantly.")


# ---------------------------
# SAMPLE TEST CASES
# ---------------------------

st.subheader("📌 Try a Sample Email")

samples = {
    "🔥 Harsh — Threatening":
        "Fix this issue immediately or I will cancel my account.",
    "⚠️ Harsh — Complaint":
        "Fix this problem now or I will file a complaint.",
    "😡 Harsh — Blaming":
        "This delay is unacceptable. Do your job properly.",
    "😤 Passive Aggressive":
        "I guess you're too busy to reply to me.",
    "📞 Too Direct":
        "Call me now.",
    "🙂 Neutral Request":
        "Please send me the updated report when you have time.",
    "😊 Positive Professional":
        "Thank you for your support. Could you please share the project updates?",
}

option = st.selectbox("Select a sample email:", list(samples.keys()))
if st.button("Use this sample"):
    st.session_state["email_text"] = samples[option]


# ---------------------------
# INPUT BOX
# ---------------------------

email_input = st.text_area(
    "Write / paste your email below:",
    key="email_text",
    height=180,
    placeholder="Type something like — Fix this issue immediately or I will cancel my account."
)


# ---------------------------
# PROCESS BUTTON
# ---------------------------

if st.button("✨ Polish Email"):
    if not email_input.strip():
        st.warning("Please enter an email 🙂")
    else:
        try:
            with st.spinner("Rewriting politely…"):
                response = requests.post(
                    BACKEND_URL,
                    json={"email": email_input}
                )

            if response.status_code == 200:
                data = response.json()
                polished = data.get("rewritten_email", "")
                analytics = data.get("analysis")

                st.subheader("🎯 Polished Email")
                st.success(polished)

                # ---------------------------
                # TONE ANALYSIS
                # ---------------------------

                st.subheader("📊 Tone Analysis")

                if analytics:
                    col1, col2 = st.columns(2)

                    col1.metric("😡 Rudeness Level", f"{analytics['rude_percent']}%")
                    col2.metric(
                        "💬 Sentiment",
                        analytics["sentiment"],
                        f"{analytics['sentiment_confidence']}%"
                    )

                else:
                    st.info("Tone analysis unavailable — backend did not return analytics.")

            else:
                st.error(f"Backend error: {response.text}")

        except Exception as e:
            st.error(f"Backend connection failed.\n\n{e}")


# ---------------------------
# FOOTER
# ---------------------------

st.markdown("---")
st.caption("Built with ❤️ for safer and more respectful communication.")
