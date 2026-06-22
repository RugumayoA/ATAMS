import { useEffect, useState, useMemo } from "react";
import API from "../components/api/axios";
import { UtensilsCrossed } from "lucide-react";

function Meals() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState("all");

  useEffect(() => {
    setLoading(true);
    API.get("/meals/summary")
      .then((res) => {
        setSummary(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filtered = useMemo(() => {
    if (!summary) return [];
    if (activeFilter === "accepted") return summary.records.filter((r) => r.meal_accepted);
    if (activeFilter === "denied")   return summary.records.filter((r) => !r.meal_accepted);
    return summary.records;
  }, [summary, activeFilter]);

  const buttons = summary ? [
    { key: "all",      label: "Total Meal Punches", value: summary.total_meal_punches, color: "#1e3a5f" },
    { key: "accepted", label: "Accepted",            value: summary.accepted,           color: "#2e7d32" },
    { key: "denied",   label: "Denied",              value: summary.denied,             color: "#c62828" },
  ] : [];

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
        <h1 style={{ margin: 0, display: "flex", alignItems: "center", gap: "10px", fontSize: "22px", fontWeight: 600, color: "white" }}>
          <UtensilsCrossed size={28} color="white" />
          MEALS REPORTS
        </h1>
      </div>

      {/* Filter Buttons */}
      {summary && (
        <div style={{ display: "flex", gap: "12px", marginBottom: "24px", flexWrap: "wrap" }}>
          {buttons.map((btn) => {
            const isActive = activeFilter === btn.key;
            return (
              <button
                key={btn.key}
                onClick={() => setActiveFilter(btn.key)}
                style={{
                  border: `2px solid ${btn.color}`,
                  borderRadius: "999px",
                  padding: "8px 20px",
                  background: isActive ? btn.color : "white",
                  fontSize: "13px",
                  color: isActive ? "white" : "#333",
                  fontWeight: 500,
                  cursor: "pointer",
                  transition: "all 0.15s",
                }}
              >
                {btn.label} : <span style={{ fontWeight: 700, color: isActive ? "white" : btn.color }}>{btn.value}</span>
              </button>
            );
          })}
        </div>
      )}

      {/* Records Table */}
      <div style={{
        background: "white",
        borderRadius: "12px",
        padding: "24px",
        boxShadow: "0 2px 12px rgba(0,0,0,0.08)"
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px" }}>
          <h3 style={{ margin: 0, color: "#1e3a5f" }}>Meal Punch Records</h3>
          <span style={{
            background: "#1e3a5f",
            color: "white",
            borderRadius: "20px",
            padding: "4px 14px",
            fontSize: "13px",
            fontWeight: 500,
          }}>
            {filtered.length} record{filtered.length !== 1 ? "s" : ""}
          </span>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : filtered.length === 0 ? (
          <p style={{ color: "#999" }}>No records found.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#1e3a5f", color: "white" }}>
                {Object.keys(filtered[0]).map((key) => (
                  <th key={key} style={{ padding: "12px", textAlign: "left", fontSize: "13px" }}>
                    {key.replace(/_/g, " ").toUpperCase()}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((rec, i) => (
                <tr key={i} style={{
                  background: i % 2 === 0 ? "#f9f9f9" : "white",
                  borderBottom: "1px solid #eee"
                }}>
                  {Object.values(rec).map((val, j) => (
                    <td key={j} style={td}>
                      {val === null ? "—" : val === true ? "Yes" : val === false ? "No" : String(val)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

const td = {
  padding: "12px",
  fontSize: "13px",
  color: "#333",
  textAlign: "left"
};

export default Meals;
