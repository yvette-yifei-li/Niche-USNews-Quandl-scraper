# Niche-USNews-Quandl-scraper
    
## CA_housing_price.ipynb

This project aims at to investigate wheather the medical and k12 education resource is related to the local housing price of each CA county, by making use of the scraped data mentioned above.

By introducing in the geographic visualization, this project reflect the distributio of k-12 education source, medical source, and the housing price. (You may need to have the .ipynb file opened locally to see the dynamic geographic visualization.)

To further explore the impact of neighbor counties, this project introduces some new features to study the areal (a county and its' neighbor counties) medical and k12 education resource.


The project looks for a positive correlation between the education source, the medical source and housing price.
## edudistrict_sraper.py

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
