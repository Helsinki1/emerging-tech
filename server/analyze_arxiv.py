import json
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure NLTK data is downloaded
nltk.data.path.append("/Users/amrutharao/nltk_data")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load categorized papers
try:
    with open("categorized_arxiv_papers.json", "r", encoding="utf-8") as f:
        categorized_papers = json.load(f)
except FileNotFoundError:
    print("Error: categorized_arxiv_papers.json not found.")
    exit()

# Count papers in each category
category_counts = {category: len(papers) for category, papers in categorized_papers.items()}

# Extract all summaries and tokenize words
all_text = " ".join(
    paper["summary"].lower() for papers in categorized_papers.values() for paper in papers
)

# Check if text is empty
if not all_text.strip():
    print("Error: No text data available for analysis.")
    exit()

try:
    words = word_tokenize(all_text)
except LookupError:
    print("Error: NLTK punkt tokenizer missing.")
    nltk.download('punkt', quiet=True)
    words = all_text.split()


# Remove stopwords and short words
stop_words = set(stopwords.words("english"))
filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

# Count frequent words
word_freq = Counter(filtered_words)
top_keywords = word_freq.most_common(20)  # Top 20 trending words

# **Plot Category Trends**
plt.figure(figsize=(10, 5))
plt.bar(category_counts.keys(), category_counts.values(), color="skyblue")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Number of Papers")
plt.title("Research Paper Trends by Category")
plt.show()

# **Print Top Keywords**
print("Emerging Keywords in Research Papers:")
for word, count in top_keywords:
    print(f"{word}: {count} occurrences")
