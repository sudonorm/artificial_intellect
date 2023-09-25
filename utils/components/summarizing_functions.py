# Packages
import openai
import fitz  # PyMuPDF
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import pickle 
import os

# Set up the OpenAI API key
openai.api_key = "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"

# Functions
class model_training:
    def __init__(self ,paper:list, summary:list):
        self.papers = paper
        self.summaries = summary

    def train_model(self):
        """This function takes as input a list of medical research papers and their corresponding summaries, 
        and trains a machine learning model to predict the importance of each sentence in the papers and summaries. 
        The function tokenizes the papers and summaries into sentences, removes stop words and punctuation, computes the TF-IDF matrix for the sentences, 
        and trains a linear regression model to predict the importance of each sentence.

        Args:
            papers (_type_): lists of strings.
            summaries (_type_): lists of strings.

        Returns:
            _type_: trained model and TF-IDF vectorizer is a text vectorizer that transforms the text into a 
            usable vector by computing the Term Frequency-Inverse Document Frequency (TF-IDF) matrix for the sentences, 
            which is a weight assigned to each word in a document based on its term frequency (TF) and the inverse document frequency (IDF).
        """
        # Tokenize the papers and summaries into sentences
        sentences = []

        for paper, summary in zip(self.papers, self.summaries):
            paper_sentences = sent_tokenize(paper)
            summary_sentences = sent_tokenize(summary)
            sentences.extend(paper_sentences)
            sentences.extend(summary_sentences)

        # Remove stop words and punctuation
        stop_words = set(stopwords.words('english'))
        sentences = [' '.join([word for word in word_tokenize(sentence.lower()) if word.isalnum() and word not in stop_words]) for sentence in sentences]

        # Compute the TF-IDF matrix for the sentences
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sentences)

        # Train a linear regression model to predict the importance of each sentence
        y = [i for i in range(len(sentences))]
        model = LinearRegression()
        model.fit(X, y)
        # Save model and vectorizer to disk
        with open('./utils/components/model.pkl', 'wb') as f:
            pickle.dump(model, f)
        with open('./utils/components/vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
        return model, vectorizer


class summary_maker:
    def __init__(self, paper:list, summary:list, text, prompt_input):
        self.papers = paper
        self.summaries = summary
        self.model_trainer = model_training(paper, summary)
        self.model, self.vectorizer = self.model_trainer.train_model()
        self.text = text
        self.prompt_input = prompt_input

        # Check if model and vectorizer exist in disk
        if os.path.exists('./utils/components/model.pkl') and os.path.exists('./utils/components/vectorizer.pkl'):
            print("Opening Saved Models....")
            with open('./utils/components/model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('./utils/components/vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)
        else:
            print("Modelling.....")
            self.model_trainer = model_training(paper, summary)
            self.model, self.vectorizer = self.model_trainer.train_model()
            # Save model and vectorizer to disk
            with open('./utils/components/model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            with open('./utils/components/vectorizer.pkl', 'wb') as f:
                pickle.dump(self.vectorizer, f)
        
    def generate_summary(self,llm_type:str = "gpt-3.5-turbo",n:int = 200):
        """Firstly, This function takes as input a trained machine learning model, a TF-IDF vectorizer, a new medical research paper, and the desired number of sentences in the summary. 
        The function tokenizes the text into sentences, removes stop words and punctuation, computes the TF-IDF matrix for the sentences, ranks the sentences based on their predicted importance, 
        and selects the top N sentences to form the summary.
        Secondly, This function takes as input a prompt and a machine learning model, and uses the OpenAI API to generate a summary of the text. 
        The prompt includes the new medical research paper and the previous summaries as context for the model.

        Args:
            n (str):  argument should be an integer representing the desired number of sentences in the summary. 
            LLM type (output): model to ask prompt to

        Returns:
            _type_: new summary
        """
        sentences = sent_tokenize(self.text)
        
        # Remove stop words and punctuation
        stop_words = set(stopwords.words('english'))
        sentences = [' '.join([word for word in word_tokenize(sentence.lower()) if word.isalnum() and word not in stop_words]) for sentence in sentences]
        
        # Compute the TF-IDF matrix for the sentences
        X = self.vectorizer.transform(sentences)
        
        # Rank the sentences based on their predicted importance and select the top N sentences to form the summary
        scores = self.model.predict(X)
        top_n = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:n]
        summary = [sentences[i] for i in top_n]
        #print(summary)
        text_input = ' '.join(summary)

        prompt = f"{self.prompt_input} {text_input}"

        # Generate a summary using the ChatGPT API
        response = openai.ChatCompletion.create(
            model=llm_type,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1050,
            n=1,
            stop=None,
            temperature=0.5,
        )
        #summary = response.choices[0].text.strip()
        summary = response['choices'][0]['message']['content']
        return summary
