import { api } from "../utilities.jsx";
import { useState } from "react";
import { ResetPasswordForm } from "../components/ResetPasswordForm.jsx";

export const ForgotPage = () => {
  const [warningText, setWarningText] = useState("");
  const [userName, setUserName] = useState("");
  const [disableButton, setDisableButton] = useState(false);
  const [showReset, setShowReset] = useState(false);

  const initReset = async (e) => {
    e.preventDefault();
    setWarningText("");
    setDisableButton(true)
    let response;
    try {
      response = await api.post("users/init-reset/", {
        email: userName,
      });
      setDisableButton(false);
      setShowReset(true);
    }
    catch (error) {
        setDisableButton(false);
        if(error.response.status == 404) {
            setWarningText("Email not found");      
        }
        else if(error.response.status == 400) {
            setWarningText(error.response.data.message)
      }
      return;
    }
    setDisableButton(false);
  };

  const resetPassword = async (e) => {
    e.preventDefault();
    setDisableButton(true);
    let response;
    try {
      response = await api.post("users/validate-reset/", {
        email: userName,
        code: code,
        password: password,
      });
      
    }
    catch {
      setDisableButton(false);
      setWarningText("Error validating code");
      return;
    }
    setDisableButton(false);
    setWarningText(response.data.message)
  }

  return (
    !showReset ? 
    <form className="invisible" onSubmit={(e) => initReset(e)} autoComplete="on">
      <h3 className="white-font">Enter Your Email</h3>
      <input
        className="field"
        placeholder="Email"
        type="email"
        value={!showReset ? userName : ""}
        onChange={(e) => setUserName(e.target.value)}
      />
      <p className="warning-text const-height center">{warningText}</p>
      <input className={disableButton ? "styled-button-disabled" : "styled-button"} type="submit" disabled={disableButton} />
    </form>
    :
    <ResetPasswordForm email={userName} />
  );
};
