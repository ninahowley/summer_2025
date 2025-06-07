import requests
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
import textwrap

model = genai.GenerativeModel('gemini-pro')

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=google_api_key)

SYSTEM_PROMPT = """
            You are a categorization specialist tasked with placing websites into 1 of 3 subcategories within 1 of 6 categories.
            Using the URL snippet you are given and your knowledge of internet domains, assign it a number 1 to 6.
            """

class Category():
    def __init__(self, name: str, description: str, examples: str):
        self.name = name
        self.description = description
        self.examples = examples

class SubCategory():
    def __init__(self, category: Category, name: str, description: str, examples: str):
        self.category = category
        self.name = name
        self.description = description
        self.examples = examples

CATEGORIES = [
    Category(
        name="Information & News",
        description="Delivering current events, factual data, encyclopedic knowledge, public records, and general information",
        examples="News outlets (CNN, BBC), Wikipedia, government sites, weather forecasts, informational blogs."
    ),
    Category(
        name="Shopping & Services",
        description="E-commerce (buying/selling goods), online marketplaces, booking services (travel, appointments), delivery platforms, and consumer-facing financial services.",
        examples="Amazon, Etsy, Booking.com, DoorDash, online banking portals."
    ),
    Category(
        name="Social & Communication",
        description="Platforms designed for user interaction, community building, content sharing among users, and direct messaging.",
        examples="Facebook, Twitter/X, Reddit, LinkedIn, Discord, dating sites, online forums."
    ),
    Category(
        name="Entertainment & Leisure",
        description="Providing media consumption (movies, music, games), recreational activities, hobbies, arts, humor, sports, and general leisure content.",
        examples="Netflix, YouTube, Spotify, gaming sites, sports news, personal hobby blogs, travel inspiration."
    ),
    Category(
        name="Education & Reference",
        description="Online learning platforms, academic resources, research databases, tutorials, skill development, and comprehensive knowledge repositories.",
        examples="Coursera, Khan Academy, university websites, online dictionaries, specialized academic journals."
    ),
    Category(
        name="Business & Professional",
        description="Corporate websites, B2B services, professional tools, finance (investment, enterprise), technology development, job search platforms, and industry-specific resources.",
        examples="Company homepages (IBM, Microsoft), Bloomberg, Indeed, developer documentation sites, cloud service providers."
    )
]

SUBCATEGORIES = [
    SubCategory(
        category=CATEGORIES[0],
        name="Current Events & Journalism",
        description="Websites primarily focused on reporting daily news, breaking stories, investigative journalism, and commentary on current affairs.",
        examples="CNN.com, BBC.com, TheNewYorkTimes.com"
    ),
    SubCategory(
        category=CATEGORIES[0],
        name="Encyclopedic & Reference",
        description="Sites providing comprehensive factual information, definitions, historical data, and knowledge bases for general research.",
        examples="Wikipedia.org, Britannica.com, Merriam-Webster.com"
    ),
    SubCategory(
        category=CATEGORIES[0],
        name="Public & Government Services",
        description="Official websites of government bodies, public services, non-profits offering public information, and civic resources.",
        examples="USA.gov, local city council sites, CDC.gov"
    ),


    SubCategory(
        category=CATEGORIES[1],
        name="E-commerce & Retail",
        description="Online stores for purchasing physical goods, clothing, electronics, groceries, and general merchandise.",
        examples="Amazon.com, Target.com, Zappos.com"
    ),
    SubCategory(
        category=CATEGORIES[1],
        name="Booking & Travel Services",
        description="Platforms for reserving flights, hotels, rental cars, event tickets, tours, and making appointments (e.g., doctor, salon).",
        examples="Booking.com, Expedia.com, OpenTable.com"
    ),
    SubCategory(
        category=CATEGORIES[1],
        name="Consumer-Oriented Financial & Utilities",
        description="Personal banking, payment processing, insurance, utility bill payments, and consumer loan services.",
        examples="Chase.com, PayPal.com, Geico.com"
    ),


    SubCategory(
        category=CATEGORIES[2],
        name="Social Networking Platforms",
        description="Sites centered on creating profiles, connecting with friends/followers, and sharing personal updates, photos, and short-form content.",
        examples="Facebook.com, Instagram.com, X.com (formerly Twitter)"
    ),
    SubCategory(
        category=CATEGORIES[2],
        name="Forums & Community Discussions",
        description="Websites built around topic-specific discussions, Q&A, message boards, and interest-based groups.",
        examples="Reddit.com, StackOverflow.com, specific hobby forums"
    ),
    SubCategory(
        category=CATEGORIES[2],
        name="Messaging & Collaboration Tools",
        description="Platforms for real-time text, voice, or video chat, and tools designed for group communication and personal file sharing.",
        examples="Discord.com, WhatsApp Web, Zoom.com"
    ),


    SubCategory(
        category=CATEGORIES[3],
        name="Streaming & Digital Media",
        description="Platforms for consuming video (movies, TV), music, podcasts, and other digital content.",
        examples="Netflix.com, Spotify.com, YouTube.com"
    ),
    SubCategory(
        category=CATEGORIES[3],
        name="Gaming & Interactive Fun",
        description="Websites hosting online games, providing gaming news, reviews, and interactive entertainment experiences.",
        examples="Steam.com, IGN.com, Twitch.tv, online casual game sites"
    ),
    SubCategory(
        category=CATEGORIES[3],
        name="Hobbies & Lifestyle Content",
        description="Blogs, magazines, and resources focused on personal interests like cooking, travel, fashion, health & wellness, arts, and humor.",
        examples="Allrecipes.com, Pinterest.com, Travel+Leisure.com"
    ),


    SubCategory(
        category=CATEGORIES[4],
        name="Online Learning Platforms",
        description="Websites offering structured courses, certifications, and academic programs (MOOCs).",
        examples="Coursera.org, edX.org, Udemy.com"
    ),
    SubCategory(
        category=CATEGORIES[4],
        name="Academic & Research Institutions",
        description="Official websites of universities, colleges, research organizations, and digital libraries for scholarly work.",
        examples="MIT.edu, JSTOR.org, PubMed.gov"
    ),
    SubCategory(
        category=CATEGORIES[4],
        name="Skill-Building & Tutorials",
        description="Sites providing practical how-to guides, coding lessons, language learning tools, and step-by-step instructions for various skills.",
        examples="KhanAcademy.org, freeCodeCamp.org, Duolingo.com"
    ),


    SubCategory(
        category=CATEGORIES[5],
        name="Corporate & Brand Presence",
        description="Official websites for companies, organizations, and brands, typically for information, investor relations, and public relations.",
        examples="IBM.com, Coca-ColaCompany.com, Tesla.com"
    ),
    SubCategory(
        category=CATEGORIES[5],
        name="Professional Services & B2B Solutions",
        description="Websites offering services or software specifically for other businesses, industry-specific platforms, consulting, and SaaS tools.",
        examples="Salesforce.com, HubSpot.com, various analytics platforms"
    ),
    SubCategory(
        category=CATEGORIES[5],
        name="Finance, Investment & Career",
        description="Platforms for stock trading, business banking, economic news, job searching, professional networking, and real estate services.",
        examples="Bloomberg.com, LinkedIn.com, Indeed.com, Zillow.com"
    ),
]




