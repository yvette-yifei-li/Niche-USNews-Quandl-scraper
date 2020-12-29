from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import time
import pandas as pd
import get_county

def load_full_page(driver, grade=False):
    
    driver.get('https://health.usnews.com/best-hospitals/area/ca')

    #This page has a dynamic button 'load_more'
    #to fully load the webpage, the page has to be scrolled to the 'load_more' position

    i=0
    while True:
        #get the coordinate of the load_more button
        try:
            load_more = driver.find_element_by_xpath("/html/body/main/div/article/div/div[5]/div[1]/div/div/div[2]/div[2]/div/button")
            loc = load_more.location
            y = loc.get('y')

            #generate progress bar
            
            if grade:
                if round(y/80)>100:
                    a = 100
                else:
                    a = round(y/80)
            else:
                if round(y/780)>100:
                    a = 100
                else:
                    a = round(7/780)
            

            print('[', '='*a , '.'*(100-a),']', f'{a}%')
            
            #scroll the page down to the load_more button
            driver.execute_script(f"window.scrollTo(0, {y-200});")

            #wait for the potential new contents to be fully loaded
            time.sleep(10)
            loc_new = load_more.location

        except:
            #if the load_botton is not click-able, it means the page has been fully loaded
            print('The full page has been loaded.')
            break 

        #if the coordinate of the 'load_more' no longer changed, the current scroll-down webpage is fully loaded      
        if loc.get('y') == loc_new.get('y'):
            i+=1
            try:
                click_load_more = load_more.click()
                
            except:
                try:
                    #close the subscription pop-up
                    close_sub = driver.find_element_by_xpath('/html/body/section/div[1]/button').click()
                    click_load_more = load_more.click()
                except:
                    print('Please wait for a short while')
                    pass
        
        if grade:
            if i == 1:
                break

    return driver


def get_hospitals(driver, grade):
    #scrap the hospitals data
    hospitals = driver.find_elements_by_xpath("/html/body/main/div/article/div/div[5]/div[1]/div/div/div[2]/ol/li")                                        
    fullpage_hospitals = list()

    for hospt in hospitals:
        hosptinfo = list()
        try:
            name = hospt.text.split('\n')
            #print(name)
            hospital = name[0]
            city = name[1].split(',')[0]
            zipcode = name[1].split(',')[1].split()[1][:5]
            rank = name[2].split()[0].strip('#')
            
            #get county by calling the get_county functions
            county = get_county.get_county_bycity(city)
            if county == 'NaN':
                county = get_county.get_county_byzip(zipcode)
   
            try:
                rank = int(rank)
                rank = str(rank)
            except:
                rank = ''

            if hospital != 'AD':
                hosptinfo.extend([county, city, hospital, rank])

            if len(hosptinfo) == 4:
                fullpage_hospitals.append(hosptinfo)
            #print(hosptinfo)

        except:
                continue

    #save the scrapped data in a dafaframe
    df = pd.DataFrame(fullpage_hospitals, columns = ['County', 'City', 'Hospital', 'Ranking'])

    #save the scrapped data to different csv file based on whether it's the grade version or not
    if grade:
        df.to_csv('../data/hospitals_sampleset.csv', index = False)
    else:
        df.to_csv('../data/hospitals_fullset.csv', index = False)

    return df

def main(version, grade=False):

    #set up the chrome driver
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    try:
        if version == 'mac':
            driver = Chrome(options = option, executable_path = '../chromedriver/chromedriver_mac')
        elif version == 'win':
            driver = Chrome(options = option, executable_path = '../chromedriver/chromedriver_win32.exe')
        elif version == 'linux_64':
            driver = Chrome(options = option, executable_path = '../chromedriver/chromedriver_linux64')
        else:
            print('Please select --version from {mac, win, linux_64} or download the corresponding version and change the working directory')
            quit()
    except OSError:
        print('Error message: Please check the Firefox and Chromedriver version or the secure and privacy setting to make sure that Chromedriver is running smoothly')
        quit()

    driver.set_window_position(0, 0)
    driver.set_window_size(580, 1080)
    driver = load_full_page(driver, grade)
    df = get_hospitals(driver,grade)
    driver.close()

    if grade:
        print('The sample dataset has been fully scrapped and the data has been saved as hospitals_sampleset.csv')
    else:
        print('The page has been fully scrapped and the data has been saved as hospitals_fullset')
    
    return df

if __name__ == '__main__':
    main(version='mac',grade=True)
