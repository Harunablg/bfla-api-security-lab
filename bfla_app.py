from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated users database
users = {
    "user_token": {"id": 1, "role": "user", "name": "Haruna"},
    "admin_token": {"id": 2, "role": "admin", "name": "Jacob"}
}

# Simulated user list (only admin should see this)
all_users = [
    {"id": 1, "name": "Haruna", "email": "haruna@example.com"},
    {"id": 2, "name": "Jacob", "email": "jacob@example.com"},
    {"id": 3, "name": "John", "email": "john@example.com"}
]

def get_current_user(token):
    return users.get(token)

#  VULNERABLE admin endpoint — no role check
@app.route("/api/admin/users", methods=["GET"])
def get_all_users():
    token = request.headers.get("Authorization")
    user = get_current_user(token)
    
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    # BUG: Only checks if user exists, NOT if they are admin
    return jsonify({"users": all_users}), 200


#  VULNERABLE admin endpoint — no role check
@app.route("/api/admin/delete-user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    token = request.headers.get("Authorization")
    user = get_current_user(token)
    
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    # BUG: Any authenticated user can delete — no admin check
    return jsonify({
        "message": f"User {user_id} deleted successfully",
        "deleted_by": user["name"]
    }), 200


#  SECURE version — with role check
@app.route("/api/secure/admin/users", methods=["GET"])
def get_all_users_secure():
    token = request.headers.get("Authorization")
    user = get_current_user(token)
    
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    
    # FIXED: Check role before allowing access
    if user["role"] != "admin":
        return jsonify({"error": "Forbidden - Admin access required"}), 403
    
    return jsonify({"users": all_users}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)