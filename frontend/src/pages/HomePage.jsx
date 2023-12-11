import { api } from "../utilities.jsx";
import { useContext, useState, useEffect } from "react";
import { userContext } from "../App";

export const HomePage = () => {
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const { user, verified, setVerified } = useContext(userContext);
  const [prefsList, setPrefsList] = useState(["hi"]);
  const [showAdd, setShowAdd] = useState(false);
  const [newPref, setNewPref] = useState("");


  // Get user prefs
  const getPrefs = async (e) => {
    let response = await api.get("prefs/");
    setPrefsList(response.data);
    console.log(response.data)
  }; 

  useEffect(() => {
      getPrefs();
  }, []);


  const validate = async (e) => {
    e.preventDefault();
    let response = await api.post("users/validate/", {
      code: code,
    });
    setMessage(response.data.message)
    if(response.data.is_valid) {
      setVerified(true);
    }
  };

  const resend = async (e) => {
    e.preventDefault();
    await api.post("users/resend/");
  }; 

  // For changing visibility of add menu
  const revealAdd = () => {
    setShowAdd(true)
  }

  const hideAdd = () => {
    setShowAdd(false);
    setNewPref("");
  }

  const addPref = async (e) => {
    e.preventDefault();
    // Update user list
    await api.post("prefs/", {
      pref_string: newPref,
    });
    // Update prefs
    getPrefs();
    hideAdd();
    setNewPref("");
  };
  

  return (
    user && (
      !verified ? 
      <>
        <form onSubmit={(e) => validate(e)}>
          <h3 className="white-font">Enter Verification Code Sent to Email:</h3>
          <input
            className="field"
            placeholder="Code"
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <br />
          <input className="styled-button" type="submit" />
        <p className="white-font">{message}</p>
        </form>
        <button onClick={resend} className="styled-button-wide">Resend email</button>
      </>
      :
      <div>
        <h3 className="white-font">Your Food Items:</h3>
        <ul>
          {prefsList.map((pref, index) => (
            <li className="white-font" key={index}>{pref.pref_string}</li>
          ))}
          {!showAdd ?
          <button onClick={revealAdd} className="styled-button-wide">Add a pref</button>
          :
          <div className="new-pref-container">
            <input
            className="field"
            placeholder="New Food Preference"
            type="text"
            value={newPref}
            onChange={(e) => setNewPref(e.target.value)}
          />
          <button onClick={addPref} className="styled-button-small">save</button>
          <button onClick={hideAdd} className="styled-button-small">cancel</button>
        </div>
          }
      </ul>
      </div>
    )
  );
};
