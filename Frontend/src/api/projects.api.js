import axios from 'axios';

const tasksApi = axios.create({
  baseURL: "http://localhost:8000/api/v1/api/tareas/",
});

export const getAllTaskss = () => {
  return tasksApi.get("/");
}

export const getTask = (id) => {
  return tasksApi.get(`/${id}/`);
}

export const createTask = (task) => {
  return tasksApi.post("/", task);
}

export const updateTask = (id, task) => {
  return tasksApi.put(`/${id}/`, task);
}

export const deleteTask = (id) => {
  return tasksApi.delete(`/${id}/`);
}
