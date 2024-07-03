import React, { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import { Table, Button, Form, Card } from 'react-bootstrap';
import { getAllTaskss, createTask, updateTask, deleteTask } from "../api/projects.api";

const TaskTablePage = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ nombre: '', descripcion: '', sin_terminar: true, terminado: false });
  const [selectedTask, setSelectedTask] = useState(null);
  const [editTask, setEditTask] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [filteredTasks, setFilteredTasks] = useState([]);

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
        toast.error('Error fetching projects');
        console.error('Error fetching projects:', error);
      });
  }, []);

  useEffect(() => {
    getAllTaskss()
      .then(response => {
        const tasksWithDates = response.data.map(task => ({
          ...task,
          fecha_inicio: new Date(task.fecha_inicio).toISOString().slice(0, 16),
          fecha_fin: task.fecha_fin ? new Date(task.fecha_fin).toISOString().slice(0, 16) : null
        }));
        setTasks(tasksWithDates);
        setFilteredTasks(tasksWithDates);
      })
      .catch(error => {
        toast.error('Error fetching tasks');
        console.error('Error fetching tasks:', error);
      });
  }, []);

  useEffect(() => {
    if (selectedProject) {
      setFilteredTasks(
        tasks.filter(task =>
          task.proyecto.toString().includes(selectedProject)
        )
      );
    } else {
      setFilteredTasks(tasks);
    }
  }, [selectedProject, tasks]);

  const handleCreateTask = () => {
    createTask(newTask)
      .then(response => {
        const newTaskData = {
          ...response.data,
          fecha_inicio: new Date(response.data.fecha_inicio).toISOString().slice(0, 16),
          fecha_fin: response.data.fecha_fin ? new Date(response.data.fecha_fin).toISOString().slice(0, 16) : null
        };
        setTasks([...tasks, newTaskData]);
        setNewTask({ nombre: '', descripcion: '', sin_terminar: true, terminado: false });
        toast.success('Task created successfully');
      })
      .catch(error => {
        toast.error('Error creating task');
        console.error('Error creating task:', error);
      });
  };

  const handleUpdateTask = (id) => {
    updateTask(id, editTask)
      .then(response => {
        const updatedTask = {
          ...response.data,
          fecha_inicio: new Date(response.data.fecha_inicio).toISOString().slice(0, 16),
          fecha_fin: response.data.fecha_fin ? new Date(response.data.fecha_fin).toISOString().slice(0, 16) : null
        };
        setTasks(tasks.map(task => task.tarea_id === id ? updatedTask : task));
        setSelectedTask(null);
        setEditTask(null);
        toast.success('Task updated successfully');
      })
      .catch(error => {
        toast.error('Error updating task');
        console.error('Error updating task:', error);
      });
  };

  const handleDeleteTask = (id) => {
    deleteTask(id)
      .then(() => {
        setTasks(tasks.filter(task => task.tarea_id !== id));
        toast.success('Task deleted successfully');
      })
      .catch(error => {
        toast.error('Error deleting task');
        console.error('Error deleting task:', error);
      });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    let updatedTask = { ...editTask, [name]: value };

    if (name === 'sin_terminar' && value === 'true') {
      updatedTask = { ...updatedTask, terminado: false };
    } else if (name === 'sin_terminar' && value === 'false') {
      updatedTask = { ...updatedTask, terminado: true };
    } else if (name === 'terminado' && value === 'true') {
      updatedTask = { ...updatedTask, sin_terminar: false };
    } else if (name === 'terminado' && value === 'false') {
      updatedTask = { ...updatedTask, sin_terminar: true };
    }

    setEditTask(updatedTask);
  };

  const handleEditClick = (task) => {
    setSelectedTask(task.tarea_id);
    setEditTask(task);
  };

  const handleCancelEdit = () => {
    setSelectedTask(null);
    setEditTask(null);
  };

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
      <Card className="p-3">
        <Table hover bordered variant="dark">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Fecha de Inicio</th>
              <th>Fecha de Fin</th>
              <th>Creado En</th>
              <th>Actualizado En</th>
              <th>Sin Terminar</th>
              <th>Terminado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filteredTasks.map((task) => (
              <tr key={task.tarea_id}>
                <td>{task.tarea_id}</td>
                <td>
                  {selectedTask === task.tarea_id ? (
                    <Form.Control
                      type="text"
                      name="nombre"
                      value={editTask.nombre}
                      onChange={handleInputChange}
                    />
                  ) : (
                    task.nombre
                  )}
                </td>
                <td>
                  {selectedTask === task.tarea_id ? (
                    <Form.Control
                      type="text"
                      name="descripcion"
                      value={editTask.descripcion}
                      onChange={handleInputChange}
                    />
                  ) : (
                    task.descripcion
                  )}
                </td>
                <td>
                  {selectedTask === task.tarea_id ? (
                    <Form.Control
                      type="datetime-local"
                      name="fecha_inicio"
                      value={editTask.fecha_inicio}
                      onChange={handleInputChange}
                    />
                  ) : (
                    new Date(task.fecha_inicio).toLocaleString()
                  )}
                </td>
                <td>
                  {selectedTask === task.tarea_id ? (
                    <Form.Control
                      type="datetime-local"
                      name="fecha_fin"
                      value={editTask.fecha_fin}
                      onChange={handleInputChange}
                    />
                  ) : (
                    task.fecha_fin ? new Date(task.fecha_fin).toLocaleString() : 'N/A'
                  )}
                </td>
                <td>{new Date(task.creado_en).toLocaleString()}</td>
                <td>{new Date(task.actualizado_en).toLocaleString()}</td>
                <td>
                  {selectedTask === task.tarea_id ? (
                    <Form.Control
                      as="select"
                      name="sin_terminar"
                      value={editTask.sin_terminar.toString()}
                      onChange={handleInputChange}
                    >
                      <option value="true">Sí</option>
                      <option value="false">No</option>
                    </Form.Control>
                  ) : (
                    task.sin_terminar ? (
                      <span className="text-warning">Sí</span>
                    ) : (
                      <span className="text-danger">No</span>
                    )
                  )}
                </td>
                <td>
                  {selectedTask === task.tarea_id ? (
                    <Form.Control
                      as="select"
                      name="terminado"
                      value={editTask.terminado.toString()}
                      onChange={handleInputChange}
                    >
                      <option value="true">Sí</option>
                      <option value="false">No</option>
                    </Form.Control>
                  ) : (
                    task.terminado ? (
                      <span className="text-success">Sí</span>
                    ) : (
                      <span className="text-danger">No</span>
                    )
                  )}
                </td>
                <td>
                  {selectedTask !== task.tarea_id ? (
                    <>
                      <Button onClick={() => handleEditClick(task)} variant="warning" size="sm">Editar</Button>
<Button onClick={() => handleDeleteTask(task.tarea_id)} variant="danger" size="sm" className="ml-2">Eliminar</Button>
</>
) : (
<>
<Button onClick={() => handleUpdateTask(task.tarea_id)} variant="success" size="sm">Guardar</Button>
<Button onClick={handleCancelEdit} variant="secondary" size="sm" className="ml-2">Cancelar</Button>
</>
)}
</td>
</tr>
))}
</tbody>
</Table>
</Card>
</div>
);
};

export default TaskTablePage;
