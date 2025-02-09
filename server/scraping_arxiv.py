import requests
import feedparser
import json
from collections import defaultdict
import nltk

# Download NLTK stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

# **🔍 Define Emerging Tech Categories & Keywords**
categories = {
    "Artificial Intelligence & ML": ["AI", "machine learning", "deep learning", "neural network", "NLP", "reinforcement learning", "transformer", "computer vision"],
    "Quantum Computing": ["quantum", "qubits", "superposition", "entanglement", "quantum circuit", "quantum algorithm"],
    "Cybersecurity & Cryptography": ["security", "cybersecurity", "cryptography", "encryption", "authentication", "malware", "phishing"],
    "Blockchain & Web3": ["blockchain", "decentralization", "smart contracts", "Ethereum", "DeFi", "NFT", "Web3"],
    "Human-Computer Interaction & AR/VR": ["virtual reality", "augmented reality", "HCI", "user experience", "VR", "AR"],
    "Robotics & Automation": ["robotics", "automation", "drones", "autonomous", "self-driving", "robot", "manipulation"],
    "Other": []  # For uncategorized papers
}

# **📡 Define arXiv API URL for Computer Science papers**
arxiv_url = "http://export.arxiv.org/api/query?search_query=cat:cs.*&sortBy=submittedDate&sortOrder=descending&max_results=100"

# **📥 Fetch arXiv papers**
response = requests.get(arxiv_url)
feed = feedparser.parse(response.text)

# **🗂️ Categorize Papers**
categorized_papers = defaultdict(list)

for entry in feed.entries:
    title = entry.title.lower()
    summary = entry.summary.lower()

    # **Check which category the paper fits into**
    paper_category = "Other"
    for category, keywords in categories.items():
        if any(keyword in title or keyword in summary for keyword in keywords):
            paper_category = category
            break  # Assign to first matching category

    # **Store paper details**
    paper_data = {
        "title": entry.title,
        "summary": entry.summary,
        "authors": [author.name for author in entry.authors],
        "published": entry.published,
        "arxiv_url": entry.link
    }
    categorized_papers[paper_category].append(paper_data)

# **💾 Save to JSON File**
with open("categorized_arxiv_papers.json", "w", encoding="utf-8") as json_file:
    json.dump(categorized_papers, json_file, indent=4, ensure_ascii=False)

print(f"Scraped and categorized {sum(len(v) for v in categorized_papers.values())} recent CS papers from arXiv.")
print(f"Saved in categorized_arxiv_papers.json")
