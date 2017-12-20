import sys, os, requests, json, re
from bs4 import BeautifulSoup

# Helper Functions
def html_to_string(html):
    string = ""
    for c in html.contents:
        if c.string is None:
            string+=html_to_string(c)
        else:
            string+=c.string
    return string

def get_file(path, url, mapping=None):
    if os.path.isfile(path):
        return json.load(open(path))
    else:
        r = requests.get(url)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        result = mapping(r.text) if mapping is not None else r.text
        with open(path, "w+") as file:
            if type(result) is str:
                file.write(result)
            else:
                json.dump(result, file)
        return result


def get_champion_list():
    if len(sys.argv) > 1:
        return sys.argv[1:]
    else:
        def mapping(contents):
            c = json.loads(contents)
            returns = []
            for item in c["items"]:
                returns.append(item["title"].replace(" ","_"))
            return returns
        return get_file("wiki/champlist.json", \
                    "http://leagueoflegends.wikia.com/api/v1/Articles/List?expand=1&category=Released_champion&limit=200", \
                    mapping)

def parse_scaling(string):
    string = string.replace(u'\u203E',"").replace(u'\xa0', u' ')
    if string == "Collected Souls":
        # Scales on collected souls for tresh
        return {"type":"collected-souls", "value":1}
    if "per" in string:
        # percentage scaling per ammount of stat (e.g. Galio Q)
        # ignore for now
        return {"type":"undefined","value":0}
    if "based on level" in string:
        return {"type":"undefined", "value":0}
    if re.match("^[a-z|A-Z|\s]*$", string):
        return {"type":"undefined","value":0}
    string = string.replace("(+", "").replace(")", "")
    splitted = string.split("%")
    type = "".join(c for c in string if c not in "1234567890/%.").strip()
    value = string[:-len(type)]
    value = parse_base_damage(value)
    return {"type":type, "value": value["value"]}

def parse_base_scaling_damage(string):
    print("NOT IMPLEMENTED: " + string)
    return {"type":"unkown", "value":[]}

def parse_base_damage(string):
    string = string.replace(u'\u203E',"").replace(u'\xa0', u' ')
    if bool(re.search("[a-zA-Z]", string)):
        # For Tahm Kench E
        return parse_scaling(string)
    type = "percentage" if "%" in string else "fixed"
    string = string.replace("%", "").replace(" ", "").replace("up to ","").strip()
    value = []
    if "/" in string:
        # scaling per level
        splitted = string.split("/")
        for split in splitted:
            value.append(float(split))
    else:
        # same on all level
        value = [float(string) for i in range(5)]
    return {"type":type, "value":value}

def parse_skill(skill):
    if len(skill.get("class")) != 2:
        return {"type":"unkown"}
    info = {"type":skill.get('class',[])[-1], "attributes":{}}
    wrapper = skill.select(".skill_header > div")[0]
    info["name"] = wrapper.get("id")
    if not info["type"] == "skill_innate":
        # Ignore passives for now
        for level in skill.select(".skill-tabs"):
            for i in range(int(len(level) / 2)):
                title = html_to_string(level.select("dt:nth-of-type(%d) > span" % (i+1))[0])
                scaling = level.select("dd:nth-of-type(%d)" % (i+1))[0]
                scales = []
                for span in scaling.findChildren():
                    if span.name == "span" and \
                        not re.match("^[\d|\/|\s|%|\.]*$",span.text) and \
                        not re.match("^[\D]*$", span.text):

                        text = html_to_string(span)
                        if "based on level" in text:
                            scales.append(parse_base_scaling_damage(text))
                        else:
                            scales.append(parse_scaling(text))
                        # Remove span so base damage can be read later
                        span.decompose()
                base_text = html_to_string(scaling).strip()
                base_text = base_text.replace("soldiers", "")
                base_text = re.sub("\((.*?)\)", "", base_text)
                if len(base_text) > 0:
                    basedamage = parse_base_damage(base_text)
                    basedamage["scalings"] = scales
                    info["attributes"][title.replace(" ","")] = basedamage
                else:
                    # There is no base damage (e.g. Ashe Damage per Arrow on Q)
                    info["attributes"][title.replace(" ", "")] = {"type":"none", "value":[], "scalings":scales}
    return info


def load_champion_information(champ):
    information = {"skills":[]}
    url = "http://leagueoflegends.wikia.com/wiki/" + champ + "/Abilities"
    r = requests.get(url)
    root = BeautifulSoup(r.text, 'html.parser')
    skill_tags = root.select(".skill")
    if "Lee Sin" in root.title.string:
        # Lee Sin has reactivations as extra skills so he needs to be handled differently
        print("NOT IMPLEMENTED (Lee Sin can't be parsed yet)")
        pass
    elif len(skill_tags) == 5 or len(skill_tags) == 6:
        # Normal skill amount. No dual form or smth like that
        # Some champions (e.g. Sion) do have multiple passives though
        skills = {"name":"default", "skills":{}}
        for skill in skill_tags:
            info = parse_skill(skill)
            skills["skills"][info["type"]] = info
        information["skills"].append(skills)
    else:
        # Champions like Nidalee and Elise have two forms and therefore 10 skills
        # Handle them differently
        # Select tabber instead
        tabber = root.select(".tabbertab")
        for tab in tabber:
            title = tab.get("title")
            skills = {"name":title,"skills":{}}
            information["skills"].append(skills)
        skill_tags = root.select(".skill")
        counter = 0
        for skill in skill_tags:
            info = parse_skill(skill)
            information["skills"][counter // 5]["skills"][info["type"]] = info
            counter+=1


    return information

champlist = get_champion_list()
print(champlist)
result = {}
for champ in champlist:
    print("Loading " + champ)
    result[champ] = load_champion_information(champ)

with open("wiki.json", "w+") as file:
    json.dump(result, file, indent=2)
