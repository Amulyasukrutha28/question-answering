# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1o8J5e1zX8D_0HIGVrTNQv4vWxC9KEv3N
"""

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

pip install pymupdf

import nltk
nltk.download('punkt')

def chunk_text(text, chunk_size=100):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(nltk.word_tokenize(sentence))
        if current_length + sentence_length > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

pip install sentence-transformers

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def embed_chunks(chunks):
    embeddings = model.encode(chunks, convert_to_tensor=False)
    return embeddings

from sklearn.mixture import GaussianMixture

def cluster_embed(embeddings, cluster_n):
    gmm=GausianMixture(n_components=cluster_n, covariance_type='full')
    gmm.fit(embeddings)
    return gmm

from transformers import pipeline

summarizer=pipeline("summarization", model="facebook/bart-large-cnn")

def summarizing_text(text):
    summary=summarizer(text, max_length=100, min_length=25, do_samples=False)
    return summary[0]['summary_text']

pip install faiss-cpu

#Storing database
import faiss
import numpy as np

def store_embed(embeddings):
    dimension=embeddings.shape[1]
    index=faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index

#Retrieval Techniques
#Query Expansion
nltk.download('wordnet')
from nltk.corpus import wordnet

def expand_query(query):
    synonyms=set()
    for word in query.split():
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
    return " ".join(synonyms)

pip install rank-bm25

from rank_bm25 import BM25Okapi

def bm25_retrieve(corpus, query):
    tokenized_corpus = [doc.split() for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    return scores

pip install rank-bm25

def dense_retrieve_for_all_chunks(index, query_embedding):
    if query_embedding.ndim == 1:
        query_embedding = np.expand_dims(query_embedding, axis=0)
    D, I = index.search(query_embedding, k=index.ntotal)
    dense_scores = D.flatten()
    return dense_scores

def combine_scores(bm25_scores, dense_scores, weight_bm25=0.5, weight_dense=0.5):
    combined_scores = weight_bm25 * np.array(bm25_scores) + weight_dense * np.array(dense_scores)
    return combined_scores



from transformers import pipeline

qa_pipeline = pipeline("question-answering")

def answer_question(question, context):
    result = qa_pipeline(question=question, context=context)
    return result['answer']

# Main workflow
text1 = extract_text_from_pdf('/content/algorithms.pdf')
text2 = extract_text_from_pdf('/content/assetization.pdf')
text3 = extract_text_from_pdf('/content/the_future.pdf')

chunks1 = chunk_text(text1)
chunks2 = chunk_text(text2)
chunks3 = chunk_text(text3)

embeddings1 = embed_chunks(chunks1)
embeddings2 = embed_chunks(chunks2)
embeddings3 = embed_chunks(chunks3)

index = store_embed(np.vstack([embeddings1, embeddings2, embeddings3]))

query = "network protocols"
expanded_query = expand_query(query)

corpus = chunks1 + chunks2 + chunks3
bm25_scores = bm25_retrieve(corpus, expanded_query)

query_embedding = embed_chunks([expanded_query])[0].reshape(1, -1)
dense_scores = dense_retrieve_for_all_chunks(index, query_embedding)

combined_scores = combine_scores(bm25_scores, dense_scores)

top_indices = combined_scores.argsort()[-5:][::-1]
top_chunks = [corpus[i] for i in top_indices]

question = "What are the key features of network protocols?"
context = " ".join(top_chunks)
answer = answer_question(question, context)

print("Answer:", answer)

# Streamlit UI

