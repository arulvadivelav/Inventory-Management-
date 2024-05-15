from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from flask_apidoc import ApiDoc

app = Flask(__name__)
ApiDoc(app)

SWAGGER_URL = "/api/docs" 
API_URL = "/static/swagger.json"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "products"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

"""Postgresql Connection"""
# # Database connection parameters
# DB_NAME = "dbname"
# DB_USER = "postgres"
# DB_PASSWORD = "username"
# DB_HOST = "localhost"
# DB_PORT = "5432"

# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# )

"""Sqlite Connection"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_management.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Models
class Products(db.Model):
    id = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(200))

    def __repr__(self):
        return self.id


class Locations(db.Model):
    id = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(200))

    def __repr__(self):
        return self.id


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movement_id = db.Column(db.String(5))
    timestamp = db.Column(db.DateTime, nullable=False)
    from_location_id = db.Column(
        db.String(5), db.ForeignKey("locations.id"), nullable=True
    )
    to_location_id = db.Column(
        db.String(5), db.ForeignKey("locations.id"), nullable=True
    )
    product_id = db.Column(db.String(5), db.ForeignKey("products.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.id


"""Fumction to create a dynamic id's"""


def create_dynamic_id(prefix, number=None):
    dynamic_id = (
        str(prefix) + str(100) if not number else str(prefix) + str(int(number) + 1)
    )
    return dynamic_id


"""This endpoint is used to create(POST) and get(GET) the all product details."""


@app.route("/products", methods=["GET", "POST"])
def products_view():
    # To get the all product details
    if request.method == "GET":
        products_list = []
        products = Products.query.all()
        for product in products:
            products_list.append({"id": product.id, "name": product.name})
        final_result = {
            "status": True,
            "data": products_list,
            "message": "Product details provided successfully.",
            "statuscode": 200,
        }
        return jsonify(final_result, "status")

    # To create a new product
    elif request.method == "POST":
        data = request.json
        if "name" not in data:
            return jsonify(
                {
                    "status": False,
                    "data": {},
                    "message": "Product name is required.",
                    "statuscode": 400,
                }
            )
        # TO create Product id
        create_product_id = Products.query.order_by(Products.id.desc()).all()
        if create_product_id:
            pre_id = create_product_id[0].id
            product_id = create_dynamic_id("PR", pre_id.split("PR")[1])
        else:
            product_id = create_dynamic_id("PR")
        new_product = Products(id=product_id, name=data["name"])
        db.session.add(new_product)
        db.session.commit()
        return jsonify(
            {
                "status": True,
                "data": {},
                "message": "Product added successfully.",
                "statuscode": 200,
            }
        )


"""This endpoint is used to get(GET), update(PUT) and delete(DELETE) a specific product."""


@app.route("/products/<product_id>", methods=["GET", "PUT", "DELETE"])
def product_detail(product_id):
    # To get a specific product details
    if request.method == "GET":
        product = Products.query.filter_by(id=product_id).first()
        if product:
            product_info = {"id": product.id, "name": product.name}
            return jsonify(
                {
                    "status": True,
                    "data": product_info,
                    "message": "Product details provided successfully.",
                    "statuscode": 200,
                }
            )
        return jsonify(
            {
                "status": False,
                "data": {},
                "message": "Product details not found.",
                "statuscode": 400,
            }
        )

    # Update a specific product details
    elif request.method == "PUT":
        data = request.json
        product = Products.query.filter_by(id=product_id).first()
        if product:
            product.name = data["name"]
            db.session.commit()
            return jsonify(
                {
                    "status": True,
                    "data": [],
                    "message": "Product details updated successfully.",
                    "statuscode": 200,
                }
            )
        else:
            return jsonify(
                {
                    "status": False,
                    "data": [],
                    "message": "Product details not found.",
                    "statuscode": 400,
                }
            )


"""This endpoint is used to create(POST) and get(GET) the all location details."""


