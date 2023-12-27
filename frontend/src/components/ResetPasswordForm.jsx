import { api } from "../utilities.jsx";
import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { userContext } from "../App.jsx";

export const ResetPasswordForm = (props) => {
  const { setUser, setVerified, setPasswordChanged } = useContext(userContext);
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");
  const [warningText, setWarningText] = useState("");
  const [disableButton, setDisableButton] = useState(false);
  const [disableResend, setDisableResend] = useState(false);
  const [clock, setClock] = useState(30);
  const navigate = useNavigate();

  const resetPassword = async (e) => {
    e.preventDefault();
    setWarningText("");
    // Guards
    if(code.length == 0 || password.length == 0 || passwordConf.lengh == 0) {
        setWarningText("All fields must be populated");
        return;
    }
    if(password != passwordConf) {
    setWarningText("Passwords must match");
    return;
    }
    if(password.length < 8) {
    setWarningText("Password must be at least 8 characters");
    return;
    }
    setDisableButton(true);
    let response;
    try {
      response = await api.post("users/validate-reset/", {
        email: props.email,
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
    // Login if valid
    const logIn = async () => {
        if(response.data.is_valid) {
            setPasswordChanged(true);
            let response;
            try {
              response = await api.post("users/login/", {
                email: props.email,
                password: password,
              });
            }
            catch (error) {
                console.error("Could not log in");
                navigate("/login");
                return;
            }
            let user = response.data.user;
            setVerified(user.is_verified);
            setUser(user);
            navigate("/");
        }
        else {
            setWarningText(response.data.message)
        }
    }
    logIn();
  }

  const timer = (secs) => {
    if(secs == 0) {
        setDisableResend(false);
        setClock(30);
    }
    else {
        setTimeout(() => {
            setClock(secs - 1);
            timer(secs - 1);
        }, 1000);
    }
  }

  const resend = async () => {
    setDisableResend(true);
    try {
        let response = await api.post("users/init-reset/", {
            email: props.email,
        });
    }
    catch {
      setDisableResend(false);
      setWarningText("Error sending email, Try again");
      return;
    }
    // Disable email button for 30 seconds
    timer(30);
  }; 

  return (
    <>
        <form onSubmit={(e) => resetPassword(e)} autoComplete="on">
            <h3 className="white-font center">Enter verification code sent to {props.email}</h3>
            <input
            className="field"
            placeholder="Code"
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            />
            <br />
            <input
            className="field"
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
            <input
            className="field"
            placeholder="Confirm Password"
            type="password"
            value={passwordConf}
            onChange={(e) => setPasswordConf(e.target.value)}
            />
            <p className="warning-text">{warningText}</p>
            <input className={disableButton ? "styled-button-disabled" : "styled-button"} type="submit" disabled={disableButton} />
        </form>
        <button onClick={resend} className={disableResend ? "styled-button-disabled wide" : "styled-button wide"} disabled={disableResend}>Resend email {disableResend && `(${clock})`}</button>
    </>
  );
};
