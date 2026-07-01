import { useState } from "react";
import API from "../components/api/axios";
import { ClipboardList } from "lucide-react";

const TABS = [
  { label: "Summary",         endpoint: "/attendance/summary",         type: "summary"  },
  { label: "By Department",   endpoint: "/attendance/by-department",   type: "dept"     },
  { label: "Public Holidays", endpoint: "/attendance/public-holidays", type: "dated"    },
  { label: "Weekends",        endpoint: "/attendance/weekends",        type: "dated"    },
];

const th = { padding: "12px", textAlign: "left", fontSize: "13px", fontWeight: 600 };
const td = { padding: "12px", fontSize: "13px", color: "#333", textAlign: "left" };

function RecordTable({ records }) {
  if (!records || records.length === 0)
    return <p style={{ color: "#999" }}>No records found.</p>;
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", tableLayout: "fixed" }}>
      <colgroup>
        <col style={{ width: "15%" }} />
        <col style={{ width: "30%" }} />
        <col style={{ width: "25%" }} />
        <col style={{ width: "15%" }} />
        <col style={{ width: "15%" }} />
      </colgroup>
      <thead>
        <tr style={{ background: "#1e3a5f", color: "white" }}>
          <th style={th}>Employee ID</th>
          <th style={th}>Name</th>
          <th style={th}>Department</th>
          <th style={th}>In Time</th>
          <th style={th}>Out Time</th>
        </tr>
      </thead>
      <tbody>
        {records.map((r, i) => (
          <tr key={i} style={{ background: i % 2 === 0 ? "#f9f9f9" : "white", borderBottom: "1px solid #eee" }}>
            <td style={td}>{r.userId}</td>
            <td style={td}>{r.userName}</td>
            <td style={td}>{r.userGroupName}</td>
            <td style={td}>{r.inTime}</td>
            <td style={td}>{r.outTime}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function SummaryView({ data }) {
  const [activeFilter, setActiveFilter] = useState("present");

  const cards = [
    { label: "Present", key: "present", count: data.present_count, color: "#2e7d32" },
    { label: "Absent",  key: "absent",  count: data.absent_count,  color: "#c62828" },
  ];

  return (
    <>
      <div style={{ display: "flex", gap: "10px", marginBottom: "16px", flexWrap: "wrap" }}>
        {cards.map((card) => (
          <div
            key={card.key}
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
            {card.label}: <strong>{card.count}</strong>
          </div>
        ))}
      </div>
      <RecordTable records={data[activeFilter]} />
    </>
  );
}

function DeptView({ data }) {
  const departments = Object.keys(data);
  const [activeDept, setActiveDept] = useState(departments[0] || "");
  const [activeFilter, setActiveFilter] = useState("present");

  if (departments.length === 0)
    return <p style={{ color: "#999" }}>No department data found.</p>;

  const deptData = data[activeDept] || {};

  return (
    <>
      {/* Department selector */}
      <div style={{ marginBottom: "16px" }}>
        <select
          value={activeDept}
          onChange={(e) => { setActiveDept(e.target.value); setActiveFilter("present"); }}
          style={{ padding: "6px 10px", borderRadius: "8px", border: "1px solid #E4E7EB", fontSize: "13px" }}
        >
          {departments.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
      </div>

      {/* Present / Absent cards */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "16px", flexWrap: "wrap" }}>
        {[
          { label: "Present", key: "present", count: deptData.present_count, color: "#2e7d32" },
          { label: "Absent",  key: "absent",  count: deptData.absent_count,  color: "#c62828" },
        ].map((card) => (
          <div
            key={card.key}
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
            {card.label}: <strong>{card.count}</strong>
          </div>
        ))}
      </div>
      <RecordTable records={deptData[activeFilter]} />
    </>
  );
}

function DatedView({ data }) {
  const dates = Object.keys(data);
  const [activeDate, setActiveDate] = useState(dates[0] || "");
  const [activeFilter, setActiveFilter] = useState("present");

  if (dates.length === 0)
    return <p style={{ color: "#999" }}>No data found for selected range.</p>;

  const dateData = data[activeDate] || {};

  return (
    <>
      {/* Date selector */}
      <div style={{ marginBottom: "16px" }}>
        <select
          value={activeDate}
          onChange={(e) => { setActiveDate(e.target.value); setActiveFilter("present"); }}
          style={{ padding: "6px 10px", borderRadius: "8px", border: "1px solid #E4E7EB", fontSize: "13px" }}
        >
          {dates.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
      </div>

      {/* Present / Absent cards */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "16px", flexWrap: "wrap" }}>
        {[
          { label: "Present", key: "present", count: dateData.present_count, color: "#2e7d32" },
          { label: "Absent",  key: "absent",  count: dateData.absent_count,  color: "#c62828" },
        ].map((card) => (
          <div
            key={card.key}
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
            {card.label}: <strong>{card.count}</strong>
          </div>
        ))}
      </div>
      <RecordTable records={dateData[activeFilter]} />
    </>
  );
}

function Attendance() {
  const [activeTab, setActiveTab] = useState(0);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate]     = useState("");
  const [userIds, setUserIds]     = useState("");
  const [data, setData]           = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState("");

  function handleFetch() {
    if (!startDate || !endDate || !userIds.trim()) {
      setError("Please fill in all fields before fetching.");
      return;
    }
    setError("");
    setLoading(true);
    setData(null);

    API.post(TABS[activeTab].endpoint, {
      start_date: startDate,
      end_date:   endDate,
      user_ids:   userIds,
    })
      .then((res) => { setData(res.data); setLoading(false); })
      .catch((err) => { console.error(err); setError("Failed to fetch data."); setLoading(false); });
  }

  const currentType = TABS[activeTab].type;

  return (
    <div style={{ fontFamily: "Segoe UI, sans-serif", padding: "30px" }}>

      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #1e3a5f, #2d6a9f)",
        borderRadius: "16px",
        padding: "30px",
        color: "white",
        marginBottom: "30px",
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
            onClick={() => { setActiveTab(i); setData(null); setError(""); }}
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
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Employee IDs (comma separated)</label>
          <input type="text" value={userIds} onChange={(e) => setUserIds(e.target.value)}
            placeholder="e.g. 01141, 01142, 770"
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

      {/* Results */}
      <div style={{ background: "white", borderRadius: "12px", padding: "24px", boxShadow: "0 2px 12px rgba(0,0,0,0.08)" }}>
        <h3 style={{ margin: "0 0 16px", color: "#1e3a5f" }}>{TABS[activeTab].label}</h3>

        {error   && <p style={{ color: "#c62828" }}>{error}</p>}
        {loading && <p>Loading...</p>}

        {!loading && !error && !data && (
          <p style={{ color: "#999" }}>Fill in the filters above and click Fetch Report.</p>
        )}

        {!loading && data && currentType === "summary" && <SummaryView data={data} />}
        {!loading && data && currentType === "dept"    && <DeptView    data={data} />}
        {!loading && data && currentType === "dated"   && <DatedView   data={data} />}
      </div>
    </div>
  );
}

export default Attendance;