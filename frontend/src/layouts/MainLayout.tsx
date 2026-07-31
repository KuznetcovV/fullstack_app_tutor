import Sidebar from "./Sidebar";
import { Outlet } from "react-router-dom";
import CreateStudents from "../pages/Students/CreateStudents";
import CreateLessons from "../pages/Lessons/CreateLessons";
import styles from "./Mainlayout.module.css";

export default function MainLayout() {
  return (
    <div className={styles.main}>
      <Sidebar />
      <Outlet />
    </div>
  );
}
