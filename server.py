import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
from dateutil.parser import parse as parse_date


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


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
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
past_competitions, present_competitions = sort_competitions_date(competitions)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template(
        'welcome.html', club=club, past_competitions=past_competitions, present_competitions=present_competitions
    )


@app.route('/book/<competition>/<club>')
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
                400,
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
            400,
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!', 'success')
    return render_template(
        'welcome.html',
        club=club,
        past_competitions=past_competitions,
        present_competitions=present_competitions,
    )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
