import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import joblib
data = pd.read_excel("udit.xlsx")


data.dropna(subset=['Text'], inplace=True)


data.dropna(subset=['Main_Class'], inplace=True)


X_train, X_test, y_train, y_test = train_test_split(data['Text'], data['Main_Class'], test_size=0.2, random_state=42)


vectorizer = TfidfVectorizer()
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)


clf = RandomForestClassifier()
clf.fit(X_train_vect, y_train)


y_pred = clf.predict(X_test_vect)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
#accuracy 95.4%

joblib.dump(clf, 'random_forest_model.joblib')
print("Model saved successfully.")
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')
print("Model and vectorizer saved successfully.")


# Read content from scraped.txt

with open("scraped.txt", "r", encoding="utf-8") as file:
    content = file.read()


content_vect = vectorizer.transform([content])


predicted_class = clf.predict(content_vect)[0]


class_probs = clf.predict_proba(content_vect)[0]

# Print predicted class and probabilities
print("Predicted Class:", predicted_class)
print("Class Probabilities:", class_probs)

# Plot a graph of class probabilities
plt.figure(figsize=(8, 6))
plt.bar(clf.classes_, class_probs, color='skyblue')
plt.xlabel('Classes')
plt.ylabel('Probability')
plt.title('Class Probability Distribution')
plt.xticks(rotation=45)
plt.show()
