<template>
  <div class="modal-overlay" @click.self="$emit('cancelar')">
    <div class="modal-content">
      <h3>{{ modo === "crear" ? "Nueva Familia" : "Editar Familia" }}</h3>
      <form @submit.prevent="guardar">
        <div>
          <label>Nombre:</label>
          <input v-model="form.nombre" type="text" required />
        </div>
        <div class="actions">
          <button type="submit">Guardar</button>
          <button type="button" @click="$emit('cancelar')">Cancelar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  familia: { type: Object, default: null },
  modo: { type: String, required: true },
});
const emit = defineEmits(["guardar", "cancelar"]);

const form = ref({
  nombre: "",
});

// Si estamos en modo editar, cargar los datos
watch(
  () => props.familia,
  (nueva) => {
    if (nueva) {
      form.value = { ...nueva };
    } else {
      form.value = { nombre: "" };
    }
  },
  { immediate: true },
);

const guardar = () => {
  emit("guardar", { nombre: form.value.nombre });
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
}
.actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
</style>
