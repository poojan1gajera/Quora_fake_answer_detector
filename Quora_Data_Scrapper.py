from selenium import webdriver
import time
import os
import Labelling_Responses
from Labelling_Responses import *

DEBUG = 0 # while debugging DEBUG = 1

def answer_crawler(url,timestr):
#open the browser and visit the url
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(url)
#scroll down to load more tweets
    src_updated = browser.page_source
    src = ""
    while src != src_updated:
        time.sleep(.4)
        src = src_updated
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        src_updated = browser.page_source
#name of the question
    question=url[22:].split('?')[0]
    if(DEBUG):print(question)
#find all elements with a class 'AnswerBase'
    responses=browser.find_elements_by_class_name('AnswerBase')
#open file to write the answers
    answers=open("Final_Output_"+timestr+"/"+'response_'+timestr+'.txt','a+')
    if(DEBUG):print("Final_Output_"+timestr+"/"+'response_'+timestr+'.txt')
    users_link=open("Final_Output_"+timestr+"/"+'users_url'+timestr+'.txt','a+',encoding='utf8')
    if(DEBUG):print("Final_Output_"+timestr+"/"+'users_url'+timestr+'.txt')
    ans,user,user_cred,user_link='NA','Anonymous','NA','NA'
# running through each response
    for response in responses:
        all_links=[]
#Username
        try: user=response.find_element_by_class_name("user").text
        except :
            if(DEBUG):print('no User')
#User Credentials
        try: user_cred=response.find_element_by_class_name("NameCredential").text
        except:
            if(DEBUG):print('no user_credentials')
#Answer
        try: ans=response.find_element_by_class_name("ui_qtext_expanded").text
        except:
            if(DEBUG):print('no ans')
#User Link
        try: user_link=response.find_element_by_class_name('feed_item_answer_user').find_element_by_css_selector('a').get_attribute('href')
        except:
            if(DEBUG):print('no link')
        if (DEBUG):print(user,user_cred,ans)
#all links to figure out answers that are marketing their products
        pop_links=response.find_elements_by_class_name('qlink_container')
        if len(pop_links):
            for link in pop_links:
                all_links.append(link.find_element_by_css_selector('a').get_attribute('href'))
        if (DEBUG):print(user,all_links)
#Write in the File
        try:
#Writting question, user, user credentials, answer, all links in responses.txt
            answers.write(question +'\t'+'$split$'+'\t'+ user.replace('\n',' ') +'\t'+'$split$'+'\t'+ user_cred.replace('\n',' ') +'\t'+'$split$'+'\t'+ ans.replace('\n',' ') +'\t'+'$split$'+'\t'+ ' '.join(all_links) +'\n')
#Writting users_url in users_url.txt
            users_link.write(user_link.replace('\n',' ') + '\n')
        except Exception as ex:
            print('exception',ex)
#Close file and Browser
    answers.close()
    users_link.close()
    browser.quit()

def get_related_questions(url,i,que_list,timestr):
#ending the recursive funciton
    if i==1:
        q_url_file=open("Final_Output_"+timestr+"/"+'question_urls'+timestr+'.txt','a+')
#removing duplicates before adding to the file-
        for link in list(set(que_list[:10])):
            q_url_file.write(link+'\n')
        print('DONE GETTING RELATED QUESTIONS, Number of related questions found:',str(len(list(set(que_list)))))
        return len(list(set(que_list)))
    question_url=que_list
#open the browser and visit the url
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get(url)
#scroll down to load more tweets
    src_updated = browser.page_source
    src = ""
    while src != src_updated:
        time.sleep(.4)
        src = src_updated
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        src_updated = browser.page_source
#find all elements with a class 'related_question'
    questions = browser.find_elements_by_css_selector('li.related_question')
#running through each question to get the link
    ques_url='NA'
    for question in questions:
        if (DEBUG):print(question.text)
        try: ques_url=question.find_element_by_css_selector('a').get_attribute('href')
        except:
            if(DEBUG):print('no ques url')
        question_url.append(ques_url)
    browser.quit()
#removing duplicates before adding to the list
    list(set(question_url))
#recursive call with an increament in i value
    get_related_questions(question_url[i],i+1,question_url,timestr)

if __name__ == '__main__':
    print('Started with the process of Quora Data scrapping')
    timestr = time.strftime("%Y_%m_%d-%H_%M_%S") # to name the file/folder according to the time of creation
    final_dir = "Final_Output_"+timestr
    os.mkdir(final_dir)

    url1='https://www.quora.com/What-is-an-Uber-clone'#https://www.quora.com/How-does-Uber-earn-their-profits
    #answer_crawler(url1,timestr)
    emp_list=[]
    total_questions=get_related_questions(url1,0,emp_list,timestr)
    questions_links_r=open("Final_Output_"+timestr+"/"+'question_urls'+timestr+'.txt','r')
    i=0
    for ques in questions_links_r:
        i+=1
        ques=ques.split('\n')
        answer_crawler(ques[0],timestr)
        print('answer_crawler done for:'+str(i)+'/'+ str(total_questions))

    print('Ended with the process of Quora Data scrapping')
    Labelling_Responses.main(timestr)
