import { useEffect, useState } from "react";
import API from "../components/api/axios";
import { Users as UsersIcon, AlertTriangle, UserPlus } from "lucide-react";

const TABS = [
  { label: "All Users",        endpoint: "/users/all"            },
  { label: "New Users",        endpoint: "/users/new"            },
  { label: "No Credentials",   endpoint: "/users/no-credentials" },
  { label: "Expiring Soon",    endpoint: "/users/expiring-soon"  },
  { label: "On Device",        endpoint: "/users/active"         },
  { label: "Exceptional",      endpoint: "/users/exceptional"    },
];


const C = {
  ink: "#101826",
  navy: "#1e3a5f",
  sky: "#2C72B0",
  mute: "#6B7785",
  border: "#E4E7EB",
  runway: "#F3F5F7",
  green: "#2F8F5B",
  red: "#C9483D",
};

const MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";

const cardStyle = {
  background: "white",
  borderRadius: "12px",
  padding: "24px",
  border: `1px solid ${C.border}`,
};

function Users() {
  const [activeTab, setActiveTab] = useState(0);
  const [users, setUsers]         = useState([]);
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    setLoading(true);
    API.get(TABS[activeTab].endpoint)
      .then((res) => {
        setUsers(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [activeTab]);

  const summaryCards = [
    { label: "Total Users", value: users.length, color: C.sky, icon: UsersIcon },
    { label: "No Credentials", value: users.filter(u => !u.has_credentials).length, color: C.red, icon: AlertTriangle },
    { label: "New Users", value: users.filter(u => u.is_new_user).length, color: C.green, icon: UserPlus },
  ];

  return (
    <div style={{ fontFamily: "Segoe UI, sans-serif", padding: "30px" }}>

      {/* Header */}
      <div style={{
        background: `linear-gradient(110deg, ${C.navy} 0%, ${C.sky} 100%)`,
        borderRadius: "16px",
        padding: "30px",
        color: "white",
        marginBottom: "30px",
        display: "flex",
        alignItems: "center",
        gap: "12px",
      }}>
        <UsersIcon size={24} />
        <h1 style={{ margin: 0, fontSize: "22px", fontWeight: 600, color: "white" }}> USER REPORTS</h1>
      </div>


      {/* Tabs */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "20px", flexWrap: "wrap" }}>
        {TABS.map((tab, i) => (
          <button
            key={i}
            onClick={() => setActiveTab(i)}
            style={{
              padding: "10px 18px",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              fontWeight: activeTab === i ? 600 : 400,
              background: activeTab === i ? C.navy : C.runway,
              color: activeTab === i ? "white" : C.mute,
              fontSize: "13px",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Table */}
      <div style={cardStyle}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "16px" }}>
          <h3 style={{ margin: 0, color: C.ink, fontSize: "15px" }}>
            {TABS[activeTab].label}
          </h3>
          <span style={{
            background: C.navy,
            color: "white",
            borderRadius: "20px",
            padding: "4px 14px",
            fontSize: "13px",
            fontWeight: 500,
          }}>
            {users.length} record{users.length !== 1 ? "s" : ""}
          </span>
        </div>

        {loading ? (
          <p style={{ color: C.mute }}>Loading...</p>
        ) : users.length === 0 ? (
          <p style={{ color: C.mute }}>No records found.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: C.navy, color: "white" }}>
                {["ID", "Name", "Department", "Category", "Card ID", "Card Status", "Credentials", "Expiry"].map((h) => (
                  <th key={h} style={{ padding: "12px", textAlign: "left", fontSize: "13px", fontWeight: 600 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {users.map((user, i) => (
                <tr key={user.user_id} style={{
                  background: i % 2 === 0 ? C.runway : "white",
                  borderBottom: `1px solid ${C.border}`
                }}>
                  <td style={td}>{user.user_id}</td>
                  <td style={td}>{user.name}</td>
                  <td style={td}>{user.department}</td>
                  <td style={td}>{user.category}</td>
                  <td style={td}>{user.card_id}</td>
                  <td style={td}>
                    <span style={{
                      background: user.card_status === "active" ? `${C.green}1A` : `${C.red}1A`,
                      color:      user.card_status === "active" ? C.green : C.red,
                      padding: "4px 10px",
                      borderRadius: "20px",
                      fontSize: "12px"
                    }}>
                      {user.card_status}
                    </span>
                  </td>
                  <td style={td}>
                    <span style={{
                      background: user.has_credentials ? `${C.green}1A` : `${C.red}1A`,
                      color:      user.has_credentials ? C.green : C.red,
                      padding: "4px 10px",
                      borderRadius: "20px",
                      fontSize: "12px"
                    }}>
                      {user.has_credentials ? "Yes" : "No"}
                    </span>
                  </td>
                  <td style={td}>{user.account_expiry}</td>
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