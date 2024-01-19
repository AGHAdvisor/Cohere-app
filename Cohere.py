import streamlit as st
import requests
import cohere
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

# Cohere API key
cohere_api_key = 'IIBK826Z2lH3HLRzLBy60pLzi3G5gMQ2ONN7su4W'
co = cohere.Client(cohere_api_key)

# Functions for Cohere Summarization
def generate_cohere_summary(text):
    response = co.summarize(
        text=text,
        length='auto',
        format='auto',
        model='summarize-xlarge',
        additional_command='Give it as a paragraph',
        temperature=0.3,
    )
    summary = response.summary
    return summary

def generate_cohere_points(text):
    response1 = co.summarize(
        text=text,
        length='auto',
        format='auto',
        model='summarize-xlarge',
        additional_command='give 5 bullet points giving key highlights in 8 words each',
        temperature=0.3,
    )
    summary1 = response1.summary
    summary1_html = summary1.replace('\n', '<br>')
    return summary1_html

# Function to scrape PDF text
def scrape_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    text = page.extract_text()
    return text

# Function to scrape links from URL
def scrape_links(url):
    details = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    if paragraphs:
        main_text = '\n'.join([paragraph.get_text(strip=True) for paragraph in paragraphs])
        details['main_text'] = main_text
    return details

# Streamlit App
st.title('Cohere Summary and Pointers')

# User input for choice
choice = st.radio("Choose an option:", ('URL Link', 'PDF Upload', 'Text Paste'))

if choice == 'URL Link':
    website_url = st.text_input("Enter the URL:")
    if st.button("Generate Summary"):
        details = scrape_links(website_url)
        text = details.get('main_text', '')
        st.write("Text from URL:\n", text)
        cohere_summary = generate_cohere_summary(text)
        cohere_points = generate_cohere_points(text)
        st.write("Summary:\n", cohere_summary)
        st.write("Pointers:\n", cohere_points)

elif choice == 'PDF Upload':
    uploaded_file = st.file_uploader("Upload a PDF File", type=["pdf"])
    if uploaded_file is not None:
        if st.button("Generate Summary"):
            pdf_text = scrape_pdf(uploaded_file)
            st.write("PDF Text:\n", pdf_text)
            cohere_summary = generate_cohere_summary(pdf_text)
            cohere_points = generate_cohere_points(pdf_text)
            st.write("Summary:\n", cohere_summary)
            st.write("Pointers:\n", cohere_points)

elif choice == 'Text Paste':
    text_input = st.text_area("Enter your Text:")
    if st.button("Generate Summary"):
        st.write(text_input)
        cohere_summary = generate_cohere_summary(text_input)
        cohere_points = generate_cohere_points(text_input)
        st.write("Summary:\n", cohere_summary)
        st.write("Pointers:\n", cohere_points)

# Add a separator
st.markdown("---")

# Resultant box in white
st.title("Resultant Box")
# Display any additional information or results here
