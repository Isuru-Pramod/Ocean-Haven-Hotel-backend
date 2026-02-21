from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from services.blockchain import (
    build_create_asset_tx,
    build_buy_primary_tx,
    build_list_shares_tx,
    build_buy_listing_tx,
    build_update_asset_tx,     # 🔥 NEW
    build_delete_asset_tx,     # 🔥 NEW
    get_asset,
    get_total_assets,
    get_listing
)

assets = Blueprint("assets", __name__)

# =========================================================
# ADMIN - CREATE ASSET
# =========================================================

@assets.route("/create", methods=["POST"])
@jwt_required()
def create_asset():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    data = request.json

    required_fields = [
        "name",
        "location",
        "description",     # 🔥 NEW
        "image_url",       # 🔥 NEW
        "total_shares",
        "share_price"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    result = build_create_asset_tx(
        data["name"],
        data["location"],
        data["description"],     # 🔥 NEW
        data["image_url"],       # 🔥 NEW
        int(data["total_shares"]),
        int(data["share_price"]),
        claims["wallet"]
    )

    return jsonify(result)


# =========================================================
# ADMIN - UPDATE ASSET (Only if no shares sold)
# =========================================================

@assets.route("/update", methods=["PUT"])
@jwt_required()
def update_asset():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    data = request.json

    required_fields = [
        "asset_id",
        "name",
        "location",
        "description",
        "image_url",
        "share_price"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    result = build_update_asset_tx(
        int(data["asset_id"]),
        data["name"],
        data["location"],
        data["description"],
        data["image_url"],
        int(data["share_price"]),
        claims["wallet"]
    )

    return jsonify(result)


# =========================================================
# ADMIN - DELETE ASSET (Only if no shares sold)
# =========================================================

@assets.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_asset():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    data = request.json

    if "asset_id" not in data:
        return jsonify({"error": "asset_id is required"}), 400

    result = build_delete_asset_tx(
        int(data["asset_id"]),
        claims["wallet"]
    )

    return jsonify(result)


# =========================================================
# PRIMARY MARKET - BUY SHARES
# =========================================================

@assets.route("/buy-primary", methods=["POST"])
@jwt_required()
def buy_primary():

    claims = get_jwt()

    if claims["role"] != "customer":
        return jsonify({"message": "Customer only"}), 403

    data = request.json

    total_value = int(data["amount"]) * int(data["share_price"])

    result = build_buy_primary_tx(
        int(data["asset_id"]),
        int(data["amount"]),
        claims["wallet"],
        total_value
    )

    return jsonify(result)


# =========================================================
# MARKETPLACE - SELL SHARES
# =========================================================

@assets.route("/sell", methods=["POST"])
@jwt_required()
def sell_shares():

    claims = get_jwt()

    if claims["role"] != "customer":
        return jsonify({"message": "Customer only"}), 403

    data = request.json

    result = build_list_shares_tx(
        int(data["asset_id"]),
        int(data["amount"]),
        int(data["price_per_share"]),
        claims["wallet"]
    )

    return jsonify(result)


# =========================================================
# MARKETPLACE - BUY LISTED SHARES
# =========================================================

@assets.route("/buy-listing", methods=["POST"])
@jwt_required()
def buy_listing():

    claims = get_jwt()

    if claims["role"] != "customer":
        return jsonify({"message": "Customer only"}), 403

    data = request.json

    total_value = int(data["amount"]) * int(data["price_per_share"])

    result = build_buy_listing_tx(
        int(data["listing_id"]),
        claims["wallet"],
        total_value
    )

    return jsonify(result)


# =========================================================
# PUBLIC READ ENDPOINTS
# =========================================================

@assets.route("/total", methods=["GET"])
def total_assets():
    return jsonify(get_total_assets())


@assets.route("/<int:asset_id>", methods=["GET"])
def single_asset(asset_id):
    return jsonify(get_asset(asset_id))


@assets.route("/listing/<int:listing_id>", methods=["GET"])
def single_listing(listing_id):
    return jsonify(get_listing(listing_id))