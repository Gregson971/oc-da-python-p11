import json
from flask import Flask, render_template, request, redirect, flash, url_for
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


def update_booked_places(competition, club, places_required):
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


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()
booked_places = loadBookedPlaces(competitions, clubs)
past_competitions, present_competitions = sort_competitions_date(competitions)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template(
            'welcome.html', club=club, past_competitions=past_competitions, present_competitions=present_competitions
        )
    except IndexError:
        if request.form["email"] == "":
            flash("Please enter your email address")
        else:
            flash("The email address you entered does not exist")
        return render_template("index.html"), 401


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        if parse_date(found_competition['date']) < datetime.now():
            flash("This competition is over.", 'error')
            return (
                render_template(
                    'welcome.html',
                    club=club,
                    past_competitions=past_competitions,
                    present_competitions=present_competitions,
                ),
                403,
            )
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again", 'error')
        return (
            render_template(
                'welcome.html',
                club=club,
                past_competitions=past_competitions,
                present_competitions=present_competitions,
            ),
            403,
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    if int(club['points']) < places_required:
        flash('You do not have enough points')
        return render_template('booking.html', club=club, competition=competition), 400
    elif places_required > 12:
        flash('Sorry, you cannot purchase more than 12 places')
        return render_template('booking.html', club=club, competition=competition), 400
    else:
        try:
            update_booked_places(competition['name'], club['name'], places_required)
            club['points'] = int(club['points']) - places_required
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
            flash('Great-booking complete!', 'success')
            return render_template(
                'welcome.html',
                club=club,
                past_competitions=past_competitions,
                present_competitions=present_competitions,
            )
        except ValueError as e:
            flash(e, 'error')
            return render_template('booking.html', club=club, competition=competition), 400


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
