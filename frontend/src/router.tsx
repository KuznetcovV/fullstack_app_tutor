import { createBrowserRouter } from "react-router-dom";

import AuthLayout from "./layouts/AuthLayout";
import MainLayout from "./layouts/MainLayout";

import Registration from "./pages/Auth/Registration";
import Authorization from "./pages/Auth/Authorization";
import Students from "./pages/Students/Students";
import CreateStudents from "./pages/Students/CreateStudents";
import UpdateStudents from "./pages/Students/UpdateStudents";

export const router = createBrowserRouter([
  {
    element: <AuthLayout />,
    children: [
      {
        path: "/",
        element: <MainLayout />,
        children: [
          {
            index: true,
            element: <Students />,
          },
          {
            path: "students",
            element: <Students />,
          },
          {
            path: "students/create",
            element: <CreateStudents />,
          },
          {
            path: "students/:id/edit",
            element: <UpdateStudents />,
          },
        ],
      },
    ],
  },
  {
    path: "/registration",
    element: <Registration />,
  },
  {
    path: "/login",
    element: <Authorization />,
  },
]);
