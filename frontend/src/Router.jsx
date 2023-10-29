import { createBrowserRouter } from "react-router-dom";
import { HomePage } from "./pages/HomePage"
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
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
        ],
    },
]);

export default router;