import { useState, useEffect, useRef } from "react";
import "./App.css";
import { Link, Outlet, useNavigate, useLocation, json } from "react-router-dom";
import { createContext } from "react";
import { api } from "./utilities.jsx";

export const userContext = createContext();

function App() {

  const location = useLocation();
  const lastVisited = useRef();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [hasLoaded, setHasLoaded] = useState(false);
  const [verified, setVerified] = useState(false);
  const [passwordChanged, setPasswordChanged] = useState(false);
  const [logoutLoading, setLogoutLoading] = useState(false);

  const whoAmI = async () => {
    // If the token exists, set it in the API headers for authentication
    let response;
    try {
      response = await api.get("users/me/");
      setUser(response.data);
      setVerified(response.data.is_verified);
      // Navigate to logged-in page
      if (lastVisited.current) {
        navigate(lastVisited.current);
      } else {
        navigate("/");
      }
    }
    catch {
      navigate("/login");
    }
    setHasLoaded(true)
  };

  // This useEffect block runs once when the component mounts (due to the empty dependency array [])
  // Also runs whenever verified is updated
  // It calls the whoAmI function to check the user's authentication status and perform redirection accordingly
  useEffect(() => {
    whoAmI();
  }, []);

  // This useEffect block runs whenever the location (pathname) changes
  // It updates the lastVisited ref with the current location pathname
  // This allows the whoAmI function to access the lastVisited page for redirection if needed
  useEffect(() => {
    if (!user) {
      // If the user is not authenticated, update the lastVisited ref with the current location pathname
      lastVisited.current = location.pathname;
    }
  }, [location]);
  
  const logOut = async () => {
    setLogoutLoading(true);
    let response;
    try {
      response = await api.post("users/logout/");
    }
    catch {
      setLogoutLoading(false);
      console.log("could not log out");
      return;
    }
    if (response.status === 204) {
      setUser(null);
      setVerified(false);
      navigate("/login");
    }
  };

  const goHome = () => {
    // Go home when logged in
    if(user) {
      navigate("/");
    }
  }

  return (
    (hasLoaded && 
    <div id="app">
      <div className="navbar-container">
        <div className="white-font title" onClick={goHome}>Yale Menus Scraper</div>
        <br />
        <header>
          <nav>
            {user ? 
              <div className="navbar-aligner">
                <button className="settings-button" onClick={() => navigate("/settings")}>⚙</button>
                <button className={!logoutLoading ? "styled-button" : "styled-button-disabled"} disabled={logoutLoading} onClick={logOut}>Log Out</button>
              </div> :
              <>
                <Link className="nav-links" to="/signup">Sign Up</Link>
                <Link className="nav-links" to="/login">Log In</Link>
              </>
            }
          </nav>
        </header>
      </div>
      <userContext.Provider 
        value={{ 
          user, 
          setUser, 
          verified, 
          setVerified, 
          passwordChanged, 
          setPasswordChanged,
          logoutLoading,
          setLogoutLoading }}>
        <Outlet />
      </userContext.Provider>
    </div>)
  );
}

export default App;
