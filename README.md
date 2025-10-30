# BookSage-AI  
*A Personalized Book Recommendation System built by Riya Mandowara using NLP and Hybrid Machine Learning*

---

## Project Overview  

**BookSage-AI** is an intelligent book recommendation system developed by **Riya Mandowara** that uses **Natural Language Processing (NLP)** and **Machine Learning** to recommend books tailored to each user’s preferences.  

The goal of this project is to provide accurate, personalized book suggestions by combining multiple recommendation techniques — **Collaborative Filtering**, **Content-Based Filtering**, and a **Hybrid Model** that merges the strengths of both.  

Unlike basic recommendation systems, **BookSage-AI** applies NLP techniques like **TF-IDF Vectorization** and **Cosine Similarity** to understand relationships between book descriptions, authors, and publishers — resulting in highly relevant and context-aware suggestions.

---

## Key Features  

**Three Intelligent Filters**
1. **Collaborative Filtering**  
   - Uses user–item interactions (ratings and preferences)  
   - Builds a *User-Item Matrix* and applies *KNN (Nearest Neighbors)* for similarity  

2. **Content-Based Filtering**  
   - Uses book metadata (title, author, publisher)  
   - Applies *TF-IDF Vectorization* to extract text features  
   - Uses *Cosine Similarity* to find books similar to the one the user liked  

3. **Hybrid Model**  
   - Combines both collaborative and content-based predictions  
   - Uses *Weighted Fusion* for balanced, accurate recommendations  
**NLP Integration**  
- TF-IDF (Term Frequency – Inverse Document Frequency) for text-based feature extraction  
- Cosine Similarity for semantic similarity between books  
 **Interactive User Interface**  
- Built with **Flask** and **HTML/CSS/JavaScript**  
- Simple, user-friendly interface for entering favorite books or user IDs and getting instant recommendations  
**Fast and Reusable Models**  
- Models are stored in `.pkl` files for fast loading and reuse  
- Includes trained files such as `model.pkl` and `vectorizer.pkl`  
**Feedback-Driven Improvement**  
- Future enhancements can use user feedback or ratings to improve accuracy  

---

## System Architecture  

<img width="576" height="667" alt="image" src="https://github.com/user-attachments/assets/63166bf5-3a2d-465e-8e2d-a95bf00a9cfd" />


## Installation & Setup
To run this project locally:
### 1. Go to Desktop and clone project

⁠ bash
cd ~/Desktop
git clone https://github.com/riyamandowara/BookSage-AI.git
cd BookSage-AI

### 2. Install compatible Python (3.11)

⁠ bash
brew install python@3.11

### 3. Create & activate virtual environment

⁠ bash
python3.11 -m venv venv
source venv/bin/activate

### 4. Upgrade pip

⁠ bash
pip install --upgrade pip


###  5. Install *specific working versions* of dependencies

(This avoids Python 3.13–related issues and ensures pickle compatibility)

⁠ bash
pip install flask==2.3.3
pip install numpy==1.26.4
pip install pandas==2.2.2
pip install scikit-learn==1.3.2
pip install scipy==1.11.4
pip install nltk==3.8.1
pip install gunicorn==21.2.0
 ⁠

	⁠These versions are stable for 3.11 and known to work perfectly with BookSage-AI’s ⁠ .pkl ⁠ files.

### 6. Run the Flask app

⁠ bash
python app.py
 ⁠
	⁠You’ll see something like:
>
> 
⁠ > * Running on http://127.0.0.1:5000
>  ⁠

### 7. Open the web app

Open your browser and go to:
*[http://127.0.0.1:5000](http://127.0.0.1:5000)*

You’ll see the *BookSage-AI interface* where you can:

•⁠  ⁠search or browse books
•⁠  ⁠get AI-based recommendations
•⁠  ⁠view book details

## 8. (Optional) Stop the server

When done, press:

⁠ bash
CTRL + C
 ⁠

## 9. Next time (for your class demo)

Just do these three steps (no need to reinstall everything):

⁠ bash
cd ~/Desktop/BookSage-AI
source venv/bin/activate
python app.py

## Future Enhancements

Integration of Deep Learning models (BERT/Word2Vec) for contextual understanding.

Sentiment analysis on user reviews.

Deploy app on AWS / Render / Hugging Face Spaces.

Add user login and profile-based recommendation history.

## Developer

Developed by: Riya Mandowara
Email: riyamandowara4@gmail.com
GitHub: https://github.com/riyamandowara

"Turning reading data into intelligent book choices with AI."
