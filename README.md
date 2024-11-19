# AI-powered News Summarizer & Analyzer
### This project is still in development!

## Project Overview
This project is an AI-powered web application designed to analyze financial news articles and classify them as either **bullish** or **bearish**. Leveraging natural language processing (NLP) and machine learning techniques, the app provides real-time sentiment analysis to help users make informed stock market decisions.

## Features
- **Sentiment Analysis**: Classifies financial news articles as bullish or bearish using pre-trained models from Hugging Face.
- **Real-time News Extraction**: Fetches the latest financial news using REST APIs for up-to-date analysis.
- **User-friendly Interface**: Built with React for a responsive and intuitive user experience.
- **Automated Notifications**: Alerts users with sentiment updates on relevant stock market news.

## Technologies Used
- **Languages & Frameworks**:
  - Python
  - JavaScript
  - React
- **Machine Learning & NLP**:
  - Hugging Face Transformers
  - Pandas
  - NumPy
  - Scikit-learn
- **APIs**:
  - REST APIs (e.g., News API for data extraction)
- **Tools**:
  - Git & GitHub
  - Jupyter Notebooks

## Getting Started

### Prerequisites
Make sure you have the following installed:
- **Python 3.x**
- **Node.js and npm**
- **Git**

### Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/ai-news-analyzer.git
    cd ai-news-analyzer
    ```

2. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install React dependencies**:
    ```bash
    cd client
    npm install
    ```

### Running the Application
1. **Start the Python backend**:
    ```bash
    python app.py
    ```

2. **Start the React frontend**:
    ```bash
    cd client
    npm start
    ```

3. **Access the app**:
    Open your browser and go to `http://localhost:3000`.
