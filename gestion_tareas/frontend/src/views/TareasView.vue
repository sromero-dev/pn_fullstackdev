<template>
  <div>
    <h2>Gestión de Tareas</h2>
    <router-link to="/tareas/nueva">+ Nueva Tarea</router-link>

    <div class="filters">
      <select v-model="filtroEstado">
        <option value="">Todos los estados</option>
        <option value="pendiente">Pendiente</option>
        <option value="en_progreso">En progreso</option>
        <option value="completada">Completada</option>
      </select>

      <label>
        <input type="checkbox" v-model="filtroVencidas" />
        Solo vencidas
      </label>

      <select v-model="ordenarPor">
        <option value="fecha_creacion">Fecha creación</option>
        <option value="fecha_vencimiento">Fecha vencimiento</option>
        <option value="estado">Estado</option>
      </select>

      <button @click="aplicarFiltros">Aplicar</button>
      <button @click="limpiarFiltros">Limpiar</button>
    </div>

    <TareaList
      :tareas="tareas"
      @ver-detalle="verDetalle"
      @editar="editarTarea"
      @eliminar="eliminarTarea"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import TareaList from "../components/TareaList.vue";
import api from "../services/api";

const router = useRouter();
const tareas = ref([]);

// Mantengo el estado de los filtros de forma reactiva
const filtroEstado = ref("");
const filtroVencidas = ref(false);
const ordenarPor = ref("fecha_creacion");

// Preparo y ejecuto la llamada a la API con los parámetros actuales
const cargarTareas = async () => {
  const params = {};
  // Solo añado los parámetros al objeto si tienen un valor seleccionado
  if (filtroEstado.value) params.estado = filtroEstado.value;
  if (filtroVencidas.value) params.vencidas = true;
  if (ordenarPor.value) params.ordering = ordenarPor.value;

  try {
    const { data } = await api.getTareas(params);
    // Gestiono la respuesta tanto si viene paginada como si es un array simple
    tareas.value = data.results || data;
  } catch (error) {
    console.error("Error al cargar tareas:", error);
  }
};

// Función para disparar la recarga tras cambiar filtros manualmente
const aplicarFiltros = () => {
  cargarTareas();
};

// Reseteo todos los filtros a sus valores por defecto y recargo la lista
const limpiarFiltros = () => {
  filtroEstado.value = "";
  filtroVencidas.value = false;
  ordenarPor.value = "fecha_creacion";
  cargarTareas();
};

// Navegación programática hacia el detalle o edición
const verDetalle = (id) => {
  router.push(`/tareas/${id}`);
};

const editarTarea = (id) => {
  router.push(`/tareas/${id}/editar`);
};

// Borro la tarea y, si tiene éxito, refresco la lista para mostrar los cambios
const eliminarTarea = async (id) => {
  if (!confirm("¿Eliminar esta tarea permanentemente?")) return;
  try {
    await api.deleteTarea(id);
    await cargarTareas();
  } catch (error) {
    console.error("Error al eliminar tarea:", error);
  }
};

// Cargo los datos por primera vez en cuanto el componente está listo
onMounted(cargarTareas);
</script>

<style scoped>
/* Organizo los filtros en una línea flexible y espaciada */
.filters {
  margin: 20px 0;
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}
</style>
