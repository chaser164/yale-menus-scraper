import { api } from "../utilities.jsx";
import { useState, useContext } from "react";
import { userContext } from "../App";
import { useNavigate } from "react-router-dom";

export const LoginPage = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const { setUser, setVerified } = useContext(userContext);
  const navigate = useNavigate();

  const logIn = async (e) => {
    e.preventDefault();
    let response = await api.post("users/login/", {
      email: userName,
      password: password,
    });
    let token = response.data.token;
    let user = response.data.user;
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
    setVerified(user.is_verified);
    setUser(user);
    navigate("/");
  };

  return (
    <form onSubmit={(e) => logIn(e)} autoComplete="on">
      <h3 className="white-font">Log In</h3>
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
      <br />
      <input className="styled-button" type="submit" />
    </form>
  );
};
