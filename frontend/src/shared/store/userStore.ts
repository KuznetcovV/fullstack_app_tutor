import { create } from "zustand";
import { persist } from "zustand/middleware";

import { usersApi } from "../api/users";
import type { User } from "../../entities/user";
import type { Token } from "../../entities/token";

interface UserStore {
  isAuth: boolean;
  token: Token | null;
  registration: (user: User) => Promise<void>;
  authorization: (user: Partial<User>) => Promise<void>;
  logout: () => void;
}

export const useUserStore = create<UserStore>()(
  persist(
    (set) => ({
      isAuth: false,
      token: null,

      registration: async (user) => {
        const { registration } = usersApi;

        try {
          const token = await registration(user);

          set({
            isAuth: true,
            token: token.data,
          });
        } catch (error) {
          set({
            isAuth: false,
            token: null,
          });
        }
      },

      authorization: async (user) => {
        const { authorization } = usersApi;

        try {
          const token = await authorization(user);

          set({
            isAuth: true,
            token: token.data,
          });
        } catch (error) {
          set({
            isAuth: false,
            token: null,
          });
        }
      },

      logout: () => {
        const { logout } = usersApi;
        logout();
        set({
          isAuth: false,
          token: null,
        });
      },
    }),
    {
      name: "user-storage",
    },
  ),
);

export const useUser = () => {
  const { isAuth, token, registration, authorization, logout } = useUserStore();

  return {
    isAuth,
    token,
    registration,
    authorization,
    logout,
  };
};
