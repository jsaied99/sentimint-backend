import pickle

class sentimintSVM:
    def __init__(self):
        m = open("SVM/model.svm","rb")
        v = open("SVM/vocab.tfidf","rb")
        self._SVC_alg = pickle.load(m)
        self._vectorizer = pickle.load(v)
        m.close()
        v.close()

    def predict(self,text):
        tfidf_vector = self._vectorizer.transform([text])
        return self._SVC_alg.predict(tfidf_vector)[0]