def build_categorization_prompt(url_to_categorize: str) -> str:
    prompt_parts = []

    # System Prompt/Instructions
    SYSTEM_PROMPT = """You are a categorization specialist tasked with placing websites into 1 of 3 subcategories within 1 of 6 main categories.
Use the URL snippet you are given, your knowledge of internet domains, and the provided category definitions.
Output your answer in JSON format, strictly adhering to the schema below. Do not include any other text or explanation outside the JSON.
"""
    prompt_parts.append(SYSTEM_PROMPT)

    # Output Schema Definition
    prompt_parts.append(textwrap.dedent("""
    Output JSON Schema:
    ```json
    {
      "main_category_number": <int, 1-6>,
      "main_category_name": "<string>",
      "sub_category_number": <int, 1-3>,
      "sub_category_name": "<string>"
    }
    ```
    """))

    # Add Main Categories
    prompt_parts.append("\n## Main Categories:\n")
    for i, cat in enumerate(CATEGORIES):
        prompt_parts.append(f"{i + 1}. **{cat.name}**\n   - Description: {cat.description}\n   - Examples: {cat.examples}\n")

    # Add Subcategories
    prompt_parts.append("\n## Subcategories:\n")
    for i, cat in enumerate(CATEGORIES):
        prompt_parts.append(f"### {i + 1}. {cat.name} Subcategories:\n")
        sub_counter = 0
        for j, subcat in enumerate(SUBCATEGORIES):
            if subcat.category == cat:
                sub_counter += 1
                prompt_parts.append(f"    {sub_counter}. **{subcat.name}**\n       - Description: {subcat.description}\n       - Examples: {subcat.examples}\n")
        prompt_parts.append("\n") # Add a newline for separation

    # Add the request for categorization
    prompt_parts.append(f"## Categorize the following URL:\nURL: {url_to_categorize}\nOutput:")

    return "\n".join(prompt_parts)

# --- 5. Example Usage ---
if __name__ == "__main__":
    urls_to_test = [
        "https://www.nytimes.com/",
        "https://www.amazon.com/",
        "https://discord.com/",
        "https://www.twitch.tv/",
        "https://www.coursera.org/",
        "https://github.com/",
        "https://www.google.com/",
        "https://www.espn.com/",
        "https://www.nasa.gov/",
        "https://www.zillow.com/" # Let's test a new one
    ]

    for url in urls_to_test:
        print(f"\n--- Categorizing: {url} ---")
        prompt = build_categorization_prompt(url)
        # print(prompt) # Uncomment to see the full prompt being sent

        try:
            response = model.generate_content(prompt)
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error categorizing {url}: {e}")