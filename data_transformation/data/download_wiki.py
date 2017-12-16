#! /usr/bin/env python3
import json, re
import os.path
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import html.parser as HTMLParser
from bs4 import BeautifulSoup

renamed = {
    "of Jarvan IV's maximum health":"maximum health",
    "of Zac's maximum health":"maximum health",
    "of target's missing healt": "of target's missing health",
    "of kicked target's bonus health": "of target's bonus health"
}

keywords = {
    "charm":("charm", "charms"),
    "stun":("stun", "stuns"),
    "root":("root", "roots"),
    "knockup":("knockup", "knocking up", "knocking them up"),
    "slow": ("slowing", "slows"),
    "heal": ("heals", "heal"),
    "shield": ("shields", "shield")
}

def parse_stat_name(name):
    if name in renamed:
        name = renamed[name]
    return name.replace("of ", "").replace("target's", "target")


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def get_champion_list():
    if os.path.isfile("wiki/champlist.json"):
        print("File 'wiki/champlist.json' already there; not retrieving")
        with open("wiki/champlist.json") as file:
            return json.loads(file.read())
    else:
        champlist = urlopen("http://leagueoflegends.wikia.com/api/v1/Articles/List?expand=1&category=Released_champion&limit=200").read()
        jsonlist = json.loads(champlist.decode("utf-8"))
        with open("wiki/champlist.json",'w') as outfile:
            json.dump(jsonlist["items"], outfile)
        return jsonlist["items"]

def get_champion_page(url, key):
    if os.path.isfile("wiki/html/" + key + ".html"):
        with open("wiki/html/" + key + ".html") as file:
            return file.read()
    else:
        print("Requesting champion page for " + key)
        request = urlopen("http://leagueoflegends.wikia.com" + url + "/Abilities")
        with open("wiki/html/" + key + ".html", "w") as file:
            content = request.read().decode()
            file.write(content)
            return content

def html_to_string(html):
    string = ""
    for c in html.contents:
        if c.string is None:
            string+=html_to_string(c)
        else:
            string+=c.string
    return string

def parse_champion_page(page):
    root = BeautifulSoup(page, 'html.parser')
    early = {"cooldown":{}}
    late = {"cooldown":{}}
    for skill_tabs in root.select(".skill-tabs > dd > span"):
        string = html_to_string(skill_tabs)
        # Check if the scaling scales with level as well e.g. Ashe Q
        if re.match(r"^\(\+\s([0-9]*\.[0-9]+|[0-9]+)%\s[\w|\s]*\)$", string):
            # matches (+ 65% AP)
            # remove parentheses and + sign
            string = string[2:-1]
            splitted = string.split(" ")
            value = float(splitted[0][:-1]) #Remove percent sign
            stat = parse_stat_name(" ".join(splitted[1:]))
            early[stat] = early[stat] + value if stat in early else value
            late[stat] = late[stat] + value if stat in late else value
        elif re.match(r"^(\(\+\s)?([\d|\.|\s]*\/)*([\d|\.|\s]*%)[\w|\s\']*\)?$", string):
            # matches 10 / 11 / 12 / 13 / 14% maximum health
            # matches (+ 50 / 60 / 70 / 80 / 90% bonus AD)
            if string.startswith("("):
                string = string[3:-1]
            splitted = string.split("%")
            stat = parse_stat_name(splitted[1].strip())
            scalings = [s.strip() for s in splitted[0].split("/")]
            early[stat] = early[stat] + float(scalings[0]) if stat in early else float(scalings[0])
            late[stat] = late[stat] + float(scalings[-1]) if stat in late else float(scalings[-1])
            pass
    keys = {}
    for ability in root.select(".skill_header.skill_wrapper > div > table:nth-of-type(2)"):
        for key, keyword in keywords.items():
            string = html_to_string(ability)
            for word in keyword:
                if word in string:
                    keys[key] = keys[key] + 1 if key in keys else 1
                    break
    index = 0
    for stats in root.select(".skill_header.skill_wrapper > div"):
        cd = stats.select("#cooldowncontainer")
        if not len(cd) > 0:
            cd = stats.select("#staticcontainer")
        if len(cd) > 0:
            string = html_to_string(cd[0])
            cooldown = string.split(":")[1].strip()
            if "(" in cooldown:
                tmp = cooldown.split("(")[0]
                cooldown = tmp.split("-")
            early["cooldown"][index] = float(cooldown[0].strip())
            late["cooldown"][index] = float(cooldown[-1].strip())
        index+=1


    map = {"early":early,"late":late, "keywords":keys}
    return map

if __name__ == "__main__":
    if os.path.isfile("wiki.json"):
        print("File 'wiki.json' already there; not retrieving")
    else:
        champlist = get_champion_list()
        wikiinfo = {"scaling":{}}
        for champ in champlist:
            page = get_champion_page(champ["url"], champ["title"].replace(" ", "").replace("'",""))
            data = parse_champion_page(page)
            wikiinfo["scaling"][champ["title"].replace(" ", "").replace("'","")] = data
        with open("wiki.json", "w") as file:
            json.dump(wikiinfo, file)
