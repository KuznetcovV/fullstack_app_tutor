import type { Token } from "./token";

export interface User {
  login: string;
  email: string;
  password: string;
  confirmPassword: string;
  token?: Token;
}
