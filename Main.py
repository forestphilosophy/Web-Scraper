# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:39:30 2020

@author: jimmlin
"""
from selenium import webdriver
from time import sleep
import os,glob,shutil


dossiers = [26131,25029,35220]
chromedriver_location = "C:/Users/jimmlin/OneDrive - Deloitte (O365D)/Desktop/Grabber/chromedriver"
ukdbt_location = "https://teams.deloitte.nl/sites/rbbnkuhkbrdlngdocs/Calculation/_layouts/15/start.aspx#/Testing/Forms/AllItems.aspx?RootFolder=%2Fsites%2Frbbnkuhkbrdlngdocs%2FCalculation%2FTesting%2FDelta%20Team%2FCLT%20Runs%20%28Using%20UKDBT%29&FolderCTID=0x012000C7CA178B0F36B344B2FB445870D135F0&View=%7BD7E785F2%2D62DD%2D4443%2D82F2%2DB41827427A08%7D"
cltdbt_location = "https://teams.deloitte.nl/sites/rbbnkuhkbrdlngdocs/Calculation/_layouts/15/start.aspx#/Testing/Forms/AllItems.aspx?RootFolder=%2Fsites%2Frbbnkuhkbrdlngdocs%2FCalculation%2FTesting%2FDelta%20Team%2FCLT%20Runs%20%28Using%20CLTDBT%29&FolderCTID=0x012000C7CA178B0F36B344B2FB445870D135F0&View=%7BD7E785F2%2D62DD%2D4443%2D82F2%2DB41827427A08%7D"


def download_files(dbt_location):
    """
String manipulation, i.e removing spaces and commas in the dossiers list
to prepare it for string operations in the following iterations
"""
    list= []
    for i in dossiers:
        str(i).replace(' ','')
        list.append(i)
    list_str = [str(i) for i in list]
    
    for i in range(3):#iteration for the first 3 output folders, could potentially be improved to be more dynamic,however sufficient for the time being
        chromedriver = chromedriver_location
        driver = webdriver.Chrome(chromedriver)
        driver.get(dbt_location)
        driver.maximize_window()
        sleep(0.5)
        classes = driver.find_elements_by_class_name('ms-vb-title') #all the output folders
        classes[i].click()#iterations to click on different output folders
        sleep(0.5)
        table = driver.find_elements_by_class_name('ms-listviewtable')[0] #table within the output folders
        rows = table.find_elements_by_tag_name('tr') #all the rows within the output folders
        
        for j in rows: 
            if j.text[0:5] in list_str:
                list_str = [str for str in list_str if str != j.text[0:5]] #removing the dossier that has already been downloaded from the list to make sure only latest version is downloaded
                row = j
                dots1 = row.find_elements_by_tag_name('td')[3] #clicking on the first dots
                dots1.click()
                sleep(0.5)
                dots2 = dots1.find_elements_by_tag_name('span')[14] #clicking on the second dots
                dots2.click()
                sleep(0.5)
                download = dots2.find_elements_by_xpath("//*[contains(@id,'ID_DownloadACopy')]")[0]
                download.click()
                
        sleep(3)    
        driver.close()
        
        #breaking out the loop once the list_str is empty so program won't search the next output folder
        if not list_str:
            break
        
 def move_files(src,dst):
    """
    This function is sued to move downloaded files to desired location
    """
    src = "C:/Users/jimmlin/Downloads"
    dst = "C:/Users/jimmlin/OneDrive - Deloitte (O365D)/Desktop/Be Positive/folder_UKDBT"

    list_of_files = glob.glob('C:/Users/jimmlin/Downloads/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print (latest_file)

    try:
        shutil.move(latest_file,dst)
    except:
        print ('This dossier is already in the destination folder.')
        
#calling download and move_files functions   
download_files(ukdbt_location)
download_files(cltdbt_location)
move_files("C:/Users/jimmlin/Downloads","C:/Users/jimmlin/OneDrive - Deloitte (O365D)/Desktop/Be Positive/folder_UKDBT")


