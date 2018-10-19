# Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib import request
import time
import os

# Setup Scrapper 
def setupChrome(path_chrome_dv, directory):
    options = Options()
    options.add_experimental_option("prefs", {
    "download.default_directory": directory ,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome( path_chrome_dv ,chrome_options=options)
    return driver

# Login Web-Page
def logInOjala(driver,config):
    driver.get(r"https://oja.la/login")
    username = driver.find_element_by_name('LoginForm[username]')    
    password = driver.find_element_by_name('LoginForm[password]')
    username.send_keys(config[0])
    password.send_keys(config[1])
    driver.find_element_by_name('commit').click()
    time.sleep(3)

# Get Links from a Course
def getAllLinkByCourse(driver, url_page_course):
    links = []
    driver.get(url_page_course)
    time.sleep(3)
    for lesson in driver.find_element_by_class_name('lessons').find_elements_by_tag_name('a'):
        link = lesson.get_attribute('href')
        name_chapter = str(lesson.text.split('\n')[0])
        name_course = driver.title
        links.append([link,name_chapter,name_course])
    return links
#https://oja.la/curso/desarrollo-web/aprende-como-usar-google-analytics-de-forma-simple-para-tu-pagina-web-parte-II

# Get config from plain text file
def getConfigAndCoursesForDownload():
    f = open('config.ojala.txt')
    lines = f.readlines()
    courses = []
    config = []
    directory = '' 
    path_chrome_dv = ''  
    for x,line in enumerate(lines,1):
        line = line.replace('\n','')
        # user
        if x==1:
            config.append( line.split('|')[1] )
        # password
        elif x==2:
            config.append( line.split('|')[1] )
        # directory
        elif x==3:
            directory = line.split('|')[1]
        # chrome-driver
        elif x==4:
            path_chrome_dv = line.split('|')[1]
        else:
            courses.append(line)
    return config, directory, courses, path_chrome_dv

# Download All Videos from a Course
def DownloadVideosOfCourse(driver,chapters,directory):
    directory_new = directory + "\\" + chapters[0][2].replace('Ojala | ', '').replace(':', '')
    CreateDirectoryOfCourse(directory_new)
    for chapter in chapters:
        if '<OK>' not in chapter[0]:
            driver.get(chapter[0])
            time.sleep(4) 
            html = str(driver.page_source)
            html = html[ html.find('<video id="wistia_simple_video_') : ]
            html = html[ html.find('src="https://embedwistia-a.akamaihd.net/deliveries') : ]
            html = html[ html.find('https://embedwistia-a.akamaihd.net/deliveries') : ]
            url_video =  html[ : html.find('"') ]
            name_file = directory_new + '\\' + chapter[1] + ".mp4"
            
            if not(url_video == ''):
                if not os.path.exists(name_file):
                    try:
                        request.urlretrieve( url_video , name_file ) 
                        print(name_file + ' OK')
                    except:
                        #print(str(FileNotFoundError) + 'ERROR ')
                        print(name_file + 'ERROR ')
        else:
            print(chapter[0]+' ESTABA OK')
            

def CreateDirectoryOfCourse(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def main():
    #Get config from plain text file
    config, directory, courses, path_chrome_dv = getConfigAndCoursesForDownload()
    #Setup chrome-driver
    driver = setupChrome(path_chrome_dv, directory)
    #LogIn in WebPage
    logInOjala(driver,config)
    #Find all courses from plain text file
    for url_page_course in courses:
        if '<OK>' not in url_page_course:
            chapters = getAllLinkByCourse(driver,url_page_course)
            #Download All Videos of Course
            DownloadVideosOfCourse(driver,chapters,directory)
        else:
            print(url_page_course + ' YA DESCARGADO')

main()