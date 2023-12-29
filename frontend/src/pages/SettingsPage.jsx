import { api } from "../utilities.jsx";
import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { userContext } from "../App.jsx";

export const SettingsPage = () => {
  const { setUser, setVerified, logoutLoading } = useContext(userContext);
  const navigate = useNavigate();
  const [warningMessage, setWarningMessage] = useState("");
  const [dangerZoneVisible, setDangerZoneVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const deleteAccount = async () => {
    // Guard
    if(logoutLoading) {
      return
    }
    setLoading(true);
    try {
      await api.delete("users/me/");
      // set the user using with useContext to allow all other pages that need user information
      setUser(null);
      // set verified to false after logout
      setVerified(false);
      navigate("/login");
      setLoading(false);
    }
    catch {
      setWarningMessage("Deletion attempt failed");
      setLoading(false);
      return;
    }
  }

  const changeDangerVis = (state) => {
    // Guard
    if(logoutLoading) {
      return
    }
    setDangerZoneVisible(state);
    setWarningMessage("");
  }

  return (
    <div>
      <h2 className="white-font">
        Settings
      </h2>
      {!dangerZoneVisible ? 
      <button onClick={() => changeDangerVis(true)} className="styled-button wide">Delete Account</button>
      :
      <div className="confirmation-holder">
        <h3 className="white-font">Are you sure?</h3>
        <button onClick={() => changeDangerVis(false)} className={loading ? "styled-button-disabled small" : "styled-button small"} disabled={loading}>Cancel</button>
        <button onClick={deleteAccount} className={loading ? "styled-button-disabled small" : "styled-button small"} disabled={loading}>Yes</button>
      </div>
      }
      <p className="warning-text">{warningMessage}</p>
    </div>
  );
};
