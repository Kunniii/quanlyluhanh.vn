from QuanLyLuHanh import QuanLyLuHanh
import json
import re
import requests
import bs4

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

options = data["options"]


def createUrl(id="", dp=""):
    return f"https://www.quanlyluhanh.vn/index.php/search/{id}?tendn=&sogiayphep=&diaphuong={dp}&phamvihd=3&keyword="


for opt in options:
    name = opt["name"]
    id = opt["value"]
    print(name)
    QuanLyLuHanh(id, name).run()

# with open("./index.html", 'r', encoding='utf-8') as f:
#     c = f.read()

# soup = bs4.BeautifulSoup(c, 'html.parser')
# q = QuanLyLuHanh(1, 1)

# dataContainer = soup.find_all("div", {"class": "row no-padding"})[0]
# divName = dataContainer.find_all(
#     "div", {"class": "col-md-12 company-name mar-bot"})
# divData = dataContainer.find_all("ul", {"class": "other-info"})

# data = q.getDataFromElement(divData)

# addr = data.get("Địa chỉ", "none")
# phone = data.get("Điện thoại", "none")
# web = data.get("Website", "none")
# email = data.get("Email", "none")

# print(addr, phone, web, email)
