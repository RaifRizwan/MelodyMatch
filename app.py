from flask import Flask, request, render_template, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Configure Spotify Client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e31f67e9750b4e398fdc4b57c1ff3422",
                                                           client_secret="a1376810ca244920ad85e270eb9efa60"))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    song_name = request.form['song_name']
    results = sp.search(q=song_name, limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_id = track['id']
        artist_id = track['artists'][0]['id']
        artist = sp.artist(artist_id)
        track_genre = artist['genres'][0] if artist['genres'] else "Unknown Genre"

        recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)
        response = [{
            'name': rec_track['name'],
            'artist': ', '.join(artist['name'] for artist in rec_track['artists']),
            'genre': track_genre
        } for rec_track in recommendations['tracks']]

        return jsonify(response)
    else:
        return jsonify({'error': 'Song not found'})


if __name__ == '__main__':
    app.run(debug=True)
