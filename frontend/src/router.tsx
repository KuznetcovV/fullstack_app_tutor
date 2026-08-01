import { createBrowserRouter } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import CreateStudents from "./pages/Students/CreateStudents";
import Students from "./pages/Students/Students";
import UpdateStudents from "./pages/Students/UpdateStudents";

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
        path: "students/",
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
]);
