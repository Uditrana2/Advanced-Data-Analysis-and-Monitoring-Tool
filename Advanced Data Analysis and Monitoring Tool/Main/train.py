import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
import joblib
# Load the dataset
df = pd.read_excel('udit.xlsx')

# Drop rows with missing values in the 'Text' and 'Main_Class' columns
df.dropna(subset=['Text', 'Main_Class'], inplace=True)

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Main_Class'], test_size=0.2, random_state=42)

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the training data
X_train_vect = vectorizer.fit_transform(X_train.astype('U'))  # Convert to Unicode strings

# Transform the test data
X_test_vect = vectorizer.transform(X_test.astype('U'))  # Convert to Unicode strings

# Initialize and train the classifier
clf = MultinomialNB()
clf.fit(X_train_vect, y_train)

# Evaluate the classifier
accuracy = clf.score(X_test_vect, y_test)
print("Accuracy:", accuracy)
#accuracy = 86.5%
# Read content from scraped.txt


# Save the trained model to a file
joblib.dump(clf, 'naive_bayes_model.pkl')
print("Model saved successfully.")
with open("scraped.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Transform content using the same vectorizer
content_vect = vectorizer.transform([content])

# Predict class of the content
predicted_class = clf.predict(content_vect)[0]

# Get class probabilities
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
