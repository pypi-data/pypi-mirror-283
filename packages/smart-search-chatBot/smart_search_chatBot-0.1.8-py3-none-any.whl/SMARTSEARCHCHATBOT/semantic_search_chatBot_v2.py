import pandas as pd
from sentence_transformers import SentenceTransformer, util
from googletrans import Translator
import re
import torch
import os

class SemanticSearch_v2:
    def __init__(self, products_df, product_embeddings_path='savedproduct_embeddings.pt', category_embeddings_path='savedcategory_embeddings.pt'):
        self.model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        self.model = SentenceTransformer(self.model_name)
        self.products_df = products_df.dropna().drop_duplicates(subset=['product_name'])
        self.category_df = products_df[['category_Name_en', 'category_id']].drop_duplicates()

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
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
        return text.lower()

    def __clean_text(self, text):
        pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'please', 'want', 'buy', 'to','the','dollars']
        pronoun_pattern = r'\b(?:{})\b'.format('|'.join(pronouns))
        text = re.sub(pronoun_pattern, '', text, flags=re.IGNORECASE)
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def __encode_products(self):
        normalized_product_names = self.products_df['product_name'].apply(self.__normalize_text).apply(self.__clean_text)
        return self.model.encode(normalized_product_names.tolist(), convert_to_tensor=True)

    def __save_embeddings(self, embeddings, path):
        torch.save(embeddings, path)

    def __load_embeddings(self, path):
        return torch.load(path)

    def __encode_categories(self):
        normalized_categories = self.category_df['category_Name_en'].apply(self.__normalize_text).apply(self.__clean_text)
        return self.model.encode(normalized_categories.tolist(), convert_to_tensor=True)

    def __translate_text(self, text, target_language='en'):
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text

    def get_product_ids_by_category(self, category_id):
        filtered_df = self.products_df[self.products_df['category_id'] == category_id]
        product_ids = filtered_df['product_id'].tolist()
        product_dict = {'product_ids': product_ids}
        return product_dict

    def semantic_search(self, query):
        # Check the length of the query
        query_words = query.split()
        if len(query_words) < 2:
            # Perform category search if the query is less than 2 words
            query_translated = self.__translate_text(query)
            query_translated = self.__clean_text(query_translated)
            query_embedding = self.model.encode(self.__normalize_text(query_translated), convert_to_tensor=True)
            category_similarities = util.pytorch_cos_sim(query_embedding, self.category_embeddings)
            category_similarities = category_similarities.cpu().numpy().flatten()
            best_category_indices = category_similarities.argsort()[-3:][::-1]
            best_categories = self.category_df.iloc[best_category_indices][['category_id', 'category_Name_en']]
            return {
                'categories': best_categories.to_dict(orient='records'),
                'similarity': category_similarities[best_category_indices].tolist(),
                'method': 'category_fallback'
            }

        # Basic string matching
        query_translated = self.__translate_text(query)
        query_cleaned = self.__normalize_text(query_translated)
        query_cleaned = self.__clean_text(query)

        basic_matches = self.products_df[self.products_df['product_name'].str.contains(query_cleaned, case=False, na=False)]

        if not basic_matches.empty:
            basic_matches = basic_matches.head(5)
            return {
                'products': basic_matches[['product_id', 'product_name']].to_dict(orient='records'),
                'method': 'basic_string_matching'
            }

        # If no basic matches, perform semantic search
        query_translated = self.__translate_text(query)
        query_translated = self.__clean_text(query_translated)
        print(f"Translated query: {query_translated}")

        query_embedding = self.model.encode(self.__normalize_text(query_translated), convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, self.product_embeddings)
        similarities = similarities.cpu().numpy().flatten()

        print(f"Similarity scores: {similarities}")

        top_5_indices = similarities.argsort()[-5:][::-1]
        top_5_similarities = similarities[top_5_indices]

        print(f"Top 5 match indices: {top_5_indices}")
        print(f"Top 5 similarity scores: {top_5_similarities}")

        threshold = 0.95  # Adjust threshold as needed
        top_5_results = []
        for i, idx in enumerate(top_5_indices):
            if top_5_similarities[i] >= threshold:
                top_5_results.append({
                    'product_id': self.products_df.iloc[idx]['product_id'],
                    'product_name': self.products_df.iloc[idx]['product_name'],
                    'similarity': top_5_similarities[i]
                })

        if top_5_results:
            return {
                'products': top_5_results,
                'method': 'semantic_search'
            }
        else:
            category_similarities = util.pytorch_cos_sim(query_embedding, self.category_embeddings)
            category_similarities = category_similarities.cpu().numpy().flatten()

            #print(f"Category similarity scores: {category_similarities}")

            best_category_indices = category_similarities.argsort()[-5:][::-1]

            print(f"Best category indices: {best_category_indices}")
            print(f"Best category similarity scores: {category_similarities[best_category_indices]}")

            best_categories = self.category_df.iloc[best_category_indices][['category_id', 'category_Name_en']]
            return {
                'categories': best_categories.to_dict(orient='records'),
                'similarity': category_similarities[best_category_indices].tolist(),
                'method': 'category_fallback'
            }

