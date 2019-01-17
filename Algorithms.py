# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import   MultinomialNB
from sklearn import linear_model, ensemble
from sklearn.metrics import accuracy_score

import pandas as pd
import os

#read the reviews and their polarities from a given file

def loadData(fname):
    reviews=[]
    labels=[]
    questions=[]
    length =[]
    words = []
    f=open(fname)
    for line in f:
        q,review,rating=line.strip().split('\t')
        questions.append(q.lower())
        reviews.append(review.lower())
        labels.append(int(rating))
        words = line.split(" ")
        length.append(len(words))
    f.close()

    return questions,reviews,labels, length

def train_model(name,classifier, feature_vector_train, label, feature_vector_valid,valid_y, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)

    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)

    if is_neural_net:
        predictions = predictions.argmax(axis=-1)

    accuracy = accuracy_score(valid_y,predictions )

    tn, fp, fn, tp = confusion_matrix(valid_y,predictions).ravel()
    cm = [name,tn, fp, fn, tp, accuracy ]
    return accuracy , cm, predictions

def main(timestr):#if __name__ == "__main__":
    print('Started with the process of Algorithms')
    questions_train,rev_train,labels_train,len1=loadData("Final_Output_"+timestr+"/"+'final_balanced_'+timestr+'.txt')
    questions_test,rev_test,labels_test,len2=loadData("Final_Output_"+timestr+"/"+'final_'+timestr+'.txt')

    fn_analysis = "Final_Output_"+timestr+"/"+"Final_Analysis/"
    os.mkdir(fn_analysis)

    #Build a counter based on the training dataset
    counter = CountVectorizer()
    counter.fit(rev_train)

    #count the number of times each term appears in a document and transform each doc into a count vector
    counts_train = counter.transform(rev_train)#transform the training data
    counts_test = counter.transform(rev_test)#transform the testing data

    # word level tf-idf
    tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
    tfidf_vect.fit(rev_train)
    xtrain_tfidf =  tfidf_vect.transform(rev_train)
    xvalid_tfidf =  tfidf_vect.transform(rev_test)

    # ngram level tf-idf
    tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
    tfidf_vect_ngram.fit(rev_train)
    xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(rev_train)
    xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(rev_test)

    # characters level tf-idf
    tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
    tfidf_vect_ngram_chars.fit(rev_train)
    xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(rev_train)
    xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(rev_test)

    rev_test_excel = []
    for line in range(len(rev_test)):
        if len(rev_test[line]) > 30000:
            rev_test_excel.append(rev_test[line][:30000])

        else:
            rev_test_excel.append(rev_test[line][:])

    col = ["Algorithm","True Negative","False Positive","False Negative","True Positive","Accuracy"]

    # Naive Bayes on Count Vectors
    accuracy,cm, predictions = train_model("Naive Bayes on Count Vectors",MultinomialNB(), counts_train, labels_train, counts_test, labels_test)
    df_algorithm_analysis = pd.DataFrame([cm],columns = col)
    print ("NB, Count Vectors: ", accuracy)

    df_buffer = pd.DataFrame({'Question': questions_test,'Answer': rev_test_excel,'Actual': labels_test, 'Predicted': predictions})
    df_buffer.to_csv(fn_analysis+"NB_Count_Vectors.csv")

    # Naive Bayes on Word Level TF IDF Vectors
    accuracy,cm, predictions = train_model("Naive Bayes on Word Level TF IDF Vectors",MultinomialNB(), xtrain_tfidf, labels_train, xvalid_tfidf, labels_test)
    print ("NB, Word Level: ", accuracy)
    df_buffer = pd.DataFrame({'Question': questions_test,'Answer': rev_test,'Actual': labels_test, 'Predicted': predictions})
    df_buffer.to_csv(fn_analysis+"NB_Word_lvl_tfidf.csv")

    df_nb2 = pd.DataFrame([cm],columns = col)
    df_algorithm_analysis = df_algorithm_analysis.append(df_nb2)

    # Naive Bayes on Ngram Level TF IDF Vectors
    accuracy,cm, predictions = train_model("Naive Bayes on Ngram Level TF IDF Vectors",MultinomialNB(), xtrain_tfidf_ngram, labels_train, xvalid_tfidf_ngram, labels_test)
    print ("NB, Ngram Level: ", accuracy)

    df_buffer = pd.DataFrame({'Question': questions_test,'Answer': rev_test,'Actual': labels_test, 'Predicted': predictions})
    df_buffer.to_csv(fn_analysis+"NB_Ngram_lvl_tfidf.csv")

    df_nb3 = pd.DataFrame([cm],columns = col)
    df_algorithm_analysis = df_algorithm_analysis.append(df_nb3)

    # Naive Bayes on Character Level TF IDF Vectors
    accuracy,cm, predictions = train_model("Naive Bayes on Character Level TF IDF Vectors",MultinomialNB(), xtrain_tfidf_ngram_chars, labels_train, xvalid_tfidf_ngram_chars, labels_test)
    print ("NB, CharLevel Vectors: ", accuracy)

    df_buffer = pd.DataFrame({'Question': questions_test,'Answer': rev_test,'Actual': labels_test, 'Predicted': predictions})
    df_buffer.to_csv(fn_analysis+"NB_Char_lvl_tfidf.csv")

    df_nb4 = pd.DataFrame([cm],columns = col)
    df_algorithm_analysis = df_algorithm_analysis.append(df_nb4)

    # RF on Count Vectors
    accuracy,cm, predictions = train_model("Random Forest on Count Vectors", ensemble.RandomForestClassifier(), counts_train, labels_train, counts_test, labels_test)
    print ("RF, Count Vectors: ", accuracy)

    df_buffer = pd.DataFrame({'Question': questions_test,'Answer': rev_test,'Actual': labels_test, 'Predicted': predictions})
    df_buffer.to_csv(fn_analysis+"RF_Count_Vectors.csv")

    df_RF1 = pd.DataFrame([cm],columns = col)
    df_algorithm_analysis = df_algorithm_analysis.append(df_RF1)

    # RF on Word Level TF IDF Vectors
    accuracy,cm, predictions = train_model("Random Forest on Word Level TF IDF Vectors", ensemble.RandomForestClassifier(), xtrain_tfidf, labels_train, xvalid_tfidf, labels_test)
    print ("RF, WordLevel TF-IDF: ", accuracy)

    df_buffer = pd.DataFrame({'Question': questions_test,'Answer': rev_test,'Actual': labels_test, 'Predicted': predictions})
    df_buffer.to_csv(fn_analysis+"RF_Word_lvl_tfidf.csv")

    df_RF2 = pd.DataFrame([cm],columns = col)
    df_algorithm_analysis = df_algorithm_analysis.append(df_RF2)

    print(df_algorithm_analysis)
    df_algorithm_analysis.to_csv("Final_Output_"+timestr+"/"+"Final_Analysis.csv")

    print('Ended with the process of Algorithms')
