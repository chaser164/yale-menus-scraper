import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { userContext } from "../App";
import { api } from "../utilities.jsx";

export const RegisterPage = () => {
  const [warningText, setWarningText] = useState("");
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");
  const { setUser } = useContext(userContext);
  const navigate = useNavigate();


  const signUp = async (e) => {
    setWarningText("");
    e.preventDefault();
    // Guards
    if(userName.length == 0 || password.length == 0 || passwordConf.lengh == 0) {
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
    let response;
    try {
      response = await api.post("users/signup/", {
        email: userName,
        password: password,
      });
    }
    catch (error) {
      setWarningText(error.response.data.message);
      return;
    }
    console.log(response.data)
    let user = response.data.user;
    let token = response.data.token;
    // Store the token securely (e.g., in localStorage or HttpOnly cookies)
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
    // set the user using with useContext to allow all other pages that need user information
    setUser(user);
    navigate("/");
  };

  return (
    <form onSubmit={(e) => signUp(e)} autoComplete="on">
      <h3 className="white-font">Sign Up</h3>
      <input
        className="field"
        placeholder="Email"
        type="email"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
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
      <br />
      <input className="styled-button" type="submit" />
    </form>
  );
};
