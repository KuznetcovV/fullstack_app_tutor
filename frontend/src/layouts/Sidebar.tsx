import { NavLink } from "react-router-dom";
import { useState } from "react";
import styles from "./Sidebar.module.css";

export default function Sidebar() {
  const [expanded, setExpanded] = useState(false);

  const links = [
    {
      path: "/",
      icon: "🏠",
      label: "Главная",
    },
    {
      path: "students/create",
      icon: "👨‍🎓",
      label: "Ученики",
    },
    // {
    //   path: "/lessons",
    //   icon: "📅",
    //   label: "Занятия",
    // },
    // {
    //   path: "/subscriptions",
    //   icon: "💳",
    //   label: "Абонементы",
    // },
  ];

  return (
    <aside className={`${styles.sidebar} ${expanded ? styles.expanded : ""}`}>
      <button
        className={styles.logo}
        onClick={() => setExpanded((prev) => !prev)}
      >
        ☰
      </button>

      <nav className={styles.menu}>
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            className={({ isActive }) =>
              `${styles.item} ${isActive ? styles.active : ""}`
            }
          >
            <span>{link.icon}</span>

            {expanded && <span>{link.label}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
