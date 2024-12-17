import praw

def fetch_subreddit_posts(subreddit_name, limit=10):
    reddit = praw.Reddit(
        client_id="SFSkzwY_19O3mOsbuwukqg",
        client_secret="ZDGonQJlJHIIz59ubKv-U8Dyho_V2w",
        password="hatelenovo",
        user_agent="testscript by u/Severe_Asparagus_103",
        username="Severe_Asparagus_103",
        check_for_async=False
    )
    subreddit = reddit.subreddit(subreddit_name)
    posts_list = []
    try:
        for post in subreddit.hot(limit=limit * 2):  # Fetch more to account for filtered posts
            if post.over_18:
                continue
            post.comments.replace_more(limit=0)  # Expand "More comments" placeholders
            comments = [comment.body for comment in post.comments.list()]
            post_details = {
                'title': post.title,
                'content': post.selftext,  # Text content for self posts
                'url': post.url,  # URL of the post or linked content
                'score': post.score,
                'num_comments': post.num_comments,
                'comments': comments  # List of all comments
            }
            posts_list.append(post_details)
            if len(posts_list) == limit:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    return posts_list


def main():
    subreddit_name = 'story'
    posts = fetch_subreddit_posts(subreddit_name, limit=10)
    for i, post in enumerate(posts, 1):
        print(f"Post {i}:")
        print(f"Title: {post['title']}")
        print(f"Content: {post['content']}")  # Print content
        print(f"URL: {post['url']}")
        print(f"Score: {post['score']}")
        print(f"Comments: {post['num_comments']}")
        print("Comments:")
        for comment in post['comments']:
            print(f"  - {comment}")
        print("-" * 50)


if __name__ == "__main__":
    main()
