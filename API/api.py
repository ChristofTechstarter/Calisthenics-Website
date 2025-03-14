from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


def load_json(key):
    with open("users_list.json", "r") as file_user:
        content = file_user.read()
        return json.loads(content)[key]


def save_json_partial(key, index, updated_data, filename="users_list.json"):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        file_data[key][index] = updated_data
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.truncate()  # Entfernt eventuelle alte Datenreste


def add_json(key, new_data, filename="users_list.json"):
    with open(filename, "r+") as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside a given key
        file_data[key].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


def delete_json(key, removevalue, filename="users_list.json"):
    with open(filename, "r+") as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside a given key
        file_data[key].remove(removevalue)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)
        file.truncate()


# Users


@app.route("/users")
def get_users():
    return jsonify(load_json("users"))


@app.route("/users/signup", methods=["POST"])
def signup():
    users = load_json("users")
    id = max([p["id"] for p in users], default=0) + 1
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    password = data["password"]
    first_name = data["firstName"]
    family_name = data["familyName"]
    for user in users:
        if user["username"] == username:
            return jsonify({"message": f"The Username {username} is already used!"})
        elif user["email"] == email:
            return jsonify({"message": f"The Email {email} is already used!"})
    new_user = {
        "id": id,
        "email": email,
        "username": username,
        "password": password,
        "firstName": first_name,
        "familyName": family_name,
    }
    add_json("users", new_user)
    return jsonify(
        {"message": f"Successfully signed up a New User!", "Data saved": f"{new_user}"}
    )


@app.route("/users/update", methods=["PUT"])
def update_username():
    users = load_json("users")
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    new_username = data["newUsername"]
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                user["username"] = new_username
                save_json_partial("users", users.index(user), user)
                return jsonify(
                    {"message": f"Successfully changed {username} to {new_username}!"}
                )
            else:
                return jsonify(
                    {"message": f"Your Password for User {username} is incorrect!"}
                )
    return jsonify({"message": f"No Username: {username} was found!"})


@app.route("/login", methods=["POST"])
def login():
    users = load_json("users")
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    user = next((user for user in users if user["username"] == username), None)

    if user is None:
        return jsonify({"message": f"No user {username} found!"}), 404

    if user["password"] == password:
        return jsonify({"message": f"Successfully logged in {username}!"}), 200
    else:
        return jsonify({"message": "Incorrect password!"}), 401


@app.route("/users/delete", methods=["DELETE"])
def delete_user():
    users = load_json("users")
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                delete_json("users", user)

                return jsonify({"message": f"Successfully deleted User!"})
            else:
                return jsonify(
                    {"message": f"Your Password for User {username} is incorrect!"}
                )
    return jsonify({f"message": f"No User {username} found!"})


if __name__ == "__main__":
    app.run(debug=True, port=6060)
