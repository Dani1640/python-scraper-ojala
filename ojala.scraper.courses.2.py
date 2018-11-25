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

# Get config from plain text file
def getConfigAndCoursesForDownload():
    f = open('config.ojala2.txt')
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
        # links
        else:
            courses.append(line)
    return config, directory, courses, path_chrome_dv

# Get Links from all Course
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

def getAllCourses(driver, url_page_group):
    links=[]
    driver.get(url_page_group)
    time.sleep(3)
    last_num_page = driver.find_element_by_class_name('»').find_element_by_tag_name('a').get_attribute('href')
    last_num_page = int(last_num_page[ last_num_page.find('page=')+5 : ])
    for page in range(1,last_num_page+1):
        driver.get(url_page_group+'?page='+str(page))
        time.sleep(3)
        for course in driver.find_element_by_id('list-auth-items').find_elements_by_class_name('col-md-4'):
            link = course.find_element_by_class_name('caption').find_element_by_tag_name('a').get_attribute('href')
            links.append(link)
    return links

# Download All Videos from a Course
def DownloadVideosOfCourse(driver,chapters,directory):
    directory_new = directory + "\\" + DeleteCharactesSpecials(chapters[0][2].replace('Ojala | ', '').replace(':', ''))
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
            new_name_file = DeleteCharactesSpecials(chapter[1])
            name_file = directory_new + '\\' + new_name_file + ".mp4"
            if not(url_video == ''):
                if not os.path.exists(name_file):
                    try:
                        request.urlretrieve( url_video , name_file ) 
                        print(name_file + ' OK')
                    except:
                        #print(str(FileNotFoundError) + 'ERROR ')
                        print(name_file + ' ERROR ')
                else:
                    print(name_file + ' YA DESCARGADO')
        
        
            

        else:
            print(chapter[0]+' OK')
            

def CreateDirectoryOfCourse(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def DeleteCharactesSpecials(word):
    word = word.replace('\\','')
#    word = word.replace('\/','')
    word = word.replace(':','')
    word = word.replace('*','')
    word = word.replace('?','')
    word = word.replace('"','')
    word = word.replace('<','')
    word = word.replace('>','')
    word = word.replace('|','')
    return word

def SaveLinksFileTXT(links):
    file1 = open(r"Links.txt","w+") 
    txt = ''
    for link in links:
        txt += link + '\n'
    file1.write(txt)
    file1.close() 
    print('Links guardados')

def main():
    #Get config from plain text file
    config, directory, courses, path_chrome_dv = getConfigAndCoursesForDownload()
    #Setup chrome-driver
    driver = setupChrome(path_chrome_dv, directory)
    #Login
    logInOjala(driver,config)
    #Find all courses from plain text file
    for url_page_group in courses:
        links  = getAllCourses(driver, url_page_group)
        SaveLinksFileTXT(links)
        for url_course in links:
            if '<OK>' not in url_course:
                chapters = getAllLinkByCourse(driver,url_course)
                DownloadVideosOfCourse(driver,chapters,directory)
            else:
                print(url_course + ' DESCARGADO')

    driver.close()
    print('**** FIN ****')


main()