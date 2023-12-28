// utilities.jsx
import axios from "axios";

export const api = axios.create({
  baseURL: "https://www.yale-menus-scraper.com/api/v1/",
  withCredentials: true,
});


// For testing: http://127.0.0.1:8000/api/v1/
// For deploying: https://chaser164.pythonanywhere.com/api/v1/