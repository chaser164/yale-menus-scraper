import { api } from "../utilities.jsx";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const ForgotPage = () => {
  const [warningText, setWarningText] = useState("");
  const [userName, setUserName] = useState("");
  const [disableButton, setDisableButton] = useState(false)
  const navigate = useNavigate();

  const sendCode = async (e) => {
    e.preventDefault();
    setWarningText("");
    setDisableButton(true)
    let response;
    try {
        console.log("TODO: send email")
    //   response = await api.post("users/forgot/", {
    //     email: userName,
    //   });
    }
    catch (error) {
      setDisableButton(false)
      console.log(error)
      setWarningText(error.response.data.message);
      return;
    }
    setDisableButton(false)
  };

  return (
    <form onSubmit={(e) => sendCode(e)} autoComplete="on">
      <h3 className="white-font">Enter Your Email</h3>
      <input
        className="field"
        placeholder="Email"
        type="email"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      <p className="warning-text const-height">{warningText}</p>
    <input className={disableButton ? "styled-button-disabled" : "styled-button"} type="submit" disabled={disableButton} />
    </form>
  );
};
