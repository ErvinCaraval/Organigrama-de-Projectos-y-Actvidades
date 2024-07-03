import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { createTask, getTask, updateTask } from "../api/projects.api";
import { toast } from "react-hot-toast";

export function ProjectFormPage() {
    const {
        register,
        handleSubmit,
        formState: { errors },
        setError,
        setValue,
    } = useForm();
    const navigate = useNavigate();
    const params = useParams();
    const [projects, setProjects] = useState([]);
    const [selectedProject, setSelectedProject] = useState(null);

    // Función para cargar los proyectos desde la API
    useEffect(() => {
        async function loadProjects() {
            try {
                const response = await fetch('http://localhost:8000/api/v1/api/proyectos/');
                if (!response.ok) {
                    throw new Error('Error al cargar los proyectos');
                }
                const projectsData = await response.json();
                setProjects(projectsData);
            } catch (error) {
                console.error('Error al cargar proyectos:', error);
            }
        }

        loadProjects();
    }, []);

 

    // Función para manejar el envío del formulario
    const onSubmit = handleSubmit(async (data) => {
        data.fecha_inicio = data.fecha_inicio ? new Date(data.fecha_inicio).toISOString() : null;
        data.fecha_fin = data.fecha_fin ? new Date(data.fecha_fin).toISOString() : null;
        data.sin_terminar = !!data.sin_terminar; // Convertir a booleano
        data.terminado = !!data.terminado; // Convertir a booleano

        try {
            if (params.id) {
                await updateTask(params.id, sanitizeData(data));
                toast.success("Tarea actualizada", {
                    position: "bottom-right",
                    style: {
                        background: "#101010",
                        color: "#fff",
                    },
                });
            } else {
                await createTask(sanitizeData(data));
                toast.success("Nueva Tarea agregada", {
                    position: "bottom-right",
                    style: {
                        background: "#101010",
                        color: "#fff",
                    },
                });
            }
            navigate("/tareas");
        } catch (error) {
            if (error.response && error.response.data) {
                const apiErrors = error.response.data;
                Object.keys(apiErrors).forEach((key) => {
                    setError(key, {
                        type: "manual",
                        message: apiErrors[key].join(", "),
                    });
                });
                if (apiErrors.non_field_errors) {
                    toast.error(apiErrors.non_field_errors.join(" "), {
                        position: "bottom-right",
                        style: {
                            background: "#101010",
                            color: "#fff",
                        },
                    });
                }
            }
        }
    });

    // Función para cargar los datos de la tarea si se está editando
    useEffect(() => {
        async function loadTask() {
            if (params.id) {
                try {
                    const { data } = await getTask(params.id);
                    setValue("proyecto", data.proyecto);
                    setValue("nombre", data.nombre);
                    setValue("descripcion", data.descripcion);
                    setValue("fecha_inicio", data.fecha_inicio ? data.fecha_inicio.substring(0, 16) : null);
                    setValue("fecha_fin", data.fecha_fin ? data.fecha_fin.substring(0, 16) : null);
                    setSelectedProject(projects.find(project => project.proyecto_id === data.proyecto));
                    setValue("sin_terminar", data.sin_terminar); // Asignar valor a sin_terminar
                    setValue("terminado", data.terminado); // Asignar valor a terminado
                } catch (error) {
                    console.error('Error al cargar la tarea:', error);
                }
            }
        }

        loadTask();
    }, [params.id, setValue, projects]);

    // Función para manejar el cambio de proyecto seleccionado
    const handleProjectChange = (event) => {
        const selectedProjectId = event.target.value;
        const project = projects.find(project => project.proyecto_id === selectedProjectId);
        setSelectedProject(project);
        setValue("proyecto", selectedProjectId);
    };

    // Función para sanitizar los datos antes de enviarlos al backend
    const sanitizeData = (data) => {
        const sanitizedData = {
            ...data,
            nombre: sanitizeInput(data.nombre),
            descripcion: sanitizeInput(data.descripcion),
        };
        return sanitizedData;
    };

    // Función para sanitizar la entrada contra inyección SQL
    const sanitizeInput = (input) => {
        if (!input) return input;
        // Eliminar caracteres especiales que podrían ser parte de un ataque de SQL injection
        const sanitizedInput = input.replace(/[;'"\\]/g, '');
        return sanitizedInput;
    };

    return (
        <div className="max-w-xl mx-auto mt-10">
            <form onSubmit={onSubmit} className="bg-gray-900 p-8 rounded-lg shadow-lg">
                <h2 className="text-2xl font-bold mb-6 text-center text-white">
                    {params.id ? "Editar Tarea" : "Nueva Tarea"}
                </h2>

                <div className="mb-4">
                    <label className="block text-white mb-2">Proyecto</label>
                    <select
                        {...register("proyecto", { required: "Este campo es obligatorio" })}
                        className="bg-gray-800 text-white p-3 rounded-lg block w-full"
                        onChange={handleProjectChange}
                    >
                        <option value="">Seleccione un proyecto</option>
                        {projects.map((project) => (
                            <option key={project.proyecto_id} value={project.proyecto_id}>
                                {project.nombre}
                            </option>
                        ))}
                    </select>
                    {errors.proyecto && <span className="text-red-500">{errors.proyecto.message}</span>}
                    {selectedProject && (
                        <div className="text-white mt-2">
                            <p>Fecha de inicio del proyecto: {new Date(selectedProject.fecha_inicio).toLocaleString()}</p>
                            <p>Fecha de fin del proyecto: {selectedProject.fecha_fin ? new Date(selectedProject.fecha_fin).toLocaleString() : "No definida"}</p>
                        </div>
                    )}
                </div>

                <div className="mb-4">
                    <label className="block text-white mb-2">Nombre</label>
                    <input
                        type="text"
                        placeholder="Nombre"
                        {...register("nombre", { required: "Este campo es obligatorio" })}
                        className="bg-gray-800 text-white p-3 rounded-lg block w-full"
                        autoFocus
                    />
                    {errors.nombre && <span className="text-red-500">{errors.nombre.message}</span>}
                </div>

                <div className="mb-4">
                    <label className="block text-white mb-2">Descripción</label>
                    <textarea
                        placeholder="Descripción"
                        {...register("descripcion", { required: "Este campo es obligatorio" })}
                        className="bg-gray-800 text-white p-3 rounded-lg block w-full"
                    />
                    {errors.descripcion && <span className="text-red-500">{errors.descripcion.message}</span>}
                </div>

                <div className="mb-4">
                    <label className="block text-white mb-2">Fecha de Inicio</label>
                    <input
                        type="datetime-local"
                        {...register("fecha_inicio", { required: "Este campo es obligatorio" })}
                        className="bg-gray-800 text-white p-3 rounded-lg block w-full"
                    />
                    {errors.fecha_inicio && <span className="text-red-500">{errors.fecha_inicio.message}</span>}
                </div>

                <div className="mb-4">
                    <label className="block text-white mb-2">Fecha de Fin</label>
                    <input
                        type="datetime-local"
                        {...register("fecha_fin")}
                        className="bg-gray-800 text-white p-3 rounded-lg block w-full"
                    />
                </div>

                <div className="mb-4">
                    <label className="block text-white mb-2">
                        <input
                            type="checkbox"
                            {...register("sin_terminar")}
                            className="mr-2"
                        />
                        Tarea sin terminar
                    </label>
                </div>

                <div className="mb-4">
                    <label className="block text-white mb-2">
                        <input
                            type="checkbox"
                            {...register("terminado")}
                            className="mr-2"
                        />
                        Tarea terminada
                    </label>
                </div>

                <button
                    type="submit"
                    className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-lg block w-full transition duration-200"
                >
                    Guardar
                </button>
            </form>
        </div>
    );
}











































    