import requests
import bs4

class Level:
    def __init__(self, _name, _id, _description, _information, _attempts):
        self.name = _name
        self.id = _id
        self.description = _description
        self.information = _information
        self.attempts = _attempts


def filterData(data):
    """
    Filter string of data

    :param str data:
    :return: Filtered Data
    :rtype: str
    """
    return data.split("\n")[1].replace("</td>", "").strip()


def getData(element, idx) -> str:
    """
    Gets data from element

    :param bs4.element element: Element to get data from
    :param int idx: Index of data
    :return: Filtered Data
    :rtype: str
    """
    item = element[idx]
    if isinstance(item, bs4.element.Tag):
        string = str(item)
        if "\n" in string:
            return filterData(string)
        else:
            return "No data found"
    else:
        return "No data found"


def getLevelData(level):
    """
    Gets level data from URL

    :param str level: URL of level from knflrpn.com
    :return: Level Data
    :rtype: Level
    """
    req = requests.get(level)
    if req.status_code == 200:
        response = req.text
        soup = bs4.BeautifulSoup(response, "lxml")
        table = soup.find_all("table")
        maintable = table[0]
        td = maintable.find_all("td")
        level_id = str(maintable.find("th")).split("level id is ")[1].replace("</th>", "")  # this very bad
        level_name = getData(td, 0)
        level_desc = (getData(td, 1) == "" and "No description" or getData(td, 1))
        level_information = getData(td, 2)
        level_attempts = level_information.split(" attempts")[0].split("It has ")[1]
        level = Level(level_name, level_id, level_desc, level_information, level_attempts)
        return level
    else:
        return "Website blocking requests or website down"
