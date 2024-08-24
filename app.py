import streamlit as st
import pickle
class SentimentClassifier:
    model_prediction  = {
        -1 : 'Negative',
        0 : 'Neutral',
        1 : 'Positive'
    }
    def __init__(self, model_file):
        with open(model_file, 'rb') as model_file:
            self.model, self.vectorizer = pickle.load(model_file)
    def predict(self, text):
        X = self.vectorizer.transform([text])
        y = self.model.predict(X)
        return SentimentClassifier.model_prediction[y[0]]
model = SentimentClassifier('sentiment_model.pkl')
def main():
    st.title("Sentiment Analysis App")
    user_input = st.text_area("Enter your text here:")
    if st.button("Analyze"):
        if user_input:
            prediction = model.predict(user_input)
            st.write(f"Sentiment: {prediction}")
        else:
            st.write("Please enter some text to analyze.")
if __name__ == "__main__":
    main()