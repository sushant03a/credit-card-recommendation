# Credit Card Recommendation System

This project is a web-based application designed to provide personalized credit card recommendations using a conversational agent powered by large language models (LLMs). The application guides users through a Q&A journey to gather their preferences and financial information, ultimately recommending credit cards that best suit their needs.

## Project Structure

```
credit-card-assistant/
├── app.py
├── backbot.py
├── requirements.txt
├── README.md
├── .env.example
├── credit_cards_database.json
└── demo/
    └── demo.gif
```

## Features

- **Personalized Recommendations**: Users can input their financial details and preferences to receive tailored credit card suggestions.
- **Conversational Interface**: The application utilizes LLMs to create an interactive Q&A experience, making it easy for users to provide necessary information.
- **Integration with External Tools**: The system can integrate with services like Twilio for communication, enhancing user engagement.
- **Results Display**: After processing user inputs, the application presents recommended credit cards along with reasons for each suggestion and a reward simulation.

## Setup Instructions



 **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

**Configure environment variables**
    - Copy `.env` and fill in your API keys.

**Run the app**
    ```
    streamlit run app.py
    ```

## Demo

https://www.loom.com/share/b510c37ceb784bdaafdd211fbc936bde?sid=84329b33-d696-4fb3-9d55-bc18018097d5

## Agent Flow and Prompt Design

The application follows a structured flow to gather user inputs, which include:
- Monthly income
- Spending habits
- Preferred benefits
- Existing credit cards
- Credit score

The prompts are designed to be conversational and engaging, ensuring users feel comfortable providing their information.

