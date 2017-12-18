#
# Retrieves rowCount rows from the participant data in source database,
# transforms the rows and inserts the transformed rows into a table
# style_prediction_data in the destination database.
#
# Input: first cli argument is number of retrieved rows
# Call from /data_transformation/:  python perkstyle/perkstyle.py [rowCount]
#
# style_prediction_data
# champion_id |   tag1   |   tag2   |  role  | perk_primary_style | perk_sub_style
#
import psycopg2
from config import config
import database
from data import championById, wikiById
import sys
def getOrDefault(key, dict, default):
    if key in dict:
        return dict[key]
    else:
        return default
rowCount = sys.argv[1]
print("Retrieving " + rowCount + " rows from matches!")

# Connect to source and destination database
try:
    src = config["database"]["src"]
    dest = config["database"]["dest"]
    dataSrc = database.connect(
        src["url"], src["username"], src["password"], src["database"])
    dataDest = database.connect(
        dest["url"], dest["username"], dest["password"], dest["database"])
except Exception as e:
    print(e)
    print("Failed to connect to source or dest database!")
    exit(1)
print("Successfully connected to both databases!")

print("Executing select to get " + rowCount + " rows!")
srcCursor = dataSrc.cursor()
srcCursor.execute("SELECT \"championId\", \"perkPrimaryStyle\", \"perkSubStyle\", \"lane\", \"role\", \"perk0\", "
                    + "\"perk1\", \"perk2\", \"perk3\", \"perk4\", \"perk5\" FROM "
                    + "match_participant_stats mps JOIN match_participant mp ON "
                    + "mps.\"match_platformId\" = mp.\"match_platformId\" AND "
                    + "mps.\"match_gameId\" = mp.\"match_gameId\" AND "
                    + "mp.\"participantId\" = mps.\"match_participant_participantId\" "
                    + "JOIN match_participant_timeline mpt ON "
                    + "mps.\"match_platformId\" = mpt.\"match_platformId\" AND "
                    + "mps.\"match_gameId\" = mpt.\"match_gameId\" AND "
                    + "mpt.\"match_participant_participantId\" = mps.\"match_participant_participantId\" "
                    + "WHERE mps.\"perkPrimaryStyle\" IS NOT NULL and mps.\"perkSubStyle\" IS NOT NULL LIMIT " + rowCount)


destCursor = dataDest.cursor()
print("Creating table in destination database if not exists!")
# TODO could also use " integer not null".join(integerColumns) here
destCursor.execute("""CREATE TABLE IF NOT EXISTS style_prediction_data (champion_id integer NOT NULL, 
                    tag1 varchar(10) NOT NULL, tag2 varchar(10) NULL, \"role\" varchar(10) NOT NULL, 
                    root integer not null, slow integer NOT NULL, stun integer NOT NULL, charm integer 
                    NOT NULL, knockup integer not null, heal integer not null, shield integer not null, 
                    base_ad decimal(7,2) not null, base_health decimal(7,2) not null, 
                    base_armor decimal(7,2) not null, base_mres decimal(7,2) not null, 
                    base_as decimal(7, 2) not null, ad_scaling  decimal(7,2) not null, health_scaling decimal(7,2) 
                    not null, armor_scaling  decimal(7,2) not null, mres_scaling  decimal(7,2) not null,
                    as_scaling decimal(8, 3) not null, q_cd_early decimal(7,2) not null, w_cd_early  
                    decimal(7,2) not null, e_cd_early  decimal(7,2) not null, r_cd_early  decimal(7,2) not null,
                    q_cd_late decimal(7,2) not null, w_cd_late  decimal(7,2) not null, e_cd_late  
                    decimal(7,2) not null, r_cd_late  decimal(7,2) not null,
                    ap_ability_scaling_early decimal(7,2), ad_ability_scaling_early decimal(7,2), max_hp_scaling_early decimal(7,2),
                    bonus_armor_scaling_early decimal(7,2), bonus_magic_resist_scaling_early decimal(7,2),
                    ap_ability_scaling_late decimal(7,2), ad_ability_scaling_late decimal(7,2), max_hp_scaling_late decimal(7,2),
                    bonus_armor_scaling_late decimal(7,2), bonus_magic_resist_scaling_late decimal(7,2), \"resource\" varchar(20) NOT NULL,
                    perk_primary_style integer NOT NULL, 
                    perk_sub_style integer NOT NULL, perk0 integer NOT NULL, perk1 integer NOT NULL, perk2  integer NOT NULL,
                    perk3 integer NOT NULL, perk4 integer NOT NULL, perk5 integer NOT NULL);""")
dataDest.commit()
print("Created table style_prediction_data")

baseInsert = """INSERT INTO style_prediction_data (champion_id, tag1, tag2, \"role\", root, slow, stun, charm, knockup, 
                heal, shield, base_ad, base_health, base_armor, base_mres, base_as, ad_scaling, health_scaling, 
                armor_scaling, mres_scaling, as_scaling, q_cd_early, w_cd_early, e_cd_early, r_cd_early,
                q_cd_late, w_cd_late, e_cd_late, r_cd_late, ap_ability_scaling_early, ad_ability_scaling_early, 
                max_hp_scaling_early, bonus_armor_scaling_early, bonus_magic_resist_scaling_early, 
                ap_ability_scaling_late, ad_ability_scaling_late, 
                max_hp_scaling_late, bonus_armor_scaling_late, bonus_magic_resist_scaling_late,
                resource, perk0, perk1, perk2, perk3, perk4, perk5, perk_primary_style, perk_sub_style) VALUES """
