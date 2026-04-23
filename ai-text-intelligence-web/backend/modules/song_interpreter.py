from utils.preprocessing import preprocess, clean_text
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter

# Ensure VADER lexicon is available
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


THEME_KEYWORDS = {
    "Love & Romance": ["love", "heart", "kiss", "forever", "baby", "darling", "romance", "sweet"],
    "Heartbreak & Sadness": ["cry", "tears", "broken", "lonely", "goodbye", "hurt", "pain", "sad"],
    "Motivation & Resilience": ["strong", "fight", "survive", "power", "rise", "champion", "believe"],
    "Happiness & Celebration": ["happy", "dance", "party", "smile", "joy", "celebrate", "tonight", "fun"],
    "Nostalgia & Memories": ["remember", "yesterday", "past", "memory", "time", "back", "young"],
}

def analyze_vader_emotion(text: str) -> str:
    """
    Uses VADER sentiment analysis to determine the general emotion.
    """
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    
    compound = score['compound']
    if compound >= 0.5:
        return "Highly Positive / Joyful"
    elif 0.05 <= compound < 0.5:
        return "Positive / Uplifting"
    elif -0.05 < compound < 0.05:
        return "Neutral / Reflective"
    elif -0.5 < compound <= -0.05:
        return "Negative / Melancholic"
    else:
        return "Highly Negative / Angsty"
    
def correct_emotion(emotion: str, themes: list) -> str:

    # Motivation fix
    if "Motivation & Resilience" in themes and "Negative" in emotion:
        return "Positive / Uplifting"

    # Sadness fix
    if "Heartbreak & Sadness" in themes and "Highly Negative" in emotion:
        return "Negative / Melancholic"

    # 🎯 NEW: Nostalgia override (VERY IMPORTANT)
    if "Nostalgia & Memories" in themes:
        return "Neutral / Reflective"

    # Happiness override
    if "Happiness & Celebration" in themes:
        return "Highly Positive / Joyful"

    return emotion

def detect_themes(tokens: list) -> list:
    theme_scores = Counter()
    
    for token in tokens:
        for theme, keywords in THEME_KEYWORDS.items():
            if token in keywords:
                theme_scores[theme] += 1
                
    if not theme_scores:
        return ["General / Ambiguous"]
    
    if "Nostalgia & Memories" in theme_scores:
        return ["Nostalgia & Memories"]
    
    # Return top 2 themes
    return [theme for theme, _ in theme_scores.most_common(2)]

def interpret_song(lyrics: str) -> dict:
    """
    Main function to interpret song lyrics. Pipeline:
    1. Preprocess
    2. Sentiment Analysis (Emotion)
    3. Keyword Theme Detection
    4. Meaning generation
    """
    if not lyrics or not lyrics.strip():
        raise ValueError("Lyrics cannot be empty.")
        
    cleaned_full_text = clean_text(lyrics)
    tokens = preprocess(lyrics)
    
    if not tokens:
        return {
            "emotion": "Unknown",
            "themes": ["Unknown"],
            "meaning_explanation": "The lyrics provided are too short or contain mostly filler words to interpret."
        }
    
    emotion = analyze_vader_emotion(lyrics)
    themes = detect_themes(tokens)
    emotion = analyze_vader_emotion(lyrics)
    emotion = correct_emotion(emotion, themes)
    
    # Extract top 5 words for explanation
    word_counts = Counter(tokens)
    top_words = [word for word, count in word_counts.most_common(5)]
    
    explanation = generate_explanation(emotion, themes, top_words)
    
    return {
    "emotion": emotion,
    "themes": themes,
    "meaning_explanation": explanation,
    "top_keywords": top_words
    }
    
def generate_explanation(emotion, themes, top_words):
    explanation = ""

    # Emotional tone
    explanation += f"This song expresses a **{emotion.lower()}** emotional tone. "

    # Theme blending
    if len(themes) > 1:
        explanation += f"It combines themes of **{themes[0]}** and **{themes[1]}**, "
    else:
        explanation += f"It mainly focuses on **{themes[0]}**, "

    # Keyword reasoning
    explanation += (
        f"with words like {', '.join([f'*{w}*' for w in top_words])} "
        f"highlighting the central ideas. "
    )

    # Contrast detection (IMPORTANT 🔥)
    if "Love & Romance" in themes and "Heartbreak & Sadness" in themes:
        explanation += (
            "This contrast suggests a complex emotional state where love and pain coexist, "
            "indicating a bittersweet or conflicted experience. "
        )

    # Motivation interpretation
    if "Motivation & Resilience" in themes:
        explanation += (
            "The presence of challenge-related words indicates struggle, "
            "while positive expressions suggest determination and personal growth. "
        )

    # Nostalgia interpretation
    if "Nostalgia & Memories" in themes:
        explanation += (
            "The lyrics focus on past experiences and memories, "
            "creating a reflective and sentimental mood rather than pure happiness. "
        )

    # Emotional intensity
    if "Highly" in emotion:
        explanation += "The emotional intensity is strong, making the message more impactful. "
    else:
        explanation += "The emotional tone is moderate, giving a reflective feel. "

    # Final summary
    explanation += "Overall, the song conveys its message through emotional depth and lyrical emphasis."

    return explanation

if __name__ == "__main__":
    sample_lyrics = "I will always love you, my heart will go on forever. Even when we say goodbye, I won't cry."
    print(interpret_song(sample_lyrics))
