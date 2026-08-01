import { useState } from "react";
import { Navigate, NavLink } from "react-router-dom";

import Input from "../../shared/ui/input";
import Button from "../../shared/ui/button";
import { useUser } from "../../shared/store/userStore";
import type { User } from "../../entities/user";
import styles from "./Authorization.module.css";

export default function Authorization() {
  const [user, setUser] = useState<Partial<User>>({
    login: "",
    password: "",
  });
  const { isAuth, authorization } = useUser();

  if (isAuth) {
    return <Navigate to="/" replace />;
  }
  return (
    <div className={styles.main}>
      <div className={styles.form}>
        <h1 className={styles.title}>Авторизация</h1>

        <Input
          label="Логин"
          value={user.login || ""}
          onChange={(value) => setUser({ ...user, login: String(value) })}
        />

        <Input
          label="Пароль"
          value={user.password || ""}
          type="password"
          onChange={(value) => setUser({ ...user, password: String(value) })}
        />

        <Button
          label="Авторизоваться"
          onClick={() => {
            authorization(user);
          }}
        />
        <p className={styles.switch}>
          <NavLink to="/registration">Нет аккаунта? Зарегистрироваться</NavLink>
        </p>
      </div>
    </div>
  );
}
