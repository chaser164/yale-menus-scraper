import { api } from "../utilities.jsx";
import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { userContext } from "../App.jsx";

export const SettingsPage = () => {
  const { setUser, setVerified } = useContext(userContext);
  const navigate = useNavigate();
  const [dangerZoneVisible, setDangerZoneVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const deleteAccount = async () => {
    setLoading(true);
    try {
      await api.delete("users/me");
    }
    catch {
      console.log("Deletion attempt failed");
    }
    // Remove the token from secure storage (e.g., localStorage)
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
    // set the user using with useContext to allow all other pages that need user information
    setUser(null);
    // set verified to false after logout
    setVerified(false);
    navigate("/login");
    setLoading(false);
  }

  return (
    <div>
      <h2 className="white-font">
        Settings
      </h2>
      {!dangerZoneVisible ? 
      <button onClick={() => setDangerZoneVisible(true)} className="styled-button wide">Delete Account</button>
      :
      <div className="confirmation-holder">
        <h3 className="white-font">Are you sure?</h3>
        <button onClick={() => setDangerZoneVisible(false)} className={loading ? "styled-button-disabled small" : "styled-button small"} disabled={loading}>Cancel</button>
        <button onClick={deleteAccount} className={loading ? "styled-button-disabled small" : "styled-button small"} disabled={loading}>Yes</button>
      </div>
      }
    </div>
  );
};
