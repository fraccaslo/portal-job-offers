import requests
from bs4 import BeautifulSoup
import string

# Most of the hard word needs to be done here
# Words need to be input lowercase as text is lowered before processing

ListGoodFit = ["fun", "motivated", "analyst", "growth", "startup", "multitask", "python", "data", "r", "sales"]
ListBadFit = ["investment", "banking", "bank", "financial" ,"consult", "consulting", "kpmg", "mckinsey","accounting", "accountant", "swedish", "excellent", "academic", "performance"]

# Here we get the page and make a BeautifulSoup out of it; then we take the objects we're interested in (offers)

# STEP ONE: from link to offers, which is a list of Beautifulsoup objects representing offers

with requests.Session() as c:
    loginurl = 'https://sse-csm.symplicity.com/students/index.php'
    payload = {
        'username' : 'your_email_here', # YOUR EMAIL HERE
        'password' : 'your_password_here', # YOUR PASSWORD HERE
        '__pin' : ''
    }
    c.post(loginurl, data=payload)
    urljobs = 'https://sse-csm.symplicity.com/students/index.php?s=jobs&ss=jobs&mode=list'
    page = c.get(urljobs).text
    soup = BeautifulSoup(page, "html5lib")
    offers_employers = soup.findAll('a', {'class':'ListPrimaryLink'})

    offers = [] # getting offers, not employers
    for x in offers_employers:   # x is beautifulsoup object, I can use "get" on it
        href = x.get("href")
        if href[1] == "m":  # we have two types of href, this keeps the title and link, the other is the employer
            offers.append(x)

# it makes sense to end step1 here, I guess
# Now we need to open the links;
# It's quite simple; the href needs to be pasted after "https://sse-csm.symplicity.com/students/index.php"

scores = [0]*len(offers)   # we initialize a scores vector
links = []
for i in range(len(offers)-1):
    item = offers[i]
    href = item.get("href")
    link = "https://sse-csm.symplicity.com/students/index.php" + href  # magic here
    links.append(link)
    soup = BeautifulSoup(c.get(link).text, "html5lib")  # Note: we're still using c (from "with request.Session() as c" from above; indented?)
    jobdescr = soup.find('div', {'class':'job_description'}).get_text()
    # descriptions are processed here. currently, there's just one metric,
    for w in jobdescr.lower().split():
        w = w.translate(str.maketrans('','',string.punctuation))
        if w in ListGoodFit:
            scores[i] += 1
        if w in ListBadFit:
            scores[i] -= 1


offers_text = [i.get_text() for i in offers]  # CHECK HERE WRITTEN OFFLINE!
offersdetails = [[x, y, z] for x, y, z in zip(offers_text, scores, links)]  # so very pythonian <3


def mykey(i):
    return i[1]
output_list = sorted(offersdetails, key=mykey, reverse=True)

# Print results in some tidy way

with open("Output.txt", "w") as text_file:
    for x in output_list:
        print(x, file=text_file)
