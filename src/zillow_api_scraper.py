import requests
import pandas as pd
import quandl
from bs4 import BeautifulSoup
import json
import os

#This program does not take'grade' parameter since it only makes two requests to retrieve two different dataset.

def get_region_code():  
    '''
    This api provides both api method and wrapped python library
    Below commented expressions are the wrapped lib access
    '''
    #quandl.ApiConfig.api_key = 'LHZrqhRuQW7Sxe-uxeyh'
    #d = quandl.get_table('ZILLOW/REGIONS', region_type  = 'city')
  
    d = requests.get('https://www.quandl.com/api/v3/datatables/ZILLOW/REGIONS?region_type=city&api_key=LHZrqhRuQW7Sxe-uxeyh')
    d = d.json()
    d = d.get('datatable').get('data')
    # store the crawled data in a dafaframe
    d = pd.DataFrame(d, columns = ['region_id', 'region_type', 'region'])
    
    citylist = list()
    countylist = list()
    statelist = list()
    
    # filter out the city, county and state data that we needed
    for region in d['region']:
        reglist = str(region).split(';')
        citylist.append(reglist[0])
        statelist.append(reglist[1])
        countylist.append(reglist[-1])
    
    d['city'] = citylist
    d['county'] = countylist
    d['state'] = statelist
    
    d = d.drop(columns = ['region', 'region_type'])
    
    cacode = pd.DataFrame()
    
    reg = list()
    cityl = list()
    countyl = list()
    
    # filter out the California home value data
    for reg_id, city, county, state in zip(d['region_id'],d['city'], d['county'], d['state']):
        state = state.lstrip()
        if state == 'CA':
            county = county.replace(' County', '')
            reg.append(reg_id)
            cityl.append(city)
            countyl.append(county)
    cacode['region_id'] = reg
    cacode['city'] = cityl
    cacode['county'] = countyl
    print('Region code successfully scrapped')
    
    # here returns a DataFrame variable with 3 columns of region_id, city, and county
    return cacode


# acquired region_id, we can use the region_id to map the corresponding house value
def get_home_value(region_code):
    '''
    same as above, both api and wrapped lib are able to query the value data
    here we use the wrapped lib
    '''
    quandl.ApiConfig.api_key = 'LHZrqhRuQW7Sxe-uxeyh'
    d = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id = region_code)  
    # the data is stored by month, and we only need the house price for past 12 months
    year_data  = d.iloc[0:12, 1:4]
    
    # return the average house value of CA cities for each month in the recent year
    return year_data


def main():

    # store the house value data by city and by month
    res = pd.DataFrame()
    reg = get_region_code()
    
    countylist = []
    citylist = []
    reglist = []
    datelist = []
    valuelist = []
    
    for reg, city, county in zip(reg['region_id'], reg['city'], reg['county']):
        valuedf = get_home_value(reg)
        for date, value in zip(valuedf['date'], valuedf['value']):
            countylist.append(county)
            citylist.append(city)
            reglist.append(reg)
            datelist.append(date)
            valuelist.append(value)
    
    res['County'] = countylist
    res['City'] = citylist
    res['Region_id'] = reglist
    res['Collect_date'] = datelist
    res['Home_value'] = valuelist
    
    # check if the ../data/ directory exists 
    # if not, create the directory
    dir = '../data/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    # store the full house value dataset by city by month in the csv file
    res.to_csv('../data/homevalue_fullset.csv', index= False)
    print('The crawled home value by city dataset has been saved as homevalue_fullset.csv')
    
    #mean = res.groupby('County').mean().round(2)
    #mean = mean.sort_values(by=['Home_value'], ascending = False)
    
    #Store the average house value by county for the past 12 months in the csv file
    #mean.to_csv('../data/home_value_bycounty.csv')
    #print('The home value by county dataset has been saved as home_value_bycounty.csv')
            
    return res

if __name__ ==  "__main__":
    main()
