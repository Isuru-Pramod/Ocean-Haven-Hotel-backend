from flask import Blueprint, jsonify
from services.blockchain import get_asset_count, get_asset, get_top_10

analytics = Blueprint("analytics", __name__)

@analytics.route("/assets", methods=["GET"])
def assets():
    count = get_asset_count()
    return jsonify({"total_assets": count})


@analytics.route("/asset/<int:asset_id>", methods=["GET"])
def asset(asset_id):
    data = get_asset(asset_id)
    return jsonify({
        "id": data[0],
        "name": data[1],
        "location": data[2],
        "totalShares": data[3],
        "sharePrice": data[4],
        "sharesSold": data[5],
        "creator": data[6],
        "isActive": data[7]
    })


@analytics.route("/asset/<int:asset_id>/top10", methods=["GET"])
def top10(asset_id):
    data = get_top_10(asset_id)
    return jsonify(data)
