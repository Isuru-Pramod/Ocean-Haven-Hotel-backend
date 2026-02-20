from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.blockchain import (
    build_create_asset_tx,
    build_buy_primary_tx,
    build_list_shares_tx,
    build_buy_listing_tx,
    get_asset,
    get_total_assets,
    get_listing
)

assets = Blueprint("assets", __name__)

# =====================================================
# ADMIN - CREATE ASSET
# =====================================================

@assets.route("/create", methods=["POST"])
@jwt_required()
def create_asset():

    user_id = get_jwt_identity()   # "1"
    claims = get_jwt()             # full JWT payload

    print("User identity:", user_id)

    # ✅ Check admin
    if claims["role"] != "admin":
        return jsonify({"error": "Admin only"}), 403

    # ✅ Get wallet from claims
    user_wallet = claims["wallet"]

    print("User wallet:", user_wallet)

    data = request.json

    result = build_create_asset_tx(
        data["name"],
        data["location"],
        int(data["total_shares"]),
        int(data["share_price"]),
        claims["wallet"]
    )

    return jsonify(result)


# =====================================================
# PRIMARY MARKET - BUY SHARES
# =====================================================

@assets.route("/buy-primary", methods=["POST"])
@jwt_required()
def buy_primary():

    identity = get_jwt_identity()

    if identity["role"] != "customer":
        return jsonify({"success": False, "message": "Customer only"}), 403

    data = request.json

    total_value = int(data["amount"]) * int(data["share_price"])

    result = build_buy_primary_tx(
        int(data["asset_id"]),
        int(data["amount"]),
        identity["wallet"],
        total_value
    )

    return jsonify(result)


# =====================================================
# MARKETPLACE - SELL SHARES
# =====================================================

@assets.route("/sell", methods=["POST"])
@jwt_required()
def sell_shares():

    identity = get_jwt_identity()

    if identity["role"] != "customer":
        return jsonify({"success": False, "message": "Customer only"}), 403

    data = request.json

    result = build_list_shares_tx(
        int(data["asset_id"]),
        int(data["amount"]),
        int(data["price_per_share"]),
        identity["wallet"]
    )

    return jsonify(result)


# =====================================================
# MARKETPLACE - BUY LISTED SHARES
# =====================================================

@assets.route("/buy-listing", methods=["POST"])
@jwt_required()
def buy_listing():

    identity = get_jwt_identity()

    if identity["role"] != "customer":
        return jsonify({"success": False, "message": "Customer only"}), 403

    data = request.json

    total_value = int(data["amount"]) * int(data["price_per_share"])

    result = build_buy_listing_tx(
        int(data["listing_id"]),
        identity["wallet"],
        total_value
    )

    return jsonify(result)


# =====================================================
# PUBLIC READ
# =====================================================

@assets.route("/total", methods=["GET"])
def total_assets():
    return jsonify(get_total_assets())


@assets.route("/<int:asset_id>", methods=["GET"])
def single_asset(asset_id):
    return jsonify(get_asset(asset_id))


@assets.route("/listing/<int:listing_id>", methods=["GET"])
def single_listing(listing_id):
    return jsonify(get_listing(listing_id))
