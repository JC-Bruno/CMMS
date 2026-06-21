import { AppRouter } from "./app/router/AppRouter";
import { AuthProvider } from "./modules/auth/context/AuthContext";

export default function App() {
  return (
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  );
}