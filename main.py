from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/user/<user_id>")
def user_id(user_id):
    user_data = {
        "user_id": 0,
        "request": "datetime",
        "token": "124",
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

if __name__ == "__main__":
    app.run(debug=True)