import spacy
from newspaper import Article as NewsArticle
from ..models import Article, Author

class ArticleSummarizer():
    url = ""
    news_article = None
    article = None
    def __init__(self, url) -> None:
        self.url = url

    def process(self):
        # TODO: Handle null
        self.news_article = NewsArticle(self.url)
        self.news_article.download()
        self.news_article.parse()
    
    def save_to_model(self):
        self.article = Article(title = self.news_article.title, top_image = self.news_article.top_image, description= self.news_article.meta_description, summary= self.news_article.text, url= self.url,publish_date=self.news_article.publish_date, authors=[])
        for author_name in self.news_article.authors:
            self.article.authors.append(Author(name = author_name))

    def get_article(self):
        self.process()
        self.save_to_model()
        return self.article
    
    def summarize_text(self, text, k = 5):
        nlp = spacy.load("en_core_web_lg")
        doc = nlp(text)
        # Extract the most important sentences.
        sentence_scores = []
        for sentence in doc.sents:
            sentence_scores.append((sentence.text, sentence.similarity(doc)))
        # Sort the sentences by their scores.
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        # Get the top k sentences.
        sentences = [sentence[0] for sentence in sentence_scores[:k]]
        # Combine the sentences to form a summary.
        summary = " ".join(sentences)
        return summary