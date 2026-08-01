import { api } from "./client";
import type { User } from "../../entities/user";

export const usersApi = {
  registration(user_cred: Partial<User>) {
    return api.post("/auth/register", user_cred);
  },
  authorization(user_cred: Partial<User>) {
    return api.post("/auth/login", user_cred);
  },
  logout() {
    return api.post("/auth/logout");
  },
  refreshPairToken() {},
};
