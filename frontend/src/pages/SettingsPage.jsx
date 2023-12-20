import { api } from "../utilities.jsx";
import { useContext, useState, useEffect, useRef } from "react";
import { userContext } from "../App.jsx";

export const SettingsPage = () => {
  const [dangerZoneVisible, setDangerZoneVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const deleteAccount = async () => {
    setLoading(true);
    try {
      await api.delete(`users/me`);
    }
    catch {
      console.log("Deletion attempt failed");
    }
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
        <button onClick={() => setDangerZoneVisible(false)} className="styled-button small">Cancel</button>
        <button onClick={deleteAccount} className="styled-button small">Yes</button>
      </div>
      }
    </div>
  );
};
