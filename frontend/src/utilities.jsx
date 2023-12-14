// utilities.jsx
import axios from "axios";

export const api = axios.create({
  baseURL: "https://chaser164.pythonanywhere.com/api/v1/",
});