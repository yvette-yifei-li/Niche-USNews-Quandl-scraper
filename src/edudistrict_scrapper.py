from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import time
import pandas as pd
import random
import get_county

#This function scrapped selected data on one page
def get_one_page(grade, driver):
    print('Scrap each page may take up to 100 seconds, please wait for a while')
    if grade:
        time.sleep(random.randint(60,90))
    else:
        time.sleep(random.randint(80,90))
    #driver.get(url)
    try:
        cookie_ok = driver.find_element_by_xpath("/html/body/div[2]/div/div/button").click()
    except:
        pass

    #locate data
    k12s = driver.find_elements_by_xpath("/html/body/div[1]/div/section/main/div/div/section/div[2]/ol/li")
    time.sleep(4)
  
    onepage = list()
    #for each page, go through all the universities list on it
    for k12 in k12s:
        k12info = list()
        
        try:
            name = k12.find_element_by_tag_name('h2')
            name = name.text
            
            try:
                
                rank = k12.find_element_by_class_name('search-result-badge')
                rank = rank.text.split()[0].strip('#')
            
            except:
                rank = 'NaN'

            try:
                location = k12.find_elements_by_class_name('search-result-tagline__item')
                for i in range(len(location)):
                    if 'CA' in location[i].text:
                        city = location[i].text
                        city = city.split(',')[0]
            
            except:
                city = 'NaN'

            try:
                grade = k12.find_elements_by_tag_name('figure')
                grade = grade[0].text.split()[0]
            
            except:
                grade = 'NaN'
                
            try:
                sponsored = k12.find_element_by_class_name('search-result__sponsored-bar')
                sponsored = sponsored.text
                
            except:
                sponsored = 'not sponsored'
            
            try:
                county = get_county.get_county_byedu(name)
                if county == 'NaN':
                    county = get_county.get_county_bycity(city)
                
            except:
                county = 'NaN'

            k12info.extend([county, city, name, rank, grade, sponsored])
            onepage.append(k12info)                                         
        
        except:
            continue
    #print(onepage_univ)
            
    return onepage


def main(version, grade=False):
    
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #option.add_argument('--proxy-server=http://172.106.165.2:2926')
    try:
        if version == 'mac':
            driver = Chrome(options = option, executable_path = '../chromedriver/chromedriver_mac')
        elif version == 'win':
            driver = Chrome(options = option, executable_path = '../chromedriver/chromedriver_win32.exe')
        elif version == 'linux_64':
            driver = Chrome(options = option, executable_path = '../chromedriver/chromedriver_linux64')
        else:
            print('Please select --version from {mac, win_64, linux_64} or download the corresponding version and change the working directory')
            quit()
    except OSError:
        print('Error message: Please check the Firefox and geckodriver version or the secure and privacy setting to make sure that geckodriver is running smoothly')
        quit()

    driver.set_window_position(0, 0)
    driver.set_window_size(580, 1080)

    #get the number of total pages
    url = 'https://www.niche.com/k12/search/best-school-districts/s/california/'
    driver.get(url)
    pages = driver.find_element_by_xpath("/html/body/div[1]/div/section/main/div/div/section/div[3]/section/div/ul/li/div/div")
    pages = pages.text.split()[2]

    k12list = list()

    if grade:
        for i in range(1,4):           
            if i == 1:
                content = get_one_page(grade, driver)
            else:
                url = f'https://www.niche.com/k12/search/best-school-districts/s/california/?page={i}'
                driver.get(url)
                time.sleep(10)
                content = get_one_page(grade, driver)
                
            k12list.extend(content)
            print(f'Page {i}/3 successfully scrapped at %s'%time.ctime())    

    else:
        for i in range(1,int(pages)+1):
            #print(pages)
            if i == 1:
                content = get_one_page(grade, driver)  
            else:
                url = f'https://www.niche.com/k12/search/best-school-districts/s/california/?page={i}' 
                driver.get(url)
                time.sleep(10)
                content = get_one_page(grade, driver)
            
            k12list.extend(content)
            print(f'Page {i}/{pages} successfully scrapped at %s'%time.ctime())
        
    driver.close()
    
    df = pd.DataFrame(k12list, columns = ['County', 'City', 'School_district', 'Ranking', 'Grade', 'Sponsored'])
    df = df[df['Sponsored'] == 'not sponsored'] 
    k12_f = df.drop(columns=['Sponsored'])
    
    if grade:
        k12_f.to_csv('../data/edu_sampleset.csv', index = False)
        print('The scrapped k12 education district sample dataset has been saved as edu_sampleset.csv')
    else:
        k12_f.to_csv('../data/edu_fullset.csv', index = False)
        print('The scrapped k12 education district dataset has been saved as edu_fullset.csv')

    return k12_f   

if __name__ == "__main__": 
    main(version='mac', grade=False)
