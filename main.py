import praw
import os
from playwright.sync_api import sync_playwright

def fetch_subreddit_posts(subreddit_name, limit=10):
    """
    Fetch posts from a specified subreddit, excluding NSFW content.
    
    Args:
    subreddit_name (str): Name of the subreddit to fetch posts from
    limit (int, optional): Maximum number of posts to retrieve. Defaults to 10.
    
    Returns:
    list: A list of dictionaries containing post details
    """
    # Reddit API credentials
    reddit = praw.Reddit(
    client_id="SFSkzwY_19O3mOsbuwukqg",
    client_secret="ZDGonQJlJHIIz59ubKv-U8Dyho_V2w",
    password="hatelenovo",
    user_agent="testscript by u/Severe_Asparagus_103",
    username="Severe_Asparagus_103",
    check_for_async=False
    )
    
    # Select the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    # List to store post details
    posts_list = []
    
    # Fetch posts (can use .hot(), .new(), .top(), etc.)
    try:
        for post in subreddit.hot(limit=limit*2):  # Fetch more to account for filtered posts
            # Skip NSFW posts
            if post.over_18:
                continue
            
            post_details = {
                'title': post.title,
                'url': post.permalink,  # Full Reddit post URL
                'content': post.selftext,
                'score': post.score,
                'num_comments': post.num_comments
            }
            posts_list.append(post_details)
            
            # Break if we've reached the desired number of non-NSFW posts
            if len(posts_list) == limit:
                break
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return posts_list

def capture_reddit_post_titles(subreddit_name, limit=10, output_dir='reddit_screenshots'):
    """
    Capture screenshots of Reddit post titles from a specified subreddit.
    
    Args:
    subreddit_name (str): Name of the subreddit to fetch posts from
    limit (int, optional): Maximum number of posts to capture. Defaults to 10.
    output_dir (str, optional): Directory to save screenshots. Defaults to 'reddit_screenshots'.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Fetch posts
    posts = fetch_subreddit_posts(subreddit_name, limit)
    
    # Use Playwright to capture screenshots
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(
            headless=True,  # Ensure headless mode
            args=['--no-sandbox', '--disable-setuid-sandbox']  # Add these for better compatibility
        )
        
        # Create a new browser context with specific viewport
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            device_scale_factor=2  # For higher resolution screenshots
        )
        
        # Disable images and stylesheets to speed up loading
        context.route('**/*', lambda route: route.abort() 
            if route.request.resource_type in ['image', 'stylesheet', 'font'] 
            else route.continue_())
        
        page = context.new_page()
        
        # Capture screenshots for each post
        for i, post in enumerate(posts, 1):
            try:
                # Navigate to the full Reddit post URL
                page.goto(f'https://www.reddit.com{post["url"]}', 
                          wait_until='networkidle', 
                          timeout=30000)  # Increased timeout
                
                # Wait for the title element to be visible
                page.wait_for_selector('h1[slot="title"]', timeout=10000)
                
                # Find the title element
                title_element = page.query_selector('h1[slot="title"]')
                
                if title_element:
                    # Generate filename (sanitize title to use as filename)
                    safe_filename = "".join(x for x in post['title'] if x.isalnum() or x in [' ', '-', '_']).rstrip()
                    safe_filename = safe_filename[:50]  # Limit filename length
                    screenshot_path = os.path.join(output_dir, f'{i}_post_{safe_filename}.png')
                    
                    # Take screenshot of the title element
                    title_element.screenshot(
                        path=screenshot_path,
                        type='png',
                        scale='device'  # Ensures high-quality screenshot
                    )
                    print(f"Screenshot saved: {screenshot_path}")
                else:
                    print(f"Could not find title element for post {i}")
            
            except Exception as e:
                print(f"Error capturing screenshot for post {i}: {e}")
        
        # Close browser
        browser.close()

def main():
    # Example usage
    subreddit_name = 'story'
    
    # Capture screenshots of post titles
    capture_reddit_post_titles(subreddit_name, limit=5)

if __name__ == "__main__":
    main()
