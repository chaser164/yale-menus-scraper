import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { userContext } from "../App";
import { api } from "../utilities.jsx";

export const RegisterPage = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConf, setPasswordConf] = useState("");
  const { setUser } = useContext(userContext);
  const navigate = useNavigate();


  const signUp = async (e) => {
    e.preventDefault();
    let response = await api.post("users/signup/", {
      email: userName,
      password: password,
    });
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
    <form onSubmit={(e) => signUp(e)}>
      <h3 className="white-font">Sign Up</h3>
      <input
        className="field"
        placeholder="email"
        type="email"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
      />
      <input
        className="field"
        placeholder="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        className="field"
        placeholder="confirm password"
        type="password"
        value={passwordConf}
        onChange={(e) => setPasswordConf(e.target.value)}
      />
      <br />
      <input className="styled-button" type="submit" />
    </form>
  );
};
