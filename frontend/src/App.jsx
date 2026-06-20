import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Users from "./pages/Users";
import Attendance from "./pages/Attendance";
import Exceptions from "./pages/Exceptions";
import Shifts from "./pages/Shifts";
import Overtime from "./pages/Overtime";
import Leave from "./pages/Leave";
import Meals from "./pages/Meals";
import Cards from "./pages/Cards";

function App() {
  return (
    <Router>
      <div style={{ display: "flex" }}>
        <Sidebar />
        <div style={{ flex: 1, padding: "20px" }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<Users />} />
            <Route path="/attendance" element={<Attendance />} />
            <Route path="/exceptions" element={<Exceptions />} />
            <Route path="/shifts" element={<Shifts />} />
            <Route path="/overtime" element={<Overtime />} />
            <Route path="/leave" element={<Leave />} />
            <Route path="/meals" element={<Meals />} />
            <Route path="/cards" element={<Cards />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
