from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
import joblib

# Load the saved model
loaded_model = joblib.load('naive_bayes_model.pkl')

# Load content from scraped.txt
with open("scraped.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Initialize the TfidfVectorizer and load its vocabulary from the trained model
vectorizer = TfidfVectorizer()

# Fit and transform the training data
content = vectorizer.fit_transform(content)  # Conv

# Transform content using the same vectorizer


# Predict class of the content
predicted_class = loaded_model.predict(content)[0]

# Get class probabilities
class_probs = loaded_model.predict_proba(content)[0]

# Print predicted class and probabilities
print("Predicted Class:", predicted_class)
print("Class Probabilities:", class_probs)
