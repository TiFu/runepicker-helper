#! /usr/bin/env python3.6

# main.py <summoner_name> <region>
# Key provided through environment variable RIOT_API_KEY
import random, math, sys, time
import json
from sortedcontainers import SortedList
from datetime import datetime

import cassiopeia as cass
from cassiopeia.core import Summoner, MatchHistory, Match, League
from cassiopeia.data import Queue, Tier, Division
from cassiopeia.datastores.riotapi.common import APIError, APIRequestError

unpulled_summoner_ids = SortedList()
pulled_summoner_ids = SortedList()

unpulled_match_ids = SortedList()
pulled_match_ids = SortedList()

def filter_match_history(summoner):
    if summoner.league_positions[Queue.ranked_solo_fives] and not Tier(summoner.league_positions[Queue.ranked_solo_fives].to_dict()["tier"]) in (Tier.bronze, Tier.silver):
        end_time = int(datetime.now().timestamp())*1000
        match_history = MatchHistory(summoner=summoner, region=summoner.region, queues={Queue.ranked_solo_fives}, begin_time=1512518400000, end_time=end_time)
        return match_history
    else:
        return []


def collect_matches(initial_summoner_name, region):
    if len(unpulled_summoner_ids) <= 0:
        summoner = Summoner(name=initial_summoner_name, region=region)
        unpulled_summoner_ids.add(summoner.id)
    while unpulled_summoner_ids:
        # Get a random summoner from our list of unpulled summoners and pull their match history
        new_summoner_id = random.choice(unpulled_summoner_ids)
        new_summoner = Summoner(id=new_summoner_id, region=region)
        matches = filter_match_history(new_summoner)
        unpulled_match_ids.update([match.id for match in matches])
        unpulled_summoner_ids.remove(new_summoner_id)
        pulled_summoner_ids.add(new_summoner_id)

        while unpulled_match_ids:
            # Get a random match from our list of matches
            new_match_id = random.choice(unpulled_match_ids)
            new_match = Match(id=new_match_id, region=region)
            new_match.timeline.frame_interval
            for participant in new_match.participants:
                if participant.summoner.id not in pulled_summoner_ids and participant.summoner.id not in unpulled_summoner_ids:
                    unpulled_summoner_ids.add(participant.summoner.id)
            unpulled_match_ids.remove(new_match_id)
            pulled_match_ids.add(new_match_id)

if __name__ == "__main__":
    cass.apply_settings("config.json")
    while True:
        try:
            collect_matches(sys.argv[1], sys.argv[2])
        except (APIError, APIRequestError) as e:
            if e.code == 403:
                print("APIKey is not valid or expired")
                break
            else:
                print("An APIError occured")
                time.sleep(5)
