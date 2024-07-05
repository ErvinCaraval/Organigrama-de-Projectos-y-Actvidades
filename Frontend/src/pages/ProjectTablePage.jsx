import React, { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import { Table, Button, Form, Card } from 'react-bootstrap';
import { getTask, updateTask, getAllTasks, deleteTask, createTask } from "../api/tasks.api";

const ProjectTablePage = () => {
  const [projects, setProjects] = useState([]);
  const [newTask, setNewTask] = useState({ nombre: '', descripcion: '' });
  const [selectedTask, setSelectedTask] = useState(null);
  const [editTask, setEditTask] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredProjects, setFilteredProjects] = useState([]);

  useEffect(() => {
    getAllTasks()
      .then(response => {
        const projectsWithDates = response.data.map(project => ({
          ...project,
          fecha_inicio: new Date(project.fecha_inicio).toISOString().slice(0, 16),
          fecha_fin: project.fecha_fin ? new Date(project.fecha_fin).toISOString().slice(0, 16) : null
        }));
        setProjects(projectsWithDates);
        setFilteredProjects(projectsWithDates);
      })
      .catch(error => {
        toast.error('Error fetching projects');
        console.error('Error fetching projects:', error);
      });
  }, []);

  useEffect(() => {
    setFilteredProjects(
      projects.filter(project =>
        project.proyecto_id.toString().includes(searchTerm)
      )
    );
  }, [searchTerm, projects]);

  const handleCreateTask = () => {
    createTask(newTask)
      .then(response => {
        const newProject = {
          ...response.data,
          fecha_inicio: new Date(response.data.fecha_inicio).toISOString().slice(0, 16),
          fecha_fin: response.data.fecha_fin ? new Date(response.data.fecha_fin).toISOString().slice(0, 16) : null
        };
        setProjects([...projects, newProject]);
        setNewTask({ nombre: '', descripcion: '' });
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
        const updatedProject = {
          ...response.data,
          fecha_inicio: new Date(response.data.fecha_inicio).toISOString().slice(0, 16),
          fecha_fin: response.data.fecha_fin ? new Date(response.data.fecha_fin).toISOString().slice(0, 16) : null
        };
        setProjects(projects.map(project => project.proyecto_id === id ? updatedProject : project));
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
        setProjects(projects.filter(project => project.proyecto_id !== id));
        toast.success('Task deleted successfully');
      })
      .catch(error => {
        toast.error('Error deleting task');
        console.error('Error deleting task:', error);
      });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditTask({
      ...editTask,
      [name]: value
    });
  };

  const handleEditClick = (project) => {
    setSelectedTask(project.proyecto_id);
    setEditTask(project);
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
          type="text"
          placeholder="Buscar por ID del Projecto "
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="form-control"
        />
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
              <th>Terminado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filteredProjects.map((project) => (
              <tr key={project.proyecto_id}>
                <td>{project.proyecto_id}</td>
                <td>
                  {selectedTask === project.proyecto_id ? (
                    <Form.Control
                      type="text"
                      name="nombre"
                      value={editTask.nombre}
                      onChange={handleInputChange}
                    />
                  ) : (
                    project.nombre
                  )}
                </td>
                <td>
                  {selectedTask === project.proyecto_id ? (
                    <Form.Control
                      type="text"
                      name="descripcion"
                      value={editTask.descripcion}
                      onChange={handleInputChange}
                    />
                  ) : (
                    project.descripcion
                  )}
                </td>
                <td>
                  {selectedTask === project.proyecto_id ? (
                    <Form.Control
                      type="datetime-local"
                      name="fecha_inicio"
                      value={editTask.fecha_inicio}
                      onChange={handleInputChange}
                    />
                  ) : (
                    new Date(project.fecha_inicio).toLocaleString()
                  )}
                </td>
                <td>
                  {selectedTask === project.proyecto_id ? (
                    <Form.Control
                      type="datetime-local"
                      name="fecha_fin"
                      value={editTask.fecha_fin}
                      onChange={handleInputChange}
                    />
                  ) : (
                    project.fecha_fin ? new Date(project.fecha_fin).toLocaleString() : 'N/A'
                  )}
                </td>
                <td>{new Date(project.creado_en).toLocaleString()}</td>
                <td>{new Date(project.actualizado_en).toLocaleString()}</td>
                <td>
                  {project.terminado ? (
                    <span className="text-success">Sí</span>
                  ) : (
                    <span className="text-danger">No</span>
                  )}
                </td>
                <td>
                  {selectedTask !== project.proyecto_id ? (
                    <>
                      <Button onClick={() => handleEditClick(project)} variant="warning" size="sm">Editar</Button>
                      <Button onClick={() => handleDeleteTask(project.proyecto_id)} variant="danger" size="sm" className="ml-2">Eliminar</Button>
                    </>
                  ) : (
                    <>
                      <Button onClick={() => handleUpdateTask(project.proyecto_id)} variant="success" size="sm">Guardar</Button>
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

export default ProjectTablePage;
