import { useEffect, useState, useMemo } from "react";
import API from "../components/api/axios";
import { RefreshCw } from "lucide-react";

const TABS = [
  { label: "Shift Allocations",  endpoint: "/shifts/allocations", type: "table" },
  { label: "Overlapping Shifts", endpoint: "/shifts/overlapping", type: "table" },
];

function Shifts() {
  const [activeTab, setActiveTab]             = useState(0);
  const [records, setRecords]                 = useState([]);
  const [loading, setLoading]                 = useState(true);
  const [filterTemplate, setFilterTemplate]   = useState("All");
  const [filterShift, setFilterShift]         = useState("All");

  useEffect(() => {
    setLoading(true);
    setFilterTemplate("All");
    setFilterShift("All");
    API.get(TABS[activeTab].endpoint)
      .then((res) => {
        setRecords(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [activeTab]);

  const templates = useMemo(
    () => ["All", ...new Set(records.map((r) => r.schedule_template).filter(Boolean))],
    [records]
  );
  const shifts = useMemo(
    () => ["All", ...new Set(records.map((r) => r.shift).filter(Boolean))],
    [records]
  );

  const filtered = useMemo(() => {
    if (activeTab !== 0) return records;
    return records.filter((r) => {
      const matchTemplate = filterTemplate === "All" || r.schedule_template === filterTemplate;
      const matchShift    = filterShift    === "All" || r.shift            === filterShift;
      return matchTemplate && matchShift;
    });
  }, [records, filterTemplate, filterShift, activeTab]);

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
          <RefreshCw size={28} color="white" />
          SHIFT REPORTS
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
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px", flexWrap: "wrap", gap: "12px" }}>
          <h3 style={{ margin: 0, color: "#1e3a5f" }}>{TABS[activeTab].label}</h3>

          <div style={{ display: "flex", alignItems: "center", gap: "12px", flexWrap: "wrap" }}>
            {/* Filters — only on Shift Allocations tab */}
            {activeTab === 0 && (
              <>
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <span style={labelStyle}>SCHEDULE TEMPLATE:</span>
                  <select value={filterTemplate} onChange={(e) => setFilterTemplate(e.target.value)} style={selectStyle}>
                    {templates.map((t) => <option key={t}>{t}</option>)}
                  </select>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <span style={labelStyle}>SHIFT:</span>
                  <select value={filterShift} onChange={(e) => setFilterShift(e.target.value)} style={selectStyle}>
                    {shifts.map((s) => <option key={s}>{s}</option>)}
                  </select>
                </div>
              </>
            )}

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
        </div>

        {loading ? (
          <p>Loading...</p>
        ) : filtered.length === 0 ? (
          <p style={{ color: "#999" }}>No records found.</p>
        ) : (
          <div style={{ overflowY: "auto", maxHeight: "55vh" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ background: "#1e3a5f", color: "white" }}>
                  {Object.keys(filtered[0]).map((key) => (
                    <th key={key} style={{ padding: "12px", textAlign: "left", fontSize: "13px", position: "sticky", top: 0, background: "#1e3a5f", zIndex: 1 }}>
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
                        {val === null ? "—" : String(val)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
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

const labelStyle = {
  fontSize: "12px",
  fontWeight: 600,
  color: "#1e3a5f",
  whiteSpace: "nowrap",
};

const selectStyle = {
  padding: "7px 12px",
  borderRadius: "8px",
  border: "1px solid #d0d7e3",
  fontSize: "13px",
  color: "#1e3a5f",
  background: "white",
  cursor: "pointer",
  outline: "none",
};

export default Shifts;
