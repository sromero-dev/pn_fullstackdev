<template>
  <div>
    <h2>Detalle de Tarea</h2>
    <TareaDetalle
      :tarea="tarea"
      @editar="editar"
      @eliminar="eliminar"
      @volver="volver"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import TareaDetalle from "../components/TareaDetalle.vue";
import api from "../services/api";

// Inicializo las herramientas de navegación y obtengo la información de la ruta actual
const route = useRoute();
const router = useRouter();
// Aquí guardaré la tarea una vez que la API me la devuelva
const tarea = ref(null);

// En cuanto el componente se monta en el DOM, disparo la carga de datos
onMounted(async () => {
  try {
    // Extraigo el ID de la URL y llamo a mi servicio de API
    const { data } = await api.getTarea(route.params.id);
    tarea.value = data;
  } catch (error) {
    console.error("Error al cargar detalle:", error);
    // Si la tarea no existe o hay un error, redirijo al usuario al listado por seguridad
    router.push("/tareas");
  }
});

// Navego a la pantalla de edición usando el ID que tengo en la ruta
const editar = () => {
  router.push(`/tareas/${route.params.id}/editar`);
};

// Gestiono el borrado con una confirmación previa para evitar desastres
const eliminar = async () => {
  if (!confirm("¿Eliminar esta tarea?")) return;
  try {
    await api.deleteTarea(route.params.id);
    // Tras borrar con éxito, mando al usuario de vuelta a la lista global
    router.push("/tareas");
  } catch (error) {
    console.error("Error al eliminar:", error);
  }
};

// Una función sencilla para volver atrás sin guardar cambios
const volver = () => {
  router.push("/tareas");
};
</script>
