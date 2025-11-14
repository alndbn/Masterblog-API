from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    missing_fields = []
    if not data.get("title"):
        missing_fields.append("title")
    if not data.get("content"):
        missing_fields.append("content")

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    new_id = max((post["id"] for post in POSTS), default=0) + 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"],
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global POSTS

    post_to_delete = next((post for post in POSTS if post["id"] == post_id), None)

    if post_to_delete is None:
        return jsonify(
            {"message": f"Post with id {post_id} was not found."}
        ), 404

    POSTS = [post for post in POSTS if post["id"] != post_id]

    return jsonify(
        {"message": f"Post with id {post_id} has been deleted successfully."}
    ), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json() or {}

    post_to_update = next((post for post in POSTS if post["id"] == post_id), None)

    if post_to_update is None:
        return jsonify(
            {"message": f"Post with id{post_id} was not found."}
        ), 404

    if "title" in data:
        post_to_update["title"] = data["title"]

    if "content" in data:
        post_to_update["content"] = data["content"]

    return jsonify(post_to_update), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get("title", "").lower()
    content_query = request.args.get("content", "").lower()

    filtered_posts = []

    for post in POSTS:
        title_match = title_query in post["title"].lower() if title_query else False
        content_match = content_query in post["content"].lower() if content_query else False

        if title_match or content_match:
            filtered_posts.append(post)

    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
