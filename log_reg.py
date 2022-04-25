##############################################
# This file contains an implementation of logistic regression for Twitter sentiment analysis.
# Mainly the load_model() function will be used in the sentiment analysis website.
##############################################
# import pandas as pd
# import numpy as np
import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.linear_model import LogisticRegression
# from sklearn import metrics


LABEL_DICT = { # I found the model easier to test with numeric labels
    "positive": 1, "negative": -1, "neutral": 0
}


def save_model(model, save_file_path):
    """
    Saves the input model to the input file path.
    """
    with open(save_file_path, "wb") as f:
        pickle.dump(model, f)


def load_model(file_path):
    """
    Tries to load and return the model from the input file path.
    """
    with open(file_path, "rb") as f:
        model = pickle.load(f)
    return model


# def test_model(model, test_data):
#     """
#     Tests the input model using the input test data.
#     Uses a variety of metrics from sklearn's API.
#     """
#     # step 1: get the labels from the dataframe
#     truth_labels = np.array(test_data.sentiment)

#     # step 2: get the predicted labels from the model
#     pred_labels = model.predict(test_data.text)

#     # step 3: compute the accuracy of the model and display it
#     acc = np.mean(truth_labels == pred_labels)
#     print("\nmodel accuracy: {:.2f}%".format(acc))

#     # step 4: compute the model's report from sklearn
#     print(metrics.classification_report(truth_labels, pred_labels, target_names=['positive', 'negative', 'neutral']))


# def load_processed_dataset():
#     """
#     Loads the dataset and performs all necessary preprocessing steps.
#     """
#     data_path = "cleaned_data.csv"
#     data = pd.read_csv(data_path)[['text','sentiment']]
#     train, test = train_test_split(data, test_size=0.1) # split into training and testing partitions

#     # change labels to numbers
#     train["sentiment"] = train["sentiment"].map(LABEL_DICT)
#     test["sentiment"] = test["sentiment"].map(LABEL_DICT)

#     # fill the NaN values with empty string (training doesn't work without this step)
#     train.fillna('',inplace=True)
#     test.fillna('',inplace=True)

#     return train, test # return both partitions


# def build_log_reg_model():
#     """
#     Builds and returns a logistic regression model Pipeline using the sklearn API.
#     """
#     # step 1: create CountVectorizer dict
#     # count vect => { 'word': count, 'word2': count2, ... }
#     # e.g., it stores the number of occurrences for each word in the dataset
#     count_vect = CountVectorizer() # pass in more params to try out diff configurations

#     # step 2: create TfIdf transformer
#     # normalizes the counts of each word in count vect by dividing by doc length
#     tf_idf = TfidfTransformer()

#     # step 3: create Logistic Regression model
#     # I experimented with different solvers, and the newton-cg one was best
#     solver_name = 'newton-cg' # can change this, it's just a parameter to Logistic Regression
#     log_reg = LogisticRegression(solver=solver_name)

#     # step 4: create a pipeline that makes it easier to prepare and predict with data
#     # pipeline = input data -> step 1 -> step 2 -> step 3 -> prediction
#     full_pipeline = Pipeline([('vect', count_vect), ('tfidf', tf_idf), ('clf', log_reg)])
#     return full_pipeline


# def train_new_model():
#     """
#     Trains and evaluates a new logistic regression model from scratch.
#     """
#     # get the dataset
#     train, test = load_processed_dataset()

#     # create the model
#     log_reg_model = build_log_reg_model()

#     # train the model
#     # just a simple call to sklearn fit using the data and labels
#     log_reg_model.fit(train.text, train.sentiment)

#     # test the model
#     print("\ntesting newly trained model...")
#     test_model(log_reg_model, test)

#     # save the model
#     model_save_file_name = "models/log_reg_model.pkl"
#     save_model(log_reg_model, model_save_file_name)


def convert_number_to_text_label(num):
    """
    Uses the label dict from before to convert the output number back into a text label.
    E.g., 0 => Positive.
    """
    reverse_dict = {v: k for k, v in LABEL_DICT.items()}
    return reverse_dict[num]


def predict_on_single_input(text, model):
    """
    Predicts the sentiment for a single input text using the input model.
    Using this function, we can predict on raw text from any input.
    """
    pred_num = model.predict([text])[0]
    # pred_name = convert_number_to_text_label(pred_num)
    # print("\nprediction: text = {}, label = {}".format(text, pred_name))
    return pred_num

def main():

    print("welcome to log reg")
    
    # train_new_model() # if you want to train a new model from scratch

    # if you want to use an old model
    model_file_name = "models/log_reg_model.pkl"
    model = load_model(model_file_name)

    while True:

        # evaluate on a piece of text
        input_text = input("\nplease enter a piece of text to analyze: ")
        predict_on_single_input(input_text, model)

        # ask the user if they want to do it again
        cont = input("\nwould you like to do this again? (y/n): ")
        if cont == 'n':
            break
    
    print("\nexiting...\n")


if __name__ == '__main__':
    main()
