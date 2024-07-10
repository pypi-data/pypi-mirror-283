import pandas as pd
from sentence_transformers import SentenceTransformer, util
from googletrans import Translator, LANGUAGES
import re
import torch
import os

class SemanticSearch:

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
        try:
            text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
            text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
            return text.lower()
        except Exception as e:
            print(f"Normalization error: {e}")
            return text

    def __clean_text(self, text):
        try:
            pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'please', 'want', 'buy', 'to', 'the', 'dollars','Cards','cards','Card','Card']
            pronoun_pattern = r'\b(?:{})\b'.format('|'.join(pronouns))
            text = re.sub(pronoun_pattern, '', text, flags=re.IGNORECASE)
            text = re.sub(r'[^\w\s]', '', text)
            return text
        except Exception as e:
            print(f"Cleaning error: {e}")
            return text

    def __encode_products(self):
        try:
            normalized_product_names = self.products_df['product_name'].apply(self.__normalize_text).apply(self.__clean_text)
            return self.model.encode(normalized_product_names.tolist(), convert_to_tensor=True)
        except Exception as e:
            print(f"Product encoding error: {e}")
            return None

    def __save_embeddings(self, embeddings, path):
        try:
            torch.save(embeddings, path)
        except Exception as e:
            print(f"Saving embeddings error: {e}")

    def __load_embeddings(self, path):
        try:
            return torch.load(path)
        except Exception as e:
            print(f"Loading embeddings error: {e}")
            return None

    def __encode_categories(self):
        try:
            normalized_categories = self.category_df['category_Name_en'].apply(self.__normalize_text).apply(self.__clean_text)
            return self.model.encode(normalized_categories.tolist(), convert_to_tensor=True)
        except Exception as e:
            print(f"Category encoding error: {e}")
            return None

    def __translate_text(self, text, target_language='en'):
        try:
            translator = Translator()
            translation = translator.translate(text, dest=target_language)
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def get_product_ids_by_category(self, category_id):
        try:
            filtered_df = self.products_df[self.products_df['category_id'] == category_id]
            product_ids = filtered_df['product_id'].tolist()
            product_dict = {'product_ids': product_ids}
            return product_dict
        except Exception as e:
            print(f"Error getting product IDs by category: {e}")
            return {'product_ids': []}

    def semantic_search(self, query):
        try:
            query_words = query.split()

            if len(query_words) <= 2:
                query_translated = self.__translate_text(query)
                query_cleaned = self.__normalize_text(query_translated)
                query_cleaned = self.__clean_text(query_cleaned)
            
                basic_matches_categories = self.category_df[self.category_df['category_Name_en'].str.contains(query_cleaned, case=False, na=False)]
                if not basic_matches_categories.empty:
                    best_categories = basic_matches_categories[['category_id', 'category_Name_en']].head(5)
                    return {
                        'categories': best_categories.to_dict(orient='records'),
                        'method': 'basic_string_matching_categories'
                    }
                else:
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

            # If no basic matches, perform semantic search
            query_translated = self.__translate_text(query)
            query_translated = self.__clean_text(query_translated)

            # Get the semantic search embeddings and similarity scores
            query_embedding = self.model.encode(self.__normalize_text(query_translated), convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(query_embedding, self.product_embeddings)
            similarities = similarities.cpu().numpy().flatten()

            # Get top 25 matches based on similarity scores
            top_25_indices = similarities.argsort()[-25:][::-1]
            top_25_similarities = similarities[top_25_indices]

            threshold = 0.95  # Adjust threshold as needed
            top_25_results = []
            for i, idx in enumerate(top_25_indices):
                if top_25_similarities[i] >= threshold:
                    top_25_results.append({
                        'product_id': self.products_df.iloc[idx]['product_id'],
                        'product_name': self.products_df.iloc[idx]['product_name'],
                        'similarity': top_25_similarities[i]
                    })

            if top_25_results:
                # Convert the results to a DataFrame for further processing
                top_25_df = pd.DataFrame(top_25_results)

                # Apply basic string matching on the top 25 results
                query_cleaned = self.__normalize_text(query_translated)
                query_cleaned = self.__clean_text(query_cleaned)
                basic_matches_products = top_25_df[top_25_df['product_name'].str.contains(query_cleaned, case=False, na=False)]
                
                if not basic_matches_products.empty:
                    basic_matches_products = basic_matches_products.head(5)
                    return {
                        'products': basic_matches_products[['product_id', 'product_name', 'similarity']].to_dict(orient='records'),
                        'method': 'basic_string_matching_products'
                    }
                
                return {
                    'products': top_25_df[['product_id', 'product_name', 'similarity']].head(5).to_dict(orient='records'),
                    'method': 'semantic_search'
                }
            else:
                category_similarities = util.pytorch_cos_sim(query_embedding, self.category_embeddings)
                category_similarities = category_similarities.cpu().numpy().flatten()

                best_category_indices = category_similarities.argsort()[-5:][::-1]

                best_categories = self.category_df.iloc[best_category_indices][['category_id', 'category_Name_en']]
                return {
                    'categories': best_categories.to_dict(orient='records'),
                    'similarity': category_similarities[best_category_indices].tolist(),
                    'method': 'category_fallback'
                }

        except Exception as e:
            print(f"Semantic search error: {e}")
            return {'products': [], 'method': 'error', 'message': str(e)}