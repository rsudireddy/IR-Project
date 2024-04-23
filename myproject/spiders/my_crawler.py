import scrapy
from pathlib import Path
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import re

class MySpider(scrapy.Spider):
    name = 'my_crawler'
    allowed_domains = ['javatpoint.com']
    start_urls = ['https://www.javatpoint.com/']

    custom_settings = {
        'DEPTH_LIMIT': 3,  
        'CLOSESPIDER_PAGECOUNT': 20,  
    }
    page_count = 0
    documents = []
    document_names = []

    
    def cleaning_text(self, text):
        cleaning_text = re.sub(r'<.*?>', '', text)
        cleaning_text = re.sub(r'\\[ntr]', '', cleaning_text)
        cleaning_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaning_text)
        cleaning_text = re.sub(r'\s+', ' ', cleaning_text)
        cleaning_text = cleaning_text.lower()
        return cleaning_text

    def get_valid(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def parse(self, response):
        self.page_count += 1
        filename = self.get_valid(response.url.split("/")[-1]) + '.html'
        self.document_names.append(filename)  # Store document name
        if self.page_count > self.settings.get('CLOSESPIDER_PAGECOUNT'):
            return
        if response.meta['depth'] > self.settings.get('DEPTH_LIMIT'):
            return
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log(f"Saved file {filename}")

        with open(filename, "rb") as f:
            html_content = f.read().decode('utf-8')
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            cleaning_text = self.cleaning_text(text)
            self.documents.append(cleaning_text)

        for next_page in response.css('a::attr(href)').getall():
            yield response.follow(next_page, callback=self.parse)

    def closed(self, reason):
        self.building_index()

    def building_index(self):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.documents)
        cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        index = {}
        for idx, (doc_name, doc) in enumerate(zip(self.document_names, self.documents)):
            index[idx] = {
                'document_name': doc_name,
                'document': doc,
                'tfidf_vector': tfidf_matrix[idx],
                'cosine_similarities': cosine_sim_matrix[idx]
            }

        with open('index.pkl', 'wb') as f:
            pickle.dump(index, f)



