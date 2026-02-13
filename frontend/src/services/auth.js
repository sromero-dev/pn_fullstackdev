import { apiClient } from "./api";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const REDIRECT_URI = `${window.location.origin}/auth/callback`;

const GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";

export default {
  loginGoogle() {
    const params = new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID,
      redirect_uri: REDIRECT_URI,
      response_type: "code",
      scope: "openid email profile",
      access_type: "offline",
      prompt: "consent",
    });
    const url = `${GOOGLE_AUTH_URL}?${params.toString()}`;
    console.log("🚀 Redirigiendo a Google:", url);
    window.location.href = url;
  },

  async handleCallback(code) {
    const response = await apiClient.post("/auth/social/google/callback/", {
      code,
      redirect_uri: REDIRECT_URI,
    });
    return response.data;
  },

  // Obtiene los datos del usuario actual
  async getUser() {
    const response = await apiClient.get("/auth/user/");
    return response.data;
  },

  // Cierra sesión
  async logout() {
    await apiClient.post("/auth/logout/");
  },

  // Refresca el token (si usas refresh tokens)
  async refreshToken() {
    await apiClient.post("/auth/token/refresh/");
  },
};
