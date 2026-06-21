import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

export function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin12345");
  const [tenantCode, setTenantCode] = useState("demo");
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      await login({
        username,
        password,
        tenantCode,
      });
      navigate("/", { replace: true });
    } catch {
      setErrorMessage(
        "No se pudo iniciar sesión. Revisa usuario, contraseña y cliente.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="login-card__brand">
          <div className="login-card__logo">CM</div>
          <div>
            <p className="login-card__eyebrow">CMMS Enterprise</p>
            <h1 className="login-card__title">Iniciar sesión</h1>
          </div>
        </div>

        <p className="login-card__description">
          Accede al sistema de mantenimiento con tu usuario, contraseña y código
          de cliente.
        </p>

        <form className="login-form" onSubmit={handleSubmit}>
          <label className="form-field">
            <span>Usuario</span>
            <input
              value={username}
              autoComplete="username"
              onChange={(event) => setUsername(event.target.value)}
              required
            />
          </label>

          <label className="form-field">
            <span>Contraseña</span>
            <input
              type="password"
              value={password}
              autoComplete="current-password"
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>

          <label className="form-field">
            <span>Código de cliente</span>
            <input
              value={tenantCode}
              onChange={(event) => setTenantCode(event.target.value)}
              required
            />
          </label>

          {errorMessage ? (
            <div className="form-error" role="alert">
              {errorMessage}
            </div>
          ) : null}

          <button
            className="button button--primary login-form__submit"
            disabled={isSubmitting}
            type="submit"
          >
            {isSubmitting ? "Ingresando..." : "Entrar"}
          </button>
        </form>
      </section>
    </main>
  );
}