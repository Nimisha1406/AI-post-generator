import requests

def upload_image_to_linkedin(access_token, linkedin_id, image_path):

    # Step 1: Register image upload

    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": f"urn:li:person:{linkedin_id}",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent",
                }
            ],
        }
    }

    response = requests.post(register_url, headers=headers, json=payload)

    data = response.json()

    upload_url = data["value"]["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]

    asset = data["value"]["asset"]

    # Step 2: Upload actual image

    with open(image_path, "rb") as image:

        upload_response = requests.put(
            upload_url, headers={"Authorization": f"Bearer {access_token}"}, data=image
        )

    return asset


def post_to_linkedin(access_token, linkedin_id, content, image_path=None):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    media = []

    if image_path:

        asset = upload_image_to_linkedin(access_token, linkedin_id, image_path)

        media.append(
            {"status": "READY", "media": asset, "title": {"text": "AI Generated Image"}}
        )

    payload = {
        "author": f"urn:li:person:{linkedin_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "IMAGE" if image_path else "NONE",
                "media": media,
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts", headers=headers, json=payload
    )
    
    print("Post Response:")
    print(response.json())

    return response
