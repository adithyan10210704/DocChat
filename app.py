import streamlit as st
import fitz  # PyMuPDF
import docx
import ollama

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def query_llm(prompt, context):
    full_prompt = f"Answer based on the following document:\n\n{context}\n\nUser: {prompt}\n\nAnswer:"
    response = ollama.chat(model='llama3', messages=[{"role": "user", "content": full_prompt}])
    return response['message']['content']

st.set_page_config(page_title="DocChat 💬📄", layout="wide")

st.title("📄 DocChat: Chat with your document using LLM")
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        content = extract_text_from_pdf(uploaded_file)
    else:
        content = extract_text_from_docx(uploaded_file)

    st.success("Document uploaded and processed!")
    
    user_query = st.text_input("Ask a question about the document:")
    
    if st.button("Get Answer") and user_query:
        with st.spinner("Thinking..."):
            answer = query_llm(user_query, content)
        st.markdown(f"**Answer:** {answer}")
