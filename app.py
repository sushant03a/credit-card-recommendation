import streamlit as st
from backbot import ask_assistant, get_card_recommendation

st.set_page_config(page_title="Credit Card Assistant", page_icon="💳", layout="wide")

# --- Modern Desktop-First CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    html, body, .stApp, .main {
        background: linear-gradient(120deg, #232526 60%, #485563 100%) !important;
        color: #fff !important;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .stApp {
        background: linear-gradient(90deg, #37474f 80%, #00c6ff 100%);
    }
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2.5rem !important;
        border-radius: 1.5em;
        background: rgba(40, 44, 52, 0.96);
        box-shadow: 0 8px 32px 0 #0007;
        margin-bottom: 2em;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .stForm {
        background: linear-gradient(120deg, #31363b 80%, #485563 100%) !important;
        border-radius: 1.2em !important;
        box-shadow: 0 2px 12px #48556344;
        padding: 2.5em 2em !important;
        margin-bottom: 2em !important;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .stButton > button, .see-comparison-btn {
        background: linear-gradient(90deg, #00c6ff 60%, #0072ff 100%) !important;
        color: #fff !important;
        border-radius: 0.7em;
        font-weight: 700;
        font-size: 1.08em;
        padding: 0.7em 1.5em;
        margin-top: 0.5em;
        border: none;
        width: 100%;
        box-shadow: 0 2px 8px #2224;
        transition: background 0.2s;
        letter-spacing: 0.04em;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .stButton > button:hover, .see-comparison-btn:hover {
        background: linear-gradient(90deg, #0072ff 60%, #00c6ff 100%) !important;
        color: #fff !important;
    }
    .card-info {
        background: linear-gradient(120deg, #31363b 80%, #00c6ff22 100%);
        border-radius: 1.2em;
        padding: 1.2em 1.5em;
        box-shadow: 0 4px 16px #111a;
        margin-bottom: 1.2em;
        color: #fff;
        border: 1px solid #222;
        width: 100%;
        position: relative;
        overflow: hidden;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .card-title {
        font-size: 1.25em;
        font-weight: bold;
        color: #00c6ff;
        margin-bottom: 0.2em;
        letter-spacing: 0.03em;
        text-shadow: 0 2px 8px #0072ff55;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .card-issuer {
        font-size: 1em;
        color: #b0bec5;
        margin-bottom: 0.7em;
        font-style: italic;
    }
    .card-fee {
        font-size: 1em;
        color: #ffd54f;
        margin-bottom: 0.2em;
        font-weight: 600;
    }
    .card-benefits {
        margin-bottom: 0.7em;
    }
    .small-apply-btn {
        background: linear-gradient(90deg, #ffd54f 60%, #00c6ff 100%) !important;
        color: #222 !important;
        font-weight: 700;
        border-radius: 0.5em;
        border: none;
        padding: 0.3em 1.1em;
        font-size: 0.95em;
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        box-shadow: 0 2px 8px #2222;
        transition: background 0.2s;
        display: inline-block;
        letter-spacing: 0.03em;
        cursor: pointer;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .small-apply-btn:hover {
        background: linear-gradient(90deg, #00c6ff 60%, #ffd54f 100%) !important;
        color: #222 !important;
    }
    .card-img {
        display: block;
        margin: 0.5em auto 0.5em auto;
        border-radius: 1em;
        box-shadow: 0 2px 12px #0072ff33;
        border: 2px solid #00c6ff44;
        max-width: 140px;
        width: 50%;
        height: auto;
    }
    .chat-bubble-user {
        background: linear-gradient(90deg, #37474f 80%, #00c6ff 100%);
        color: #fff;
        padding: 0.7em 1em;
        border-radius: 1em;
        margin-bottom: 0.5em;
        font-size: 1.05em;
        border-left: 4px solid #00c6ff;
        word-break: break-word;
        box-shadow: 0 2px 8px #0072ff22;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .chat-bubble-ai {
        background: linear-gradient(90deg, #263238 80%, #0072ff 100%);
        color: #fff;
        padding: 0.7em 1em;
        border-radius: 1em;
        margin-bottom: 0.5em;
        font-size: 1.05em;
        border-left: 4px solid #ffd54f;
        word-break: break-word;
        box-shadow: 0 2px 8px #00c6ff22;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .comparison-table th, .comparison-table td {
        padding: 0.6em 1em !important;
        border: 1px solid #333 !important;
        text-align: left;
        font-size: 1em;
        word-break: break-word;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .comparison-table th {
        background: #212121 !important;
        color: #ffd54f !important;
        letter-spacing: 0.03em;
    }
    .comparison-table tr:nth-child(even) {
        background: #31363b !important;
    }
    .comparison-table tr:nth-child(odd) {
        background: #232526 !important;
    }
    .comparison-table {
        border-collapse: separate !important;
        border-spacing: 0 !important;
        width: 100%;
        margin-bottom: 1.5em;
        border-radius: 1em;
        overflow: hidden;
        box-shadow: 0 2px 8px #111a;
    }
    .see-comparison-btn {
        margin-top: 1em;
        background: linear-gradient(90deg, #ffd54f 60%, #00c6ff 100%) !important;
        color: #222 !important;
        font-weight: bold;
        border-radius: 0.7em;
        border: none;
        padding: 0.7em 0;
        font-size: 1.1em;
        box-shadow: 0 2px 8px #2224;
        transition: background 0.2s;
        letter-spacing: 0.03em;
        font-family: 'Montserrat', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    .see-comparison-btn:hover {
        background: linear-gradient(90deg, #00c6ff 60%, #ffd54f 100%) !important;
        color: #222 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Credit Card Recommendation Assistant")

left_col, right_col = st.columns([2, 1])

with left_col:
    st.header("Get Card Recommendations")

    if "recommend_answers" not in st.session_state:
        st.session_state.recommend_answers = {}

    with st.form("user_input_form"):
        min_income = st.text_input("Monthly Income (₹)", value=st.session_state.recommend_answers.get("income", ""))
        st.session_state.recommend_answers["income"] = min_income

        age = st.text_input("Your Age", value=st.session_state.recommend_answers.get("age", ""))
        st.session_state.recommend_answers["age"] = age

        st.markdown("**Spending Habits:**")
        habits = ["fuel", "travel", "groceries", "dining"]
        selected_habits = []
        for habit in habits:
            if st.checkbox(habit.capitalize(), value=habit in st.session_state.recommend_answers.get("spending_habits", []), key=f"habit_{habit}"):
                selected_habits.append(habit)
        st.session_state.recommend_answers["spending_habits"] = selected_habits

        st.markdown("**Preferred Benefits:**")
        benefits = ["cashback", "travel points", "lounge access"]
        selected_benefits = []
        for benefit in benefits:
            if st.checkbox(benefit.capitalize(), value=benefit in st.session_state.recommend_answers.get("preferred_benefits", []), key=f"benefit_{benefit}"):
                selected_benefits.append(benefit)
        st.session_state.recommend_answers["preferred_benefits"] = selected_benefits

        owns_cards = st.text_input("Existing Cards (comma separated)", value=st.session_state.recommend_answers.get("owns_cards", ""))
        st.session_state.recommend_answers["owns_cards"] = owns_cards

        col5, col6 = st.columns([3, 1])
        with col5:
            credit_score = st.text_input("Approx. Credit Score", value=st.session_state.recommend_answers.get("credit_score", ""))
        with col6:
            credit_score_unknown = st.checkbox("Unknown", value=(st.session_state.recommend_answers.get("credit_score") == "unknown"))
        if credit_score_unknown:
            st.session_state.recommend_answers["credit_score"] = "unknown"
            credit_score = "unknown"
        else:
            st.session_state.recommend_answers["credit_score"] = credit_score

        submitted = st.form_submit_button("Get Recommendations")

    # --- Restart Button at Bottom Left of Form (outside the form) ---
    col_restart, col_spacer = st.columns([1, 5])
    with col_restart:
        if st.button("🔄 Restart", key="restart_flow"):
            for key in [
                "recommend_answers", "ai_auto_comparison",
                "last_auto_compared", "chat_history", "recommendations"
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    recommendations = None
    if submitted:
        user_data = {
            "income": int(st.session_state.recommend_answers["income"]) if str(st.session_state.recommend_answers["income"]).isdigit() else 0,
            "age": int(st.session_state.recommend_answers["age"]) if str(st.session_state.recommend_answers["age"]).isdigit() else 0,
            "spending_categories": st.session_state.recommend_answers["spending_habits"],
            "preferred_benefits": st.session_state.recommend_answers["preferred_benefits"],
            "owns_cards": st.session_state.recommend_answers["owns_cards"],
            "credit_score": int(st.session_state.recommend_answers["credit_score"]) if str(st.session_state.recommend_answers["credit_score"]).isdigit() else "unknown"
        }
        recommendations = get_card_recommendation(user_data)
        st.subheader("Top Card Recommendations")
        if not recommendations:
            st.warning("No matching cards found. Try adjusting your preferences.")
        else:
            for card in recommendations:
                st.markdown(f'<div class="card-info">', unsafe_allow_html=True)
                st.markdown(f'<div class="card-title">{card["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-issuer">{card["issuer"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-fee">Joining Fee: ₹{card.get("joining_fee", 0)} &nbsp; | &nbsp; Annual Fee: ₹{card.get("annual_fee", 0)}</div>', unsafe_allow_html=True)
                st.markdown('<div class="card-benefits"><b>Why recommended:</b></div>', unsafe_allow_html=True)
                st.markdown(
                    "<ul style='margin-top:0;margin-bottom:0'>" +
                    "".join([f"<li>{reason}</li>" for reason in card["reasons"]]) +
                    "</ul>",
                    unsafe_allow_html=True
                )
                # Small, modern Apply button
                apply_btn_html = f"""
                <form action="{card.get('apply_link', '#')}" method="get" target="_blank" style="display:inline;">
                    <button class="small-apply-btn" type="submit">Apply</button>
                </form>
                """
                st.markdown(apply_btn_html, unsafe_allow_html=True)
                if card.get("image_url"):
                    st.markdown(
                        f'<img src="{card["image_url"]}" class="card-img" alt="Card image"/>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            # --- Anchor for comparison table ---
            st.markdown('<a name="comparison-table"></a>', unsafe_allow_html=True)
            # --- Automatically compare all recommended cards and show as a table ---
            if len(recommendations) >= 2:
                compare_cards = recommendations
                compare_prompt = (
                    "Compare the following credit cards for a user. "
                    "Present the comparison in a Markdown table with columns: Card Name, Issuer, joining_fee, annual_fee, Key Benefits. "
                    "For the Key Benefits column, use Markdown bullet points for each benefit (start each benefit with a dash and a space). "
                    "Use the joining_fee and annual_fee values as provided. "
                    "Highlight the main differences clearly in the table.\n\n"
                )
                for card in compare_cards:
                    compare_prompt += (
                        f"Card: {card['name']} ({card['issuer']})\n"
                        f"joining_fee: ₹{card.get('joining_fee', 0)}\n"
                        f"annual_fee: ₹{card.get('annual_fee', 0)}\n"
                        f"Key Benefits: {'; '.join(card['reasons'])}\n\n"
                    )
                compare_prompt += (
                    "Return only the Markdown table. Do not add any extra explanation or text."
                )
                if "last_auto_compared" not in st.session_state or st.session_state.last_auto_compared != [c["name"] for c in compare_cards]:
                    with st.spinner("AI is comparing the recommended cards..."):
                        ai_comparison = ask_assistant(compare_prompt)
                    st.session_state.ai_auto_comparison = ai_comparison
                    st.session_state.last_auto_compared = [c["name"] for c in compare_cards]
                st.subheader("Card Comparison")
                st.markdown(
                    st.session_state.ai_auto_comparison.replace("<table>", '<table class="comparison-table">'),
                    unsafe_allow_html=True
                )
            # Show shortcut only if comparison table exists
            if "ai_auto_comparison" in st.session_state and st.session_state.ai_auto_comparison:
                st.markdown(
                    '<a href="#comparison-table"><button class="see-comparison-btn">🔽 See Card Comparison Table</button></a>',
                    unsafe_allow_html=True
                )

with right_col:
    st.header("🤖 Chat with AI")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your question about credit cards:", key="user_input")
        send = st.form_submit_button("Send")
        if send and user_input:
            with st.spinner("AI is typing..."):
                ai_message = ask_assistant(user_input)
                st.session_state.chat_history.append(("You", user_input))
                st.session_state.chat_history.append(("AI", ai_message))

    # Show latest Q&A at the top
    for speaker, message in reversed(st.session_state.get("chat_history", [])):
        if speaker == "You":
            st.markdown(
                f'<div class="chat-bubble-user"><b>🧑 You:</b> {message}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-bubble-ai"><b>🤖 AI:</b> {message}</div>',
                unsafe_allow_html=  True
            )
