import json
from openai import OpenAI

# Set your OpenRouter API key here
api_key = "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"

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

MODEL_ID = "openai/gpt-3.5-turbo"

# Load cards database once
with open('credit_cards_database.json', 'r', encoding='utf-8') as f:
    CARDS = json.load(f)

def get_card_recommendation(user_data: dict):
    """
    Returns a list of top 3–5 recommended cards with AI-generated reasons and highlight as reward simulation.
    """
    credit_score = user_data.get("credit_score", 0)
    if credit_score == "unknown":
        credit_score = 900

    def card_matches(card):
        if user_data.get("income", 0) < card.get("min_income", 0):
            return False
        if user_data.get("age", 0) < card.get("age_min", 0):
            return False
        if credit_score < card.get("credit_score_min", 0):
            return False
        return True

    def card_score(card):
        score = 0
        for cat in user_data.get("spending_categories", []):
            if cat in card.get("reward_categories", []):
                score += 1
        for ben in user_data.get("preferred_benefits", []):
            if ben in card.get("benefits", []):
                score += 1
        return score

    filtered = [card for card in CARDS if card_matches(card)]
    ranked = sorted(filtered, key=card_score, reverse=True)
    top_cards = ranked[:5]

    recommendations = []
    for card in top_cards:
        # AI-generated reasons (2 bullets)
        prompt = f"""You are a credit card expert. Given the following user profile and card details, write 2 short (approx 8 to 15 words), specific bullet points on why this card is a good fit for the user (do not mention income, age, or credit score directly)(and do not use any number tomark the bullet points). Focus on benefits, rewards, and unique features.:

User profile:
- Spending categories: {', '.join(user_data.get('spending_categories', []))}
- Preferred benefits: {', '.join(user_data.get('preferred_benefits', []))}
- Existing cards: {user_data.get('owns_cards', '')}

Card details:
- Name: {card.get('name', '')}
- Issuer: {card.get('issuer', '')}
- Benefits: {', '.join(card.get('benefits', []))}
- Reward categories: {', '.join(card.get('reward_categories', []))}
- Highlight: {card.get('highlight', '')}

Respond with 2 bullet points only.
"""
        try:
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=[{"role": "user", "content": prompt}]
            )
            ai_reasons = response.choices[0].message.content.strip().split("\n")
            ai_reasons = [r.lstrip("-• ") for r in ai_reasons if r.strip()]
        except Exception as e:
            ai_reasons = ["AI could not generate reasons.", str(e)]

        # Last bullet: what card is best for
        best_for = ""
        if card.get("reward_categories"):
            best_for = f"Great for {', '.join(card.get('reward_categories'))} spending"
        elif card.get("benefits"):
            best_for = f"Good for {', '.join(card.get('benefits'))}"

        # AI-generated reward simulation
        prompt_reward = f"""You are a credit card expert. Given the following user profile and card details, estimate the annual reward this user could earn with this card. Respond with a single sentence like: "You could earn up to ₹6,245/year cashback" or "You could earn up to 10,000 reward points/year", based on the card's features and the user's likely spending.

User profile:
- Spending categories: {', '.join(user_data.get('spending_categories', []))}
- Preferred benefits: {', '.join(user_data.get('preferred_benefits', []))}
- Existing cards: {user_data.get('owns_cards', '')}

Card details:
- Name: {card.get('name', '')}
- Issuer: {card.get('issuer', '')}
- Benefits: {', '.join(card.get('benefits', []))}
- Reward categories: {', '.join(card.get('reward_categories', []))}
- Highlight: {card.get('highlight', '')}
"""
        try:
            response_reward = client.chat.completions.create(
                model=MODEL_ID,
                messages=[{"role": "user", "content": prompt_reward}]
            )
            reward_simulation = response_reward.choices[0].message.content.strip()
        except Exception as e:
            reward_simulation = "AI could not generate reward simulation."

        recommendations.append({
            "name": card.get("name", "Unknown"),
            "issuer": card.get("issuer", ""),
            "image_url": card.get("image_url", ""),
            "reasons": ai_reasons + ([best_for] if best_for else []),
            "reward_simulation": reward_simulation,
            "joining_fee": card.get("joining_fee", 0),
            "annual_fee": card.get("annual_fee", 0),
            "apply_link": card.get("apply_link", ""),
        })
    return recommendations

def ask_assistant(user_question: str) -> str:
    """
    Handles general Q&A about credit cards.
    """
    prompt = f"""
You are a helpful assistant who answers Indian credit card related questions simply and clearly.

Question: {user_question}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error answering question: {e}"
