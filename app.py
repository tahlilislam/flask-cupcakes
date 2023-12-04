"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

with app.app_context():

    @app.route('/api/cupcakes')
    def all_cupcakes():
        """Returns json data of all cupcake listings"""
        all_cupcakes = [cupcake.serialize_cupcake() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=all_cupcakes)
    
    @app.route('/api/cupcakes/<int:id>')
    def get_cupcake(id):
        """Returns JSON for one cupcake in particular"""
        cupcake = Cupcake.query.get_or_404(id)
        return jsonify(cupcake=cupcake.serialize_cupcake())
    
    @app.route('/api/cupcakes', methods=["POST"])
    def create_cupcake():
        """Create a cupcake with flavor, size, rating and image data from the body of the request and responds with json"""
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]
        image = request.json.get("image")

        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

        db.session.add(new_cupcake)
        db.session.commit()

        response_json = jsonify(cupcake=new_cupcake.serialize_cupcake())
        return (response_json, 201)
    
    @app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
    def update_cupcake(id):
        """Updates a particular cupake information and responds w/ JSON """
        cupcake = Cupcake.query.get_or_404(id)
        cupcake.flavor = request.json.get('flavor', cupcake.flavor)
        cupcake.size = request.json.get('size', cupcake.size)
        cupcake.rating = request.json.get('rating', cupcake.rating)
        cupcake.image = request.json.get('image', cupcake.image)
 
        db.session.commit()
        return jsonify(cupcake=cupcake.serialize_cupcake())