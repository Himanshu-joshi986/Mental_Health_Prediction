# 🧠🎬 Mental Health Analyzer & Movie Recommender Web App

A machine learning-powered **Django web application** that does two things:
- **Mental Health Prediction:** Analyzes user-submitted text and predicts mental health conditions like **Depression**, **Anxiety**, **Stress**, and more.
- **Movie Recommendation System:** Suggests relevant movies based on the genre entered by the user.

All powered by ML models, modern frontend design, and an intuitive user experience.

---

## 🚀 Features

### 🧠 Mental Health Analyzer
- 📝 **Text Analysis:** Users describe their mental state in free-form text.
- 🤖 **ML Model Integration:** Predicts mental health condition using a trained classifier.
- ⚙️ **TF-IDF Vectorization:** Preprocesses user input text effectively before model inference.
- 🔐 **Secure CSRF Handling:** Ensures safe form interactions.

### 🎬 Movie Recommender
- 🔍 **Genre-based Recommendations:** Enter a genre (e.g., "Action", "Romance", "Thriller") to get top movie suggestions.
- 🧠 **TF-IDF + Cosine Similarity:** Finds similar movies by comparing genre-based vectors.

### 🎨 Modern UI
- 🌙 **Dark Mode:** Eye-friendly interface with smooth gradients.
- ✨ **Glassmorphism Styling:** Sleek, frosted-glass card layouts.
- 🌀 **Animations & Effects:** Loading transitions, floating logo, hover animations, and more.
- 📱 **Fully Responsive:** Works beautifully across devices.

---

## 🛠️ Tech Stack

| Layer       | Tools / Libraries                                      |
|-------------|--------------------------------------------------------|
| **Backend** | Django 5.2, Python 3.13                                |
| **Frontend**| HTML5, CSS3, JavaScript (Vanilla)                      |
| **ML/NLP**  | Scikit-learn, NLTK, TF-IDF, Cosine Similarity          |
| **Modeling**| Logistic Regression (Mental Health), TF-IDF Recommender|
| **Serialization** | Joblib for saving and loading ML components    |
| **UX Enhancements** | Dark mode, hover effects, loading animations |

---

## 🧪 How to Run Locally

```bash
git clone https://github.com/your-username/ML_pro.git
cd ML_pro
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py runserver
