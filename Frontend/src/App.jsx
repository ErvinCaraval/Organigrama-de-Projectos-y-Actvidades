import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Navigation } from "./components/Navigation";
import { TaskFormPage } from "./pages/TaskFormPage";
import { TasksPage } from "./pages/TasksPage";
import { Toaster } from "react-hot-toast";
import 'bootstrap/dist/css/bootstrap.min.css';

import 'react-toastify/dist/ReactToastify.css';



import { ProjectFormPage } from "./pages/ProjectFormPage";
import ProjectTablePage from "./pages/ProjectTablePage";
import TaskTablePage from "./pages/TaskTablePage"
import   TaskTimeline   from "./pages/TaskTimeline"
function App() {
  return (
    <BrowserRouter>
      <div className="container mx-auto">
        <Navigation />
        <Routes>
          {/* redirect to tasks */}
          <Route path="/" element={<Navigate to="/tasks" />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="/tasks/:id" element={<TaskFormPage />} />
          <Route path="/tasks-create" element={<TaskFormPage />} />
          <Route path="/projects/:id" element={<ProjectFormPage />} />
          <Route path="/project-create" element={<ProjectFormPage />} />

          <Route path="/projects" element={<ProjectTablePage/>} />
          <Route path="/sasks" element={<TaskTablePage/>} />
          <Route path="/task-timeline" element={<TaskTimeline/>} />
          
        </Routes>
        <Toaster />
      </div>
    </BrowserRouter>
  );
}

export default App;
