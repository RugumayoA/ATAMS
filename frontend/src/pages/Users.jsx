import { useState, useEffect, useMemo } from "react";
import API from "../components/api/axios";
import { Users as UsersIcon } from "lucide-react";
import ExportButtons from "../components/ExportButtons";

// Active Staff (1326 users) rather than All Users (1919), so exited staff
// appear only when deliberately selected.
const DEFAULT_GROUP_ID = "5760";

const ACTIVE_STAFF_ID = "5760";
const NONE_ACTIVE_ID = "1016";

// Colour by branch, shade by depth.
//   navy  = Active Staff side
//   amber = NONE Active STAFFS side (EXITED, CASUALS, BASALA, Duplicate IDs)
// Index is the group's depth, so directorates read dark and sections light.
const BRANCH_COLORS = {
  active:   ["#0f2b47", "#1e3a5f", "#2d6a9f", "#3d7fa5", "#5e9cb8", "#84b4c9"],
  inactive: ["#0f2b47", "#7a5a1c", "#8a6a2a", "#9c7c3d", "#b09055", "#c2a670"],
  neutral:  ["#333333", "#555555", "#777777", "#888888", "#999999", "#aaaaaa"],
};

// Note: option colours are honoured by Chrome, Edge and Firefox on Windows.
// Safari and most mobile browsers ignore them and fall back to plain text —
// the indentation still carries the hierarchy, so nothing is lost.
function colorForGroup(group) {
  const palette = BRANCH_COLORS[group.branch] || BRANCH_COLORS.neutral;
  return palette[Math.min(group.depth, palette.length - 1)];
}

// All nine reports. `ready` marks what is actually built.
const TABS = [
  { label: "User Information",            endpoint: "/users/information", ready: true  },
  { label: "Users on Device",             endpoint: null,                 ready: false },
  { label: "Users Without Credentials",   endpoint: null,                 ready: false },
  { label: "Users Category",              endpoint: null,                 ready: false },
  { label: "New Users",                   endpoint: null,                 ready: false },
  { label: "All Users",                   endpoint: null,                 ready: false },
  { label: "Exceptional Users",           endpoint: null,                 ready: false },
  { label: "Periods Expiring (30 Days)",  endpoint: null,                 ready: false },
  { label: "Idle Active Operators",       endpoint: null,                 ready: false },
];

const COLUMNS = [
  { key: "user_id",       label: "User ID"       },
  { key: "name",          label: "Name"          },
  { key: "department",    label: "Department"    },
  { key: "directorate",   label: "Directorate"   },
  { key: "category",      label: "Category"      },
  { key: "credentials",   label: "Credentials"   },
  { key: "operator_role", label: "Operator Role" },
  { key: "status",        label: "Status"        },
  { key: "expiry_date",   label: "Expires (EAT)" },
];

