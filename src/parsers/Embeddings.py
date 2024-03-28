import os

import numpy as np
from transformers import AutoTokenizer, AutoModel
from langchain_openai import OpenAIEmbeddings

class Embeddings:
    def __init__(self, embedding_model_str: str):
        self.embedding_model_str = embedding_model_str

        # API Embedding Models
        self.openai_str = "openai"

        # Local Models
        # Hugging Face models
        self.distilbert_base_uncased = "distilbert-base-uncased"
        self.roberta_base = "roberta-base"
        self.bert_base_uncased = "bert-base-uncased"
        self.hugging_face_models = [self.distilbert_base_uncased, 
                               self.roberta_base, 
                               self.bert_base_uncased]

    ########## Hugging Face Wrapper ##########
    def initialize_hugging_face_model(self, embedding_model_str: str):
        tokenizer = AutoTokenizer.from_pretrained(embedding_model_str)
        model = AutoModel.from_pretrained(embedding_model_str)
        return tokenizer, model
    
    def calculate_hugging_face_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.last_hidden_state
    
    ########## OpenAI Wrapper ##########
    def initialize_openai_model(self):
        try: 
            self.model = OpenAIEmbeddings()
        except Exception as e:
            raise Exception("Please provide an OpenAI API key.")

    def calculate_openai_embedding(self, text):
        return self.model.embed_documents([text])[0]
    
    ########## Main Functions ##########
    def initialize_embedding_model(self):
        if self.embedding_model_str == "openai":
            return True
        elif self.embedding_model_str in self.hugging_face_models:
            self.tokenizer, self.model = self.initialize_hugging_face_model(self.embedding_model_str)

    def calculate_embedding(self, text):
        if self.embedding_model_str == self.openai_str:
            return self.calculate_openai_embedding(text)
        elif self.embedding_model_str in self.hugging_face_models:
            return self.calculate_hugging_face_embedding(text)
    
    def initialize_model_calculate_embedding(self, text):
        self.initialize_embedding_model(self.embedding_model_str)
        return self.calculate_embedding(text)