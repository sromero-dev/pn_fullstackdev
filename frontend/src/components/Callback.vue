<template>
  <div>Autenticando con Google...</div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import authService from "../services/auth";

const route = useRoute();
const router = useRouter();

onMounted(async () => {
  const code = route.query.code;

  if (!code) {
    console.error("❌ No se recibió código de autorización");
    router.push("/login");
    return;
  }

  try {
    // Intercambiar el código por las cookies JWT
    await authService.handleCallback(code);
    // Pequeña pausa para que las cookies se asienten
    await new Promise((resolve) => setTimeout(resolve, 1000));
    // Verificar que la sesión se ha establecido
    await authService.getUser();
    router.push("/tareas");
  } catch (error) {
    console.error("❌ Error en callback:", error);
    router.push("/login");
  }
});
</script>
