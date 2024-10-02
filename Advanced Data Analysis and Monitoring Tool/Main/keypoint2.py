import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Read the scraped text file
with open("scraped.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Tokenize the text into sentences
sentences = sent_tokenize(text)

# Remove non-alphanumeric characters and convert to lowercase for each sentence
cleaned_sentences = [re.sub(r'[^a-zA-Z0-9\s]', '', sentence.lower()) for sentence in sentences]

# Tokenize the cleaned sentences into words
tokenized_sentences = [word_tokenize(sentence) for sentence in cleaned_sentences]

# Remove stopwords and lemmatize words in each sentence
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
filtered_sentences = []
for sentence in tokenized_sentences:
    filtered_sentence = [lemmatizer.lemmatize(word) for word in sentence if word not in stop_words]
    filtered_sentences.append(filtered_sentence)

# Flatten the list of words in filtered sentences
all_words = [word for sentence in filtered_sentences for word in sentence]

# Calculate word frequency
fdist = nltk.FreqDist(all_words)

# Get the most common words as key phrases
important_keywords = [word for word, freq in fdist.most_common(20)]

# Extract sentences containing the important keywords
key_phrases = []
for sentence in sentences:
    for keyword in important_keywords:
        if keyword in sentence.lower():
            key_phrases.append(sentence)
            break

# Output the key points
print("Important Key Points:")
for i, key_phrase in enumerate(key_phrases[:40], start=1):
    print(f"{i}. {key_phrase}")
