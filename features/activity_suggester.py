import random

activity_rules = {
    "Clear": [
        "Go take a hike", "Have a picnic", "Do outdoor yoga", "Ride your bike",
        "Take photos of the sky", "Visit a park", "Do a backyard workout",
        "Eat lunch outside", "Go rollerblading", "Walk your dog",
        "Play outdoor sports", "Start a botanical garden🌿", "Go hiking",
        "Fly a kite", "Climb onto a roof", "Have a BBQ",
        "Do gardening", "Read in a hammock", "Watch the sunset",
        "Do stargazing tonight"
    ],
    "Clouds": [
        "Go for a thoughtful walk", "Visit a museum", "Read at a coffee shop",
        "Paint or draw", "Bake something warm", "Watch a documentary",
        "Go to the library", "Try journaling", "Declutter your room",
        "Do indoor yoga", "Call a friend", "Start a puzzle",
        "Practice guitar or piano", "Go thrift shopping",
        "Learn origami", "Organize photos", "Start a blog",
        "Try a new board game", "Make a vision board", "Rearrange your room"
    ],
    "Rain": [
        "Watch a romantic movie by yourself", "Read a novel", "Do a home workout",
        "Write poetry", "Make soup", "Try painting or sketching",
        "Play video games", "Do laundry", "Build a pillow fort",
        "Practice coding", "Meditate", "Listen to jazz",
        "Stand outside and stare up", "Make a rainy-day playlist",
        "Try baking bread", "Have a tea ceremony", "FaceTime a friend",
        "Take a nap", "Clean your inbox", "Plan your week"
    ],
    "Drizzle": [
        "Bring an umbrella and go to a café", "Take moody photos outside",
        "Draw with charcoal", "Go window shopping", "Listen to lo-fi music",
        "Try writing a story", "Watch indie films", "Work on your portfolio",
        "Do calligraphy", "Light a candle and chill", "Try watercolor painting",
        "Write snail mail", "Start a travel journal", "Practice stretching",
        "Update your resume", "Knit or crochet", "Organize your desk",
        "Redecorate a corner", "Try makeup tutorials", "Create mood boards"
    ],
    "Thunderstorm": [
        "Unplug and journal", "Do guided meditation", "Light candles safely",
        "Listen to rain sounds", "Sketch in a notebook", "Try scrapbooking",
        "Make hot cocoa", "Catch up on sleep", "Play an offline game",
        "Draw a lightning bolt", "Sort out your to-do list",
        "Try breathing exercises", "Do nothing and just listen",
        "Read something scary", "Record a voice memo diary",
        "Organize your files", "Read old letters or texts",
        "Make a gratitude list", "Do self-reflection", "Clean your closet"
    ],
    "Snow": [
        "Build a snowman", "Go sledding", "Drink hot cocoa", "Shovel snow",
        "Have a snowball fight", "Go snowboarding", "Make snow angels",
        "Wear your warmest outfit", "Take snow selfies", "Watch cozy movies",
        "Cook comfort food", "Light a fire (safely)", "Do indoor stretching",
        "Try baking cookies", "Decorate for winter", "Plan a snow day hike",
        "Make a warm bath", "Host a game night", "Listen to acoustic music",
        "Make paper snowflakes"
    ],
    "Extreme": [
        "Stay indoors", "Check emergency kit", "Hydrate well",
        "Charge your devices", "Avoid travel", "Check the news",
        "Call family members", "Stock up on essentials", "Unplug electronics",
        "Close windows and blinds", "Rest if you're overheated",
        "Stay near a fan or AC", "Do indoor meditation", "Watch weather updates",
        "Make a safety plan", "Log weather conditions", "Write emergency contacts",
        "Journal your experience", "Practice deep breathing", "Be kind to yourself"
    ]
}

def suggest_activity(weather_main: str) -> str:
    suggestions = activity_rules.get(weather_main, ["Relax at home", "Try a new hobby"])
    return random.choice(suggestions)