@app.route("/locations", methods=["GET", "POST"])
def location_view():
    # To get the all location details
    if request.method == "GET":
        locations_list = []
        locations = Locations.query.all()
        for location in locations:
            locations_list.append({"id": location.id, "name": location.name})
        final_result = {
            "status": True,
            "data": locations_list,
            "message": "Location details provided successfully.",
            "statuscode": 200,
        }
        return jsonify(final_result, "status")

    # To create a new location
    elif request.method == "POST":
        data = request.json
        if "name" not in data:
            return jsonify(
                {
                    "status": False,
                    "data": {},
                    "message": "Location name is required.",
                    "statuscode": 400,
                }
            )
        # TO create Location id
        create_location_id = Locations.query.order_by(Locations.id.desc()).all()
        if create_location_id:
            pre_id = create_location_id[0].id
            location_id = create_dynamic_id("LC", pre_id.split("LC")[1])
        else:
            location_id = create_dynamic_id("LC")

        new_location = Locations(id=location_id, name=data["name"])
        db.session.add(new_location)
        db.session.commit()
        return jsonify(
            {
                "status": True,
                "data": {},
                "message": "Location added successfully.",
                "statuscode": 200,
            }
        )


"""This endpoint is used to get(GET), update(PUT) and delete(DELETE) a specific location."""


@app.route("/locations/<location_id>", methods=["GET", "PUT", "DELETE"])
def location_detail(location_id):
    # To get a specific location details
    if request.method == "GET":
        location = Locations.query.filter_by(id=location_id).first()
        if location:
            location_info = {"id": location.id, "name": location.name}
            return jsonify(
                {
                    "status": True,
                    "data": location_info,
                    "message": "Location details provided successfully.",
                    "statuscode": 200,
                }
            )
        return jsonify(
            {
                "status": False,
                "data": {},
                "message": "Location details not found.",
                "statuscode": 400,
            }
        )

    # Update a specific location details
    elif request.method == "PUT":
        data = request.json
        location = Locations.query.filter_by(id=location_id).first()
        if location:
            location.name = data["name"]
            db.session.commit()
            return jsonify(
                {
                    "status": True,
                    "data": [],
                    "message": "Location details updated successfully.",
                    "statuscode": 200,
                }
            )
        else:
            return jsonify(
                {
                    "status": False,
                    "data": [],
                    "message": "Location details not found.",
                    "statuscode": 400,
                }
            )


"""This endpoint is used to create(POST) and get(GET) the all product movement details."""


@app.route("/product_movement", methods=["GET", "POST"])
def product_movement_view():
    # To get the all product movement details
    if request.method == "GET":
        product_movement_list = []
        product_movement = ProductMovement.query.all()
        for pro_move in product_movement:
            product_movement_list.append(
                {
                    "id": pro_move.id,
                    "movement_id": pro_move.movement_id,
                    "timestamp": datetime.strftime(
                        pro_move.timestamp, "%Y-%m-%d %H:%M:%S"
                    ),
                    "from_location_id": pro_move.from_location_id,
                    "to_location_id": pro_move.to_location_id,
                    "product_id": pro_move.product_id,
                    "qty": pro_move.qty,
                }
            )
        final_result = {
            "status": True,
            "data": product_movement_list,
            "message": "Product movement details provided successfully.",
            "statuscode": 200,
        }
        return jsonify(final_result, "status")

    # To create a new product movement
    elif request.method == "POST":
        data = request.json
        try:
            from_location = data["from_location_id"]
            to_location = data["to_location_id"]
            product = data["product_id"]
            qty = data["qty"]
        except:
            return jsonify(
                {
                    "status": False,
                    "data": {},
                    "message": "Required fields are missing.",
                    "statuscode": 400,
                }
            )
        try:
            # TO create Produc
            create_movement_id = ProductMovement.query.order_by(
                ProductMovement.id.desc()
            ).all()
            if create_movement_id:
                pre_id = create_movement_id[0].movement_id
                movement_id = create_dynamic_id("PM", pre_id.split("PM")[0])
            else:
                movement_id = create_dynamic_id("PM")

            new_product_movement = ProductMovement(
                movement_id=movement_id,
                timestamp=datetime.now(),
                from_location_id=from_location if from_location else None,
                to_location_id=to_location if to_location else None,
                product_id=product,
                qty=qty,
            )
            db.session.add(new_product_movement)
            db.session.commit()
            return jsonify(
                {
                    "status": True,
                    "data": {},
                    "message": "Product movement details added successfully.",
                    "statuscode": 200,
                }
            )
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "status": False,
                    "data": {},
                    "message": "Something went wrong try again later.",
                    "statuscode": 500,
                }
            )


