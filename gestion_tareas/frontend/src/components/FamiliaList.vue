<template>
  <div>
    <table v-if="familias.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="familia in familias" :key="familia.id">
          <td>{{ familia.id }}</td>
          <td>{{ familia.nombre }}</td>
          <td>
            <button @click="$emit('editar', familia)">Editar</button>
            <button @click="$emit('eliminar', familia.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay familias registradas.</p>
  </div>
</template>

<script setup>
// Defino la propiedad que voy a recibir, asegurándome de que sea un array obligatorio
defineProps({
  familias: { type: Array, required: true },
});

// Declaro los eventos que voy a "gritar" hacia arriba para que el componente padre los gestione
defineEmits(["editar", "eliminar"]);
</script>
