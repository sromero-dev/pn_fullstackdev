<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Iniciar sesión</h2>
      <button @click="handleLogin" class="google-btn">
        Continuar con Google
      </button>
    </div>
  </div>
</template>

<script setup>
import authService from "../services/auth";

const handleLogin = () => {
  console.log("🟢 handleLogin ejecutado");
  authService.loginGoogle();
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}
.login-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}
.google-btn {
  background: #4285f4;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
}
.google-btn:hover {
  background: #3367d6;
}
</style>
