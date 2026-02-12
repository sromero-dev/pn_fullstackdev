import axios from "axios";

export const apiClient = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
});

export default {
  // Familias CRUD
  getFamilias() {
    return apiClient.get("/familias/");
  },
  createFamilia(data) {
    return apiClient.post("/familias/", data);
  },
  updateFamilia(id, data) {
    return apiClient.put(`/familias/${id}/`, data);
  },
  deleteFamilia(id) {
    return apiClient.delete(`/familias/${id}/`);
  },

  // Tareas CRUD
  getTareas(params = {}) {
    return apiClient.get("/tareas/", { params });
  },
  getTarea(id) {
    return apiClient.get(`/tareas/${id}/`);
  },
  createTarea(data) {
    return apiClient.post("/tareas/", data);
  },
  updateTarea(id, data) {
    return apiClient.put(`/tareas/${id}/`, data);
  },
  deleteTarea(id) {
    return apiClient.delete(`/tareas/${id}/`);
  },
};
