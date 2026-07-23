import { useEffect, useState, useMemo } from "react";
import API from "../components/api/axios";
import ExportButtons from "../components/ExportButtons";
import { UtensilsCrossed, RefreshCw } from "lucide-react";

/**
 * Meal punch event codes seen in live data.
 *
 * PROVISIONAL - confirm with IT before treating these as authoritative.
 * Derived from the device trigger_actions config on the BioStar server:
 *   4865 IDENTIFY_SUCCESS_FINGERPRINT
 *   4098 VERIFY_SUCCESS_ID_FINGERPRINT
 *   6405 / 6406 timed anti-passback (a repeat punch, i.e. denied)
 */
const EVENT_CODE_LABELS = {
  "4865": { label: "Identified", color: "#1b5e20", bg: "#e8f5e9", isMeal: true },
  "4098": { label: "Verified",   color: "#1b5e20", bg: "#e8f5e9", isMeal: true },
  "4356": { label: "Failed : fingerprint",         color: "#b71c1c", bg: "#fdecea", isMeal: false },
  "6403": { label: "Denied : user expired",        color: "#b71c1c", bg: "#fdecea", isMeal: false },
  "6405": { label: "Denied : anti-passback",       color: "#b71c1c", bg: "#fdecea", isMeal: false },
  "6406": { label: "Denied : timed anti-passback", color: "#b71c1c", bg: "#fdecea", isMeal: false },
  "8704": { label: "Record updated", color: "#555", bg: "#f0f0f0", isMeal: false },
};

const codeInfo = (code) =>
  EVENT_CODE_LABELS[code] || { label: `Code ${code}`, color: "#555", bg: "#f0f0f0" };
const todayISO = () => new Date().toISOString().slice(0, 10);

