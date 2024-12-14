import praw
import requests
import os

def capture_reddit_screenshots(subreddit_name, limit=5):
    # Reddit API credentials
    reddit = praw.Reddit(
        client_id="SFSkzwY_19O3mOsbuwukqg",
        client_secret="ZDGonQJlJHIIz59ubKv-U8Dyho_V2w",
        password="hatelenovo",
        user_agent="testscript by u/Severe_Asparagus_103",
        username="Severe_Asparagus_103",
        check_for_async=False
    )

    # Create screenshots directory
    os.makedirs('reddit_screenshots', exist_ok=True)

    # Fetch posts from subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    for i, post in enumerate(subreddit.hot(limit=limit), 1):
        try:
            # Construct full Reddit URL
            full_url = f'https://www.reddit.com{post.permalink}'
            
            # Use screenshot API service
            screenshot_api_url = f'https://api.urlbox.io/v1/render?url={full_url}&full_page=true&format=png'
            
            # Headers to mimic browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Fetch screenshot
            response = requests.get(screenshot_api_url, headers=headers)
            
            if response.status_code == 200:
                # Sanitize filename
                safe_filename = "".join(x for x in post.title if x.isalnum() or x in [' ', '-', '_']).rstrip()[:50]
                
                # Save screenshot
                screenshot_path = f'reddit_screenshots/{i}_post_{safe_filename}.png'
                with open(screenshot_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"Screenshot saved: {screenshot_path}")
            else:
                print(f"Failed to capture screenshot for post {i}")
        
        except Exception as e:
            print(f"Error processing post {i}: {e}")

# Example usage
capture_reddit_screenshots('story', limit=5)
