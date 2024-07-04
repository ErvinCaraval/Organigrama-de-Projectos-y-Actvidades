import { Link } from "react-router-dom";

export function Navigation() {
  return (
    <nav className="bg-gray-900 p-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/tasks">
          <h1 className="font-bold text-3xl text-white">Organigrama de Proyectos y Actividades</h1>
        </Link>
        <div className="flex space-x-4">
          <Link to="/tasks-create">
            <button className="bg-indigo-500 hover:bg-indigo-700 text-white p-3 rounded-lg transition duration-200">
              Crear Proyecto
            </button>
          </Link>
          <Link to="/project-create">
            <button className="bg-green-500 hover:bg-green-700 text-white p-3 rounded-lg transition duration-200">
              Crear Tarea
            </button>
          </Link>
          <Link to="/projects">
            <button className="bg-blue-500 hover:bg-blue-700 text-white p-3 rounded-lg transition duration-200">
              Visualizar Proyectos
            </button>
          </Link>
          <Link to="/sasks">
            <button className="bg-yellow-500 hover:bg-yellow-700 text-white p-3 rounded-lg transition duration-200">
              Visualizar Tareas
            </button>
          </Link>
          <Link to="/task-timeline">
            <button className="bg-purple-500 hover:bg-purple-700 text-white p-3 rounded-lg transition duration-200">
              Visualizar Línea de Tiempo
            </button>
          </Link>
        </div>
      </div>
    </nav>
  );
}
