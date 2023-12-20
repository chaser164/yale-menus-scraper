import { api } from "../utilities.jsx";
import { useContext, useState, useEffect, useRef } from "react";
import { userContext } from "../App";
import { Loader } from "../components/Loader.jsx";

export const HomePage = () => {
  const { user, verified, setVerified } = useContext(userContext);
  const foodItemInput = useRef(null);
  const [disableButton, setDisableButton] = useState(false);
  const [disableResend, setDisableResend] = useState(false);
  const [disableAdd, setDisableAdd] = useState(false);
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [prefsList, setPrefsList] = useState([]);
  const [showAdd, setShowAdd] = useState(false);
  const [showRemove, setShowRemove] = useState(false);
  const [newPref, setNewPref] = useState("");
  const [loading, setLoading] = useState(true);
  const [warningMessage, setWarningMessage] = useState("");

  // Get user prefs
  const getPrefs = async () => {
    setLoading(true);
    try {
      let response = await api.get("prefs/");
      setPrefsList(response.data);
    }
    catch {
      setWarningMessage("Could not load preferences");
      console.error("Could not load preferences")
    }
    setLoading(false);
    setDisableAdd(false);
  }; 

  useEffect(() => {
      getPrefs();
  }, []);

  useEffect(() => {
    // Focus on the text input when showAdd is true
    if (showAdd) {
      foodItemInput.current.focus();
    }
  }, [showAdd]);

  const validate = async (e) => {
    e.preventDefault();
    setDisableButton(true);
    let response;
    try {
      response = await api.post("users/validate/", {
        code: code,
      });
    }
    catch {
      setDisableButton(false);
      setMessage("Error validating code");
      return;
    }
    setDisableButton(false);
    setMessage(response.data.message)
    if(response.data.is_valid) {
      setVerified(true);
    }
  };

  const resend = async () => {
    setDisableResend(true);
    try {
      await api.post("users/resend/");
    }
    catch {
      setDisableResend(false);
      setMessage("Error sending email. Try again.")
    }
    // Disable email button for 5 seconds
    setTimeout(() => {
      setDisableResend(false);
    }, 5000);
  }; 

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !disableAdd) {
      e.preventDefault();
      addPref();
    }
  };

  const addPref = async () => {
    setDisableAdd(true);
    setWarningMessage("");
    // Guards
    if(newPref.length == 0) {
      setWarningMessage("Cannot be empty");
      setDisableAdd(false);
      return;
    }
    if(newPref.length > 30) {
      setWarningMessage("Must not exceed 30 characters");
      setDisableAdd(false);
      return;
    }
    for(let i = 0; i < prefsList.length; i++) {
      // Case insensitive comparisons
      if(prefsList[i].pref_string.toLowerCase() == newPref.toLowerCase()) {
        setWarningMessage("Already added");
        setDisableAdd(false);
        return;
      }
    }
    // Update user list
    try {
      await api.post("prefs/", {
        pref_string: newPref,
      });
    }
    catch {
      setWarningMessage("Could not add preference");
      console.error("Error adding preference");
      setShowAdd(false);
      setNewPref("");
      setDisableAdd(false);
      return;
    }
    // Update prefs
    getPrefs();
    setShowAdd(false);
    setNewPref("");
  };

  const delPref = async (id) => {
    // Immediately update frontend
    const prevPrefsList = prefsList;
    const newPrefsList = [...prefsList].filter((pref) => pref.id !== id);
    setPrefsList(newPrefsList);
  
    // Update backend too
    try {
      await api.delete(`prefs/${id}`);
    } catch (error) {
      // Revert if unsuccessful
      setPrefsList(prevPrefsList);
      setWarningMessage("Error deleting preference");
      console.error("Could not delete food preference", error);
    }
  };

  const changeAddVis = (state) => {
    setShowAdd(state);
    setWarningMessage("");
  }

  const changeRemoveVis = (state) => {
    setShowRemove(state);
    setWarningMessage("");
  }

  return (
    user && (
      !verified ? 
      <>
        <form onSubmit={(e) => validate(e)}>
          <h3 className="white-font center">Enter verification code sent to {user.email}:</h3>
          <input
            className="field"
            placeholder="Code"
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <p className="warning-text">{message}</p>
          <input className={disableButton ? "styled-button-disabled" : "styled-button"} type="submit" disabled={disableButton} />
        </form>
        <button onClick={resend} className={disableResend ? "styled-button-disabled wide" : "styled-button wide"} disabled={disableResend}>Resend email</button>
      </>
      :
      <div>
        <h4 className="grey-font">
          Every day at 6AM EST, I will run a (case insensitive) 
          scrape of every Yale residential college dining hall menu. 
          You will then receive a personalized email digest detailing 
          which of your specified food items are present in the day's menus.
        </h4>
        <h2 className="white-font">
          Your Food Items:
        </h2>
        {!loading ? 
          <ul>
            {prefsList.map((pref, index) => (
              <li className="white-font list-item-container" key={index}>
                {index + 1}. {pref.pref_string}
                {showRemove &&
                  <button onClick={() => delPref(pref.id)} className="delete-button">x</button>
                }
              </li>
            ))}
            <br />
            <p className="warning-text">{warningMessage}</p>
            {!showAdd && !showRemove ?
            <>
              {/* Cap the list at 50 */}
              {prefsList.length <= 50 && 
                <button onClick={() => changeAddVis(true)} className="styled-button">Add Food</button>
              }
              {prefsList.length > 0 && 
                <button onClick={() => changeRemoveVis(true)} className="styled-button">Remove Food</button>
              }
            </>
            :
            (showAdd ? 
              <div className="new-pref-container">
                <input
                className="field"
                placeholder="New Food Preference"
                type="text"
                value={newPref}
                ref={foodItemInput}
                onKeyDown={handleKeyDown}
                onChange={(e) => setNewPref(e.target.value)}
              />
              <button onClick={addPref} className={disableAdd ? "styled-button-disabled small" : "styled-button small"} disabled={disableAdd}>Save</button>
              <button onClick={() => changeAddVis(false)} className={disableAdd ? "styled-button-disabled small" : "styled-button small"} disabled={disableAdd}>Cancel</button>
            </div>
            :
            <>
              <button onClick={() => changeRemoveVis(false)} className="styled-button small">Done</button>
            </>
            )
            }
          </ul>
        :
          <Loader size={35} />
        }
      </div>
    )
  );
};
