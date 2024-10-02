import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import string

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Read the scraped text file
with open("scraped.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Tokenization
tokens = word_tokenize(text)

# Cleaning
# Remove punctuation and convert to lowercase
clean_tokens = [token.lower() for token in tokens if token not in string.punctuation]

# Remove stopwords
stop_words = set(stopwords.words('english'))
clean_tokens = [token for token in clean_tokens if token not in stop_words]

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(token) for token in clean_tokens]

# Stemming (Optional)
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(token) for token in clean_tokens]

# Print the cleaned and lemmatized/stemmed tokens
print("Cleaned and Lemmatized Tokens:")
print(lemmatized_tokens)
