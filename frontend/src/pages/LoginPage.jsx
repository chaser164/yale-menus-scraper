import { api } from "../utilities.jsx";
import { useState, useEffect, useContext } from "react";
import { userContext } from "../App";
import { useNavigate, Link } from "react-router-dom";

export const LoginPage = () => {
  const { setUser, setVerified, passwordChanged, setPasswordChanged } = useContext(userContext);
  const [warningText, setWarningText] = useState("");
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [disableButton, setDisableButton] = useState(false)
  const navigate = useNavigate();

  useEffect(() => {
    if(passwordChanged) {
      setPasswordChanged(false);
      alert("Password updated successfully!");
    }
}, []);

  const logIn = async (e) => {
    e.preventDefault();
    setWarningText("");
    setDisableButton(true)
    let response;
    try {
      response = await api.post("users/login/", {
        username: userName,
        password: password,
      });
    }
    catch (error) {
      setDisableButton(false)
      console.log(error)
      setWarningText(error.response.data.message);
      return;
    }
    setDisableButton(false)
    let user = response.data.user;
    setVerified(user.is_verified);
    setUser(user);
    navigate("/");
  };

  return (
    <form onSubmit={(e) => logIn(e)} autoComplete="on">
      <h3 className="white-font label">Log In</h3>
      <input
        className="field"
        placeholder="Username"
        type="text"
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
      <p className="warning-text const-height center">{warningText}</p>
    <input className={disableButton ? "styled-button-disabled" : "styled-button"} type="submit" disabled={disableButton} />
    <br />
    <Link className="forgot-link" to="/forgot">Forgot Password?</Link>
    </form>
  );
};
