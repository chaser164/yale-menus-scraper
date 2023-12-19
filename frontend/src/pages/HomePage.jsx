import { api } from "../utilities.jsx";
import { useContext, useState, useEffect, useRef } from "react";
import { userContext } from "../App";

export const HomePage = () => {
  const { user, verified, setVerified } = useContext(userContext);
  const foodItemInput = useRef(null);
  const [disableButton, setDisableButton] = useState(false);
  const [disableResend, setDisableResend] = useState(false);
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [prefsList, setPrefsList] = useState([]);
  const [showAdd, setShowAdd] = useState(false);
  const [showRemove, setShowRemove] = useState(false);
  const [newPref, setNewPref] = useState("");


  // Get user prefs
  const getPrefs = async () => {
    let response = await api.get("prefs/");
    setPrefsList(response.data);
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
    if (e.key === "Enter") {
      e.preventDefault();
      addPref();
    }
  };

  const addPref = async () => {
    // Update user list
    await api.post("prefs/", {
      pref_string: newPref,
    });
    // Update prefs
    getPrefs();
    setShowAdd(false);
    setNewPref("");
  };

  const delPref = async (id) => {
    // Update user list
    await api.delete(`prefs/${id}`);
    // Update prefs
    getPrefs();
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
        <ul>
          {prefsList.map((pref, index) => (
            <li className="white-font" key={index}>
              {index + 1}. {pref.pref_string}
              {showRemove &&
                <button onClick={() => delPref(pref.id)} className="delete-button">x</button>
              }
            </li>
          ))}
          <br />
          {!showAdd && !showRemove ?
          <>
            {/* Cap the list at 50 */}
            {prefsList.length <= 50 && 
              <button onClick={() => setShowAdd(true)} className="styled-button">Add Food</button>
            }
            {prefsList.length > 0 && 
              <button onClick={() => setShowRemove(true)} className="styled-button">Remove Food</button>
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
            <button onClick={addPref} className="styled-button small">Save</button>
            <button onClick={() => setShowAdd(false)} className="styled-button small">Cancel</button>
          </div>
          :
          <>
            <button onClick={() => setShowRemove(false)} className="styled-button small">Done</button>
          </>
          )
          }
      </ul>
      </div>
    )
  );
};
