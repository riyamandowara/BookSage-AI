from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import pickle
import os
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load models and data
def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")

    models = {}
    files = {
        'cf_model': 'cf_model.pkl',
        'book_pivot': 'book_pivot.pkl',
        'tfidf': 'tfidf_vectorizer.pkl',
        'content_sim_matrix': 'content_sim_matrix.pkl',
        'title_to_idx': 'title_to_idx.pkl',
        'books_content': 'books_content.pkl',
        'final_rating': 'final_rating.pkl',
        'books': 'books_data.pkl'
    }

    for key, filename in files.items():
        file_path = os.path.join(models_dir, filename)
        with open(file_path, 'rb') as f:
            models[key] = pickle.load(f)

    return models

models = load_models()

# Recommendation functions
def collaborative_recommendations(book_title, top_n=9):
    """Generate collaborative filtering recommendations"""
    try:
        if book_title not in models['book_pivot'].index:
            return []
            
        book_idx = np.where(models['book_pivot'].index == book_title)[0][0]
        distances, indices = models['cf_model'].kneighbors(
            models['book_pivot'].iloc[book_idx, :].values.reshape(1, -1),
            n_neighbors=top_n+1)
        
        recs = []
        for i in range(1, len(indices.flatten())):
            title = models['book_pivot'].index[indices.flatten()[i]]
            # Try books_content first, then fallback to original books data
            book_info = models['books_content'][models['books_content']['title'] == title]
            if book_info.empty:
                book_info = models['books'][models['books']['title'] == title]
                if book_info.empty:
                    continue
            
            book_info = book_info.iloc[0]
            
            # Validate image URL
            img_url = book_info['img_url']
            if not isinstance(img_url, str) or not img_url.startswith('http'):
                img_url = "/static/images/no-image.jpg"
            
            recs.append({
                'title': title,
                'author': book_info['author'],
                'year': book_info['year'],
                'publisher': book_info['publisher'],
                'image_url': img_url,
                'score': (1 - distances.flatten()[i]),
                'type': 'collaborative'
            })
        
        return recs[:top_n]
    
    except Exception as e:
        print(f"Error in collaborative recommendations: {e}")
        return []

def content_recommendations(book_title, top_n=9):
    """Generate content-based recommendations"""
    try:
        if book_title not in models['title_to_idx']:
            return []
            
        cb_idx = models['title_to_idx'][book_title]
        sim_scores = list(enumerate(models['content_sim_matrix'][cb_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        
        recs = []
        for i, score in sim_scores:
            title = models['books_content']['title'].iloc[i]
            book_info = models['books_content'][models['books_content']['title'] == title].iloc[0]
            
            # Validate image URL
            img_url = book_info['img_url']
            if not isinstance(img_url, str) or not img_url.startswith('http'):
                img_url = "/static/images/no-image.jpg"
            
            recs.append({
                'title': title,
                'author': book_info['author'],
                'year': book_info['year'],
                'publisher': book_info['publisher'],
                'image_url': img_url,
                'score': score,
                'type': 'content'
            })
        
        return recs[:top_n]
    
    except Exception as e:
        print(f"Error in content recommendations: {e}")
        return []

def hybrid_recommendations(book_title, cf_weight=0.6, cb_weight=0.4, top_n=9):
    """Generate hybrid recommendations"""
    try:
        # Get recommendations from both methods
        cf_recs = collaborative_recommendations(book_title, top_n*2)
        cb_recs = content_recommendations(book_title, top_n*2)
        
        # If no recommendations from either method, return empty
        if not cf_recs and not cb_recs:
            return []
        
        # Combine results from both methods
        combined_scores = {}
        
        # Add CF recommendations with weighted scores
        for rec in cf_recs:
            combined_scores[rec['title']] = {
                'data': rec,
                'score': rec['score'] * cf_weight
            }
        
        # Add CB recommendations with weighted scores
        for rec in cb_recs:
            if rec['title'] in combined_scores:
                combined_scores[rec['title']]['score'] += rec['score'] * cb_weight
            else:
                combined_scores[rec['title']] = {
                    'data': rec,
                    'score': rec['score'] * cb_weight
                }
        
        # Sort by combined score
        sorted_recs = sorted(combined_scores.values(), key=lambda x: x['score'], reverse=True)
        
        # Prepare final recommendations
        final_recs = []
        for rec in sorted_recs[:top_n]:
            final_rec = rec['data'].copy()
            final_rec['score'] = rec['score']
            final_rec['type'] = 'hybrid'
            final_recs.append(final_rec)
        
        return final_recs
    
    except Exception as e:
        print(f"Error in hybrid recommendations: {e}")
        return []

@app.route('/')
def home():
    # Get the search term from the query parameters if it exists
    search_term = request.args.get('search_term', '')
    
    # Get some popular books for the homepage
    popular_books = models['final_rating'].groupby('title')['rating'].count().sort_values(ascending=False).head(12).index.tolist()
    books_data = []
    
    for title in popular_books:
        book_info = models['books_content'][models['books_content']['title'] == title]
        if book_info.empty:
            book_info = models['books'][models['books']['title'] == title]
            if book_info.empty:
                continue
        
        book_info = book_info.iloc[0]
        img_url = book_info['img_url'] if isinstance(book_info['img_url'], str) and book_info['img_url'].startswith('http') else "/static/images/no-image.jpg"
        
        books_data.append({
            'title': title,
            'author': book_info['author'],
            'image_url': img_url
        })
    
    return render_template('index.html', popular_books=books_data, search_term=search_term)

@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form['book_title']
    method = request.form.get('method', 'hybrid')
    
    if method == 'hybrid':
        recommendations = hybrid_recommendations(book_title)
    elif method == 'collaborative':
        recommendations = collaborative_recommendations(book_title)
    elif method == 'content':
        recommendations = content_recommendations(book_title)
    else:
        recommendations = []
    
    return render_template('recommendations.html', 
                         recommendations=recommendations,
                         book_title=book_title,
                         method=method)

@app.route('/search_books', methods=['GET'])
def search_books():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])
    
    # Search in books_content first, then fallback to books
    matching_books = models['books_content'][models['books_content']['title'].str.lower().str.contains(query)]
    if len(matching_books) < 5:
        additional_matches = models['books'][models['books']['title'].str.lower().str.contains(query)]
        matching_books = pd.concat([matching_books, additional_matches]).drop_duplicates('title')
    
    results = []
    for _, row in matching_books.head(9).iterrows():
        img_url = row['img_url'] if isinstance(row['img_url'], str) and row['img_url'].startswith('http') else "/static/images/no-image.jpg"
        results.append({
            'title': row['title'],
            'author': row['author'],
            'image_url': img_url
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)