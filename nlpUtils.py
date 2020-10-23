import spacy

class TextSimilarity(object):

    def __init__(self):
        '''
        Initialise the library for NLP
        '''
        self.nlp = spacy.load("en_core_web_lg")

    def remove_stopwords_fast(self, text):
        doc = self.nlp(text.lower())
        result = [
            token.text for token in doc if token.text not in nlp.Defaults.stop_words]
        return " ".join(result)

    def remove_pronoun(self, text):
        doc = self.nlp(text.lower())
        result = [token for token in doc if token.lemma_ != '-PRON-']
        return " ".join(result)

    def process_text(self, text):
        '''
        preprocess sentences by removing stopwords and pronouns
        '''
        doc = self.nlp(text.lower())
        result = []
        for token in doc:
            if token.text in self.nlp .Defaults.stop_words:
                continue
            if token.is_punct:
                continue
            if token.lemma_ == '-PRON-':
                continue
            result.append(token.lemma_)
        return " ".join(result)

    def get_similarity_score(self, text1, text2):
        '''
        Get the vector similarity between 2 sentences.
        '''
        text1_processed = self.nlp(self.process_text(text1))
        text2_processed = self.nlp(self.process_text(text2))
        return text1_processed.similarity(text2_processed)