function Users() {
  const [activeTab, setActiveTab] = useState(0);
  const [groups, setGroups]       = useState([]);
  const [groupId, setGroupId]     = useState(DEFAULT_GROUP_ID);
  const [search, setSearch]       = useState("");
  const [report, setReport]       = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState("");

  const tab = TABS[activeTab];

  // The group picker is one fast call, so it loads on mount. The report is not
  // — a large group is many sequential requests to BioStar.
  useEffect(() => {
    API.get("/users/groups")
      .then((res) => setGroups(res.data.groups || []))
      .catch(() => setError("Could not load the group list. Check that you are on the CAA network."));
  }, []);

  // Tag every group with the branch it belongs to. The list arrives ordered
  // depth-first, so the most recent depth-1 entry is the current branch.
  const styledGroups = useMemo(() => {
    let branch = "neutral";

    return groups.map((g) => {
      if (g.depth === 1) {
        if (g.id === ACTIVE_STAFF_ID) branch = "active";
        else if (g.id === NONE_ACTIVE_ID) branch = "inactive";
        else branch = "neutral";
      } else if (g.depth === 0) {
        branch = "neutral";
      }
      return { ...g, branch };
    });
  }, [groups]);

  // Directorate name -> colour, so table rows tie back to the picker.
  const directorateColors = useMemo(() => {
    const map = {};
    styledGroups.forEach((g) => {
      if (g.is_directorate) map[g.name] = colorForGroup(g);
    });
    return map;
  }, [styledGroups]);

  const rows = report?.rows || [];

  const term = search.trim().toLowerCase();
  const filtered = !term
    ? rows
    : rows.filter((r) =>
        [r.user_id, r.name, r.department, r.directorate, r.category]
          .join(" ").toLowerCase().includes(term)
      );

  const selectedGroup = styledGroups.find((g) => g.id === groupId);
  const selectedGroupName = selectedGroup?.name || "";
  const groupSlug = selectedGroupName.toLowerCase().replace(/\s+/g, "_");

  function handleFetch() {
    if (!tab.ready) return;
    setError("");
    setLoading(true);
    setReport(null);

    API.get(tab.endpoint, { params: { group_id: groupId } })
      .then((res) => { setReport(res.data); setLoading(false); })
      .catch((err) => {
        console.error(err);
        setError(err.response?.data?.message || "Failed to fetch data.");
        setLoading(false);
      });
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
        <h1 style={{ margin: 0, display: "flex", alignItems: "center", gap: "10px", fontSize: "22px", fontWeight: 600, color: "white" }}>
          <UsersIcon size={28} color="white" />
          USERS REPORTS
        </h1>
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px", flexWrap: "wrap" }}>
        {TABS.map((t, i) => (
          <button
            key={i}
            onClick={() => { setActiveTab(i); setReport(null); setError(""); setSearch(""); }}
            style={{
              padding: "10px 16px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              fontWeight: activeTab === i ? "bold" : "normal",
              background: activeTab === i ? "#1e3a5f" : "#f0f0f0",
              color: activeTab === i ? "white" : t.ready ? "#333" : "#888",
              fontSize: "13px",
            }}
          >
            {t.label}
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
        <div style={{ flex: 1, minWidth: "280px" }}>
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Group</label>
          <select
            value={groupId}
            onChange={(e) => setGroupId(e.target.value)}
            disabled={!tab.ready || groups.length === 0}
            style={{
              width: "100%", padding: "8px 10px", borderRadius: "8px",
              border: "1px solid #E4E7EB", fontSize: "13px", boxSizing: "border-box",
              background: "white",
              color: selectedGroup ? colorForGroup(selectedGroup) : "#333",
              fontWeight: selectedGroup && selectedGroup.depth <= 2 ? 600 : 400,
            }}
          >
            {styledGroups.map((g) => (
              <option
                key={g.id}
                value={g.id}
                style={{
                  color: colorForGroup(g),
                  fontWeight: g.depth <= 2 ? 700 : 400,
                }}
              >
                {"\u00A0".repeat(g.depth * 3)}{g.name}{g.direct_user_count > 0 ? ` (${g.direct_user_count})` : ""}
              </option>
            ))}
          </select>
        </div>
        <div style={{ flex: 1, minWidth: "200px" }}>
          <label style={{ display: "block", fontSize: "12px", color: "#666", marginBottom: "4px" }}>Filter results (optional)</label>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="e.g. Okot, 1141, Licensing"
            disabled={!tab.ready}
            style={{ width: "100%", padding: "8px 10px", borderRadius: "8px", border: "1px solid #E4E7EB", fontSize: "13px", boxSizing: "border-box" }}
          />
        </div>
        <button
          onClick={handleFetch}
          disabled={!tab.ready || loading}
          style={{
            padding: "9px 20px", borderRadius: "8px", border: "none",
            background: "#1e3a5f", color: "white", fontWeight: 600,
            fontSize: "13px", cursor: tab.ready && !loading ? "pointer" : "not-allowed",
            opacity: tab.ready && !loading ? 1 : 0.55,
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
          <h3 style={{ margin: 0, color: "#1e3a5f" }}>{tab.label}</h3>

          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <ExportButtons
              data={filtered}
              filename={`user_${tab.label.toLowerCase().replace(/\s+/g, "_")}_${groupSlug}`}
              title={`${tab.label} — ${selectedGroupName}`}
              columns={COLUMNS}
            />
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

        {error && <p style={{ color: "#c62828" }}>{error}</p>}

        {report && !error && !loading && (
          <p style={{ color: "#666", fontSize: "13px", marginTop: 0 }}>
            <strong>{report.group.name}</strong>
            {report.group.directorate ? ` · ${report.group.directorate}` : ""}
            {" — "}
            {filtered.length === rows.length
              ? `${report.returned} of ${report.reported_total} users`
              : `${filtered.length} of ${report.returned} shown`}
            {!report.complete && (
              <span style={{ color: "#b06a12", fontWeight: 600 }}>
                {" "}· incomplete: fewer rows returned than the server reported
              </span>
            )}
            {report.unassigned_count > 0 && (
              <span style={{ color: "#b06a12" }}>
                {" "}· {report.unassigned_count} user{report.unassigned_count !== 1 ? "s" : ""} with no directorate assigned
              </span>
            )}
          </p>
        )}

        {!tab.ready ? (
          <p style={{ color: "#999" }}>This report has not been built yet.</p>
        ) : loading ? (
          <p>Loading... Large groups are fetched in pages of 100, so this can take a while.</p>
        ) : !error && filtered.length === 0 ? (
          <p style={{ color: "#999" }}>
            {report
              ? "No users match the current group and filter."
              : "No records found. Choose a group above and click Fetch Report."}
          </p>
        ) : !error && (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#1e3a5f", color: "white" }}>
                {COLUMNS.map((col) => (
                  <th key={col.key} style={{ padding: "12px", textAlign: "left", fontSize: "13px" }}>
                    {col.label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map((rec, i) => (
                <tr key={rec.user_id} style={{
                  background: rec.unassigned ? "#fffaf0" : i % 2 === 0 ? "#f9f9f9" : "white",
                  borderBottom: "1px solid #eee"
                }}>
                  {COLUMNS.map((col) => (
                    <td
                      key={col.key}
                      style={
                        col.key === "directorate" && directorateColors[rec.directorate]
                          ? { ...td, color: directorateColors[rec.directorate], fontWeight: 600 }
                          : td
                      }
                    >
                      {rec[col.key] === null || rec[col.key] === "" ? "—" : String(rec[col.key])}
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

export default Users;