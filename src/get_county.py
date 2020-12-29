from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os


def get_city_list():
    
    driver = Chrome(executable_path = '../chromedriver/chromedriver_mac')
    url = 'https://www.zipcodestogo.com/California/'
    driver.get(url)
    pages = driver.find_elements_by_xpath("/html/body/div/div[2]/table/tbody/tr/td/table/tbody/tr/td")
    
    clist = list()
    for page in pages:
        page = page.text
        
        if page != 'View Map':
            clist.append(page)
    
    clist = clist[5:]
    ziplist = list()
    citylist= list()
    countylist = list()
    for i in range(len(clist)):
        if i%3 == 0:
            #print(clist[i])
            ziplist.append(clist[i])
        elif i%3 == 1:
            #print(clist[i])
            citylist.append(clist[i])
        elif i%3 == 2:
            #print(clist[i])
            countylist.append(clist[i])
    
    ctdf = pd.DataFrame()
    ctdf['Zipcode'] = ziplist
    ctdf['County'] = countylist
    ctdf['City'] = citylist
    ctdf = ctdf.sort_values(by = ['County'])
    #ctdf = ctdf.reset_index(drop = True)
    
    dir = '../data/'

    if not os.path.exists(dir):
        os.makedirs(dir)

    driver.close()

    #scrape the fip codes data
    content = requests.get("https://www.nrcs.usda.gov/wps/portal/nrcs/detail/ca/home/?cid=nrcs143_013697")
    soup = BeautifulSoup(content.content, 'html.parser')
    c = soup.findAll('td')
    
    infolist = list()
    res = dict()
    
    for i in range(len(c)):
        try:
            a = c[i].get_text().strip()
            infolist.append(a)
        except:
            continue
        
    #print(infolist)
    for i in range(len(infolist)):
        if infolist[i] == 'CA':
            fip = infolist[i-2]
            county = infolist[i-1]
            res[county] = fip
    #print(res)
    
    fiplist = list()
    #cty = pd.read_csv('../data/CA_county_city_list1.csv')

    for a in ctdf['County']:
        fiplist.append(str(res.get(a)))

    ctdf['Fips'] = fiplist
    ctdf.to_csv('../data/CA_county_city_list1.csv', index = False)

    return ctdf

def get_edu_district_list():

    content = requests.get("https://www.greatschools.org/schools/districts/California/CA/")
    soup = BeautifulSoup(content.content, 'html.parser')
    c = soup.findAll('td')

    edulist = list()
    citylist = list()
    countylist = list()


    for i in range(len(c)):
        a = c[i].get_text().strip()
        if i%3 == 0:
            edulist.append(a)
        elif i%3 == 1:
            citylist.append(a)
        else:
            countylist.append(a)
    edu = pd.DataFrame()
    edu['Edu_district'] = edulist
    edu['City'] = citylist
    edu['County'] = countylist

    dir = '../data/'

    if not os.path.exists(dir):
        os.makedirs(dir)    

    edu.to_csv('../data/edulist.csv', index = False)

def get_county_byedu(edu):

    dir = '../data/edulist.csv'

    if os.path.exists(dir):
        cty = pd.read_csv(dir)

        try:
            county = cty[cty['Edu_district']==edu]['County'].values[0]
        except:
            county = 'NaN'
    
    else:
        get_edu_district_list()
        cty = pd.read_csv(dir)

        try:
            county = cty[cty['Edu_district']==edu]['County'].values[0]
        except:
            county = 'NaN'

    return county


def get_county_bycity(cityname):
    
    dir = '../data/CA_county_city_list1.csv'

    if os.path.exists(dir):
        cty = pd.read_csv(dir)

        try:
            county = cty[cty['City']==cityname]['County'].values[0]
        except:
            county = 'NaN'
    
    else:
        get_city_list()
        cty = pd.read_csv(dir)

        try:
            county = cty[cty['City'].get_==cityname]['County'].values[0]
        except:
            county = 'NaN'
    
    return county


def get_county_byzip(zipcode):

    dir = '../data/CA_county_city_list1.csv'

    if os.path.exists(dir):
        cty = pd.read_csv(dir)
        
        try:
            county = cty[cty['Zipcode']==zipcode]['County'].values[0]
        except:
            county = 'NaN'
   
    else:
        get_city_list()
        cty = pd.read_csv(dir)

        try:
            county = cty[cty['Zipcode']==zipcode]['County'].values[0]
        except:
            county = 'NaN'

    return county


def get_fips(county):

    dir = '../data/CA_county_city_list1.csv'

    if os.path.exists(dir):
        cty = pd.read_csv(dir, converters={'Fips': lambda x: str(x)})
        
        try:
            fips = cty[cty['County']==county]['Fips'].values[0]
        except:
            fips = 'NaN'

    else:
        get_city_list()
        cty = pd.read_csv(dir, converters={'Fips': lambda x: str(x)})
        
        try:
            fips = cty[cty['County']==county]['Fips'].values[0] 
        except:
            fips = 'NaN'
    
    return fips

if __name__ == "__main__":
    get_city_list()