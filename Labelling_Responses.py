# -*- coding: utf-8 -*-
import codecs
import time
import Algorithms

def duplicate_links_rule(list_of_urls_str):
#checking if LIST and SET of urls have same length, if not:there are some urls that have been used multiple times meaning its marketed.
    if (len(list_of_urls_str.split(" ")) != len(set(list_of_urls_str.split(" ")))) : return 1
    else : return 0

def spam_user_credentials_rule(user_credentials_str):
#list of words that can describe a person who is marketing his/her product in an answer More words can be added in the list
    list_of_spam_credentials=['marketing','business','developemnt','ceo','co-founder','sales']
    for word in user_credentials_str.split(' '):
        if word.lower() in list_of_spam_credentials : return 1
#will only come here if doesnt encounter return statement in for loop meaning all are good credentials
    return 0

def split_file_in_ratio(original_filename,train_filename,test_filename,train_ratio):
#count the total number of lines in the original file
    lines_count = len(codecs.open(original_filename).readlines())
#splitting the lines in ratios
    line_number_to_split = int(train_ratio * lines_count)
    with codecs.open(original_filename) as originalFile:
        allLines = originalFile.readlines()
        firstNLines, restOfTheLines = allLines[:line_number_to_split], allLines[(line_number_to_split+1):]
#writing the training file
    train_f = codecs.open(train_filename,'w')
    for line in firstNLines:
        train_f.write(line)
    train_f.close()
#writing the testing file
    test_f = codecs.open(test_filename,'w')
    for line in restOfTheLines:
        test_f.write(line)
    test_f.close()

def balanced_data(string):
    list_of_string = string.split("\n")
    flag_for_0 = "next"  # flag to see if already one 0 labeled item added or not
    flag_for_1 = "next"  # flag to see if already one 1 labeled item added or not
    final_balanced_string = ""

    for item in list_of_string:
        try:
            if (item[-1] == "0" and flag_for_0 == "next"):
                flag_for_0 = "taken"
                flag_for_1 = "next"
                final_balanced_string += item + "\n"
            elif (item[-1] == "1" and flag_for_1 == "next"):
                flag_for_0 = "next"
                flag_for_1 = "taken"
                final_balanced_string += item + "\n"
        except Exception as ex:
            break # break because of inbalanced labels dont worry about it
            #print("Exception because of inbalanced labels dont worry about it, you good to go",ex)

    return final_balanced_string

def labelling_answers(file):
    string = ""

    for line in file:
        try:
            split_line = line.split("$split$")
            sum_rule_value = 0
    #striping each element to remove spaces and \ts from both the sides
            for item in range(len(split_line)) :
                split_line[item] = split_line[item].strip()
    #input wil be all the urls in string format
            duplicate_links_rule_value = duplicate_links_rule(split_line[-1])
            sum_rule_value += duplicate_links_rule_value
    #input will be user credentials in string format
            spam_user_credentials_rule_value = spam_user_credentials_rule(split_line[2])
            sum_rule_value += spam_user_credentials_rule_value
    #check if the sum of all the rules are greater than 0 meaning even if one rule is satisfied
            if sum_rule_value > 0:
                QA_with_label = (split_line[0] + "\t" + split_line[-2] + "\t" + "1" + "\n")
            else:
                QA_with_label = (split_line[0] + "\t" + split_line[-2] + "\t" + "0" + "\n")

            string += QA_with_label

        except Exception as ex:
            #print(ex," labelling answers",split_line[0])
            continue

    return string

def main(timestr):
#if __name__ == "__main__":
    print('Started with the process of Labelling_Responses')

# the string contains all the responses labelled and it is possible that the labels may be imbalanced
#    string = labelling_answers(codecs.open("Final_Output_"+timestr+"/"+'response_'+timestr+'.txt','r',encoding='utf-8', errors='ignore'))
    string = labelling_answers(codecs.open('final_response_Copy.txt','r',encoding='utf-8', errors='ignore'))
    res = codecs.open("Final_Output_"+timestr+"/"+'final_'+timestr+'.txt','a+')
    res.write(string)
    res.close()
# split file in ratio is used to split the files in test and train data
    split_file_in_ratio("Final_Output_"+timestr+"/"+'final_'+timestr+'.txt',"Final_Output_"+timestr+"/"+'final_train_'+timestr+'.txt',"Final_Output_"+timestr+"/"+'final_test_'+timestr+'.txt',0.7)

# balanced_string contains balanced labels of 1 and 0 with which we can go ahead and train our algorithms
    balanced_string = balanced_data(string)
    res = codecs.open("Final_Output_"+timestr+"/"+'final_balanced_'+timestr+'.txt','a+')
    res.write(balanced_string)
    res.close()
# split file in ratio is used to split the files in test and train data
    split_file_in_ratio("Final_Output_"+timestr+"/"+'final_balanced_'+timestr+'.txt',"Final_Output_"+timestr+"/"+'final_balanced_train_'+timestr+'.txt',"Final_Output_"+timestr+"/"+'final_balanced_test_'+timestr+'.txt',0.7)
    print('Ended with the process of Labelling_Responses')
    Algorithms.main(timestr)
