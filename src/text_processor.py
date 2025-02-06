import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextProcessor:
    def __init__(self):
        # Download required NLTK data with error handling
        try:
            # Use proper resource names
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            print(f"Warning: Error downloading NLTK data: {e}")

        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        """Preprocess text by tokenizing, removing stopwords, and lemmatizing."""
        try:
            # Tokenize
            tokens = word_tokenize(text.lower())
            # Remove stopwords and lemmatize
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                     if token not in self.stop_words and token.isalnum()]
            return tokens
        except Exception as e:
            print(f"Warning: Error in text preprocessing: {e}")
            return text.split()  # Fallback to simple splitting

    def extract_entities(self, text):
        """Extract simple entities from text using NLTK."""
        try:
            words = word_tokenize(text)
            # Basic named entity extraction (capitalized words)
            entities = [word for word in words if word[0].isupper()]
            return [('ENTITY', word) for word in entities]
        except Exception as e:
            print(f"Warning: Error in entity extraction: {e}")
            return []

    def get_summary(self, text):
        """Generate a simple summary using sentence scoring."""
        try:
            sentences = sent_tokenize(text)
            if not sentences:
                return text[:500] + "..."  # Fallback summary

            # Simple scoring based on sentence length and position
            scores = {}
            for i, sent in enumerate(sentences):
                words = word_tokenize(sent.lower())
                score = (len(words) / (i + 1))  # Favor longer sentences that appear earlier
                scores[sent] = score

            # Get top 3 sentences for summary
            summary_sentences = sorted(scores.items(), 
                                    key=lambda x: x[1], 
                                    reverse=True)[:3]

            return ' '.join([sent[0] for sent in summary_sentences])
        except Exception as e:
            print(f"Warning: Error in summarization: {e}")
            return text[:500] + "..."  # Fallback summary