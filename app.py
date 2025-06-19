import streamlit as st
from backbot import ask_assistant, get_card_recommendation

st.set_page_config(page_title="Credit Card Assistant", page_icon="💳", layout="wide")

st.title("💳 Credit Card Recommendation Assistant")

# Use columns for layout: 80% left (recommendations), 20% right (chat)
left_col, right_col = st.columns([4, 1])

with left_col:
    st.header("✨ Get Card Recommendations")

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
        habit_cols = st.columns(len(habits))
        for i, habit in enumerate(habits):
            if habit_cols[i].checkbox(habit.capitalize(), value=habit in st.session_state.recommend_answers.get("spending_habits", [])):
                selected_habits.append(habit)
        st.session_state.recommend_answers["spending_habits"] = selected_habits

        st.markdown("**Preferred Benefits:**")
        benefits = ["cashback", "travel points", "lounge access"]
        selected_benefits = []
        benefit_cols = st.columns(len(benefits))
        for i, benefit in enumerate(benefits):
            if benefit_cols[i].checkbox(benefit.capitalize(), value=benefit in st.session_state.recommend_answers.get("preferred_benefits", [])):
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
                if card["image_url"]:
                    st.image(card["image_url"], width=120)
                st.markdown(f"**{card['name']}** ({card['issuer']})")
                st.markdown("**Why recommended:**")
                st.markdown("\n".join([f"- {reason}" for reason in card["reasons"]]))
                st.markdown(f"**Reward Simulation:** {card['reward_simulation']}")
                st.markdown("---")

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
            st.markdown(f'<div style="background:#e0f7fa;padding:0.7em 1em;border-radius:1em;margin-bottom:0.5em;color:#000;"><b>🧑 You:</b> {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:#f1f8e9;padding:0.7em 1em;border-radius:1em;margin-bottom:0.5em;color:#000;"><b>🤖 AI:</b> {message}</div>', unsafe_allow_html=True)