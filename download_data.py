import configparser
import urllib.request
import os

config = configparser.ConfigParser()
config.read('company_config.ini')

url_template = config['COMPANIES']['URL_TEMPLATE']

company_list = config['COMPANIES']['COMPANY_LIST'].split(', ')

# Create the data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

for company_name in company_list:
    url = url_template.format(company_name=company_name)
    filename = f'{company_name}.csv'


    filepath = os.path.join('data', filename)
    urllib.request.urlretrieve(url, filepath)
    print(url)
    
    print(f'{filename} downloaded and saved to {filepath}')
