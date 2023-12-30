import { api } from "../utilities.jsx";
import { useState } from "react";
import { ResetPasswordForm } from "../components/ResetPasswordForm.jsx";

export const ForgotPage = () => {
  const [warningText, setWarningText] = useState("");
  const [phone, setPhone] = useState("");
  const [disableButton, setDisableButton] = useState(false);
  const [showReset, setShowReset] = useState(false);

  const initReset = async (e) => {
    e.preventDefault();
    setWarningText("");
    setDisableButton(true)
    let response;
    try {
      response = await api.post("users/init-reset/", {
        phone: phone,
      });
      console.log(response)
      setDisableButton(false);
      setShowReset(true);
    }
    catch (error) {
        setDisableButton(false);
        if(error.response.status == 404) {
            setWarningText("Phone number not found");      
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
        phone: phone,
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
      <h3 className="white-font">Enter Your Phone Number</h3>
      <input
        className="field"
        placeholder="Phone Number"
        type="text"
        value={!showReset ? phone : ""}
        onChange={(e) => setPhone(e.target.value)}
      />
      <p className="warning-text const-height center">{warningText}</p>
      <input className={disableButton ? "styled-button-disabled" : "styled-button"} type="submit" disabled={disableButton} />
    </form>
    :
    <ResetPasswordForm phone={phone} />
  );
};
