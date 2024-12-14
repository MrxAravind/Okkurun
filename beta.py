import praw
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Reddit API credentials
def fetch_subreddit_posts(subreddit_name, limit=10):
    """
    Fetch posts from a specified subreddit, excluding NSFW content.
    """
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
        for post in subreddit.hot(limit=limit * 2):  # Fetch extra to account for NSFW filtering
            if post.over_18:  # Skip NSFW posts
                continue
            post_details = {
                'title': post.title,
                'content': post.selftext[:200],  # Truncate long content
                'score': post.score,
                'num_comments': post.num_comments,
                'author': post.author.name,
                'url': post.url
            }
            posts_list.append(post_details)
            if len(posts_list) == limit:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    return posts_list

def generate_reddit_post_image(post_data, output_path="reddit_post.png"):
    """
    Generate an image that resembles a Reddit post using post data.
    """
    # Image setup
    img_width, img_height = 1080, 600
    background_color = (18, 18, 18)
    text_color = (255, 255, 255)
    highlight_color = (30, 215, 96)
    font_path = "arial.ttf"  # Replace with your font path

    # Create image
    image = Image.new("RGB", (img_width, img_height), color=background_color)
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        title_font = ImageFont.truetype(font_path, 40)
        body_font = ImageFont.truetype(font_path, 25)
        small_font = ImageFont.truetype(font_path, 20)
    except:
        raise Exception("Font not found! Replace 'arial.ttf' with a valid font path.")

    margin = 40
    y_position = margin

    # Username
    draw.text((margin, y_position), f"u/{post_data['author']} • {post_data['score']} upvotes", font=small_font, fill=text_color)
    y_position += 40

    # Title
    title_lines = textwrap.wrap(post_data['title'], width=40)
    for line in title_lines:
        draw.text((margin, y_position), line, font=title_font, fill=text_color)
        y_position += 50

    # Content
    if post_data['content']:
        body_lines = textwrap.wrap(post_data['content'], width=50)
        for line in body_lines[:5]:  # Limit content to 5 lines
            draw.text((margin, y_position), line, font=body_font, fill=text_color)
            y_position += 35

    # Badge (Optional Sci-Fi style)
    badge_text = "Story"
    bbox = draw.textbbox((0, 0), badge_text, font=small_font)
    badge_width = bbox[2] - bbox[0]
    badge_height = bbox[3] - bbox[1]
    badge_padding = 10
    badge_rect = [margin, y_position, margin + badge_width + badge_padding * 2, y_position + badge_height + badge_padding]
    draw.rectangle(badge_rect, fill=highlight_color)
    draw.text((margin + badge_padding, y_position + badge_padding / 2), badge_text, font=small_font, fill=(0, 0, 0))
    y_position += 70
    
    # Footer
    footer_text = f"💬 {post_data['num_comments']} Comments"
    draw.text((margin, img_height - margin), footer_text, font=small_font, fill=text_color)

    # Save the image
    image.save(output_path)
    print(f"Image saved: {output_path}")

def main():
    subreddit_name = 'story'  # Change this to the subreddit you want
    posts = fetch_subreddit_posts(subreddit_name, limit=3)
    output_folder = "reddit_images"
    os.makedirs(output_folder, exist_ok=True)

    # Generate images for each post
    for i, post in enumerate(posts, start=1):
        output_path = os.path.join(output_folder, f"reddit_post_{i}.png")
        generate_reddit_post_image(post, output_path)

if __name__ == "__main__":
    main()
