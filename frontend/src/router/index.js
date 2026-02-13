import { createRouter, createWebHistory } from "vue-router";
// Importación de los componentes que actúan como "páginas" de la aplicación
import FamiliasView from "../views/FamiliasView.vue";
import TareasView from "../views/TareasView.vue";
import TareaDetalleView from "../views/TareaDetalleView.vue";
import TareaFormView from "../views/TareaFormView.vue";
import LoginView from "../views/LoginView.vue";
import Callback from "../components/Callback.vue";
import { apiClient } from "../services/api";

// Definición de la lista de rutas
const routes = [
  {
    // Ruta raíz: si el usuario no escribe nada tras el dominio, lo redirigimos a /tareas
    path: "/",
    redirect: "/tareas",
  },
  {
    // Ruta para ver el listado de familias de tareas
    path: "/familias",
    name: "Familias",
    component: FamiliasView,
  },
  {
    // Ruta principal para ver el listado de todas las tareas
    path: "/tareas",
    name: "Tareas",
    component: TareasView,
  },
  {
    // Ruta para el formulario de creación de una nueva tarea
    path: "/tareas/nueva",
    name: "NuevaTarea",
    component: TareaFormView,
  },
  {
    // Ruta para editar una tarea específica. El ":id" es un parámetro dinámico
    path: "/tareas/:id/editar",
    name: "EditarTarea",
    component: TareaFormView,
    // props: true permite que el ":id" llegue al componente como una propiedad (prop) de Vue
    props: true,
  },
  {
    // Ruta para ver la información detallada de una tarea concreta
    path: "/tareas/:id",
    name: "TareaDetalle",
    component: TareaDetalleView,
    // También pasamos el ":id" como prop para facilitar la carga de datos
    props: true,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/auth/callback",
    name: "Callback",
    component: Callback,
  },
];

// Creación de la instancia del router
const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const publicPages = ["/login", "/auth/callback"];
  const authRequired = !publicPages.includes(to.path);

  if (authRequired) {
    try {
      await apiClient.get("/auth/user/");
      next();
    } catch {
      next("/login");
    }
  } else {
    next();
  }
});

export default router;
