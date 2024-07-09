# smart_search/semantic_search.py

import pandas as pd
from sentence_transformers import SentenceTransformer, util
from googletrans import Translator
import re
import torch 
import os

class SemanticSearch:
    def __init__(self, products_df, product_embeddings_path='savedproduct_embeddings.pt', category_embeddings_path='savedcategory_embeddings.pt'):
        self.model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        self.model = SentenceTransformer(self.model_name)
        self.products_df = products_df.dropna()
        self.category_df = products_df[['category_Name_en', 'category_id']]

        self.product_embeddings_path = product_embeddings_path
        self.category_embeddings_path = category_embeddings_path

        if os.path.exists(self.product_embeddings_path) and os.path.exists(self.category_embeddings_path):
            self.product_embeddings = self.__load_embeddings(self.product_embeddings_path)
            self.category_embeddings = self.__load_embeddings(self.category_embeddings_path)
        else:
            self.product_embeddings = self.__encode_products()
            self.category_embeddings = self.__encode_categories()
            self.__save_embeddings(self.product_embeddings, self.product_embeddings_path)
            self.__save_embeddings(self.category_embeddings, self.category_embeddings_path)

    def __normalize_text(self, text):
        # Normalize the text by removing special characters and converting to lowercase
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
        return text.lower()

    def __clean_text(self, text):
        # Remove pronouns (replace with an empty string)
        pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'please', 'want', 'buy', 'to']
        pronoun_pattern = r'\b(?:{})\b'.format('|'.join(pronouns))
        text = re.sub(pronoun_pattern, '', text, flags=re.IGNORECASE)
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def __encode_products(self):
        # Encode product names
        normalized_product_names = self.products_df['product_name'].apply(self.__normalize_text)
        return self.model.encode(normalized_product_names.tolist(), convert_to_tensor=True)

    def __save_embeddings(self, embeddings, path):
        torch.save(embeddings, path)

    def __load_embeddings(self, path):
        return torch.load(path)

    def __encode_categories(self):
        # Encode category names
        normalized_categories = self.category_df['category_Name_en'].apply(self.__normalize_text)
        return self.model.encode(normalized_categories.tolist(), convert_to_tensor=True)

    def __translate_text(self, text, target_language='en'):
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text

    def get_product_ids_by_category(self, category_id):
        # Filter the DataFrame by the given category_id
        filtered_df = self.products_df[self.products_df['category_id'] == category_id]
        
        # Extract the product IDs
        product_ids = filtered_df['product_id'].tolist()
        
        # Create a dictionary with product IDs
        product_dict = {'product_ids': product_ids}
        
        return product_dict

    def semantic_search(self, query):
        # Normalize and translate the query
        query_translated = self.__translate_text(query)
        query_translated = self.__clean_text(query_translated)
        print(f"Translated query: {query_translated}")

        # Encode query
        query_embedding = self.model.encode(self.__normalize_text(query_translated), convert_to_tensor=True)

        # Calculate cosine similarity between query and precomputed product embeddings
        similarities = util.pytorch_cos_sim(query_embedding, self.product_embeddings)
        similarities = similarities.cpu().numpy().flatten()  # Convert to numpy array

        print(f"Similarity scores: {similarities}")

        # Find the index of the highest similarity score
        best_match_index = similarities.argmax()

        print(f"Best match index: {best_match_index}")
        print(f"Best match similarity score: {similarities[best_match_index]}")

        # Return the ID of the best matching product if similarity score is above threshold
        threshold = 0.93  # Adjust threshold as needed based on observed scores
        if similarities[best_match_index] >= threshold:
            return {
                'product_id': self.products_df.loc[best_match_index, 'product_id'],
                'similarity': similarities[best_match_index]
            }
        else:
            # If similarity is below threshold, fallback to category similarity
            category_similarities = util.pytorch_cos_sim(query_embedding, self.category_embeddings)
            category_similarities = category_similarities.cpu().numpy().flatten()  # Convert to numpy array

            print(f"Category similarity scores: {category_similarities}")

            # Find the indices of the highest category similarity scores
            best_category_indices = category_similarities.argsort()[-5:][::-1]  # Top 5 categories

            print(f"Best category indices: {best_category_indices}")
            print(f"Best category similarity scores: {category_similarities[best_category_indices]}")

            best_categories = self.category_df.loc[best_category_indices, ['category_id', 'category_Name_en']]
            return {
                'categories': best_categories.to_dict(orient='records'),
                'similarity': category_similarities[best_category_indices].tolist()
            }
