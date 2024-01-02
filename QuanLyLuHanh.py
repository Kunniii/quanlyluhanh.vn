from nis import cat
import re
from requests import get
from bs4 import BeautifulSoup as bs


class QuanLyLuHanh:
    START = None
    END = None
    DIA_PHUONG_ID = None
    DIA_PHUONG = ""
    HOST = "https://www.quanlyluhanh.vn/index.php/search"

    def __init__(self, diaPhuongID, diaPhuongName):
        self.DIA_PHUONG_ID = diaPhuongID
        self.DIA_PHUONG = diaPhuongName

    def createUrl(self, id=1):
        return f"{self.HOST}/{id}?tendn=&sogiayphep=&diaphuong={self.DIA_PHUONG_ID}&phamvihd=3&keyword="

    def getDataFromElement(self, element):
        data = {}
        for tag in element.find_all("li"):
            text = re.sub(" +", " ", tag.text)
            try:
                k, v = text.split(" - Fax:")[0].split(": ")
                data[k.strip()] = v.strip()
            except Exception as e:
                print(text.split(" - Fax:")[0].split(":"))
                text = re.sub("( : )", "", text)
                # k, v = text.split(" - Fax:")[0].split(":")
                coli = text.find(":")
                k = text[:coli].strip()
                v = text[coli+1:].split(" - Fax:")[0]
                print(f"Recover with:\n --key: {k}\n --val: {v}")
                data[k.strip()] = v.strip()

        return data

    def getCompanyNameFromElement(self, element: bs):
        el: bs = element.find_all("div")[0]
        print(f' + {el.text.split(".")[0]}/{self.TOTAL}', end='\r')

        try:
            el: bs = element.find_all("div")[1]
        except:
            el: bs = element.find_all("div")[0]

        text = re.sub(" +", " ", el.text)
        for i in range(len(text) - 1, 0, -1):
            if text[i] == ":":
                return text[i + 1:].strip()

    def run(self):
        # get the end value
        s = bs(get(self.createUrl(1)).text, "html.parser")
        a = s.find("ul", {"class": "pagination"}).find_all("a")
        if len(a) <= 4:
            self.END = len(a)
        elif len(a) == 5:
            t = a[-1]["onclick"]
            p = re.compile(r"https?://(?:www\.)?\w+\.\w+/\S*")
            end = p.findall(t)[0].split(";")[0].split("/")[-1].replace("'", "")
            self.END = int(end) + 1

        with open(
            f"./output/{self.DIA_PHUONG}.csv", "w+", encoding="utf-8"
        ) as csv_file:

            total = s.find("h4", {"class": "total-number"}).text
            if total != "Không có kết quả":
                self.TOTAL = int(total)
                print(
                    "Name,Contact Person,Phone Number,Email,Address,Website", file=csv_file
                )

                for i in range(1, self.END + 1):
                    url = self.createUrl(str(i))
                    res = get(url)
                    soup = bs(res.text, "html.parser")

                    dataContainer = soup.find_all(
                        "div", {"class": "row no-padding"})[0]

                    divName = dataContainer.find_all(
                        "div", {"class": "col-md-12 company-name mar-bot"}
                    )
                    divData = dataContainer.find_all(
                        "ul", {"class": "other-info"})

                    for nameElement, dataElement in list(zip(divName, divData)):
                        name = self.getCompanyNameFromElement(nameElement)
                        data = self.getDataFromElement(dataElement)

                        addr = data.get("Địa chỉ", "none")
                        phone = data.get("Điện thoại", "none")
                        web = data.get("Website", "none")
                        email = data.get("Email", "none")

                        if phone == "none":
                            if "Điện thoại" in divData:
                                print("\n\n#" * 20)
                                print(dataElement)
                                print()
                                print(data)
                                exit(1)
                            else:
                                pass

                        nameUrl = f"{self.HOST}?tendn={re.sub(' ', '+', name)}"
                        print(
                            f'"=HYPERLINK(""{nameUrl}"", ""{name}"")",,"\'{phone}","{email}","{addr}","{web}"',
                            file=csv_file,
                        )
            else:
                print('\tKhông có kết quả')
