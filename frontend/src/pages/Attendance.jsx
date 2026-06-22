import { useEffect, useState } from "react";
import API from "../components/api/axios";
import { ClipboardList } from "lucide-react";

const TABS = [
  { label: "Summary",         endpoint: "/attendance/summary",        type: "summary" },
  { label: "By Department",   endpoint: "/attendance/department",     type: "dept"    },
  { label: "Public Holidays", endpoint: "/attendance/public-holiday", type: "staff"   },
  { label: "Weekends",        endpoint: "/attendance/weekend",        type: "staff"   },
];

function DeptSection({ data, activeFilter, setActiveFilter, deptFilter }) {
  const allRecords = data[FILTER_MAP[activeFilter]] || [];
  const filtered = deptFilter === "All" ? allRecords : allRecords.filter(r => r.department === deptFilter);

  return (
    <>
      <div style={{ display: "flex", gap: "10px", marginBottom: "16px", flexWrap: "wrap" }}>
        {[
          { label: "Total",    key: "total",    value: data.total,    color: "#1e3a5f" },
          { label: "Present",  key: "present",  value: data.present,  color: "#2e7d32" },
          { label: "Absent",   key: "absent",   value: data.absent,   color: "#c62828" },
          { label: "On Leave", key: "on_leave", value: data.on_leave, color: "#f57f17" },
        ].map((card) => (
          <div
            key={card.label}
            onClick={() => setActiveFilter(card.key)}
            style={{
              background: activeFilter === card.key ? card.color : "#fafafa",
              border: `1px solid ${card.color}`,
              borderRadius: "8px",
              padding: "8px 16px",
              cursor: "pointer",
              fontSize: "13px",
              fontWeight: 500,
              color: activeFilter === card.key ? "white" : "#333",
              transition: "background 0.2s",
            }}
          >
            {card.label} : <strong>{card.value}</strong>
          </div>
        ))}
      </div>
      <DeptTable records={filtered} />
    </>
  );
}

function DeptTable({ records }) {
  if (!records || records.length === 0)
    return <p style={{ color: "#999" }}>No records found.</p>;
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", tableLayout: "fixed" }}>
      <colgroup>
        <col style={{ width: "20%" }} />
        <col style={{ width: "20%" }} />
        <col style={{ width: "35%" }} />
        <col style={{ width: "25%" }} />
      </colgroup>
      <thead>
        <tr style={{ background: "#1e3a5f", color: "white" }}>
          <th style={th}>Department</th>
          <th style={th}>Employee ID</th>
          <th style={th}>Name</th>
          <th style={th}>Card No</th>
        </tr>
      </thead>
      <tbody>
        {records.map((r, i) => (
          <tr key={i} style={{ background: i % 2 === 0 ? "#f9f9f9" : "white", borderBottom: "1px solid #eee" }}>
            <td style={td}>{r.department}</td>
            <td style={td}>{r.employee_id}</td>
            <td style={td}>{r.name}</td>
            <td style={td}>{r.card_id}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function StaffTable({ records }) {
  if (!records || records.length === 0)
    return <p style={{ color: "#999" }}>No records found.</p>;
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", tableLayout: "fixed" }}>
      <colgroup>
        <col style={{ width: "25%" }} />
        <col style={{ width: "50%" }} />
        <col style={{ width: "25%" }} />
      </colgroup>
      <thead>
        <tr style={{ background: "#1e3a5f", color: "white" }}>
          <th style={th}>Employee ID</th>
          <th style={th}>Name</th>
          <th style={th}>Card No</th>
        </tr>
      </thead>
      <tbody>
        {records.map((r, i) => (
          <tr key={i} style={{ background: i % 2 === 0 ? "#f9f9f9" : "white", borderBottom: "1px solid #eee" }}>
            <td style={td}>{r.employee_id}</td>
            <td style={td}>{r.name}</td>
            <td style={td}>{r.card_id}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const FILTER_MAP = {
  total:    "all_records",
  present:  "present_records",
  absent:   "absent_records",
  on_leave: "on_leave_records",
};

function Attendance() {
  const [activeTab, setActiveTab]       = useState(0);
  const [data, setData]                 = useState(null);
  const [loading, setLoading]           = useState(true);
  const [activeFilter, setActiveFilter] = useState("total");
  const [deptFilter, setDeptFilter]     = useState("All");

  useEffect(() => {
    setLoading(true);
    setActiveFilter("total");
    setDeptFilter("All");
    API.get(TABS[activeTab].endpoint)
      .then((res) => {
        setData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [activeTab]);

  const currentType = TABS[activeTab].type;

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
          <ClipboardList size={28} color="white" />
          ATTENDANCE REPORTS
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

      {/* Content */}
      <div style={{
        background: "white",
        borderRadius: "12px",
        padding: "24px",
        boxShadow: "0 2px 12px rgba(0,0,0,0.08)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "16px" }}>
          <h3 style={{ margin: 0, color: "#1e3a5f" }}>{TABS[activeTab].label}</h3>
          {currentType === "dept" && data && (
            <select
              value={deptFilter}
              onChange={(e) => setDeptFilter(e.target.value)}
              style={{
                padding: "6px 10px",
                borderRadius: "8px",
                border: "1px solid #E4E7EB",
                fontSize: "13px",
                color: "#333",
                background: "white",
                cursor: "pointer",
              }}
            >
              {["All", ...new Set((data.all_records || []).map(r => r.department))].map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          )}
        </div>

        {loading ? (
          <p>Loading...</p>

        ) : currentType === "summary" && data ? (
          <>
            {/* ── Summary Cards (clickable) ── */}
            <div style={{ display: "flex", gap: "10px", marginBottom: "24px", flexWrap: "wrap" }}>
              {[
                { label: "Total",    key: "total",    value: data.total,    color: "#1e3a5f" },
                { label: "Present",  key: "present",  value: data.present,  color: "#2e7d32" },
                { label: "Absent",   key: "absent",   value: data.absent,   color: "#c62828" },
                { label: "On Leave", key: "on_leave", value: data.on_leave, color: "#f57f17" },
              ].map((card) => (
                <div
                  key={card.label}
                  onClick={() => setActiveFilter(card.key)}
                  style={{
                    background: activeFilter === card.key ? card.color : "#fafafa",
                    border: `1px solid ${card.color}`,
                    borderRadius: "8px",
                    padding: "8px 16px",
                    cursor: "pointer",
                    fontSize: "13px",
                    fontWeight: 500,
                    color: activeFilter === card.key ? "white" : "#333",
                    transition: "background 0.2s",
                  }}
                >
                  {card.label} : <strong>{card.value}</strong>
                </div>
              ))}
            </div>
            {/* ── Filtered Staff List ── */}
            <StaffTable records={data[FILTER_MAP[activeFilter]]} />
          </>

        ) : currentType === "dept" && data ? (
          <DeptSection data={data} activeFilter={activeFilter} setActiveFilter={setActiveFilter} deptFilter={deptFilter} />

        ) : currentType === "staff" && Array.isArray(data) ? (
          <StaffTable records={data} />

        ) : (
          <p style={{ color: "#999" }}>No data available.</p>
        )}
      </div>
    </div>
  );
}

const td = { padding: "12px", fontSize: "13px", color: "#333", textAlign: "left" };
const th = { padding: "12px", textAlign: "left", fontSize: "13px", fontWeight: 600 };

export default Attendance;