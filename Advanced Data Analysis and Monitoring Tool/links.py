from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import numpy as np

# Read the links from the file
file_path = "sites705.txt"
try:
    with open(file_path, "r") as file:
        links = file.readlines()
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
    exit()

# Preprocess the links if necessary (e.g., remove special characters, numbers, etc.)

# Use TfidfVectorizer for vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.8, min_df=0.05)
X = vectorizer.fit_transform(links)

# Apply TruncatedSVD for dimensionality reduction
lsa = TruncatedSVD(n_components=10, random_state=42)
X_reduced = lsa.fit_transform(X)

# Apply KMeans clustering
k = 5  # number of clusters
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(X_reduced)

# Get the top terms per cluster
original_space_centroids = lsa.inverse_transform(kmeans.cluster_centers_)
order_centroids = original_space_centroids.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

# Print top terms per cluster
print("Top terms per cluster:")
for i in range(k):
    print(f"Cluster {i+1}:")
    top_terms = [terms[ind] for ind in order_centroids[i, :5]]
    print(top_terms)
