import requests
from bs4 import BeautifulSoup

def collectWebsite(Url):
    page = requests.get(Url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="w-4074839830")
    job_elements = results.find_all("td", class_="gallery-content-cell")  # type: ignore
    return job_elements[0].text.strip()


URL = input("Input announcements url:\n")
if URL == "":  
    URL = "https://www.smore.com/6rj5s"
savefile = open("AnnouncementsSave", "w")
savefile.write(collectWebsite(URL))
print("Saved")