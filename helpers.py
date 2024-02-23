import json
from datetime import datetime
from dateutil.parser import parse as parse_date


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def loadBookedPlaces(competitions, clubs):
    booked_places = []
    for competition in competitions:
        for club in clubs:
            booked_places.append({"competition": competition["name"], "club": club["name"], "places": 0})
    return booked_places


def update_booked_places(competition, club, booked_places, places_required):
    for place in booked_places:
        if place['competition'] == competition and place['club'] == club:
            if place['places'] + places_required <= 12:
                place['places'] += places_required
                break
            else:
                raise ValueError('Sorry, you cannot purchase more than 12 places')


def sort_competitions_date(comps):
    past = []
    present = []

    for comp in comps:
        if parse_date(comp['date']) < datetime.now():
            past.append(comp)
        elif parse_date(comp['date']) >= datetime.now():
            present.append(comp)

    return past, present
