import { api } from "../utilities.jsx";
import { useContext, useState, useEffect } from "react";
import { userContext } from "../App";

export const HomePage = () => {
  const { user, verified, setVerified } = useContext(userContext);
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [prefsList, setPrefsList] = useState(["hi"]);
  const [showAdd, setShowAdd] = useState(false);
  const [showRemove, setShowRemove] = useState(false);
  const [newPref, setNewPref] = useState("");


  // Get user prefs
  const getPrefs = async () => {
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

  const resend = async () => {
    await api.post("users/resend/");
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
          <br />
          <input className="styled-button" type="submit" />
        <p className="white-font">{message}</p>
        </form>
        <button onClick={resend} className="styled-button-wide">Resend email</button>
      </>
      :
      <div>
        <h3 className="white-font">
        Every day at 6AM EST, I will run a (case insensitive) 
        scrape of every Yale residential college dining hall menu. 
        You will then receive a personalized email digest detailing 
        which dining halls contain your specified food items. You will be notified
        about whatever is included in the list below!
        </h3>
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
            <button onClick={() => setShowAdd(true)} className="styled-button">Add Food</button>
            <button onClick={() => setShowRemove(true)} className="styled-button">Remove Food</button>
          </>
          :
          (showAdd ? 
            <div className="new-pref-container">
              <input
              className="field"
              placeholder="New Food Preference"
              type="text"
              value={newPref}
              onChange={(e) => setNewPref(e.target.value)}
            />
            <button onClick={addPref} className="styled-button-small">Save</button>
            <button onClick={() => setShowAdd(false)} className="styled-button-small">Cancel</button>
          </div>
          :
          <>
            <button onClick={() => setShowRemove(false)} className="styled-button-small">Done</button>
          </>
          )
          }
      </ul>
      </div>
    )
  );
};
