from flask import json
from flask_restful import Resource, reqparse
from models.FWN import FWNModel
from flask_jwt_extended import jwt_required
from flask import request


class FWNSongs(Resource):
    def get(self):
        title_filter = request.args.get('title')
        artist_filter = request.args.get('artist')
        album_filter = request.args.get('album')
        release_date_filter = request.args.get('release_date')
        time_filter = request.args.get('time')

        songs = FWNModel.query

        if title_filter:
            songs = songs.filter_by(title=title_filter)
        if artist_filter:
            songs = songs.filter_by(artist=artist_filter)
        if album_filter:
            songs = songs.filter_by(album=album_filter)
        if release_date_filter:
            songs = songs.filter_by(release_date=release_date_filter)
        if time_filter:
            songs = songs.filter_by(time=time_filter)
        return {"Favourite Worst Nightmare Songs": [song.json() for song in songs.all()]}


class FWNId(Resource):
    args = reqparse.RequestParser()
    args.add_argument('title', type=str, required=True,
                      help="The field 'title' cannot be left blank.")
    args.add_argument('artist', type=str, required=True,
                      help="The field 'artist' cannot be left blank.")
    args.add_argument('album', type=str, required=True,
                      help="The field 'album' cannot be left blank.")
    args.add_argument('release_date', type=str, required=True,
                      help="The field 'release_date' cannot be left blank.")
    args.add_argument('time', type=str, required=True,
                      help="The field 'time' cannot be left blank.")

    def get(self, FWN_id):
        song = FWNModel.find_song(FWN_id)
        if song:
            return song.json()
        return {" Favourite Worst Nightmare Songs": None}, 404

    @jwt_required()
    def post(self, FWN_id):
        if FWNModel.find_song(FWN_id):
            # Bad Request
            return {"message": f"Favourite Worst Nightmare Songs song id {FWN_id} already exists."}, 400
        data_post = FWNId.args.parse_args()
        new_song = FWNModel(FWN_id, **data_post)
        try:
            new_song.save_song()
        except:
            return {'message': 'An internal error ocurred trying to save Favourite Worst Nightmare Songs song.'}, 500
        return new_song.json(), 201  # Created

    @jwt_required()
    def put(self, FWN_id):
        data_put = FWNId.args.parse_args()
        search_song = FWNModel.find_song(FWN_id)
        if search_song:
            search_song.update_song(**data_put)
            search_song.save_song()
            return search_song.json(), 200

        new_song = FWNModel(FWN_id, **data_put)
        try:
            new_song.save_song()
        except:
            return {'message': "An internal error ocurred trying to save  Favourite Worst Nightmare Songs song."}, 500
        return new_song.json(), 201  # Created

    @jwt_required()
    def delete(self, FWN_id):
        song = FWNModel.find_song(FWN_id)
        if song:
            try:
                song.delete_song()
            except:
                return {'message': "An internal error ocurred trying to delete Favourite Worst Nightmare Songs song."}, 500
            return {'message': " Favourite Worst Nightmare Songs"}, 404
