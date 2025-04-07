from django.shortcuts import render
from django.http import JsonResponse
import joblib, os, nltk, string
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# === Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'predictor/ml_model/mental_health_model_new.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'predictor/ml_model/tfidf_vectorizer_new.pkl')
movie_data_path = os.path.join(BASE_DIR, 'predictor/ml_model/movies_cleaned.csv')
genre_vectorizer_path = os.path.join(BASE_DIR, 'predictor/ml_model/tfidf_vectorizer_movies.pkl')

# === Load Mental Health Model & Vectorizer ===
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# === Load Movie Data and Genre TF-IDF Vectorizer ===
movie_df = pd.read_csv(movie_data_path)
movie_df['genres_clean'] = movie_df['genres'].str.replace('|', ' ', regex=False)
genre_vectorizer = joblib.load(genre_vectorizer_path)
genre_matrix = genre_vectorizer.transform(movie_df['genres_clean'])

# === Cleaning Function ===
def clean_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return ' '.join([w for w in text.split() if w not in stop_words])

# === Label Mapping for Prediction ===
label_map = {
    'Anxiety': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Anxiety"],
        "emotion": "Fear",
        "recommended_genres": ["Comedy", "Fantasy", "Adventure"]
    },
    'Depression': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Depression"],
        "emotion": "Sadness",
        "recommended_genres": ["Feel-good", "Comedy", "Drama", "Romance"]
    },
    'Normal': {
        "message": "You are too good to conquer the world!",
        "mental_health_risk": "Low",
        "conditions_flagged": ["Normal"],
        "emotion": "Neutral",
        "recommended_genres": ["Any", "Action", "Mystery", "Sci-Fi"]
    },
    'Suicidal': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "Critical",
        "conditions_flagged": ["Suicidal Ideation"],
        "emotion": "Hopelessness",
        "recommended_genres": ["Inspirational", "Comedy", "Fantasy"]
    },
    'Stress': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "Medium",
        "conditions_flagged": ["Stress"],
        "emotion": "Overwhelmed",
        "recommended_genres": ["Comedy", "Animation", "Adventure"]
    },
    'Bipolar': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Bipolar Disorder"],
        "emotion": "Fluctuating",
        "recommended_genres": ["Drama", "Fantasy", "Thriller"]
    },
    'Personality disorder': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Personality Disorder"],
        "emotion": "Instability",
        "recommended_genres": ["Drama", "Mystery", "Psychological Thriller"]
    }
}

# === Views ===

# Home page with text analysis form
def index(request):
    return render(request, 'predictor/index.html')

# Handle mental health prediction
def analyze_text(request):
    if request.method == 'POST':
        text = request.POST.get('prompt', '')
        cleaned = clean_text(text)

        try:
            vectorized_input = vectorizer.transform([cleaned])
            prediction = model.predict(vectorized_input)[0]
        except Exception as e:
            return JsonResponse({'error': 'Model prediction failed'}, status=500)

        result = label_map.get(prediction, {
            "message": "Unknown",
            "mental_health_risk": "N/A",
            "conditions_flagged": [],
            "emotion": "N/A",
            "recommended_genres": []
        })

        return JsonResponse(result)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# Page to input genre for recommendations
def recommend_page(request):
    return render(request, 'predictor/recommend.html')

# Return JSON of recommended movies
def get_recommendations(request):
    if request.method == 'POST':
        genre_input = request.POST.get('genre', '')
        if not genre_input:
            return JsonResponse({'error': 'No genre provided'}, status=400)

        user_vec = genre_vectorizer.transform([genre_input])
        similarity_scores = cosine_similarity(user_vec, genre_matrix).flatten()
        top_indices = similarity_scores.argsort()[-10:][::-1]
        recommendations = movie_df.iloc[top_indices][['title', 'genres']]
        movie_list = recommendations.to_dict(orient='records')
        return JsonResponse({'movies': movie_list})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
