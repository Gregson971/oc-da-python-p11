from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
from dateutil.parser import parse as parse_date
from helpers import loadClubs, loadCompetitions, loadBookedPlaces, update_booked_places, sort_competitions_date


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
            flash("Please enter your email address", "error")
        else:
            flash("The email address you entered does not exist")
        return render_template("index.html"), 401


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]

        if found_club and found_competition:
            if parse_date(found_competition['date']) < datetime.now():
                flash("This competition is over.", "error")
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

    except IndexError:
        flash("Something went wrong-please try again", "error")
        return (
            render_template(
                'welcome.html',
                club=club,
                past_competitions=past_competitions,
                present_competitions=present_competitions,
            ),
            404,
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    try:
        places_required = int(request.form['places'])
    except ValueError:
        flash('Please enter a valid number for places.', 'error')
        return render_template('booking.html', club=club, competition=competition), 400

    if int(club['points']) < places_required:
        flash('You do not have enough points', 'error')
        return render_template('booking.html', club=club, competition=competition), 400
    elif places_required > 12:
        flash('Sorry, you cannot purchase more than 12 places', 'error')
        return render_template('booking.html', club=club, competition=competition), 400
    elif places_required < 1:
        flash('Please enter a number between 0 and 12.', 'error')
        return render_template('booking.html', club=club, competition=competition), 400
    else:
        update_booked_places(competition['name'], club['name'], booked_places, places_required)
        club['points'] = int(club['points']) - places_required
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        flash('Great-booking complete!', 'success')
        return render_template(
            'welcome.html',
            club=club,
            past_competitions=past_competitions,
            present_competitions=present_competitions,
        )


@app.route('/dashboard')
def view_clubs():
    club_list = sorted(clubs, key=lambda club: club['name'])
    return render_template('dashboard.html', clubs=club_list)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
