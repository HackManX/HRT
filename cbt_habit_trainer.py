import google.generativeai as genai
from googleapiclient.discovery import build

# Replace with your keys
YOUTUBE_API_KEY = "AIzaSyAJw10ift5YPoNx7PBZARXDhnNyPR7SuG0"
GEMINI_API_KEY = "AIzaSyBzxUg_6Peov5H1eYqupQQ7K3TZvKESOds"

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# YouTube API Setup
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_youtube_video(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query + " psychoeducation",
        type="video"
    )
    response = request.execute()
    if response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        video_title = response["items"][0]["snippet"]["title"]
        return f"https://www.youtube.com/watch?v={video_id}", video_title
    return None, None

def gemini_suggestions(habit):
    prompt = f"""
You are a CBT therapist. Help a person who wants to overcome the habit: {habit}.
Give:
1. A short awareness training tip
2. A good replacement behavior suggestion
3. A motivational message to encourage them
Format it clearly.
"""
    response = model.generate_content(prompt)
    return response.text

# === Main flow ===
def main():
    print("🧠 CBT Habit Reversal with AI & YouTube\n")
    habit = input("Enter your bad habit: ")

    # Get video
    url, title = search_youtube_video(habit)
    if url:
        print(f"\n📺 Watch this video to understand your habit:\n{title}\n{url}")
    else:
        print("❌ No relevant YouTube video found.")

    # Gemini suggestions
    print("\n💡 CBT-Based Recommendations:\n")
    tips = gemini_suggestions(habit)
    print(tips)

if __name__ == "__main__":
    main()
