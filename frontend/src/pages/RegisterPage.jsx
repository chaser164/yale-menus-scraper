import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { userContext } from "../App";
import { api } from "../utilities.jsx";
import PhoneInput from "react-phone-input-2";
import "react-phone-input-2/lib/style.css";

export const RegisterPage = () => {
  const { setUser } = useContext(userContext);
  const [disableButton, setDisableButton] = useState(false);
  const [warningText, setWarningText] = useState("");
  const [userName, setUserName] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");
  const navigate = useNavigate();


  const signUp = async (e) => {
    e.preventDefault();
    setWarningText("");
    // Guards
    if(userName.length == 0 || phone.length == 0 || password.length == 0 || passwordConf.lengh == 0) {
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
      response = await api.post("users/signup/", {
        username: userName,
        phone: phone,
        password: password,
      });
    }
    catch (error) {
      setDisableButton(false);
      setWarningText(error.response.data.message);
      return;
    }
    setDisableButton(false);
    let user = response.data.user;
    setUser(user);
    navigate("/");
  };

  return (
    <form onSubmit={(e) => signUp(e)} autoComplete="on">
      <h3 className="white-font label">Sign Up</h3>
      <input
        className="field"
        placeholder="Username"
        type="text"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      <div>
        <PhoneInput
          containerClass="phone-input"
          country={'us'}
          onEnterKeyPress={(e) => signUp(e)}
          onChange={(phone) => setPhone(phone)}
        />
      </div>
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
      <p className="warning-text center">{warningText}</p>
      <input className={disableButton ? "styled-button-disabled" : "styled-button"} type="submit" disabled={disableButton} />
    </form>
  );
};
