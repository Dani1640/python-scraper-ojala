# Oja.la Scraper Script

With this script you can download all videos from oja.la e-learning platform.



# Instructions!
 - Complete file config.ojala.txt with this instructions:
  - line 1: user|tu@email.com
  - line 2: pass|YouPassword
  - line 3: Directorio|YouPathWhereDownloadFiles
  - line 4: ChromeDriver|PathWhereIsChromeDriver.exe

# Libraries:
```sh
  - from selenium import webdriver
  - from selenium.webdriver.common.keys import Keys
  - from selenium.webdriver.chrome.options import Options
  - from urllib import request
  - import time
  - import os
 ```
 Note: I created/use an environment in Anaconda Suite with Selenium library.
