import { createBrowserRouter } from "react-router-dom";
import { HomePage } from "./pages/HomePage"
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { SettingsPage } from "./pages/SettingsPage";
import { ForgotPage } from "./pages/ForgotPage";
import App from "./App";


const router = createBrowserRouter([
    {
        path: "/",
        element: < App />,
        children: [
            {
                index: true,
                element: <HomePage />,
            },
            {
                path: "login",
                element: <LoginPage/>,
            },
            {
                path: "signup",
                element:<RegisterPage/>,
            },
            {
                path: "settings",
                element:<SettingsPage/>
            },
            {
                path: "forgot",
                element:<ForgotPage/>
            }
        ],
    },
]);

export default router;