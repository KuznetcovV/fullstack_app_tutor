import { useState } from "react";
import { NavLink, Navigate } from "react-router-dom";

import Input from "../../shared/ui/input";
import Button from "../../shared/ui/button";
import { useUser } from "../../shared/store/userStore";
import type { User } from "../../entities/user";
import styles from "./Registration.module.css";

export default function Registration() {
  const [user, setUser] = useState<User>({
    login: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const { isAuth, registration } = useUser();

  if (isAuth) {
    return <Navigate to="/" replace />;
  }
  return (
    <div className={styles.main}>
      <div className={styles.form}>
        <h1 className={styles.title}>Регистрация</h1>

        <Input
          label="Логин"
          value={user.login || ""}
          onChange={(value) => setUser({ ...user, login: String(value) })}
        />

        <Input
          label="Почта"
          value={user.email || ""}
          type="email"
          onChange={(value) => setUser({ ...user, email: String(value) })}
        />

        <Input
          label="Пароль"
          value={user.password || ""}
          type="password"
          onChange={(value) => setUser({ ...user, password: String(value) })}
        />

        <Input
          label="Подтвердить пароль"
          value={user.confirmPassword || ""}
          type="password"
          onChange={(value) =>
            setUser({ ...user, confirmPassword: String(value) })
          }
        />
        <Button
          label="Зарегистрироваться"
          onClick={() => {
            registration(user);
          }}
        />
        <p className={styles.switch}>
          <NavLink to="/login">Уже есть аккаунт? Войти</NavLink>
        </p>
      </div>
    </div>
  );
}