function Meals() {
  const [devices, setDevices] = useState([]);
  const [deviceId, setDeviceId] = useState("");
  const [day, setDay] = useState(todayISO());

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeFilter, setActiveFilter] = useState("all");

  // Load the device list once. Drives the picker so device ids
  // are never hardcoded in the frontend.
  useEffect(() => {
    API.get("/meals/devices")
      .then((res) => {
        const list = res.data.devices || [];
        setDevices(list);
        if (list.length) setDeviceId(list[0].device_id);
      })
      .catch((err) => {
        console.error(err);
        setError("Could not load the meal device list.");
      });
  }, []);

  // Fetch the staff report whenever device or date changes.
  useEffect(() => {
    if (!deviceId || !day) return;

    setLoading(true);
    setError(null);

    API.get("/meals/staff_by_device", { params: { device_id: deviceId, date: day } })
      .then((res) => {
        setReport(res.data);
        setActiveFilter("all");
      })
      .catch((err) => {
        console.error(err);
        setError(
          err.response?.data?.error ||
            "Could not load the meal report. Check the VPN / office network connection."
        );
        setReport(null);
      })
      .finally(() => setLoading(false));
  }, [deviceId, day]);

  const staff = report?.staff || [];
  const repeats = staff.filter((s) => s.punchCount > 1);

  const filtered = useMemo(() => {
    if (activeFilter === "repeat") return repeats;
    return staff;
  }, [staff, repeats, activeFilter]);

  // Flattened shape for CSV / PDF / Excel export.
  const exportRows = useMemo(
    () =>
      filtered.map((s) => ({
        "Staff ID": s.userId,
        "Name": s.userName,
        "Department": s.userGroupName,
        "Punches": s.punchCount,
        "Times": s.times.join(", "),
        "Status": s.eventCodes.map((c) => codeInfo(c).label).join(", "),
      })),
    [filtered]
  );

  const buttons = report
    ? [
        { key: "all", label: "Staff", value: report.staffCount, color: "#1e3a5f" },
        { key: "punches", label: "Total Punches", value: report.totalPunches, color: "#2e7d32", static: true },
        { key: "repeat", label: "Repeat Punches", value: repeats.length, color: "#c62828" },
      ]
    : [];

  return (
    <div style={{ fontFamily: "Segoe UI, sans-serif", padding: "30px" }}>
      {/* Header */}
      <div
        style={{
          background: "linear-gradient(135deg, #1e3a5f, #2d6a9f)",
          borderRadius: "16px",
          padding: "30px",
          color: "white",
          marginBottom: "24px",
        }}
      >
        <h1
          style={{
            margin: 0,
            display: "flex",
            alignItems: "center",
            gap: "10px",
            fontSize: "22px",
            fontWeight: 600,
            color: "white",
          }}
        >
          <UtensilsCrossed size={28} color="white" />
          MEALS REPORTS
        </h1>
        <p style={{ margin: "8px 0 0 38px", fontSize: "13px", opacity: 0.85 }}>
          Staff who punched at each meal device
        </p>
      </div>

      {/* Controls */}
      <div
        style={{
          background: "white",
          borderRadius: "12px",
          padding: "18px 24px",
          boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
          marginBottom: "24px",
          display: "flex",
          gap: "20px",
          alignItems: "flex-end",
          flexWrap: "wrap",
        }}
      >
        <div>
          <label style={labelStyle}>Meal Device</label>
          <select
            value={deviceId}
            onChange={(e) => setDeviceId(e.target.value)}
            style={inputStyle}
          >
            {devices.map((d) => (
              <option key={d.device_id} value={d.device_id}>
                {d.device_name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label style={labelStyle}>Date</label>
          <input
            type="date"
            value={day}
            onChange={(e) => setDay(e.target.value)}
            style={inputStyle}
          />
        </div>

        <button
          onClick={() => setDay((d) => d)}
          disabled={loading}
          style={{
            ...inputStyle,
            display: "flex",
            alignItems: "center",
            gap: "8px",
            background: "#1e3a5f",
            color: "white",
            border: "none",
            cursor: loading ? "default" : "pointer",
            opacity: loading ? 0.6 : 1,
          }}
        >
          <RefreshCw size={15} />
          {loading ? "Loading..." : "Refresh"}
        </button>

        {report && (
          <div style={{ marginLeft: "auto" }}>
            <ExportButtons
              data={exportRows}
              filename={`meals_${report.device_name.replace(/\s+/g, "_")}_${report.date}`}
              title={`Meal Report - ${report.device_name} - ${report.date}`}
            />
          </div>
        )}
      </div>

      {/* Error */}
      {error && (
        <div
          style={{
            background: "#fdecea",
            border: "1px solid #f5c6cb",
            color: "#c62828",
            borderRadius: "10px",
            padding: "14px 18px",
            marginBottom: "24px",
            fontSize: "14px",
          }}
        >
          {error}
        </div>
      )}

      {/* Filter buttons */}
      {report && !error && (
        <div style={{ display: "flex", gap: "12px", marginBottom: "24px", flexWrap: "wrap" }}>
          {buttons.map((btn) => {
            const isActive = !btn.static && activeFilter === btn.key;
            return (
              <button
                key={btn.key}
                onClick={() => !btn.static && setActiveFilter(btn.key)}
                style={{
                  border: `2px solid ${btn.color}`,
                  borderRadius: "999px",
                  padding: "8px 20px",
                  background: isActive ? btn.color : "white",
                  fontSize: "13px",
                  color: isActive ? "white" : "#333",
                  fontWeight: 500,
                  cursor: btn.static ? "default" : "pointer",
                  transition: "all 0.15s",
                }}
              >
                {btn.label} :{" "}
                <span style={{ fontWeight: 700, color: isActive ? "white" : btn.color }}>
                  {btn.value}
                </span>
              </button>
            );
          })}
        </div>
      )}

      {/* Staff table */}
      <div
        style={{
          background: "white",
          borderRadius: "12px",
          padding: "24px",
          boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: "16px",
          }}
        >
          <h3 style={{ margin: 0, color: "#1e3a5f" }}>
            {report ? `${report.device_name} — ${report.date}` : "Staff Meal Records"}
          </h3>
          <span
            style={{
              background: "#1e3a5f",
              color: "white",
              borderRadius: "20px",
              padding: "4px 14px",
              fontSize: "13px",
              fontWeight: 500,
            }}
          >
            {filtered.length} staff
          </span>
        </div>

        {loading ? (
          <p style={{ color: "#999" }}>Loading...</p>
        ) : filtered.length === 0 ? (
          <p style={{ color: "#999" }}>
            No staff punched at this device on this date.
          </p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#1e3a5f", color: "white" }}>
                <th style={th}>STAFF ID</th>
                <th style={th}>NAME</th>
                <th style={th}>DEPARTMENT</th>
                <th style={th}>PUNCHES</th>
                <th style={th}>TIMES</th>
                <th style={th}>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((s, i) => (
                <tr
                  key={s.userId}
                  style={{
                    background: i % 2 === 0 ? "#f9f9f9" : "white",
                    borderBottom: "1px solid #eee",
                  }}
                >
                  <td style={td}>{s.userId}</td>
                  <td style={td}>{s.userName || "—"}</td>
                  <td style={td}>{s.userGroupName || "—"}</td>
                  <td style={{ ...td, fontWeight: s.punchCount > 1 ? 700 : 400 }}>
                    {s.punchCount}
                  </td>
                  <td style={td}>{s.times.join(", ")}</td>
                  <td style={td}>
                    {s.eventCodes.map((c, j) => {
                      const info = codeInfo(c);
                      return (
                        <span
  key={j}
  style={{
    display: "inline-block",
    marginRight: "6px",
    marginBottom: "4px",
    padding: "3px 8px",
    borderRadius: "4px",
    fontSize: "11px",
    fontWeight: 600,
    color: info.color,
    background: info.bg,
    border: `1px solid ${info.color}22`,
  }}
>
  {info.label}
</span>
                      );
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

const th = { padding: "12px", textAlign: "left", fontSize: "13px" };

const td = {
  padding: "12px",
  fontSize: "13px",
  color: "#333",
  textAlign: "left",
};

const labelStyle = {
  display: "block",
  fontSize: "12px",
  color: "#666",
  marginBottom: "6px",
  fontWeight: 500,
};

const inputStyle = {
  padding: "9px 14px",
  borderRadius: "8px",
  border: "1px solid #ccc",
  fontSize: "13px",
  fontFamily: "inherit",
  minWidth: "180px",
};

export default Meals;