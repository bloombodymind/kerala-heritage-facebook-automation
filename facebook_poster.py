import json
import os
from datetime import datetime, timezone
import requests

def get_current_day():
    """Calculate current day number (1-35) based on days since epoch"""
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    days_since_epoch = (now - epoch).days
    return (days_since_epoch % 35) + 1

def load_posts():
    """Load posts from posts.json"""
    with open('posts.json', 'r') as f:
        return json.load(f)

def post_to_facebook(page_id, access_token, message):
    """Post message to Facebook page"""
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    data = {
        'message': message,
        'access_token': access_token
    }
    response = requests.post(url, data=data)
    return response.json()

def main():
    # Get environment variables
    page_id = os.environ.get('KERALA_PAGE_ID')
    access_token = os.environ.get('KERALA_PAGE_ACCESS_TOKEN')
    
    if not page_id or not access_token:
        print("Error: KERALA_PAGE_ID and KERALA_PAGE_ACCESS_TOKEN must be set")
        return
    
    # Get current day and load posts
    current_day = get_current_day()
    posts = load_posts()
    
    # Find post for current day
    post = next((p for p in posts if p['day'] == current_day), None)
    
    if not post:
        print(f"Error: No post found for day {current_day}")
        return
    
    # Post to Facebook
    print(f"Posting day {current_day} to Facebook...")
    result = post_to_facebook(page_id, access_token, post['message'])
    
    if 'id' in result:
        print(f"Successfully posted! Post ID: {result['id']}")
    else:
        print(f"Error posting to Facebook: {result}")

if __name__ == '__main__':
    main()
