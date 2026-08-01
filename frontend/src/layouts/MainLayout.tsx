import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Loader from "../shared/ui/Loader";
import { useLoader } from "../shared/store/loader";

import styles from "./MainLayout.module.css";

export default function MainLayout() {
  const { loading } = useLoader();

  return (
    <div className={styles.main}>
      {loading && <Loader />}

      <Sidebar />

      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}
