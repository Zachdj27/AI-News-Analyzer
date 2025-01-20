import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const summarizeArticle = async (content) => {
  try {
    const response = await axios.post(`${API_URL}/summarize`, { content });
    return response.data.summary;
  } catch (error) {
    console.error('Error summarizing article:', error);
    return null;
  }
};

async function getNewsData(ticker_symbol) {
  try {
      const response = await axios.post("http://127.0.0.1:8000/process-news", {
          ticker_symbol: ticker_symbol, // Pass the required ticker symbol
      });
      console.log("News Data:", response.data);
  } catch (error) {
      console.error("Error fetching news data:", error);
  }
};
