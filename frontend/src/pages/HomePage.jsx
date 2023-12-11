import { api } from "../utilities.jsx";
import { useContext, useState } from "react";
import { userContext } from "../App";

export const HomePage = () => {
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const { user, verified, setVerified } = useContext(userContext);

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

  const resend = async (e) => {
    e.preventDefault();
    await api.post("users/resend/");
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
        <h3 className="white-font">Your Food Items:</h3>
      </div>
    )
  );
};
