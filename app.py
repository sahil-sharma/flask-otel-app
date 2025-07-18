from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
from models import db, Users, Items
from config import Config
from datetime import datetime, timedelta, timezone
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, requests, logging
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from prometheus_flask_exporter import PrometheusMetrics
import logging

# App Setup
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
metrics = PrometheusMetrics(app)

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tracing Setup (Optional)
if Config.TRACING_ENABLED:
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import SERVICE_NAME, Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.instrumentation.flask import FlaskInstrumentor

        resource = Resource(attributes={SERVICE_NAME: "crud-app"})
        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer = trace.get_tracer(__name__)
        span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=Config.OTLP_ENDPOINT))
        trace.get_tracer_provider().add_span_processor(span_processor)
        FlaskInstrumentor().instrument_app(app)
        logger.info("Tracing enabled and configured.")
    except Exception as e:
        tracer = None
        TRACING_ENABLED = False
        logger.warning(f"Tracing setup failed: {e}")
else:
    tracer = None

# JWT Utility
def create_token(user_id):
    user = Users.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
    return token if isinstance(token, str) else token.decode("utf-8")

# Auth Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"msg": "Token is missing or malformed"}), 403
        token = auth_header.replace("Bearer ", "").strip()
        try:
            decoded = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
            current_user = Users.query.get(int(decoded["sub"]))
            if not current_user:
                return jsonify({"msg": "User not found"}), 404
            g.current_user = current_user

            if tracer:
                with tracer.start_as_current_span("authenticated-request") as span:
                    span.set_attribute("user.id", current_user.id)
                    span.set_attribute("user.username", current_user.username)

        except ExpiredSignatureError:
            return jsonify({"msg": "Token has expired"}), 401
        except InvalidTokenError as e:
            return jsonify({"msg": "Token is invalid"}), 401
        except Exception as e:
            logger.exception("Unexpected error during token validation")
            return jsonify({"msg": "Something went wrong"}), 500

        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route("/")
def home():
    return jsonify({"message": "Welcome to CRUD App version v1!"})

@app.route("/healthz")
def healthz():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.exception("Health check failed")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if Users.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "User already exists"}), 400
    hashed_password = generate_password_hash(data["password"])
    user = Users(username=data["username"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = Users.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401
    token = create_token(user.id)
    return jsonify({"access_token": token})

# ITEM ROUTES

@app.route("/items/create", methods=["POST"])
@token_required
def create_item(current_user):
    data = request.get_json()
    item = Items(name=data["name"], description=data["description"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name, "description": item.description}), 201

@app.route("/items/all", methods=["GET"])
@token_required
def list_items(current_user):
    items = Items.query.all()
    return jsonify([{"id": i.id, "name": i.name, "description": i.description} for i in items])

@app.route("/items", methods=["GET"])
@token_required
def get_item_by_query(current_user):
    item_id = request.args.get("item_id")
    if not item_id:
        return jsonify({"msg": "Missing item_id query parameter"}), 400
    item = Items.query.get_or_404(item_id)
    return jsonify({"id": item.id, "name": item.name, "description": item.description})


@app.route("/items/update", methods=["PUT", "PATCH"])
@token_required
def update_item(current_user):
    item_id = request.args.get("item_id")
    if not item_id:
        return jsonify({"msg": "item_id query parameter is required"}), 400
    item = Items.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name, "description": item.description})

@app.route("/items/delete", methods=["DELETE"])
@token_required
def delete_item(current_user):
    item_id = request.args.get("item_id")
    if not item_id:
        return jsonify({"msg": "item_id query parameter is required"}), 400
    item = Items.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"msg": "Item deleted"})

@app.route("/external", methods=["GET"])
def external():
    logger.info(f"An external call being made.")
    resp = requests.get("https://httpbin.org/get")
    return resp.json()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logger.info("Database tables created (if not already existing).")
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=5000)
