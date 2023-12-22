#!/usr/bin/python3
"""module used to handle cities"""
from flask import jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.city import City
from models.city import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def city_index(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return j.dumps(list(city, city.to_dict(),
                                state.cities))


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            return json.dumps(city.to_dict)
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
    return jsonify({'error': 'Not found'}), 404


@app_views.route('/states/<state_id>/cities', methods=["POST"])
def post_city(state_id):
    states = storage.all(State).values()
    for state in states:
        if state.id == states_id:
            try:
                info = request.get_json()
                if "name" not in info:
                    return jsonify({"message": "Missing name"}), 400
                city = City()
                city.name = info[name]
                city.state_id = state.id
                storage.new(city)
                storage.save()
                return (city.to_dict(), 201)
            except Exception:
                return jsonify({"message": "Not a JSON"}), 400
        return jsonify({'error': 'Not found'}), 404


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    try:
        info = request.get_json()
        city = storage.all(City).values()
        for key, value in info.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, key, value)
            storage.save()
            return (city.to_dict(), 200)
        return jsonify({'error': 'Not found'}), 404
    except Exception:
        return jsonify({"message": "Not a JSON"}), 400