import pandas
import numpy
import pickle

# Aiming for usability but I am somewhat new to Python so this using a lot of sklearn
from sklearn import metrics
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# POSNEG dictionary used for easily translating the dataset labels to numbers 
# that will be returned and that the algorithm can better understand

# negative := -100
# neutral  :=  0
# positive :=  100
POSNEG = {"negative": -100, "neutral": 0, "positive": 100}

# Used to train a model and generate a library for the given data file
# File should be a csv 
def SVM_train(data_file_name):

    # get data from file and put it into data lists
    data = pandas.read_csv(data_file_name)[["text","sentiment"]]
        
    # Splitting data same way as LR for consistincy
    training_data, test_data = train_test_split(data, test_size=0.1)

    # This is just chaning the labels to numeric values
    training_data["sentiment"] = training_data["sentiment"].map(POSNEG)
    test_data["sentiment"] = test_data["sentiment"].map(POSNEG)

    # shout out to Cameron. This prevents crashes occasonally
    training_data.fillna('',inplace=True)
    test_data.fillna('',inplace=True)

    # Create the trainig vector
    tfidf_vectorizer = TfidfVectorizer()

    # generate corpus IDF portion
    tfidf_vectorizer.fit(training_data["text"])
    # TODO: try ang get IDF based on full text to work
    
    # generate TF portion for training
    tfidf_vector = tfidf_vectorizer.transform(training_data["text"])

    # May set break_ties to true if we have the computational power to do so
    # Avoiding linear SVM due to Linear kernels generally having similar performance to LR
    SVC = svm.NuSVC(kernel = "rbf", break_ties=False)

    # Training time
    SVC.fit(tfidf_vector, training_data["sentiment"])

    # test model
    SVM_test(SVC, test_data, tfidf_vectorizer)

    # save model and vectorizer
    f = open("model.svm","wb")
    pickle.dump(SVC, f)
    f.close()
    f = open("vocab.tfidf","wb")
    pickle.dump(tfidf_vectorizer, f)
    f.close()
    

def SVM_test(SVC, data, tfidf_vectorizer):
    # Get answer key for correct labels
    key = numpy.array(data.sentiment)

    # generate TF for test data
    tfidf_vector = tfidf_vectorizer.transform(data["text"])
    
    # get predictions on test set
    result = SVC.predict(tfidf_vector)

    # print results
    print(metrics.classification_report(key, result, target_names=['negative', 'neutral', 'positive']))

# Running this file will create a model
SVM_train("cleaned_data.csv")