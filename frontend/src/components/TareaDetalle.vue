<template>
  <div v-if="tarea">
    <p><strong>ID:</strong> {{ tarea.id }}</p>
    <p><strong>Título:</strong> {{ tarea.titulo }}</p>

    <p><strong>Familia:</strong> {{ tarea.familia_nombre || tarea.familia }}</p>

    <p><strong>Descripción:</strong> {{ tarea.descripcion || "—" }}</p>

    <p><strong>Estado:</strong> {{ tarea.estado.replace("_", " ") }}</p>

    <p>
      <strong>Creada:</strong>
      {{ new Date(tarea.fecha_creacion).toLocaleString() }}
    </p>

    <p><strong>Vence:</strong> {{ tarea.fecha_vencimiento || "—" }}</p>

    <div class="actions">
      <button @click="$emit('editar')">Editar</button>
      <button @click="$emit('eliminar')">Eliminar</button>
      <button @click="$emit('volver')">Volver</button>
    </div>
  </div>
</template>

<script setup>
// Defino la propiedad 'tarea' como un objeto obligatorio para que este componente funcione
defineProps({
  tarea: { type: Object, required: true },
});

// Declaro los eventos que voy a emitir para que el padre controle la navegación y las acciones
defineEmits(["editar", "eliminar", "volver"]);
</script>
