import { Link } from "react-router-dom";


const links = [
  { path: "/",           label: "📊 Dashboard"   },
  { path: "/users",      label: "👥 Users"        },
  { path: "/attendance", label: "📋 Attendance"   },
  { path: "/exceptions", label: "⏰ Exceptions"   },
  { path: "/shifts",     label: "🔄 Shifts"       },
  { path: "/overtime",   label: "💼 Overtime"     },
  { path: "/leave",      label: "🏖️ Leave"        },
  { path: "/meals",      label: "🍽️ Meals"        },
  { path: "/cards",      label: "💳 Cards"        },
];

function Sidebar() {
  return (
    <div style={{
      width: "220px",
      minHeight: "100vh",
      background: "#1e3a5f",
      padding: "20px 0",
    }}>
      <h2 style={{
        color: "white",
        textAlign: "center",
        marginBottom: "30px",
        fontSize: "16px"
      }}>
        ✈️ ATAMS
      </h2>
      {links.map((link) => (
        <Link
          key={link.path}
          to={link.path}
          style={{
            display: "block",
            color: "white",
            padding: "12px 20px",
            textDecoration: "none",
            fontSize: "14px",
          }}
        >
          {link.label}
        </Link>
      ))}
    </div>
  );
}

export default Sidebar;