from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from openai import OpenAI
from database import db
from models.post import GeneratedPost
from config import Config
from models.linkedin import LinkedInProfile
from utils.linkedin_service import post_to_linkedin
from werkzeug.utils import secure_filename
import os
import uuid
import requests
import base64
from models.scheduled_post import ScheduledPost
from extensions import scheduler
from utils.scheduler_service import publish_scheduled_post
from datetime import datetime

posts = Blueprint("posts", __name__)

client = OpenAI(api_key=Config.OPENAI_API_KEY)


@posts.route("/generate", methods=["POST"])
@jwt_required()
def generate_post():

    data = request.get_json()

    topic = data.get("topic")

    if not topic:

        return jsonify({"error": "Topic is required"}), 400

    user_id = get_jwt_identity()

    prompt = f"""
Write a high-quality LinkedIn post on the topic:

{topic}

Requirements:

- Start with a strong hook in the first line that grabs attention.
- Keep the tone professional, conversational, and educational.
- Explain the topic using practical, real-world examples.
- Include 5-7 actionable points with short explanations.
- Use relevant emojis naturally.
- Keep paragraphs short and easy to read.
- Avoid AI-sounding phrases and buzzwords.
- Focus on value instead of promotion.
- End with a thought-provoking question to encourage comments.
- Add 8-12 relevant hashtags.
- Write as if you are an experienced Software Engineer sharing lessons learned from production projects.

Return only the LinkedIn post.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )

    generated_text = response.choices[0].message.content

    post = GeneratedPost(
        user_id=int(user_id),
        topic=topic,
        content=generated_text,
        image_path=None,
        image_type=None,
    )

    db.session.add(post)

    db.session.commit()

    return jsonify(
        {
            "message": "Post generated successfully",
            "post": generated_text,
            "id": post.id,
        }
    )


@posts.route("/upload-image", methods=["POST"])
@jwt_required()
def upload_image():

    if "image" not in request.files:

        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]

    if image.filename == "":

        return jsonify({"error": "No file selected"}), 400

    upload_folder = "static/uploaded_images"

    os.makedirs(upload_folder, exist_ok=True)

    filename = str(uuid.uuid4()) + "_" + secure_filename(image.filename)

    path = os.path.join(upload_folder, filename)

    image.save(path)

    return jsonify(
        {
            "message": "Image uploaded successfully",
            "image_path": path.replace("\\", "/"),
        }
    )


@posts.route("/generate-image", methods=["POST"])
@jwt_required()
def generate_image():

    data = request.get_json()

    content = data.get("content")

    if not content:

        return jsonify({"error": "Post content required"}), 400

    image_prompt = f"""

Create a modern LinkedIn infographic (1080x1080) based on this LinkedIn post:

{content}


Design Requirements:

- Use a clean, premium dark theme with green, blue, and white accents inspired by modern developer tools.
- Large bold title at the top summarizing the topic.
- Visually highlight the 5-7 key takeaways with icons and concise text.
- Include developer-themed illustrations such as code editor, laptop, terminal, API, browser, database, or architecture diagrams where appropriate.
- Use a clean grid layout with excellent spacing and typography.
- Add subtle gradients and modern UI elements.
- Keep text concise and highly readable on mobile.
- Do not clutter the design.
- Add a short takeaway banner at the bottom with an inspiring message.
- Do not include any logos, watermarks, or brand names.
- Make the design look like a premium technical infographic suitable for LinkedIn and capable of attracting high engagement.

"""

    response = client.images.generate(
        model="gpt-image-1", prompt=image_prompt, size="1024x1024"
    )

    # Get base64 image data from OpenAI response

    image_data = response.data[0].b64_json

    folder = "static/generated_images"

    os.makedirs(folder, exist_ok=True)

    filename = str(uuid.uuid4()) + ".png"

    path = os.path.join(folder, filename)

    # Save image locally

    with open(path, "wb") as f:

        f.write(base64.b64decode(image_data))

    return jsonify(
        {
            "message": "Image generated successfully",
            "image_path": path.replace("\\", "/"),
        }
    )


@posts.route("/save-image/<int:post_id>", methods=["POST"])
@jwt_required()
def save_image(post_id):

    data = request.get_json()

    image_path = data.get("image_path")
    image_type = data.get("image_type")

    post = GeneratedPost.query.filter_by(id=post_id, user_id=get_jwt_identity()).first()

    if not post:

        return jsonify({"error": "Post not found"}), 404

    post.image_path = image_path
    post.image_type = image_type

    db.session.commit()

    return jsonify({"message": "Image saved successfully"})


@posts.route("/publish/<int:post_id>", methods=["POST"])
@jwt_required()
def publish_post(post_id):

    user_id = get_jwt_identity()

    post = GeneratedPost.query.filter_by(id=post_id, user_id=user_id).first()

    if not post:
        return jsonify({"error": "Post not found"}), 404

    linkedin = LinkedInProfile.query.filter_by(user_id=user_id).first()

    if not linkedin:
        return jsonify({"error": "LinkedIn not connected"}), 400

    response = post_to_linkedin(
        linkedin.access_token, linkedin.linkedin_id, post.content, post.image_path
    )

    if response.status_code != 201:

        return (
            jsonify({"error": "LinkedIn posting failed", "details": response.json()}),
            response.status_code,
        )

    return jsonify({"message": "Posted successfully on LinkedIn"})




@posts.route("/schedule", methods=["POST"])
@jwt_required()
def schedule_post():

    data = request.get_json()

    user_id = get_jwt_identity()

    scheduled_time = datetime.fromisoformat(data["time"])

    scheduled_post = ScheduledPost(
        user_id=int(user_id),
        content=data["content"],
        image=data.get("image"),
        scheduled_datetime=scheduled_time,
    )

    db.session.add(scheduled_post)

    db.session.commit()

    scheduler.add_job(
        id=str(uuid.uuid4()),
        func=publish_scheduled_post,
        trigger="date",
        run_date=scheduled_time,
        args=[scheduled_post.id],
    )

    return jsonify({"message": "Post scheduled successfully"})
