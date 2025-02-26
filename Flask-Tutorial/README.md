# Sentiment Analysis Web App with Streamlit

A simple web application for text sentiment analysis (Negative/Neutral/Positive) built with Streamlit and scikit-learn.

## Features

- Real-time sentiment prediction
- Simple text input interface
- Three-class classification (Negative/Neutral/Positive)
- Pre-trained model integration

## Requirements

- Python 3.7+
- Streamlit
- scikit-learn
- pickle
- pandas
- numpy

## Installation

```bash
# Clone repository abd Install dependencies
pip install -r requirements.txt
```

## Model Training

1. **Prepare Dataset**

   - Use a labeled dataset (e.g., Twitter sentiment, IMDb reviews)
   - Format: CSV with 'text' and 'sentiment' columns (-1, 0, 1)

2. **Train Model**

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Sample training code
def train_model():
    # Load your dataset
    df = pd.read_csv('sentiment_data.csv')

    # Preprocess text and split data
    X = df['text']
    y = df['sentiment']

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vectors = vectorizer.fit_transform(X)

    # Train classifier
    model = LogisticRegression()
    model.fit(X_vectors, y)

    # Save model and vectorizer
    with open('sentiment_model.pkl', 'wb') as f:
        pickle.dump((model, vectorizer), f)
```

3. **Save Model**
   - Run the training script to generate `sentiment_model.pkl`

## Running the App Locally

```bash
streamlit run app.py
```

## Deployment

### Option 1: Streamlit Sharing (Impelemented)

1. Create a `requirements.txt`:
   ```
   streamlit
   scikit-learn
   pandas
   numpy
   ```
2. Push to GitHub
3. Deploy at [share.streamlit.io](https://share.streamlit.io/)

### Option 2: Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t sentiment-app .
docker run -p 8501:8501 sentiment-app
```
