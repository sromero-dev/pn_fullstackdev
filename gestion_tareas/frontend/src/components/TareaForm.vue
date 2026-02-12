<template>
  <form @submit.prevent="guardar">
    <div>
      <label>Familia *</label>
      <select v-model="form.familia" required>
        <option v-for="fam in familias" :key="fam.id" :value="fam.id">
          {{ fam.nombre }}
        </option>
      </select>
    </div>

    <div>
      <label>Título *</label>
      <input v-model="form.titulo" type="text" required />
    </div>

    <div>
      <label>Descripción</label>
      <textarea v-model="form.descripcion" rows="3"></textarea>
    </div>

    <div>
      <label>Estado</label>
      <select v-model="form.estado">
        <option value="pendiente">Pendiente</option>
        <option value="en_progreso">En progreso</option>
        <option value="completada">Completada</option>
      </select>
    </div>

    <div>
      <label>Fecha de vencimiento</label>
      <input v-model="form.fecha_vencimiento" type="date" />
    </div>

    <div class="actions">
      <button type="submit">Guardar</button>
      <button type="button" @click="$emit('cancelar')">Cancelar</button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from "vue";

// Defino las propiedades que necesito recibir para funcionar correctamente
const props = defineProps({
  tarea: { type: Object, default: null },
  familias: { type: Array, required: true },
  esEdicion: { type: Boolean, default: false },
});

// Declaro los eventos que voy a comunicar hacia afuera
const emit = defineEmits(["guardar", "cancelar"]);

// Inicializo mi objeto reactivo que contiene los campos del formulario
const form = ref({
  familia: "",
  titulo: "",
  descripcion: "",
  estado: "pendiente",
  fecha_vencimiento: "",
});

// Observo los cambios en la tarea para rellenar el formulario o limpiarlo
watch(
  () => props.tarea,
  (nueva) => {
    if (nueva) {
      // Si recibo una tarea, cargo sus valores en mi estado local
      form.value = {
        familia: nueva.familia,
        titulo: nueva.titulo,
        descripcion: nueva.descripcion || "",
        estado: nueva.estado,
        fecha_vencimiento: nueva.fecha_vencimiento || "",
      };
    } else {
      // Si no hay tarea, preparo un formulario vacío con valores por defecto
      form.value = {
        familia: props.familias.length ? props.familias[0].id : "",
        titulo: "",
        descripcion: "",
        estado: "pendiente",
        fecha_vencimiento: "",
      };
    }
  },
  { immediate: true }, // Me aseguro de ejecutar esta lógica en cuanto el componente se monta
);

// Función que ejecuto al validar el formulario para enviar los datos al padre
const guardar = () => {
  emit("guardar", form.value);
};
</script>

<style scoped>
/* Aplico estilos básicos para separar los campos visualmente */
form div {
  margin-bottom: 15px;
}
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
/* Aseguro que los inputs ocupen todo el ancho disponible */
input,
select,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
/* Alineo los botones de acción a la derecha */
.actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
</style>
