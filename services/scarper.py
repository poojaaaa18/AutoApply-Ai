import requests
import urllib.parse
from bs4 import BeautifulSoup
import json

def scrape_indeed_jobs(filters=None):
    token = "ace4669fd83046e39bc55b1e18efc9b8e20b0e51dd7"  # replace with your real token

    # Encode base query
    base_url = "https://in.indeed.com/jobs"
    params = {
        

    }

    # Add filters if provided
    if filters:
        params.update(filters)

    # Build final URL
    query_string = urllib.parse.urlencode(params)
    target_url = f"{base_url}?{query_string}"
    encoded_url = urllib.parse.quote(target_url)

    # Scrape.do render URL
    scrape_url = (
        f"http://api.scrape.do/?token={token}"
        f"&url={encoded_url}"
        f"&render=true"
        f"&super=true"
        f"&geocode=in"
    )

    response = requests.get(scrape_url, timeout=70)

    if response.status_code != 200:
        return {"error": "Failed to fetch data", "status": response.status_code}

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="cardOutline")

    job_list = []
    print(len(job_cards))
    for card in job_cards:
        
        # Title & apply link
        title_tag = card.find("h2", class_="jobTitle")
        link_tag = title_tag.find("a") if title_tag else None
        title = link_tag.get_text(strip=True) if link_tag else "No title"
        apply_link = f"https://in.indeed.com{link_tag['href']}" if link_tag and link_tag.has_attr("href") else "No link"

        # Company
        company_tag = card.find("span", {"data-testid": "company-name"})
        company = company_tag.get_text(strip=True) if company_tag else "No company"

        # Location
        location_tag = card.find("div", {"data-testid": "text-location"})
        location_text = location_tag.get_text(strip=True) if location_tag else "No location"

        # Salary
        salary_tag = card.find("div", {"data-testid": "attribute_snippet_testid"})
        salary = salary_tag.get_text(strip=True) if salary_tag else "Not listed"

        # Description snippet
        snippet_div = card.find("div", {"data-testid": "belowJobSnippet"})
        description = snippet_div.get_text(" ", strip=True) if snippet_div else "No snippet"

        job_list.append({
            "title": title,
            "company": company,
            "location": location_text,
            "salary": salary,
            "apply_link": apply_link,
            "description_snippet": description,
        })

    return job_list

# if __name__ == "__main__":
#     a= scrape_indeed_jobs('data+analyst','noida,+uttar+pradesh')
#     print(a)
    
# import requests
# import urllib.parse
# from bs4 import BeautifulSoup

# token = "ace4669fd83046e39bc55b1e18efc9b8e20b0e51dd7"
# target_url = "https://in.indeed.com/jobs?q=data+analyst&l=noida,+uttar+pradesh"
# encoded_url = urllib.parse.quote(target_url)

# scrape_url = (
#     f"http://api.scrape.do/?token={token}"
#     f"&url={encoded_url}"
#     f"&render=true"
#     f"&super=true"
#     f"&geocode=in"
# )

# response = requests.get(scrape_url, timeout=70)
# if response.status_code == 200:
#     print('inside if')
#     soup = BeautifulSoup(response.text, "html.parser")

#     job_cards = soup.find_all("div", class_="cardOutline")  
#     print(len(job_cards))

#     for i, card in enumerate(job_cards, start=1):
#          # Title
#         title_tag = card.find("h2", class_="jobTitle")
#         title = title_tag.get_text(strip=True) if title_tag else "No title"

#         # Company
#         company_tag = card.find("span", {"data-testid": "company-name"})
#         company = company_tag.get_text(strip=True) if company_tag else "No company"

#         # Location
#         location_tag = card.find("div", {"data-testid": "text-location"})
#         location = location_tag.get_text(strip=True) if location_tag else "No location"
#         print(f"\nJob #{i}")
#         print("Title   :", title)
#         print("Company :", company)
#         print("Location:", location)

    
# else:
#     print("Failed to fetch page. Status:", response.status_code)


# import requests
# import urllib.parse
# from bs4 import BeautifulSoup

# token = "ace4669fd83046e39bc55b1e18efc9b8e20b0e51dd7"
# target_url = "https://in.indeed.com/jobs?q=data+analyst&l=noida,+uttar+pradesh"
# encoded_url = urllib.parse.quote(target_url)

# scrape_url = (
#     f"http://api.scrape.do/?token={token}"
#     f"&url={encoded_url}"
#     f"&render=true"
#     f"&super=true"
#     f"&geocode=in"
# )

# response = requests.get(scrape_url, timeout=70)

# if response.status_code == 200:
#     # Save full HTML for inspection
#     with open("indeed_rendered_page.html", "w", encoding="utf-8") as file:
#         file.write(response.text)
#     print("✅ HTML saved to indeed_rendered_page.html")
# else:
#     print("❌ Failed to fetch page. Status code:", response.status_code)
