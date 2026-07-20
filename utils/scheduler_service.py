import extensions
from utils.linkedin_service import post_to_linkedin
from models.linkedin import LinkedInProfile
from models.scheduled_post import ScheduledPost
from database import db


def publish_scheduled_post(post_id):

    print("========================================")
    print("Running Scheduled Job")
    print("Post ID:", post_id)
    print("========================================")

    try:

        with extensions.flask_app.app_context():

            post = db.session.get(ScheduledPost, post_id)

            if post is None:

                print("Scheduled post not found.")

                return

            linkedin = LinkedInProfile.query.filter_by(user_id=post.user_id).first()

            if linkedin is None:

                print("LinkedIn account not connected.")

                return

            print("Posting to LinkedIn...")

            response = post_to_linkedin(
                linkedin.access_token, linkedin.linkedin_id, post.content, post.image
            )

            print("LinkedIn Response Status:", response.status_code)

            if response.status_code == 201:

                print("Post published successfully.")

                db.session.delete(post)

                db.session.commit()

            else:

                print("LinkedIn API Error:")
                print(response.text)

    except Exception as e:

        print("Scheduler Exception:")
        print(str(e))