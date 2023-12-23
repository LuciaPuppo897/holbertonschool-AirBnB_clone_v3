#!/usr/bin/python3
"""create a new view for Review that handles all default RESTFul API actions"""
from flask import jsonify, request
from api.v1.views import app_views
import json
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        return jsonify({"Missing user_id"}), 400
    if "text" not in data:
        return jsonify({"Missing text"}), 400
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    review = Review(place_id=place_id, **data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@api_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not data:
        abort(400, description='Not a JSON')
    for k, value in data.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200