import { useState, useEffect, useRef } from "react";
import "./App.css";
import { Link, Outlet, useNavigate, useLocation } from "react-router-dom";
import { createContext } from "react";
import { api } from "./utilities.jsx";

export const userContext = createContext();

function App() {

  const location = useLocation();
  const lastVisited = useRef();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [hasLoaded, setHasLoaded] = useState(false);

  const whoAmI = async () => {
    // Check if a token is stored in the localStorage
    let token = localStorage.getItem("token");
    if (token) {
      // If the token exists, set it in the API headers for authentication
      api.defaults.headers.common["Authorization"] = `Token ${token}`;
      // Fetch the user data from the server using the API
      let response = await api.get("users/me");
      // Check if the response contains the user data (email field exists)
      if (response.data.email) {
        // Set the user data in the context or state (assuming `setUser` is a state update function)
        setUser(response.data);
        // If the user is authenticated and there is a stored lastVisited page,
        // navigate to the lastVisited page; otherwise, navigate to the default homepage "/home"
        if (lastVisited.current) {
          navigate(lastVisited.current);
        } else {
          navigate("/");
        }
      }
    } else {
      // If no token is found, navigate to the login page
      navigate("/login");
    }
    setHasLoaded(true)
  };

  // This useEffect block runs once when the component mounts (due to the empty dependency array [])
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
    let response = await api.post("users/logout/");
    if (response.status === 204) {
      // Remove the token from secure storage (e.g., localStorage)
      localStorage.removeItem("token");
      delete api.defaults.headers.common["Authorization"];
      // set the user using with useContext to allow all other pages that need user information
      setUser(null);
      navigate("/login");
    }
  };


  return (
    (hasLoaded && 
    <div id="app">
      <div className="navbar-container">
        <div className="white-font title">Yale Menus Scraper</div>
        <br />
        <header>
          <nav>
            {user ? 
              <>
                <button className="styled-button" onClick={logOut}>Log out</button>
              </> :
              <>
                <Link to="/signup">Sign Up</Link>
                <Link to="/login">Log In</Link>
              </>
            }
          </nav>
        </header>
      </div>
      <userContext.Provider value={{ user, setUser }}>
        <Outlet />
      </userContext.Provider>
    </div>)
  );
}

export default App;
