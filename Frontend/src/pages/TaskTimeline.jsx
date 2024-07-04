import React, { useEffect, useState } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Card, Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { getAllTaskss } from '../api/projects.api'; // Ajusta la ruta según sea necesario
import './TaskTimeline.css'; // Archivo de estilos CSS personalizados

const TaskTimeline = () => {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [filteredTasks, setFilteredTasks] = useState([]);

  useEffect(() => {
    // Cargar tareas
    getAllTaskss()
      .then(response => {
        const tasksWithDates = response.data.map(task => ({
          ...task,
          start: new Date(task.fecha_inicio),
          end: task.fecha_fin ? new Date(task.fecha_fin) : null,
          project: task.proyecto,
        }));
        setTasks(tasksWithDates);
        setFilteredTasks(tasksWithDates); // Inicialmente, mostramos todas las tareas
      })
      .catch(error => {
        console.error('Error fetching tasks:', error);
        toast.error('Error fetching tasks');
      });
  }, []);

  useEffect(() => {
    // Cargar proyectos
    fetch('http://localhost:8000/api/v1/api/proyectos/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Error al cargar los proyectos');
        }
        return response.json();
      })
      .then(data => setProjects(data))
      .catch(error => {
        console.error('Error fetching projects:', error);
        toast.error('Error fetching projects');
      });
  }, []);

  useEffect(() => {
    // Filtrar las tareas según el proyecto seleccionado
    if (selectedProject) {
      setFilteredTasks(tasks.filter(task => task.project === parseInt(selectedProject)));
    } else {
      setFilteredTasks(tasks);
    }
  }, [selectedProject, tasks]);

  return (
    <div className="container mt-5">
      <ToastContainer />
      <Card className="p-3 mb-3">
        <Form.Control
          as="select"
          value={selectedProject || ''}
          onChange={(e) => setSelectedProject(e.target.value)}
          className="form-control"
        >
          <option value="">Seleccionar Proyecto</option>
          {projects.map(project => (
            <option key={project.proyecto_id} value={project.proyecto_id}>
              {project.nombre}
            </option>
          ))}
        </Form.Control>
      </Card>
      <div className="timeline-container">
       
        <div className="timeline">
          {filteredTasks.map((task, index) => (
            <div key={index} className={`timeline-item ${task.end ? 'completed' : 'intermediate'}`}>
              <div className="timeline-description">
                <p>{task.descripcion}</p>
              </div>
              <div className="timeline-content">
                <p>{task.nombre}</p>
                <p>{task.start.toLocaleString()} - {task.end ? task.end.toLocaleString() : 'Sin terminar'}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TaskTimeline;
