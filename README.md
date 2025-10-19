# Profile API (Flask)

A minimal Flask API that returns user profile information and a random cat fact from an external service.

## Features
- GET /me returns:
  - status, user (email, name, stack), timestamp (UTC ISO 8601), fact
- External call to https://catfact.ninja/fact with timeout and error handling
- Logging to console (INFO level)
- Pretty-printed JSON responses with stable key order

## Prerequisites
- Linux
- Python 3.8+ (recommended)
- curl (for testing)

## Dependencies
- Flask
- requests

Install with pip:
```
python -m pip install --upgrade pip
pip install Flask requests
```

## Environment Variables
All are optional. Defaults to null if not set.
- USER_EMAIL: Email to display
- USER_NAME: Name to display
- USER_STACK: Tech stack to display
- PORT: Port for the server (default: 5000)

Example (bash):
```
export USER_EMAIL="you@example.com"
export USER_NAME="Your Name"
export USER_STACK="Python/Flask"
export PORT=5000
```

## Run Locally
1) Create and activate a virtual environment (recommended):
```
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:
```
pip install Flask requests
```

3) Set any desired environment variables (see above).

4) Start the server:
```
python app.py
```

The API listens on:
- http://127.0.0.1:${PORT:-5000}
- http://localhost:${PORT:-5000}

## Test the Endpoint
- Success (200) when the Cat Facts API is reachable:
```
curl http://localhost:5000/me
```

- If the external API fails or times out, the endpoint returns:
  - 503 Service Unavailable with body:
    ```
    {
      "status": "error",
      "message": "Error: Unable to fetch cat fact."
    }
    ```
    or
    ```
    {
      "status": "error",
      "message": "Error: Request timed out. Unable to fetch cat fact."
    }
    ```

## Notes
- External dependency: https://catfact.ninja/fact