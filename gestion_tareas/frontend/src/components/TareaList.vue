<template>
  <div>
    <table v-if="tareas.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Título</th>
          <th>Familia</th>
          <th>Estado</th>
          <th>Vence</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tarea in tareas" :key="tarea.id">
          <td>{{ tarea.id }}</td>
          <td>{{ tarea.titulo }}</td>
          <td>{{ tarea.familia_nombre || tarea.familia }}</td>
          <td>
            <span :class="'estado ' + tarea.estado">
              {{ tarea.estado.replace("_", " ") }}
            </span>
          </td>
          <td>{{ tarea.fecha_vencimiento || "—" }}</td>
          <td>
            <button @click="$emit('ver-detalle', tarea.id)">Ver</button>
            <button @click="$emit('editar', tarea.id)">Editar</button>
            <button @click="$emit('eliminar', tarea.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay tareas que coincidan con los criterios.</p>
  </div>
</template>

<script setup>
// Defino las propiedades que espero recibir, asegurando que 'tareas' sea un array
defineProps({
  tareas: { type: Array, required: true },
});

// Declaro los eventos que voy a comunicar hacia el componente superior
defineEmits(["ver-detalle", "editar", "eliminar"]);
</script>

<style scoped>
/* Establezco el diseño base para las etiquetas de estado */
.estado {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85em;
  color: white;
}

/* Asigno colores específicos según la clase dinámica del estado */
.estado.pendiente {
  background-color: #ffc107;
}
.estado.en_progreso {
  background-color: #17a2b8;
}
.estado.completada {
  background-color: #28a745;
}
</style>
