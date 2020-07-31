# Jared Tewodros
# jmt5rg

import flask
from flask import *
import os
import YoutubeToSpotify
import startup
import google_auth_oauthlib.flow

CLIENT_SECRET_JSON = "C:\\Users\\jared\\codingProjects\\python_projects\\Mixify\\yt_client_secrets.json"
SCOPES = 'https://www.googleapis.com/auth/youtube.force-ssl'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
spot_client_id = ""
spot_client_secret = ""
channel_id = ""

app = Flask(__name__)
app.secret_key = "pc,r~IR~-u(u]pTnN}W:lSwMTl2]6a"

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# load homepage
@app.route("/")
def index():
    return render_template("index.html")


# log into Spotify upon button click
@app.route("/spotLog", methods=["GET"])
def spot_log():
    response = startup.getSpotUser()
    return redirect(response)


@app.route('/callback/', methods=["GET", "POST"])
def spot_authorization():
    global spot_client_id
    global spot_client_secret
    spot_client_secret = startup.getUserToken(request.args['code'])
    spot_client_id = startup.getId(spot_client_secret)
    # print(request)
    return render_template("index.html")


# log into YouTube upon button click
@app.route("/ytLog", methods=["GET"])
def yt_log():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRET_JSON, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('yt_authorization', _external=True)
    authorization_url, state = flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true')

    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/yt_authorization', methods=["GET", "POST"])
def yt_authorization():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_JSON, SCOPES, state=state)
    flow.redirect_uri = flask.url_for('yt_authorization', _external=True)
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    channel_id = startup.getChannelId(flow.credentials)
    return render_template("index.html")


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


# and that's all folks
@app.route("/convert", methods=["POST"])
def success():
    global yt_list
    global sp_list
    global desc
    yt_list = request.form['ytPL']
    sp_list = request.form['spPL']
    desc = request.form['desc']
    cp = YoutubeToSpotify.YouTubePlaylist(spot_client_id, spot_client_secret, channel_id)
    cp.add_song_to_playlist(yt_list, sp_list, desc)
    return render_template("success.html")


if __name__ == "__main__":
    app.run()

