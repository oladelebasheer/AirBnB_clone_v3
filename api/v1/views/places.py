#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    '''Retrieves a list of all Place objects in city'''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    list_places = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Retrieves a Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    return jsonify(place_obj[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places
                 if obj.id == place_id]
    if place_obj == []:
        abort(404)
    place_obj.remove(place_obj[0])
    for obj in all_places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    '''Creates a Place'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities
                if obj.id == city_id]
    if city_obj == []:
        abort(404)
    places = []
    new_place = Place(name=request.json['name'],
                      user_id=request.json['user_id'], city_id=city_id)
    all_users = storage.all("User").values()
    user_obj = [obj.to_dict() for obj in all_users
                if obj.id == new_place.user_id]
    if user_obj == []:
        abort(404)
    storage.new(new_place)
    storage.save()
    places.append(new_place.to_dict())
    return jsonify(places[0]), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updates_place(place_id):
    '''Updates a Place object'''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if place_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' in request.get_json():
        place_obj[0]['name'] = request.json['name']
    if 'description' in request.get_json():
        place_obj[0]['description'] = request.json['description']
    if 'number_rooms' in request.get_json():
        place_obj[0]['number_rooms'] = request.json['number_rooms']
    if 'number_bathrooms' in request.get_json():
        place_obj[0]['number_bathrooms'] = request.json['number_bathrooms']
    if 'max_guest' in request.get_json():
        place_obj[0]['max_guest'] = request.json['max_guest']
    if 'price_by_night' in request.get_json():
        place_obj[0]['price_by_night'] = request.json['price_by_night']
    if 'latitude' in request.get_json():
        place_obj[0]['latitude'] = request.json['latitude']
    if 'longitude' in request.get_json():
        place_obj[0]['longitude'] = request.json['longitude']
    for obj in all_places:
        if obj.id == place_id:
            if 'name' in request.get_json():
                obj.name = request.json['name']
            if 'description' in request.get_json():
                obj.description = request.json['description']
            if 'number_rooms' in request.get_json():
                obj.number_rooms = request.json['number_rooms']
            if 'number_bathrooms' in request.get_json():
                obj.number_bathrooms = request.json['number_bathrooms']
            if 'max_guest' in request.get_json():
                obj.max_guest = request.json['max_guest']
            if 'price_by_night' in request.get_json():
                obj.price_by_night = request.json['price_by_night']
            if 'latitude' in request.get_json():
                obj.latitude = request.json['latitude']
            if 'longitude' in request.get_json():
                obj.longitude = request.json['longitude']
    storage.save()
    return jsonify(place_obj[0]), 200


@app_views.route('/places_search', methods=['POST'])
def search_places():
    ''' search for places in cities and states '''
    places_objs = []
    all_states = storage.all('State').values()
    all_cities = storage.all('City').values()
    all_places = storage.all('Place').values()

    json_data = request.get_json()
    states_data = None
    cities_data = None
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'states' in json_data and json_data['states'] != []:
        states_data = json_data['states']
    if 'cities' in json_data and json_data['cities'] != []:
        cities_data = json_data['cities']
    if len(json_data) == 0 or (states_data is None and cities_data is None):
        places_objs = [obj for obj in all_places]
    elif cities_data is None:
        states_json = json_data['states']
        valid_states = [state for state in all_states
                        if state.id in states_json]
        valid_cities = []
        for state in valid_states:
            valid_cities.extend(state.cities)
        for city in valid_cities:
            places_objs.extend(city.places)
    elif states_data is None:
        cities_json = json_data['cities']
        valid_cities = [city for city in all_cities if city.id in cities_json]
        for city in valid_cities:
            places_objs.extend(city.places)
    else:
        states_json = json_data['states']
        valid_states = [state for state in all_states
                        if state.id in states_json]
        valid_state_cities = []
        for state in valid_states:
            valid_state_cities.extend(state.cities)
        for city in valid_state_cities:
            places_objs.extend(city.places)
        cities_json = json_data['cities']
        valid_cities = [city for city in all_cities if city.id in cities_json]
        for city in valid_cities:
            if city not in valid_state_cities:
                places_objs.extend(city.places)
    if 'amenities' in json_data\
            and len(json_data['amenities']):
        place_objs = [place.to_dict() for place in places_objs if
                      all(x in [a.id for a in place.amenities] for x in
                          json_data['amenities'])]
        for place in place_objs:
            amens = [amen.to_dict() for amen in place['amenities']]
            place['amenities'] = amens
        places_objs = place_objs
        return jsonify(places_objs)
    return jsonify([place.to_dict() for place in places_objs])
