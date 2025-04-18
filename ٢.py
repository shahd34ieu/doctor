# Doctor Zaki - Medical Chatbot (Streamlit Version) - Lightweight Model
import streamlit as st
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import os

# إعداد التوكن الخاص بـ Hugging Face
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_your_token_here"

# نموذج الذكاء الاصطناعي (خفيف)
qa = pipeline("question-answering", model="deepset/minilm-uncased-squad2")

# وظيفة سحب المعلومات من Drugs.com
def scrape_drug_info(drug_name):
    try:
        search_url = f"https://www.drugs.com/search.php?searchterm={drug_name}"
        res = requests.get(search_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        first_link = soup.select_one(".ddc-media-title a")
        if not first_link:
            return "No information found on Drugs.com."
        drug_url = "https://www.drugs.com" + first_link["href"]
        drug_page = requests.get(drug_url)
        drug_soup = BeautifulSoup(drug_page.text, 'html.parser')
        description = drug_soup.select_one(".contentBox p")
        return description.text if description else "No description found."
    except Exception as e:
        return f"Error while scraping: {e}"

# وظيفة البوت
def ask_doctor_zaki(question, drug_name):
    context = scrape_drug_info(drug_name)
    if "No information" in context or "Error" in context:
        return context
    result = qa(question=question, context=context)
    return result['answer']

# واجهة Streamlit
st.set_page_config(page_title="Doctor Zaki - Medical Assistant", page_icon="🧠", layout="centered")

st.title("🤓 Doctor Zaki - Medical Chatbot")
st.write("اسأل عن أي دواء وسيقوم الدكتور زكي بالبحث لك مباشرة من موقع Drugs.com")

drug = st.text_input("اسم الدواء:")
question = st.text_input("سؤالك الطبي (بالإنجليزية):")

if st.button("اسأل دكتور زكي"):
    if drug and question:
        with st.spinner("جارٍ البحث..."):
            answer = ask_doctor_zaki(question, drug)
            st.success("الإجابة:")
            st.write(answer)
    else:
        st.warning("رجاءً أدخل اسم الدواء والسؤال.")
