import { useEffect, useState } from "react";
import API from "../components/api/axios";

const TABS = [
  { label: "All Users",        endpoint: "/users/all"            },
  { label: "New Users",        endpoint: "/users/new"            },
  { label: "No Credentials",   endpoint: "/users/no-credentials" },
  { label: "Expiring Soon",    endpoint: "/users/expiring-soon"  },
  { label: "On Device",        endpoint: "/users/active"         },
  { label: "Exceptional",      endpoint: "/users/exceptional"    },
];

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
        <h1 style={{ margin: 0 }}> User Reports</h1>
        <p style={{ margin: "6px 0 0", opacity: 0.8 }}>
        
        </p>
      </div>

      {/* Summary Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "20px",
        marginBottom: "30px"
      }}>
        {[
          { label: "Total Users",      value: users.length,                                 color: "#1e3a5f", icon: "👥" },
          { label: "No Credentials",   value: users.filter(u => !u.has_credentials).length, color: "#c62828", icon: "⚠️" },
          { label: "New Users",        value: users.filter(u => u.is_new_user).length,      color: "#2e7d32", icon: "🆕" },
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
        <h3 style={{ marginTop: 0, color: "#1e3a5f" }}>
          {TABS[activeTab].label}
        </h3>

        {loading ? <p>Loading...</p> : users.length === 0 ? (
          <p style={{ color: "#999" }}>No records found.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#1e3a5f", color: "white" }}>
                {["ID", "Name", "Department", "Category", "Card ID", "Card Status", "Credentials", "Expiry"].map((h) => (
                  <th key={h} style={{ padding: "12px", textAlign: "left", fontSize: "13px" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {users.map((user, i) => (
                <tr key={user.user_id} style={{
                  background: i % 2 === 0 ? "#f9f9f9" : "white",
                  borderBottom: "1px solid #eee"
                }}>
                  <td style={td}>{user.user_id}</td>
                  <td style={td}>{user.name}</td>
                  <td style={td}>{user.department}</td>
                  <td style={td}>{user.category}</td>
                  <td style={td}>{user.card_id}</td>
                  <td style={td}>
                    <span style={{
                      background: user.card_status === "active" ? "#e8f5e9" : "#ffebee",
                      color:      user.card_status === "active" ? "#2e7d32" : "#c62828",
                      padding: "4px 10px",
                      borderRadius: "20px",
                      fontSize: "12px"
                    }}>
                      {user.card_status}
                    </span>
                  </td>
                  <td style={td}>
                    <span style={{
                      background: user.has_credentials ? "#e8f5e9" : "#ffebee",
                      color:      user.has_credentials ? "#2e7d32" : "#c62828",
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