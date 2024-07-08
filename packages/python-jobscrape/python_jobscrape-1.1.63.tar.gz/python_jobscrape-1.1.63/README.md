

**Jobscrape** is a simple, yet comprehensive, job scraping library.

## Features

- Simultaneously scrapes job postings from popular boards(**LinkedIn**, **Indeed**, **Glassdoor**, & **ZipRecruiter**) 
- Aggregates job postings into a Pandas DataFrame.
- Supports proxies for enhanced scraping capabilities.

### Installation

```
pip install -U python-jobscrape
```

_Python version >= [3.10](https://www.python.org/downloads/release/python-3100/) required_

### Usage

```python

import csv
from jobspy import scrape_jobs

search_term = "Energy Technician"  # Define your search term here
location = "Dallas, TX"

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "glassdoor"],
    search_term=search_term,
    location=location,
    results_wanted=20,
    hours_old=72,  # (only Linkedin/Indeed is hour specific, others round up to days old)
    country_indeed='USA',  # only needed for indeed / glassdoor
    # linkedin_fetch_description=True  # get full description and direct job url for linkedin (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
)

print(f"Found {len(jobs)} jobs")
print(jobs.head())

# Dynamically create the CSV filename
filename = f"{search_term.replace(' ', '_')}_{location.replace(' ', '_')}.csv"
jobs.to_csv(filename, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
print(f"CSV saved as {filename}")
```



### Parameters for `scrape_jobs()`

```plaintext
Optional
├── site_name (list|str): 
|    linkedin, zip_recruiter, indeed, glassdoor 
|    (default is all four)
│
├── search_term (str)
│
├── location (str)
│
├── distance (int): 
|    in miles, default 50
│
├── job_type (str): 
|    fulltime, parttime, internship, contract
│
├── proxies (list): 
|    in format ['user:pass@host:port', 'localhost']
|    each job board will round robin through the proxies
│
├── is_remote (bool)
│
├── results_wanted (int): 
|    number of job results to retrieve for each site specified in 'site_name'
│
├── easy_apply (bool): 
|    filters for jobs that are hosted on the job board site
│
├── description_format (str): 
|    markdown, html (Format type of the job descriptions. Default is markdown.)
│
├── offset (int): 
|    starts the search from an offset (e.g. 25 will start the search from the 25th result)
│
├── hours_old (int): 
|    filters jobs by the number of hours since the job was posted 
|    (ZipRecruiter and Glassdoor round up to next day.)
│
├── verbose (int) {0, 1, 2}: 
|    Controls the verbosity of the runtime printouts 
|    (0 prints only errors, 1 is errors+warnings, 2 is all logs. Default is 2.)

├── linkedin_fetch_description (bool): 
|    fetches full description and direct job url for LinkedIn (Increases requests by O(n))
│
├── linkedin_company_ids (list[int]): 
|    searches for linkedin jobs with specific company ids
|
├── country_indeed (str): 
|    filters the country on Indeed & Glassdoor (see below for correct spelling)
```

```
├── Indeed limitations:
|    Only one from this list can be used in a search:
|    - hours_old
|    - job_type & is_remote
|    - easy_apply
│
└── LinkedIn limitations:
|    Only one from this list can be used in a search:
|    - hours_old
|    - easy_apply
```


### JobPost Schema

```plaintext
JobPost
├── title (str)
├── company (str)
├── company_url (str)
├── job_url (str)
├── location (object)
│   ├── country (str)
│   ├── city (str)
│   ├── state (str)
├── description (str)
├── job_type (str): fulltime, parttime, internship, contract
├── job_function (str)
├── compensation (object)
│   ├── interval (str): yearly, monthly, weekly, daily, hourly
│   ├── min_amount (int)
│   ├── max_amount (int)
│   └── currency (enum)
├── date_posted (date)
├── emails (str)
└── is_remote (bool)

Indeed specific
├── company_country (str)
└── company_addresses (str)
└── company_industry (str)
└── company_employees_label (str)
└── company_revenue_label (str)
└── company_description (str)
└── ceo_name (str)
└── ceo_photo_url (str)
└── logo_photo_url (str)
└── banner_photo_url (str)
```

## Supported Countries for Job Searching

### **LinkedIn**

LinkedIn searches globally & uses only the `location` parameter. 

### **ZipRecruiter**

ZipRecruiter searches for jobs in **US/Canada** & uses only the `location` parameter.

### **Indeed / Glassdoor**

Indeed & Glassdoor supports most countries, but the `country_indeed` parameter is required. Additionally, use the `location`
parameter to narrow down the location, e.g. city & state if necessary. 

You can specify the following countries when searching on Indeed (use the exact name, * indicates support for Glassdoor):

|                      |              |            |                |
|----------------------|--------------|------------|----------------|
| Argentina            | Australia*   | Austria*   | Bahrain        |
| Belgium*             | Brazil*      | Canada*    | Chile          |
| China                | Colombia     | Costa Rica | Czech Republic |
| Denmark              | Ecuador      | Egypt      | Finland        |
| France*              | Germany*     | Greece     | Hong Kong*     |
| Hungary              | India*       | Indonesia  | Ireland*       |
| Israel               | Italy*       | Japan      | Kuwait         |
| Luxembourg           | Malaysia     | Mexico*    | Morocco        |
| Netherlands*         | New Zealand* | Nigeria    | Norway         |
| Oman                 | Pakistan     | Panama     | Peru           |
| Philippines          | Poland       | Portugal   | Qatar          |
| Romania              | Saudi Arabia | Singapore* | South Africa   |
| South Korea          | Spain*       | Sweden     | Switzerland*   |
| Taiwan               | Thailand     | Turkey     | Ukraine        |
| United Arab Emirates | UK*          | USA*       | Uruguay        |
| Venezuela            | Vietnam*     |            |                |


## Notes
* Indeed is the best scraper currently with no rate limiting.  
* All the job board endpoints are capped at around 1000 jobs on a given search.  
* LinkedIn is the most restrictive and usually rate limits around the 10th page with one ip. Proxies are a must basically.

## Frequently Asked Questions

---

**Q: Encountering issues with your queries?**  
**A:** Try reducing the number of `results_wanted` and/or broadening the filters. If problems
persist, [submit an issue](https://github.com/Bunsly/JobSpy/issues).

---

**Q: Received a response code 429?**  
**A:** This indicates that you have been blocked by the job board site for sending too many requests. All of the job board sites are aggressive with blocking. We recommend:

- Wait some time between scrapes (site-dependent).
- Try using the proxies param to change your IP address.

---
