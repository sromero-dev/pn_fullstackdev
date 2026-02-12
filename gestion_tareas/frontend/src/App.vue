<template>
  <div id="app">
    <!-- Barra de navegación: solo visible si hay usuario autenticado -->
    <nav v-if="user">
      <div class="nav-links">
        <router-link to="/tareas">Tareas</router-link>
        <template v-if="esAdmin">
          <span class="separator">|</span>
          <router-link to="/familias">Familias</router-link>
        </template>
      </div>

      <span class="user-info">
        {{ user.email }} ({{ user.rol || "usuario" }})
        <button @click="logout" class="logout-btn">Cerrar sesión</button>
      </span>
    </nav>

    <!-- Área principal: centra el contenido vertical y horizontalmente -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import authService from "./services/auth";

const router = useRouter();
const route = useRoute();
const user = ref(null);
const esAdmin = ref(false);

// Función para cargar el usuario autenticado
const fetchUser = async () => {
  try {
    const data = await authService.getUser();
    user.value = data;
    esAdmin.value = data.rol === "admin";
  } catch (error) {
    user.value = null;
    esAdmin.value = false;
  }
};

// Vigila los cambios de ruta para obtener usuario solo en páginas protegidas
watch(
  () => route.path,
  async (newPath) => {
    const publicPages = ["/login", "/auth/callback"];
    const authRequired = !publicPages.includes(newPath);
    if (authRequired) {
      await fetchUser();
    } else {
      user.value = null;
      esAdmin.value = false;
    }
  },
  { immediate: true },
);

const logout = async () => {
  try {
    await authService.logout();
  } catch (e) {
    console.error("Error en logout", e);
  }
  user.value = null;
  esAdmin.value = false;
  window.location.href = "/login";
};
</script>

<style scoped>
/* Contenedor principal: ocupar toda la pantalla y apilar elementos verticalmente */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}

/* Barra de navegación */
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  flex-shrink: 0; /* Evita que se comprima */
}

.nav-links {
  display: flex;
  gap: 10px;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #e9ecef;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 4px 12px;
  border-radius: 16px;
  cursor: pointer;
  font-size: 0.8rem;
}

.logout-btn:hover {
  background: #c82333;
}

.separator {
  color: #6c757d;
}

/* Área principal: ocupa el espacio restante y centra su contenido */
main {
  flex: 1; /* Toma todo el espacio disponible después del nav */
  display: flex;
  align-items: center; /* Centrado vertical */
  justify-content: center; /* Centrado horizontal */
  padding: 20px;
  background: #f1f3f5; /* Opcional: color de fondo suave */
}
</style>
