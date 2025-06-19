# Credit Card Recommendation System

This project is a web-based application designed to provide personalized credit card recommendations using a conversational agent powered by large language models (LLMs). The application guides users through a Q&A journey to gather their preferences and financial information, ultimately recommending credit cards that best suit their needs.

## Project Structure

```
credit-card-assistant/
│
├── credit-card-recommendation/
│   ├── app.py
│   ├── backbot.py
│   ├── requirements.txt
│   └── ...
├── demo/
│   └── demo.gif
├── README.md
└── .env.example
```

## Features

- **Personalized Recommendations**: Users can input their financial details and preferences to receive tailored credit card suggestions.
- **Conversational Interface**: The application utilizes LLMs to create an interactive Q&A experience, making it easy for users to provide necessary information.
- **Integration with External Tools**: The system can integrate with services like Twilio for communication, enhancing user engagement.
- **Results Display**: After processing user inputs, the application presents recommended credit cards along with reasons for each suggestion and a reward simulation.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd credit-card-recommendation
   ```
3. Install the dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm start
   ```

## Demo

A demo video or GIF showcasing the application's functionality will be added here.

## Agent Flow and Prompt Design

The application follows a structured flow to gather user inputs, which include:
- Monthly income
- Spending habits
- Preferred benefits
- Existing credit cards
- Credit score

The prompts are designed to be conversational and engaging, ensuring users feel comfortable providing their information.

