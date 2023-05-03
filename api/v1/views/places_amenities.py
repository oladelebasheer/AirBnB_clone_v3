#!/usr/bin/python3
"""amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv


@app_views.route('/places/<place_id>/amenities/', methods=['GET'])
def list_place_amenities(place_id):
    '''Retrieves a list of all Amenity objects of a place'''
    places = storage.all("Place").values()
    place = [place for place in places if place.id == place_id]
    if place == []:
        abort(404)
    list_amenities_dict = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        list_amenities = [obj.amenities for obj in places if obj.id == place_id]
        if list_amenities[0] != []:
            list_amenities_dict = [obj.to_dict() for obj in list_amenities[0]]
        return jsonify(list_amenities_dict)
    else:
        list_amenities = [obj.amenities for obj in places if obj.id == place_id]
        if list_amenities[0] != []:
            list_amenities_dict = [obj.to_dict() for obj in list_amenities[0]]
        return jsonify(list_amenities_dict)

@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    '''Deletes an Amenity object'''
    all_amenities = storage.all("Amenity").values()
    all_places = storage.all("Place").values()
    amenity_obj = [obj for obj in all_amenities
                   if obj.id == amenity_id]
    place_obj = [obj for obj in all_places
                   if obj.id == place_id]
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = [obj.amenities for obj in all_places
                           if obj.id == place_id]
        if amenity_obj == [] or place_obj == [] or\
                amenity_obj[0] not in place_amenities[0]:
            abort(404)
        place_amenities[0].remove(amenity_obj[0])
    else:
        place_amenities = [obj.amenity_ids for obj in all_places if obj.id == place_id]
        if amenity_obj == [] or place_obj == [] or\
            place_obj[0].id not in place_amenities[0]:
                abort(404)
        place_amenities[0].remove(amenity_obj[0].id)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    '''Updates an Amenity object'''
    all_amenities = storage.all("Amenity").values()
    amenity_obj = [obj for obj in all_amenities
                   if obj.id == amenity_id]
    all_places = storage.all("Place").values()
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = [obj.amenities for obj in all_places
                           if obj.id == place_id]
        
        if amenity_obj == [] or place_amenities == []:
            abort(404)
        if amenity_obj[0] not in place_amenities[0]:
            place_amenities[0].append(amenity_obj[0])
            storage.save()
            return jsonify(amenity_obj[0].to_dict()), 201
        else:
            return jsonify(amenity_obj[0].to_dict()), 200
    else:
        place_amenities = [obj.amenity_ids for obj in all_places if obj.id == place_id]
         
        if amenity_obj == [] or place_amenities == []:
            abort(404)
        if amenity_obj[0] not in place_amenities[0]:
            place_amenities[0].append(amenity_obj[0].id)
            storage.save()
            return jsonify(list(amenity_obj[0])), 201
        else:
            return jsonify(list(amenity_obj[0].id)), 200
    
    
