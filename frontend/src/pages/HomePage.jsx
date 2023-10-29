import { useContext, useEffect } from "react";
import { userContext } from "../App";

export const HomePage = () => {
  const { user } = useContext(userContext);

  return (
    <div>
      <h1 className="white-font">Welcome {user ? user.email : null}</h1>
    </div>
  );
};
