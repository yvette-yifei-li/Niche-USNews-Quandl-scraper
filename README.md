# Niche-USNews-Quandl-scraper

This project aims at to investigate wheather healthcase and k12 education resource is related to the local housing price of each California county.

## CA_housing_price.ipynb

By introducing in the geographic visualization, this project reflects the distributio of k-12 education source, medical source, and the housing price. (You may need to have the .ipynb file opened locally to see the dynamic geographic visualization.)

To further explore the impact of neighbor counties, this project introduces some new features to study the areal (a county and its' neighbor counties) medical and k12 education resource.

Note: This file is 40+ Mb and it may sometimes run into issues to open it in the git preview. Please have it downloaded and open it locally.

## Some findings:

You need to open the .ipynb file to see the dynamic visualization with hover tages

### CA average home value distribution by county
![Image](https://github.com/yvette-yifei-li/Niche-USNews-Quandl-scraper/blob/main/images/Screen%20Shot%202020-12-30%20at%202.51.21%20AM.png)

### CA average hopital score by county
![Image](https://github.com/yvette-yifei-li/Niche-USNews-Quandl-scraper/blob/main/images/Screen%20Shot%202020-12-30%20at%202.51.33%20AM.png)

### CA average k12 education district score by county
![Image](https://github.com/yvette-yifei-li/Niche-USNews-Quandl-scraper/blob/main/images/Screen%20Shot%202020-12-30%20at%202.51.43%20AM.png)

### County only datasets
1. The data shows that both medical and education resource are correlated to the housing price of a county.

2. For both perspectives, the 'score' indexes have higher pearson's correlation coefficient compared to the 'number' indexes.

3. The Pearson’s correlation coefficient between the housing price and the score of hospitals of the county is 0.37 while p = .005, which indicates that there's low positive coefficiency.

4. The Pearson’s correlation coefficient between the housing price and the score of school districts of the county is 0.39 while p = .002, which indicates that there's low positive coefficiency.

### Areal datasets
1. Introducing in the impacts from neighbor counties will not increase the coefficiency between medical score and the home value. Using the areal best hospital score will even decrease the correlation.

2. Introducing in the impacts from neighbor counties will increase the coefficiency between education score and the home value. Their is a medium level of coefficiency between the areal average education score and the home value where corr. = 0.64 (p < .001).

3. Therefore, the home value(housing price) of a county is not only related to the local k12 education resource, but also the neighbor education resource.

4. However, similar result is not observed in the medical resource.

## edudistrict_scraper.py

This program scrappes the California k12 school district data from https://www.niche.com/k12/search/best-school-districts/s/california/
grade dataset is stored in edu_sampleset.csv
full dataset is stored in edu_fullset.csv
Note: Due to the rather strict anti-bot rules adopted by the website, that program may trigger the reCAPTCHA authentication after frequent run. You may have to manually solve the reCAPTCHA during the short pause. The program will move on after the browser turn back to the regular contents.

## hospital_scraper.py

This program scrappes the California hospitals ranking data from https://health.usnews.com/best-hospitals/area/ca
grade dataset is stored in hospitals_sampleset.csv
full dataset is stored in hospitals_fullset.csv

## zillow_api_scraper.py

This program crawls and filters out californis housing data on https://www.quandl.com/api/v3/datatables/ZILLOW
full dataset is stored in homevalue_fullset.csv

## get_county.py

This is a helper program that generates a comprehensive CA city, county, zip and fip code list
It also provides functions that help identify the corresponding county of given cities or zipcodes. 
This program will store the scrapped data in the '../data/CA_county_city_list1.csv' and the '../data/edulist.csv' .

## LI_YIFEI_proj2.py

This is the main program that packed all the programs above

This program takes three parameters:
    
    --source [remote,local]   
    'Choose to retrive data remotely or locally
    
    --grade [flag or not]   
     'flag to request a short version for datasets

    --version [mac, win, linux_64]  
    'This program utalize chromedriver to scrap some webpages, enter your OS version to run the corresponding chromedriver. Supported OSs are MacOS, Win-34, Win-64, and Linux-32.
    This parameter is required when choose to retrive data remotely.
