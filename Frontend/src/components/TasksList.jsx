import React, { useEffect, useState } from "react";
import { getAllTasks } from "../api/tasks.api";
import { TaskCard } from "./TaskCard";
import { getAllTaskss } from "../api/projects.api";

export function TasksList() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    async function loadTasks() {
      const res = await getAllTasks();
      setTasks(res.data);
    }
    loadTasks();
  }, []);

  return (
    <div className="grid grid-cols-3 gap-3">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
}

export function ProjectsList() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    async function loadProjects() {
      const res = await getAllTaskss();
      setProjects(res.data);
    }
    loadProjects();
  }, []);

  return (
    <div>
      {projects.map((project) => (
        <div key={project.id}>
          <h3>{project.nombre}</h3>
          <p>{project.descripcion}</p>
          {/* Renderizar más detalles del proyecto según sea necesario */}
        </div>
      ))}
    </div>
  );
}
