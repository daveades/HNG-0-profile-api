import os
import requests
import logging
from datetime import datetime, timezone
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.json.sort_keys = False
app.json.compact = False

USER_EMAIL = os.getenv("USER_EMAIL")
USER_NAME = os.getenv("USER_NAME")
USER_STACK = os.getenv("USER_STACK")

CAT_FACTS_API = "https://catfact.ninja/fact"

def get_cat_fact() -> str:
    """
    Fetches a random cat fact from the external API.
    """
    try:
        logger.info("Fetching cat fact from external API...")
        response = requests.get(CAT_FACTS_API, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("fact", "No fact available.")
    except requests.Timeout:
        logger.warning("Request timed out")
        return "Error: Request timed out. Unable to fetch cat fact."
    except requests.RequestException as e:
        logger.warning(f"Request failed: {e}")
        return "Error: Unable to fetch cat fact."
    
    
@app.route("/me", methods=["GET"])
def get_profile():
    """
    GET /me endpoint - Returns profile info and a random cat fact.
    """
    fact = get_cat_fact()
    timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    if "Error" in fact:
        return jsonify({"status": "error", "message": fact}), 503

    data = {
        "status": "success",
        "user": {
            "email": USER_EMAIL,
            "name": USER_NAME,
            "stack": USER_STACK
        },
        "timestamp": timestamp,
        "fact": fact
    }
    return jsonify(data), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)