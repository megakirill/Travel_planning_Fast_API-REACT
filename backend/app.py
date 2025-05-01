from flask import Flask, request, jsonify


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"


@app.route("/trips/", methods=["POST"])
def create_trip():
    data = request.get_json()
    new_trip = Trip(title=data["title"])
    db.session.add(new_trip)
    db.session.commit()
    return jsonify({"message": "Trip created!"}), 201

@app.route("/trips/<int:trip_id>", methods=["GET"])
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify({"id": trip.id, "title": trip.title})