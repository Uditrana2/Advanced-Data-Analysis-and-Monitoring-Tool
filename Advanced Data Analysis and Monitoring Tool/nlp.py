import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)

    # Lowercase conversion
    tokens = [token.lower() for token in tokens]

    # Remove non-alphabetic characters
    tokens = [re.sub(r'[^a-zA-Z]', '', token) for token in tokens if re.sub(r'[^a-zA-Z]', '', token)]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens

def analyze_trends_activities(text):
    # Preprocess the text
    tokens = preprocess_text(text)
    text = ' '.join(tokens)

    # Create document-term matrix
    vectorizer = CountVectorizer(max_features=1000)
    X = vectorizer.fit_transform([text])

    # Apply LDA model
    lda_model = LatentDirichletAllocation(n_components=5, random_state=42)
    lda_model.fit(X)

    # Visualize topics
    feature_names = vectorizer.get_feature_names_out()
    topics = lda_model.components_

    for topic_idx, topic in enumerate(topics):
        top_words_indices = topic.argsort()[:-6:-1]
        top_words = [feature_names[i] for i in top_words_indices]
        print(f"Topic {topic_idx + 1}: {' '.join(top_words)}")

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(tokens))

    # Plot word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Read the text file
with open('sites1856.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Analyze trends and activities
analyze_trends_activities(text)
