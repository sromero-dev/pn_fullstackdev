<template>
  <div>
    <h2>Gestión de Familias</h2>
    <button @click="abrirFormulario()">+ Nueva Familia</button>

    <!-- Listado -->
    <FamiliaList
      :familias="familias"
      @editar="abrirFormulario"
      @eliminar="eliminarFamilia"
    />

    <!-- Modal formulario (crear/editar) -->
    <FamiliaForm
      v-if="showForm"
      :familia="familiaSeleccionada"
      :modo="modoFormulario"
      @guardar="guardarFamilia"
      @cancelar="cerrarFormulario"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import FamiliaList from "../components/FamiliaList.vue";
import FamiliaForm from "../components/FamiliaForm.vue";
import api from "../services/api";

const familias = ref([]);
const showForm = ref(false);
const familiaSeleccionada = ref(null);
const modoFormulario = ref("crear"); // 'crear' o 'editar'

// Obtener todas las familias
const cargarFamilias = async () => {
  try {
    const { data } = await api.getFamilias();
    familias.value = data.results || data; // soporta paginación o lista plana
  } catch (error) {
    console.error("Error al cargar familias:", error);
  }
};

// Abrir formulario para crear o editar
const abrirFormulario = (familia = null) => {
  if (familia) {
    familiaSeleccionada.value = { ...familia };
    modoFormulario.value = "editar";
  } else {
    familiaSeleccionada.value = null;
    modoFormulario.value = "crear";
  }
  showForm.value = true;
};

// Guardar (crear o actualizar)
const guardarFamilia = async (datos) => {
  try {
    if (modoFormulario.value === "crear") {
      await api.createFamilia(datos);
    } else {
      await api.updateFamilia(familiaSeleccionada.value.id, datos);
    }
    await cargarFamilias();
    cerrarFormulario();
  } catch (error) {
    console.error("Error al guardar familia:", error);
    alert("Error al guardar. Verifique los datos.");
  }
};

// Eliminar familia
const eliminarFamilia = async (id) => {
  if (
    !confirm(
      "¿Eliminar esta familia? Se eliminarán también las tareas asociadas.",
    )
  )
    return;
  try {
    await api.deleteFamilia(id);
    await cargarFamilias();
  } catch (error) {
    console.error("Error al eliminar:", error);
    alert("No se puede eliminar porque tiene tareas asociadas.");
  }
};

// Cerrar formulario
const cerrarFormulario = () => {
  showForm.value = false;
  familiaSeleccionada.value = null;
};

onMounted(cargarFamilias);
</script>
