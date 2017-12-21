import sys, os, requests, json, re
from bs4 import BeautifulSoup

keywords = {
    "charm":"charm",
    "stun":"stun",
    "root":"root",
    "slow":"slow", # Detects slowing as well
    "heal":"heal",
    "shield":"shield",
    "knockup":"knockup",
    "knocking up":"knockup",
    "knocking them up":"knockup",
    "heal": "heal",
    "knocks down":"knockdown",
    "knocking them down":"knockdown",
    "suppressed":"suppressed",
    "asleep":"sleeping",
    "brittle":"brittle"
}

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
    return {"type":"undefined", "value":[]}

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

attr_name_replacements = {
    "magicdamageperdagger":"magicdamageperinstance",
    "magicdamagepersphere":"magicdamageperinstance",
    "magicdamagepermine":"magicdamageperinstance",
    "physicaldamageperblade": "physicaldamageperinstance",
    "damageperarrow":"damageperinstance",
    "magicdamageevery0.25seconds":"magicdamageperquarterseconds",
    "enhancedmagicdamageevery0.25seconds":"enhancedmagicdamageperquarterseconds"
}
def sanitize_attribute_name(attr_name):
    string = attr_name.replace(" ", "").replace(":","")
    string = string.replace("min.","minimum").replace("max.","maximum")
    string.strip()
    string = attr_name_replacements.get(string, string)
    return string

def parse_skill(skill):
    if len(skill.get("class")) != 2:
        return {"type":"undefined"}
    info = {"type":skill.get('class',[])[-1], "attributes":{}, "tags":[], "cooldown":[]}
    wrapper = skill.select(".skill_header > div")[0]
    info["name"] = wrapper.get("id")
    if not info["type"] == "skill_innate":
        # Ignore passives for now
        for level in skill.select(".skill-tabs"):
            for i in range(int(len(level) / 2)):
                title = html_to_string(level.select("dt:nth-of-type(%d) > span" % (i+1))[0]).lower()
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
                    info["attributes"][sanitize_attribute_name(title)] = basedamage
                else:
                    # There is no base damage (e.g. Ashe Damage per Arrow on Q)
                    info["attributes"][sanitize_attribute_name(title)] = {"type":"none", "value":[], "scalings":scales}
        # Scan description for keywords
        text = html_to_string(wrapper).lower()
        for key, value in keywords.items():
            if key.lower() in text:
                info["tags"].append(value)
        # Get cooldowm
        cdcontainer = wrapper.find("div", id="cooldowncontainer")
        if not cdcontainer:
            cdcontainer = wrapper.find("div", id="staticcontainer")
        if cdcontainer:
            cdcontainer.span.decompose()
            text = html_to_string(cdcontainer).strip()
            if "based on bonus attack speed" in text:
                splitted = text.replace("(based on bonus attack speed)", "").split("-")
                info["cooldown"] = [float(split) for split in splitted]
            elif "/" in text:
                splitted = text.split("/")
                for split in splitted:
                    info["cooldown"].append(float(split.strip()))
            else:
                cd = float(text)
                for i in range(5):
                    info["cooldown"].append(cd)
    return info


def load_champion_information(champ):
    information = {"skills":[]}
    url = "http://leagueoflegends.wikia.com/wiki/" + champ + "/Abilities"
    r = requests.get(url)
    root = BeautifulSoup(r.text, 'html.parser')
    skill_tags = root.select(".skill")
    if "Lee Sin" in root.title.string:
        # Lee Sin has reactivations as extra skills so he needs to be handled differently
        flag = False
        skills = {"name":"default", "skills":{}}
        for skill in skill_tags:
            info = parse_skill(skill)
            skills["skills"][info["type"] + ("_1" if flag else "_0")] = info
            flag = not flag
        information["skills"].append(skills)
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

attributes = {}

