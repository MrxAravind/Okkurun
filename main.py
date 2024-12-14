import praw
import os

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
                'content': post.selftext,  # Text content for self posts
                'url': post.url,  # URL of the post or linked content
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

def main():
    # Example usage
    subreddit_name = 'story'  # Change this to the subreddit you want to fetch
    posts = fetch_subreddit_posts(subreddit_name, limit=10)
    
    # Print out the fetched posts
    for i, post in enumerate(posts, 1):
        print(f"Post {i}:")
        print(f"Title: {post['title']}")
        print(f"Content: {post['content']}...")  # Print content
        print(f"URL: {post['url']}")
        print(f"Score: {post['score']}")
        print(f"Comments: {post['num_comments']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
