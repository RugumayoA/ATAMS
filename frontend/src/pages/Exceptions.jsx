import { useState } from "react";
import API from "../components/api/axios";
import { AlertTriangle } from "lucide-react";

const TABS = [
  { label: "Late Clock In",         endpoint: "/time_exceptions/late_clock_in"         },
  { label: "Early Clock Out",       endpoint: "/time_exceptions/early_clock_out"       },
  { label: "Early Clock In",        endpoint: "/time_exceptions/early_clock_in"        },
  { label: "Late Clock Out",        endpoint: "/time_exceptions/late_clock_out"        },
  { label: "Incomplete Attendance", endpoint: "/time_exceptions/incomplete_attendance" },
  { label: "Abscondment",           endpoint: "/time_exceptions/abscondment"           },
  { label: "Meal Punch Only",       endpoint: "/time_exceptions/meal_punch_only"       },
  { label: "Low Working Hours",     endpoint: "/time_exceptions/low_working_hours"     },
];

function Exceptions() {
  const [activeTab, setActiveTab] = useState(0);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate]     = useState("");
  const [userIds, setUserIds]     = useState("");
  const [records, setRecords]     = useState([]);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState("");

  function handleFetch() {
    if (!startDate || !endDate) {
      setError("Please select a start and end date before fetching.");
      return;
    }
    setError("");
    setLoading(true);
    setRecords([]);

    API.post(TABS[activeTab].endpoint, {
      start_date: startDate,
      end_date:   endDate,
      user_ids:   userIds.trim() ? userIds.split(",").map((id) => id.trim()) : undefined,
    })
      .then((res) => { setRecords(res.data.records || []); setLoading(false); })
      .catch((err) => { console.error(err); setError("Failed to fetch data."); setLoading(false); });
  }

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
        <h1 style={{ margin: 0, display: "flex", alignItems: "center", gap: "10px" , fontSize: "22px", fontWeight: 600, color: "white"}}>
         <AlertTriangle size={28} color="white" />
         TIME EXCEPTIONS REPORTS
       </h1>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px", flexWrap: "wrap" }}>
        {TABS.map((tab, i) => (
          <button
            key={i}
            onClick={() => { setActiveTab(i); setRecords([]); setError(""); }}
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

      {/* Filters */}
      <div style={{
        background: "white",
        borderRadius: "12px",
        padding: "20px 24px",
        boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
        marginBottom: "20px",
        display: "flex",
        gap: "16px",
        flexWrap: "wrap",
        alignItems: "flex-end",
      }}>
        <div>
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Start Date</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)}
            style={{ padding: "8px 10px", borderRadius: "8px", border: "1px solid #E4E7EB", fontSize: "13px" }} />
        </div>
        <div>
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>End Date</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)}
            style={{ padding: "8px 10px", borderRadius: "8px", border: "1px solid #E4E7EB", fontSize: "13px" }} />
        </div>
        <div style={{ flex: 1, minWidth: "200px" }}>
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Employee IDs (comma separated, optional)</label>
          <input type="text" value={userIds} onChange={(e) => setUserIds(e.target.value)}
            placeholder="e.g. 1141, 1142"
            style={{ width: "100%", padding: "8px 10px", borderRadius: "8px", border: "1px solid #E4E7EB", fontSize: "13px", boxSizing: "border-box" }} />
        </div>
        <button
          onClick={handleFetch}
          style={{
            padding: "9px 20px", borderRadius: "8px", border: "none",
            background: "#1e3a5f", color: "white", fontWeight: 600,
            fontSize: "13px", cursor: "pointer",
          }}
        >
          Fetch Report
        </button>
      </div>

      {/* Table */}
      <div style={{
        background: "white",
        borderRadius: "12px",
        padding: "24px",
        boxShadow: "0 2px 12px rgba(0,0,0,0.08)"
      }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px" }}>
          <h3 style={{ margin: 0, color: "#1e3a5f" }}>
            {TABS[activeTab].label}
          </h3>
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

        {error && <p style={{ color: "#c62828" }}>{error}</p>}

        {loading ? <p>Loading...</p> : !error && records.length === 0 ? (
          <p style={{ color: "#999" }}>No records found. Fill in the filters above and click Fetch Report.</p>
        ) : !error && (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#1e3a5f", color: "white" }}>
                {Object.keys(records[0]).map((key) => (
                  <th key={key} style={{ padding: "12px", textAlign: "left", fontSize: "13px" }}>
                    {key.replace(/_/g, " ")}
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
  color: "#333"
};

export default Exceptions;
