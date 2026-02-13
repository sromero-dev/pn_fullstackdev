<template>
  <div>
    <h2>{{ esEdicion ? "Editar Tarea" : "Nueva Tarea" }}</h2>

    <TareaForm
      :tarea="tareaActual"
      :familias="familias"
      :es-edicion="esEdicion"
      @guardar="guardarTarea"
      @cancelar="cancelar"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import TareaForm from "../components/TareaForm.vue";
import api from "../services/api";

const route = useRoute();
const router = useRouter();

// Defino mis estados reactivos para la tarea y el listado de familias
const tareaActual = ref(null);
const familias = ref([]);

// Determino si estoy en modo edición basándome en el nombre de la ruta
const esEdicion = computed(() => route.name === "EditarTarea");

// Traigo las familias de la API para que el selector del formulario tenga opciones
const cargarFamilias = async () => {
  try {
    const { data } = await api.getFamilias();
    // Manejo la respuesta por si viene en un objeto 'results' o directamente el array
    familias.value = data.results || data;
  } catch (error) {
    console.error("Error al cargar familias:", error);
  }
};

// Si detecto que es una edición, busco los datos de la tarea específica
const cargarTarea = async () => {
  if (esEdicion.value) {
    try {
      const { data } = await api.getTarea(route.params.id);
      tareaActual.value = data;
    } catch (error) {
      console.error("Error al cargar tarea:", error);
      // Si falla la carga, devuelvo al usuario al listado para evitar errores
      router.push("/tareas");
    }
  }
};

// Proceso el guardado decidiendo si debo llamar a 'update' o a 'create'
const guardarTarea = async (datos) => {
  try {
    if (esEdicion.value) {
      await api.updateTarea(route.params.id, datos);
    } else {
      await api.createTarea(datos);
    }
    // Si todo sale bien, redirijo al listado principal
    router.push("/tareas");
  } catch (error) {
    console.error("Error al guardar tarea:", error);
    alert("Error al guardar. Verifique los datos.");
  }
};

// Simplemente devuelvo al usuario a la lista si decide no seguir
const cancelar = () => {
  router.push("/tareas");
};

// Al montar el componente, ejecuto mis funciones de carga de forma secuencial
onMounted(async () => {
  await cargarFamilias();
  await cargarTarea();
});
</script>
