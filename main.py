from requests import get
from bs4 import BeautifulSoup as bs
import re

START = 1
END = 122
DIA_PHUONG = "01"

def createUrl(id = "", diaphuong = ""):
    return f"https://www.quanlyluhanh.vn/index.php/search/{id}?tendn=&sogiayphep=&diaphuong={diaphuong}&phamvihd=3&keyword="


def getDataFromElement(element: bs):
    data = {}
    tag: bs
    for tag in element.find_all("li"):
        try:
            text = re.sub(' +', ' ', tag.text)
            k, v, *_ = text.split(" - Fax:")[0].split(": ")
            data[k.strip()] = v.strip()
        except:
            print(tag.text)
            exit(1)
    return data


def getCompanyNameFromElement(element: bs):
    el: bs = element.find_all("div")[0]

    try:
        el: bs = element.find_all("div")[1]
    except:
        el: bs = element.find_all("div")[0]

    text = re.sub(' +', ' ', el.text)
    print(text)
    for i in range(len(text)-1, 0, -1):
        if text[i] == ":":
            return text[i+1:].strip()

totalData = {
    "Name": [],
    "Contact Person": [],
    "Phone Number": [],
    "Email": [],
    "Address": [],
    "Website": [],
}

csv_file = open(f"./data_diaphuong_{DIA_PHUONG}.csv", "w+", encoding="utf-8")

print("Name,Contact Person,Phone Number,Email,Address,Website", file=csv_file)

for i in range(START, END+1):
    url = createUrl(str(i), str(DIA_PHUONG))
    res = get(url).text
    soup = bs(res, "html.parser")

    dataContainer = soup.find_all("div", {"class": "row no-padding"})[0]

    divName = dataContainer.find_all("div", {"class": "col-md-12 company-name mar-bot"})
    divData = dataContainer.find_all("ul", {"class": "other-info"})

    for nameElement, dataElement in list(zip(divName, divData)):
        name = getCompanyNameFromElement(nameElement)
        data = getDataFromElement(dataElement)

        addr = data.get("Địa chỉ", "none")
        phone = data.get("Điện thoại", "none")
        web = data.get("Website", "none")
        email = data.get("Email", "none")
        


        nameUrl = f"https://www.quanlyluhanh.vn/index.php/search?tendn={re.sub(' ', '+', name)}"
        print(f'"=HYPERLINK(""{nameUrl}"", ""{name}"")",,"\'{phone}","{email}","{addr}","{web}"', file=csv_file)


csv_file.close()
