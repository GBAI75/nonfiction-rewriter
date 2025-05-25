import streamlit as st
import openai
import pandas as pd

# Set page config
st.set_page_config(page_title="Non-Fiction Rewriter", layout="centered")

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📘 Non-Fiction Paragraph Rewriter")

# Session state to store saved paragraphs
if "entries" not in st.session_state:
    st.session_state.entries = []

# Input text box
input_text = st.text_area("Write your messy draft here", height=200)

# Rewrite logic
if st.button("✍️ Rewrite into polished paragraph"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Rewriting..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You rewrite messy, half-finished notes into clean, structured non-fiction prose. Expand on ideas and improve clarity."},
                    {"role": "user", "content": input_text}
                ],
                temperature=0.7
            )
            rewritten = response['choices'][0]['message']['content']
            st.session_state.latest = rewritten
            st.success("Here's your rewritten paragraph:")
            st.write(rewritten)

# Save title, keywords
if "latest" in st.session_state:
    with st.form("save_form"):
        title = st.text_input("Give this paragraph a title")
        keywords = st.text_input("Add some keywords (comma-separated)")
        submitted = st.form_submit_button("💾 Save this paragraph")
        if submitted:
            st.session_state.entries.append({
                "title": title,
                "keywords": keywords,
                "paragraph": st.session_state.latest
            })
            st.success("Saved! You can add more or download all below.")
            del st.session_state.latest

# Display saved entries
if st.session_state.entries:
    st.subheader("📚 Saved Paragraphs")
    for i, entry in enumerate(st.session_state.entries):
        st.markdown(f"**{i+1}. {entry['title']}**  \n*Keywords:* {entry['keywords']}  \n\n{entry['paragraph']}")

    # Download button
    df = pd.DataFrame(st.session_state.entries)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download All as CSV", data=csv, file_name="rewritten_paragraphs.csv", mime="text/csv")
