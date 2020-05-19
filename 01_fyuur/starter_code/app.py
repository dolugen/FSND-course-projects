#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from datetime import datetime
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.sql.expression import case
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, csrf
from forms import *
from flask_wtf.csrf import CSRFProtect
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
csrf = CSRFProtect(app)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref='venue')


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist')
  

class Show(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
  start_time = db.Column(db.DateTime, nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  areas = Venue.query.distinct('city', 'state').all()
  for area in areas:
    venues = db.session.query(
                          Venue.id,
                          Venue.name,
                          func.sum(
                            case([(Show.start_time > datetime.now(), 1)], else_=0
                          )).label('num_upcoming_shows'))\
                        .outerjoin(Show)\
                        .group_by(Venue.id, Venue.name)\
                        .filter(Venue.city == area.city, Venue.state == area.state)\
                        .all()
    data.append({
      'city': area.city,
      'state': area.state,
      'venues': venues
    })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
@csrf.exempt
def search_venues():
  term = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{term}%'))
  response={
    "count": result.count(), 
    "data": result
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  upcoming_shows_query = Show.query\
                      .filter(Show.venue_id == venue_id)\
                      .filter(Show.start_time > datetime.now())
  upcoming_shows = upcoming_shows_query.all()
  upcoming_shows_count = upcoming_shows_query.count()
  past_shows_query = Show.query\
                       .filter(Show.venue_id == venue_id)\
                      .filter(Show.start_time < datetime.now())
  past_shows = past_shows_query.all()
  past_shows_count = past_shows_query.count()
  return render_template('pages/show_venue.html',
                        venue=data,
                        upcoming_shows=upcoming_shows,
                        upcoming_shows_count=upcoming_shows_count,
                        past_shows=past_shows,
                        past_shows_count=past_shows_count)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  try:
    venue = Venue()
    if form.validate():
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      for error_group in form.errors.values():
        for error in error_group:
          flash(error)
      return redirect(url_for('create_venue_form'))
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
@csrf.exempt
def search_artists():
  term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{term}%'))
  response = {
    'count': artists.count(),
    'data': artists
  }
  return render_template('pages/search_artists.html', results=response, search_term=term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  upcoming_shows_query = Show.query\
                      .filter(Show.artist_id == artist_id)\
                      .filter(Show.start_time > datetime.now())
  upcoming_shows = upcoming_shows_query.all()
  upcoming_shows_count = upcoming_shows_query.count()
  past_shows_query = Show.query\
                       .filter(Show.artist_id == artist_id)\
                      .filter(Show.start_time < datetime.now())
  past_shows = past_shows_query.all()
  past_shows_count = past_shows_query.count()
  return render_template('pages/show_artist.html',
                        artist=artist,
                        upcoming_shows=upcoming_shows,
                        upcoming_shows_count=upcoming_shows_count,
                        past_shows=past_shows,
                        past_shows_count=past_shows_count)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(
    name=artist.name,
    city=artist.city,
    state=artist.state,
    phone=artist.phone,
    genres=artist.genres,
    image_link=artist.image_link,
    facebook_link=artist.facebook_link,
    website=artist.website,
    seeking_venue=artist.seeking_venue,
    seeking_description=artist.seeking_description
  )
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  if form.validate():
    artist = Artist.query.get(artist_id)
    form.populate_obj(artist)
    db.session.commit()
    db.session.close()
  else:
    breakpoint()
    flash('Something went wront, please check your input')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(
    name=venue.name,
    address=venue.address,
    city=venue.city,
    state=venue.state,
    phone=venue.phone,
    genres=venue.genres,
    image_link=venue.image_link,
    facebook_link=venue.facebook_link,
    website=venue.website,
    seeking_talent=venue.seeking_talent,
    seeking_description=venue.seeking_description
  )
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  if form.validate():
    venue = Venue.query.get(venue_id)
    form.populate_obj(venue)
    db.session.commit()
    db.session.close()
  else:
    flash('Something went wront, please check your input')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  try:
    artist = Artist()
    if form.validate():
      form.populate_obj(artist)
      db.session.add(artist)
      db.session.commit()
      flash('Artist was successfully listed!')
    else:
      for error_group in form.errors.values():
        for error in error_group:
          flash(error)
      return redirect(url_for('create_artist_form'))
  except:
    db.session.rollback()
    flash('An error occurred. Artist could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  shows = Show.query.all()
  for show in shows:
    data.append({
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  try:
    show = Show(
      artist_id=form.artist_id.data,
      venue_id=form.venue_id.data,
      start_time=form.start_time.data
    )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Something went wrong.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
