import requests
from typing import List

def search_for_stock_videos(query: str, api_key: str, it: int, min_dur: int) -> List[str]:
    headers = {
        "Authorization": api_key
    }
    qurl = f"https://api.pexels.com/videos/search?query={query}&per_page={it}"
    r = requests.get(qurl, headers=headers)
    response = r.json()
    raw_urls = []
    video_url = []
    video_res = 0
    try:
        for i in range(it):
            if response["videos"][i]["duration"] < min_dur:
                continue
            raw_urls = response["videos"][i]["video_files"]
            temp_video_url = ""
            for video in raw_urls:
                # Check if video has a valid download link
                if ".com/video-files" in video["link"]:
                    # Only save the URL with the largest resolution
                    if (video["width"]*video["height"]) > video_res:
                        temp_video_url = video["link"]
                        video_res = video["width"]*video["height"]
            if temp_video_url != "":
                video_url.append(temp_video_url)
    except Exception as e:
        print("[-] No Videos found.")
        print(e)
    print(f"Found {len(video_url)} Videos for {query}")
    return video_url




key = ""

urls = search_for_stock_videos(query = "cars", api_key = key,it=5,min_dur=5)
print(urls)