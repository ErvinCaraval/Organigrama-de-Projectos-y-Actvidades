import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { createTask, getTask, updateTask } from "../api/tasks.api";
import { toast } from "react-hot-toast";

export function TaskFormPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    setError,
  } = useForm();
  const navigate = useNavigate();
  const params = useParams();

  const onSubmit = handleSubmit(async (data) => {
    // Convertir fechas a formato ISO si es necesario
    data.fecha_inicio = data.fecha_inicio ? new Date(data.fecha_inicio).toISOString() : null;
    data.fecha_fin = data.fecha_fin ? new Date(data.fecha_fin).toISOString() : null;

    try {
      if (params.id) {
        await updateTask(params.id, data);
        toast.success("Proyecto actualizado", {
          position: "bottom-right",
          style: {
            background: "#101010",
            color: "#fff",
          },
        });
      } else {
        await createTask(data);
        toast.success("Nuevo Proyecto agregado", {
          position: "bottom-right",
          style: {
            background: "#101010",
            color: "#fff",
          },
        });
      }
      navigate("/proyectos");
    } catch (error) {
      if (error.response && error.response.data) {
        const apiErrors = error.response.data;
        // Mostrar errores específicos de los campos del formulario
        Object.keys(apiErrors).forEach((key) => {
          setError(key, {
            type: "manual",
            message: apiErrors[key],
          });
        });
        // Mostrar errores no relacionados con campos específicos
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

  useEffect(() => {
    async function loadTask() {
      if (params.id) {
        const { data } = await getTask(params.id);
        setValue("nombre", data.nombre);
        setValue("descripcion", data.descripcion);
        setValue("fecha_inicio", data.fecha_inicio ? data.fecha_inicio.substring(0, 16) : null);
        setValue("fecha_fin", data.fecha_fin ? data.fecha_fin.substring(0, 16) : null);
      }
    }
    loadTask();
  }, [params.id, setValue]);

  return (
    <div className="max-w-xl mx-auto mt-10">
      <form onSubmit={onSubmit} className="bg-gray-900 p-8 rounded-lg shadow-lg">
        <h2 className="text-2xl font-bold mb-6 text-center text-white">
          {params.id ? "Editar Proyecto" : "Nuevo Proyecto"}
        </h2>

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

        <div className="mb-6">
          <label className="block text-white mb-2">Fecha de Fin</label>
          <input
            type="datetime-local"
            {...register("fecha_fin")}
            className="bg-gray-800 text-white p-3 rounded-lg block w-full"
          />
          {errors.fecha_fin && <span className="text-red-500">{errors.fecha_fin.message}</span>}
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