rows = ["a"]  # just to get the loop started
i = 0
insert = ""
while len(rows) > 0:
    print("Fetching rows " + str(i) + " to " + str(i + 50))
    rows = srcCursor.fetchmany(50)
    rows = database.createRecord(srcCursor, rows)
    for row in rows:
        champion = championById[str(row.championId)]
        wiki = wikiById[str(row.championId)]
        tags = championById[str(row.championId)]["tags"]
        tag1 = "'" + tags[0] + "'"
        tag2 = "NULL"
        if len(tags) > 1:
            tag2 = "'" + tags[1] + "'"
        # role transform
        role = row.lane
        if role == "BOTTOM":
            if row.lane == "DUO_CARRY":
                role = "MARKSMEN"
            elif row.lane == "DUO_SUPPORT":
                role = "SUPPORT"

        resources = "'" + getOrDefault("partype", champion, "None") + "'";
        # TODO: write directly to list? see TODO below
        # cc
        slow = getOrDefault("slow", wiki["keywords"], 0)
        root = getOrDefault("root", wiki["keywords"], 0)
        stun = getOrDefault("stun", wiki["keywords"], 0)
        charm = getOrDefault("charm", wiki["keywords"], 0)
        knockup = getOrDefault("knockup", wiki["keywords"], 0)
        heal = getOrDefault("heal", wiki["keywords"], 0)
        shield = getOrDefault("shield", wiki["keywords"], 0)
        # champ stats
        stats = champion["stats"]
        hp = stats["hp"]
        hpScaling = stats["hpperlevel"]
        armor = stats["armor"]
        armorScaling = stats["armorperlevel"]
        ad = stats["attackdamage"]
        adScaling = stats["attackdamageperlevel"]
        mres = stats["spellblock"]
        mresScaling = stats["spellblockperlevel"]
        asOffset = stats["attackspeedoffset"]
        asScaling = stats["attackspeedperlevel"]
        # Cooldowns
        cdEarly = wiki["early"]["cooldown"]
        qCdEarly = getOrDefault("1", cdEarly, 0)
        wCdEarly = getOrDefault("2", cdEarly, 0)
        eCdEarly = getOrDefault("3", cdEarly, 0)
        rCdEarly = getOrDefault("4", cdEarly, 0)

        cdLate = wiki["late"]["cooldown"]
        qCdLate = getOrDefault("1", cdLate, 0)
        wCdLate = getOrDefault("2", cdLate, 0)
        eCdLate = getOrDefault("3", cdLate, 0)
        rCdLate = getOrDefault("4", cdLate, 0)

        # Ability scalings
        early = wiki["early"]
        late = wiki["late"]
        ap_ability_scaling_early = getOrDefault("AP", early, 0)
        ad_ability_scaling_early = getOrDefault("AD", early, 0) 
        max_hp_scaling_early = getOrDefault("maximum health", early, 0)
        bonus_armor_scaling_early = getOrDefault("bonus armor", early, 0)
        bonus_magic_resist_scaling_early = getOrDefault("bonus magic resistance", early, 0)
        
        ap_ability_scaling_late = getOrDefault("AP", late, 0)
        ad_ability_scaling_late = getOrDefault("AD", late, 0) 
        max_hp_scaling_late = getOrDefault("maximum health", late, 0)
        bonus_armor_scaling_late = getOrDefault("bonus armor", late, 0)
        bonus_magic_resist_scaling_late = getOrDefault("bonus magic resistance", late, 0)
        # TODO: better with ", ".join(colList)        
        insert += "(" + str(row.championId) + ", " + str(tag1) + ", " + str(tag2) + ", '" + str(role) + "', " \
            + str(root) + ", " + str(slow) + ", " + str(stun) + ", " + str(charm) + ", "\
            + str(knockup) + ", " + str(heal) + ", " + str(shield) +  ", " + str(ad) + ", " + str(hp) + ", " + str(armor) + ", " \
            + str(mres) + ", " + str(asOffset) + ", " + str(adScaling) + ", "\
            + str(hpScaling) + ", " + str(armorScaling) + ", " + str(mresScaling) + ", " + str(asScaling) + ", " \
            + str(qCdEarly) + " , " + str(wCdEarly) + ", " + str(eCdEarly) + " ," + str(rCdEarly) + ", " \
            + str(qCdLate) + " , " + str(wCdLate) + ", " + str(eCdLate) + ", " + str(rCdLate) + ", "\
            + str(ap_ability_scaling_early) + ", " + str(ad_ability_scaling_early) + ", "  \
            + str(max_hp_scaling_early) + ", " + str(bonus_armor_scaling_early) + ", " \
            + str(bonus_armor_scaling_early) + ", "\
            + str(bonus_magic_resist_scaling_early) + ", " + str(ad_ability_scaling_late) + ", "  \
            + str(max_hp_scaling_late) + ", " + str(bonus_armor_scaling_late) + ", " \
            + str(bonus_magic_resist_scaling_late) + ", " + resources + ", "\
            + str(row.perk0) + ", "+ str(row.perk1) + ", "+ str(row.perk2) + ", "+ str(row.perk3) + ", " \
            + str(row.perk4) + ", "+ str(row.perk5) + ", "\
            + str(row.perkPrimaryStyle) + ", " + str(row.perkSubStyle) + ")"
        if i > 0 and i % 50 == 0 and insert != "":
            print("Inserting rows into destination database!")
            destCursor.execute(baseInsert + insert + ";")
            dataDest.commit()
            insert = ""
        else:  # (values), (values), ...
            insert += ","
        i += 1

if insert != "":
    print("Inserting remaining rows")
    destCursor.execute(baseInsert + insert[:-1])  # remove last ,
    dataDest.commit()
print("Done!")
destCursor.close()
srcCursor.close()
