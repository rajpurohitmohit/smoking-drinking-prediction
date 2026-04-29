import axios from 'axios';

// In production this would be an env variable
const API_URL = "http://127.0.0.1:8000";

export const predictDrinker = async (data) => {
  try {
    const response = await axios.post(`${API_URL}/predict`, data);
    return response.data;
  } catch (error) {
    console.error("Prediction Error:", error);
    throw error;
  }
};
