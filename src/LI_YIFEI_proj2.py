import argparse
import sys
import pandas as pd
import os
import zillow_api_scraper
import edudistrict_scraper
import hospital_scraper


def main():

    #add parameters
    parser = argparse.ArgumentParser(description='Enter the parameters to run the program')

    #grade
    parser.add_argument('--grade', type=bool, 
                        nargs = '?', const=True, default = False,
                        help='flag for the sample datasets or leave it blank for the full datasets')

    #source
    parser.add_argument('--source', choices=['remote', 'local'],
                        required=True,
                        type = str,
                        help = 'select to fetch remote or local datasets')

    #your OS version, required when retrive data remotely
    parser.add_argument('--version', choices=['mac', 'win', 'linux_64'],
                        type = str,
                        help = 'select your operating system from mac, win, linux_64')

    args = parser.parse_args()
    source = args.source
    grade = args.grade
    version = args.version

    if source == 'remote':
        
        d = {False:'full', True:'sample'}  
        
        # fetch remote school district sample dataset
        print('\n',f'(1/3) Now scrapping the k12 school district {d.get(grade)} dataset from https://www.niche.com/k12/search/best-school-districts/s/california/')
        edu = edudistrict_scraper.main(grade=bool(grade), version=version)
        print('\n', '='*20, f'First 5 rows of the k12 school district {d.get(grade)} dataset [remote]', '='*20, '\n')
        print(edu.head())
        
        #fetch remote hospital sample dataset
        print('\n',f'(2/3) Now scrapping the hospital {d.get(grade)} dataset from https://health.usnews.com/best-hospitals/area/ca')
        hpt = hospital_scraper.main(grade=bool(grade), version=version)
        print('\n', '='*20, f'First 5 rows of the hospitals {d.get(grade)} dataset [remote]', '='*20, '\n')
        print(hpt.head())
        
        #fetch remote home value sample dataset
        print('\n','(3/3) Now scrapping the home value dataset from https://www.quandl.com/api/v3/datatables/ZILLOW')
        home = zillow_api_scraper.main()
        print('\n','='*20, 'First 5 rows of the home value dataset [remote]', '='*20, '\n')
        print(home.head())
        
        print('\n','Datasets are successfully fetched remotely. Sample school district dataset, hopitals dataset, and home value dateset are stored as the first, second, and the third element of the returned tuple')


    elif source == 'local':
        
        #Fetch local k12 school district dataset
        edu1 = '../data/edu_fullset.csv'
        edu2 = '../data/edu_sampleset.csv'

        if os.path.exists(edu1):
            edu = pd.read_csv(edu1)
            a1 = 'First 5 rows of the k12 school district full dataset [local]'
            print('\n', '='*20, a1, '='*20, '\n')
            print(f'[The data is retrived from the file edu_fullset.csv]')
            print('-'*(len(a1)+43))
            print(edu.head())
        elif os.path.exists(edu2):
            edu = pd.read_csv(edu2)
            a2 = 'First 5 rows of the k12 school district sample dataset [local]'
            print('\n', '='*20, a2, '='*20, '\n')
            print(f'[The data is retrived from the file edu_sampleset.csv]')
            print('-'*(len(a2)+43))
            print(edu.head())
        else:
            print('''There is no k12 school district dataset stored locally. Please run the program using $--source remote to acquire the dataset.''')
    
        #Fetch local hospital dataset
        hpt1 = '../data/hospitals_fullset.csv'
        hpt2 = '../data/hospitals_sampleset.csv'
        
        if os.path.exists(hpt1):
            hpt = pd.read_csv(hpt1)
            a3 = 'First 5 rows of the hospitals full dataset [local]'
            print('\n', '='*20, a3, '='*20, '\n')
            print(f'[The data is retrived from the hospitals_fullset.csv]')
            print('-'*(len(a3)+43))
            print(hpt.head())
        elif os.path.exists(hpt2):
            hpt = pd.read_csv(hpt2)
            a4 = 'First 5 rows of the hospitals sample dataset [local]'
            print('\n', '='*20, b, '='*20, '\n')
            print(f'[The data is retrived from the hospitals_sampleset.csv]')
            print('-'*(len(a4)+43))
            print(hpt.head())
        else:
            print('''There is no hospital dataset stored locally.
                     Please run the program using $--source remote to acquire the dataset.''')
        
        #Fetch local home value dataset
        home = '../data/homevalue_fullset.csv'

        if os.path.exists(home):
            home = pd.read_csv(home)
            a5 = 'First 5 rows of the home value dataset [local]'
            print('\n', '='*20, a5, '='*20, '\n')
            print(f'[The data is retrived from the homevalue_fullset.csv]')
            print('-'*(len(a5)+43))
            print(home.head())
        else:
            print('''There is no home value dataset stored locally.
                     Please run the program using $--source remote to acquire the dataset.''')
        
        print('Datasets are successfully fetched locally. School district dataset, hopitals dataset, and home value dateset are stored as the first, second, and the third element of the returned tuple.')

    return edu, hpt, home

if __name__ == '__main__':
    main()
