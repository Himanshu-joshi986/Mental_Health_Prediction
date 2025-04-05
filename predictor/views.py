from django.shortcuts import render
from django.http import JsonResponse
import joblib, os, nltk, string
from nltk.corpus import stopwords

# Download stopwords once (you can remove this after running the project once)
nltk.download('stopwords')

# Load model and vectorizer
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'predictor/ml_model/mental_health_model.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'predictor/ml_model/tfidf_vectorizer.pkl')

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# Clean the input text
def clean_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return ' '.join([w for w in text.split() if w not in stop_words])

# Map predictions to result details
label_map = {
    'Anxiety': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Anxiety"],
        "emotion": "Fear"
    },
    'Depression': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Depression"],
        "emotion": "Sadness"
    },
    'Normal': {
        "message": "You are too good to conquer the world!",
        "mental_health_risk": "Low",
        "conditions_flagged": ["Normal"],
        "emotion": "Neutral"
    },
    'Suicidal': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "Critical",
        "conditions_flagged": ["Suicidal Ideation"],
        "emotion": "Hopelessness"
    },
    'Stress': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "Medium",
        "conditions_flagged": ["Stress"],
        "emotion": "Overwhelmed"
    },
    'Bipolar': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Bipolar Disorder"],
        "emotion": "Fluctuating"
    },
    'Personality disorder': {
        "message": "I hope You are doing well!",
        "mental_health_risk": "High",
        "conditions_flagged": ["Personality Disorder"],
        "emotion": "Instability"
    },
}

# Render HTML page
def index(request):
    return render(request, 'predictor/index.html')

# Handle prediction
def analyze_text(request):
    if request.method == 'POST':
        text = request.POST.get('prompt', '')
        print("Received text:", text)

        cleaned = clean_text(text)
        print("Cleaned text:", cleaned)

        try:
            vectorized_input = vectorizer.transform([cleaned])
            prediction = model.predict(vectorized_input)[0]
            print("Prediction:", prediction)
        except Exception as e:
            print("Model error:", e)
            return JsonResponse({'error': 'Model prediction failed'}, status=500)

        result = label_map.get(prediction, {
            "message": "Unknown",
            "mental_health_risk": "N/A",
            "conditions_flagged": [],
            "emotion": "N/A"
        })

        return JsonResponse(result)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
