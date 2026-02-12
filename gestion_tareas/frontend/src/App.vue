<template>
  <div id="app">
    <nav>
      <router-link to="/tareas">Tareas</router-link> |
      <router-link to="/familias">Familias</router-link>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
nav {
  padding: 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}
nav a {
  margin: 0 10px;
  text-decoration: none;
  color: #42b983;
  font-weight: bold;
}
main {
  padding: 20px;
}
</style>
