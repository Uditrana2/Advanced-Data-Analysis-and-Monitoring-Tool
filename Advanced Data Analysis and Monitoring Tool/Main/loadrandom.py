import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import matplotlib.pyplot as plt

# Load the trained model
loaded_model = joblib.load('random_forest_model.joblib')

# Load content from scraped.txt
with open("scraped_content.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Load the vocabulary from the trained vectorizer
vectorizer = joblib.load('tfidf_vectorizer.joblib')
print("Vec loaded")

# Transform content using the same vectorizer
content_vect = vectorizer.transform([content])

# Predict class of the content
predicted_class = loaded_model.predict(content_vect)[0]

# Get class probabilities
class_probs = loaded_model.predict_proba(content_vect)[0]

# Print predicted class and probabilities
print("Predicted Class:", predicted_class)
print("Class Probabilities:", class_probs)

plt.figure(figsize=(7, 7))
plt.bar(loaded_model.classes_, class_probs, color='skyblue')
plt.xlabel('Classes')
plt.ylabel('Probability')
plt.title('Class Probability Distribution')
plt.xticks(rotation=45)
plt.show()

