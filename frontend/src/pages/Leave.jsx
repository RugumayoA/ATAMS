import { useEffect, useState } from "react";
import API from "../components/api/axios";
import { Calendar } from "lucide-react";

const TABS = [
  { label: "Staff On Leave",  endpoint: "/leave/staff-on-leave"  },
  { label: "Reconciliation",  endpoint: "/leave/reconciliation"  },
];

function Leave() {
  const [activeTab, setActiveTab] = useState(0);
  const [records, setRecords]     = useState([]);
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    setLoading(true);
    API.get(TABS[activeTab].endpoint)
      .then((res) => {
        setRecords(Array.isArray(res.data) ? res.data : [res.data]);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [activeTab]);

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
        <h1 style={{ margin: 0, display: "flex", alignItems: "center", gap: "10px", fontSize: "22px", fontWeight: 600 }}>
          <Calendar size={28} color="white" />
          LEAVE REPORTS
        </h1>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px", flexWrap: "wrap" }}>
        {TABS.map((tab, i) => (
          <button
            key={i}
            onClick={() => setActiveTab(i)}
            style={{
              padding: "10px 16px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              fontWeight: activeTab === i ? "bold" : "normal",
              background: activeTab === i ? "#1e3a5f" : "#f0f0f0",
              color: activeTab === i ? "white" : "#333",
              fontSize: "13px",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Table */}
      <div style={{
        background: "white",
        borderRadius: "12px",
        padding: "24px",
        boxShadow: "0 2px 12px rgba(0,0,0,0.08)"
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px" }}>
          <h3 style={{ margin: 0, color: "#1e3a5f" }}>{TABS[activeTab].label}</h3>
          <span style={{
            background: "#1e3a5f",
            color: "white",
            borderRadius: "20px",
            padding: "4px 14px",
            fontSize: "13px",
            fontWeight: 500,
          }}>
            {records.length} record{records.length !== 1 ? "s" : ""}
          </span>
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : records.length === 0 ? (
          <p style={{ color: "#999" }}>No records found.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#1e3a5f", color: "white" }}>
                {Object.keys(records[0]).map((key) => (
                  <th key={key} style={{ padding: "12px", textAlign: "left", fontSize: "13px" }}>
                    {key.replace(/_/g, " ").toUpperCase()}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {records.map((rec, i) => (
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

export default Leave;
