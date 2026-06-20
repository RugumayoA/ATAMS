import { useEffect, useState } from "react";
import API from "../components/api/axios";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from "recharts";

const COLORS = ["#1e3a5f", "#2e7d32", "#c62828", "#f57f17"];

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [deptData, setDeptData] = useState([]);

  useEffect(() => {
    API.get("/attendance/summary")
      .then((res) => setSummary(res.data))
      .catch((err) => console.error(err));

    API.get("/attendance/by-department")
      .then((res) => {
        const formatted = Object.entries(res.data).map(([dept, data]) => ({
          department: dept,
          Present: data.present,
          Absent: data.absent,
        }));
        setDeptData(formatted);
      })
      .catch((err) => console.error(err));
  }, []);

  const pieData = summary
    ? [
        { name: "Present",  value: summary.present  },
        { name: "Absent",   value: summary.absent   },
        { name: "On Leave", value: summary.on_leave },
      ]
    : [];

  return (
    <div style={{ fontFamily: "Segoe UI, sans-serif", padding: "30px" }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #1e3a5f, #2d6a9f)",
        borderRadius: "16px",
        padding: "30px",
        color: "white",
        marginBottom: "30px"
      }}>
        <h1 style={{ margin: 0, fontSize: "28px" }}>✈️ ATAMS Dashboard</h1>
        <p style={{ margin: "6px 0 0", opacity: 0.8 }}>
          Civil Aviation Authority of Uganda — Attendance Overview
        </p>
      </div>

      {/* Summary Cards */}
      {summary ? (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "20px", marginBottom: "30px" }}>
          {[
            { label: "Total Staff",  value: summary.total,    color: "#1e3a5f", icon: "👥" },
            { label: "Present",      value: summary.present,  color: "#2e7d32", icon: "✅" },
            { label: "Absent",       value: summary.absent,   color: "#c62828", icon: "❌" },
            { label: "On Leave",     value: summary.on_leave, color: "#f57f17", icon: "🏖️" },
          ].map((card) => (
            <div key={card.label} style={{
              background: "white",
              borderRadius: "12px",
              padding: "24px",
              boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
              borderLeft: `5px solid ${card.color}`,
            }}>
              <p style={{ margin: 0, color: "#666", fontSize: "13px" }}>{card.icon} {card.label}</p>
              <h2 style={{ margin: "8px 0 0", fontSize: "36px", color: card.color }}>{card.value}</h2>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading summary...</p>
      )}

      {/* Charts Row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>

        {/* Bar Chart */}
        <div style={{
          background: "white",
          borderRadius: "12px",
          padding: "24px",
          boxShadow: "0 2px 12px rgba(0,0,0,0.08)"
        }}>
          <h3 style={{ marginTop: 0, color: "#1e3a5f" }}>📊 Attendance by Department</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={deptData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="department" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="Present" fill="#2e7d32" radius={[4,4,0,0]} />
              <Bar dataKey="Absent"  fill="#c62828" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pie Chart */}
        <div style={{
          background: "white",
          borderRadius: "12px",
          padding: "24px",
          boxShadow: "0 2px 12px rgba(0,0,0,0.08)"
        }}>
          <h3 style={{ marginTop: 0, color: "#1e3a5f" }}>🥧 Attendance Breakdown</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                outerRadius={90}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {pieData.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

      </div>
    </div>
  );
}

export default Dashboard;