import { createBrowserRouter } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import CreateStudents from "./pages/Students/CreateStudents";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <></>,
      },
      {
        path: "students/create",
        element: <CreateStudents />,
      },
    ],
  },
]);
