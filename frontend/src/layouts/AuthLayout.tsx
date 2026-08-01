import { Navigate, Outlet } from "react-router-dom";
import { useUser } from "../shared/store/userStore";

export default function AuthLayout() {
  const { isAuth } = useUser();

  if (!isAuth) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
