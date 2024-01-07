import streamlit as st
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader

load_dotenv()

st.set_page_config(page_title="Find Similar Words App", page_icon=":robot:")
st.header("Hey, Ask me something and I will give out similar things")

# Initialize the SentenceTransformer Model
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')

loader = CSVLoader(file_path="myData.csv", csv_args={
    'delimiter': ',',
    'quotechar': '"',
    'fieldnames': ['Words']
})

# Assigning the data inside the csv to our variable here
data = loader.load()

# Assuming your CSV file has a field named 'Words'
data_list = [word.page_content[6:] for word in data]

# Encode the data using the SentenceTransformer model
embeddings = model.encode(data_list)


# Function to receive input from the user and store it in a variable
def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text

user_input = get_text()
submit = st.button("Find Similar Things")

if submit:
    # Compute cosine similarities using scikit-learn
    user_input_embedding = model.encode([user_input])
    similarities = cosine_similarity(user_input_embedding, embeddings)

    # Get indices of top matches
    top_matches_indices = similarities.argsort()[0][::-1]

    # Display the top matches
    st.subheader("Top Matches:")
    for idx in top_matches_indices[:2]:  # Display top 2 matches
        st.text(data[idx].page_content[6:])