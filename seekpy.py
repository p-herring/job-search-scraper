import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = "https://www.seek.com.au/python-jobs/in-Perth-WA-6000"

def extract(base_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to fetch {base_url}. Status code: {response.status_code}")
        return None

def get_job_summary(soup):
    job_list = []
    jobs = soup.find_all('article', {'data-automation': 'normalJob'})
    for job in jobs:
        job_dict = {
            'Description': job.find('span', {'data-automation': 'jobShortDescription'}).text.strip() if job.find('span', {'data-automation': 'jobShortDescription'}) else 'NA',
            'Title': job.find('a', {'data-automation': 'jobTitle'}).text.strip() if job.find('a', {'data-automation': 'jobTitle'}) else 'NA',
            'Salary': job.find('span', {'data-automation': 'jobSalary'}).text.strip() if job.find('span', {'data-automation': 'jobSalary'}) else 'NA',
            'Company': job.find('a', {'data-automation': 'jobCompany'}).text.strip() if job.find('a', {'data-automation': 'jobCompany'}) else 'NA',
            'Location': job.find('a', {'data-automation': 'jobLocation'}).text.strip() if job.find('a', {'data-automation': 'jobLocation'}) else 'NA',
            'Classification': job.find('a', {'data-automation': 'jobClassification'}).text.strip() if job.find('a', {'data-automation': 'jobClassification'}) else 'NA',
            'Date': job.find('span', {'data-automation': 'jobListingDate'}).text.strip() if job.find('span', {'data-automation': 'jobListingDate'}) else 'NA'
        }
        job_list.append(job_dict)
    return job_list

def scrape_seek(base_url):
    all_jobs = []
    while base_url:
        print(f'Getting page: {base_url}')
        soup = extract(base_url)
        if soup:
            all_jobs.extend(get_job_summary(soup))
            base_url = next_page_url(soup)
            time.sleep(2)  # Add a delay between requests to avoid overloading the server
    return all_jobs

def next_page_url(soup):
    next_page_link = soup.find('a', {'data-automation': 'page-next'})
    if next_page_link:
        return 'https://www.seek.com.au' + next_page_link['href']
    else:
        return None

if __name__ == "__main__":
    job_listings = scrape_seek(base_url)
    df = pd.DataFrame(job_listings)
    df.to_csv('python jobs perth.csv', index=False)
    print("Job listings saved to 'python jobs perth.csv'")
