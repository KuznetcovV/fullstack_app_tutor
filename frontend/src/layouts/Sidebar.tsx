import { NavLink } from "react-router-dom";
import { useState } from "react";
import styles from "./Sidebar.module.css";

interface Link {
  path: string;
  icon: string;
  label: string;
  end?: boolean;
  child?: Link[];
}

export default function Sidebar() {
  const [expanded, setExpanded] = useState(false);
  const [openedMenu, setOpenedMenu] = useState<string | null>("students");

  const links: Link[] = [
    {
      path: "/",
      icon: "🏠",
      label: "Главная",
      end: true,
    },
    {
      path: "/students",
      icon: "👨‍🎓",
      label: "Ученики",
      child: [
        {
          path: "/students",
          icon: "📋",
          label: "Список",
          end: true,
        },
        {
          path: "/students/create",
          icon: "➕",
          label: "Создать",
        },
      ],
    },
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
          <div key={link.path}>
            {link.child ? (
              <>
                <button
                  className={`${styles.item} ${
                    openedMenu === link.path ? styles.open : ""
                  }`}
                  onClick={() =>
                    setOpenedMenu((prev) =>
                      prev === link.path ? null : link.path,
                    )
                  }
                >
                  <span>{link.icon}</span>

                  {expanded && (
                    <>
                      <span>{link.label}</span>

                      <span className={styles.arrow}>
                        {openedMenu === link.path ? "▼" : "▶"}
                      </span>
                    </>
                  )}
                </button>

                {expanded && openedMenu === link.path && (
                  <div className={styles.children}>
                    {link.child.map((child) => (
                      <NavLink
                        key={child.path}
                        to={child.path}
                        end={child.end}
                        className={({ isActive }) =>
                          `${styles.child} ${isActive ? styles.active : ""}`
                        }
                      >
                        <span>{child.icon}</span>
                        <span>{child.label}</span>
                      </NavLink>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <NavLink
                to={link.path}
                end={link.end}
                className={({ isActive }) =>
                  `${styles.item} ${isActive ? styles.active : ""}`
                }
              >
                <span>{link.icon}</span>

                {expanded && <span>{link.label}</span>}
              </NavLink>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