# Generate scalings.json
def generate_scalings(wiki_info):
    print("Generating scalings")
    scalings = {}

    for champ, value in wiki_info.items():
        champ_scaling = {"early":{"cooldown":{}},"late":{"cooldown":{}}, "keywords":{}}
        # Iterate over skill sets
        for skills in value["skills"]:
            # Iterate over every simple skill
            second_iteration = False
            for key, skill in skills["skills"].items():
                if key == "undefined" or key == "skill_innate":
                    continue
                for tag in skill["tags"]:
                    champ_scaling["keywords"][tag] = champ_scaling["keywords"][tag] + 1 if tag in champ_scaling["keywords"] else 1
                # Ignore Lee Sins reactivations
                if "_0" in key:
                    pass
                elif len(value["skills"]) > 1:
                    if not second_iteration:
                        if len(skill["cooldown"]) <= 0:
                            champ_scaling["early"]["cooldown"][key] = 0
                            champ_scaling["late"]["cooldown"][key] = 0
                        else:
                            champ_scaling["early"]["cooldown"][key] = skill["cooldown"][0]
                            champ_scaling["late"]["cooldown"][key] = skill["cooldown"][-1]
                    else:
                        if len(skill["cooldown"]) > 0:
                            if champ_scaling["early"]["cooldown"][key] > skill["cooldown"][0]:
                                champ_scaling["early"]["cooldown"][key] = skill["cooldown"][0]
                            if champ_scaling["late"]["cooldown"][key] > skill["cooldown"][-1]:
                                champ_scaling["late"]["cooldown"][key] = skill["cooldown"][-1]
                else:
                    key.replace("_1","")
                    if len(skill["cooldown"]) <= 0:
                        champ_scaling["early"]["cooldown"][key] = 0
                        champ_scaling["late"]["cooldown"][key] = 0
                    else:
                        champ_scaling["early"]["cooldown"][key] = skill["cooldown"][0]
                        champ_scaling["late"]["cooldown"][key] = skill["cooldown"][-1]


                # Iterate over attributes
                if "attributes" in skill:
                    for attr_name, attr in skill["attributes"].items():
                        if "scalings" not in attr or len(attr["scalings"]) <= 0:
                            continue
                        if "total" in attr_name:
                            continue
                        if "minimum" in attr_name and attr_name.replace("minimum", "maximum") in skill["attributes"]:
                            # ignore because it will be handled once the maximum stat show up
                            continue
                        if "maximum" in attr_name and attr_name.replace("maximum","minimum") in skill["attributes"]:
                            minimum = skill["attributes"][attr_name.replace("maximum","minimum")]
                            average = {"value":[], "type":attr["type"],"scalings":[]}
                            average_name = attr_name.replace("maximum","average")
                            for i in range(len(attr["value"])):
                                average["value"].append((attr["value"][i] + minimum["value"][i]) / 2)
                            for j in range(len(attr["scalings"])):
                                scaling = {"type":attr["scalings"][j]["type"], "value":[]}
                                min_scale = minimum["scalings"][j]
                                max_scale = attr["scalings"][j]
                                for k in range(len(max_scale["value"])):
                                    scaling["value"].append((min_scale["value"][k] + max_scale["value"][k]) / 2)
                                average["scalings"].append(scaling)
                            attr = average
                        if not attr_name in attributes:
                            attributes[attr_name] = 0
                        attributes[attr_name] += 1
                        for s in attr["scalings"]:
                            if s["type"] == "undefined":
                                continue
                            # Add scalings onto each other
                            champ_scaling["early"][s["type"]] = champ_scaling["early"][s["type"]] + s["value"][0] if s["type"] in champ_scaling["early"] else s["value"][0]
                            champ_scaling["late"][s["type"]] = champ_scaling["late"][s["type"]] + s["value"][-1] if s["type"] in champ_scaling["late"] else s["value"][-1]
        scalings[champ] = champ_scaling
    with open("wiki.json", "w+") as file:
        json.dump(scalings, file)

if os.path.isfile("wiki_info.json"):
    with open("wiki_info.json") as file:
        generate_scalings(json.load(file))
else:
    champlist = get_champion_list()
    print(champlist)
    result = {}
    for champ in champlist:
        print("Loading " + champ)
        result[champ] = load_champion_information(champ)

    with open("wiki_info.json", "w+") as file:
        json.dump(result, file, indent=2)
    generate_scalings(result)
    print("Done...")
