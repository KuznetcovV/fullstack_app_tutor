import { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Loader from "../shared/ui/Loader";
import { useLoader } from "../shared/store/loaderStore";

import styles from "./MainLayout.module.css";

export default function MainLayout() {
  const { loading } = useLoader();
  const [expanded, setExpanded] = useState(false);
  return (
    <div className={styles.main}>
      {loading && <Loader />}

      <Sidebar expanded={expanded} setExpanded={setExpanded} />

      <main className={`${styles.main} ${expanded ? styles.expanded : ""}`}>
        <Outlet />
      </main>
    </div>
  );
}