"""This endpoint is used to get(GET), update(PUT) and delete(DELETE) a specific product movement."""


@app.route("/product_movement/<movement_id>", methods=["GET", "PUT", "DELETE"])
def product_movement_detail(movement_id):
    # To get a specific product movement details
    if request.method == "GET":
        product_movement = ProductMovement.query.filter_by(
            movement_id=movement_id
        ).first()
        if product_movement:
            product_movement_info = {
                "id": product_movement.id,
                "movement_id": product_movement.movement_id,
                "timestamp": datetime.strftime(
                    product_movement.timestamp, "%Y-%m-%d %H:%M:%S"
                ),
                "from_location_id": product_movement.from_location_id,
                "to_location_id": product_movement.to_location_id,
                "product_id": product_movement.product_id,
                "qty": product_movement.qty,
            }
            return jsonify(
                {
                    "status": True,
                    "data": product_movement_info,
                    "message": "Product movement details provided successfully.",
                    "statuscode": 200,
                }
            )
        return jsonify(
            {
                "status": False,
                "data": {},
                "message": "Details not found.",
                "statuscode": 400,
            }
        )

    # Update a specific product movement details
    elif request.method == "PUT":
        data = request.json
        pro_movement = ProductMovement.query.filter_by(movement_id=movement_id).first()
        try:
            from_location = data["from_location_id"]
            to_location = data["to_location_id"]
            product = data["product_id"]
            qty = data["qty"]
        except:
            return jsonify(
                {
                    "status": False,
                    "data": {},
                    "message": "Required fields are missing.",
                    "statuscode": 400,
                }
            )
        if pro_movement:
            pro_movement.from_location_id = from_location
            pro_movement.to_location_id = to_location
            pro_movement.product_id = product
            pro_movement.qty = qty

            db.session.commit()
            return jsonify(
                {
                    "status": True,
                    "data": [],
                    "message": "Details updated successfully.",
                    "statuscode": 200,
                }
            )
        else:
            return jsonify(
                {
                    "status": False,
                    "data": [],
                    "message": "Details not found.",
                    "statuscode": 400,
                }
            )


"""This endpoint is used to get(GET) the overall report"""


@app.route("/report", methods=["GET"])
def report():
    try:
        # To get a specific product movement details
        if request.method == "GET":
            available_qty = (
                db.session.query(
                    Locations.id,
                    Locations.name,
                    db.func.sum(ProductMovement.qty).label("total_quantity"),
                )
                .join(ProductMovement, ProductMovement.to_location_id == Locations.id)
                .group_by(Locations.id)
                .all()
            )
            moved_qty = (
                db.session.query(
                    Locations.id,
                    Locations.name,
                    db.func.sum(ProductMovement.qty).label("total_quantity"),
                )
                .join(ProductMovement, ProductMovement.from_location_id == Locations.id)
                .group_by(Locations.id)
                .all()
            )

            remaining_qty = []
            for available, moved in zip(available_qty, moved_qty):
                location_id = available.id
                location_name = available.name
                available_quantity = (
                    available.total_quantity if available.total_quantity else 0
                )
                moved_quantity = moved.total_quantity if moved.total_quantity else 0
                remaining_quantity = (
                    available_quantity - moved_quantity
                    if moved_quantity
                    else available_quantity
                )

                remaining_qty.append(
                    {
                        "location_id": location_id,
                        "location_name": location_name,
                        "remaining_quantity": remaining_quantity,
                    }
                )
            return jsonify(
                {
                    "status": True,
                    "data": remaining_qty,
                    "message": "Report generated successfully.",
                    "statuscode": 200,
                }
            )

    except Exception as e:
        print(e)
        return jsonify(
            {
                "status": False,
                "data": {},
                "message": "Something went wrong.",
                "statuscode": 500,
            }
        )


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()