import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  ClipboardList,
  AlertTriangle,
  Clock,
  Timer,
  CalendarClock,
  UtensilsCrossed,
  CreditCard,
  Plane,
} from "lucide-react";

const links = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/users", label: "Users", icon: Users },
  { path: "/attendance", label: "Attendance", icon: ClipboardList },
  { path: "/exceptions", label: "Time Exceptions", icon: AlertTriangle },
  { path: "/shifts", label: "Shifts", icon: Clock },
  { path: "/overtime", label: "Overtime", icon: Timer },
  { path: "/leave", label: "Leave", icon: CalendarClock },
  { path: "/meals", label: "Meals", icon: UtensilsCrossed },
  { path: "/cards", label: "Cards", icon: CreditCard },
];

const NAVY = "#1e3a5f";
const NAVY_ACTIVE = "#2C72B0";
const MUTED = "#9FB0C3";

function Sidebar() {
  return (
    <div
      style={{
        width: "220px",
        height: "100vh",
        position: "fixed",
        top: 0,
        left: 0,
        background: NAVY,
        padding: "20px 0",
        overflowY: "auto",
        zIndex: 100,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "8px",
          color: "white",
          marginBottom: "30px",
          fontSize: "16px",
          fontWeight: 600,
        }}
      >
        <Plane size={18} />
        ATAMS
      </div>

      {links.map(({ path, label, icon: Icon }) => (
        <NavLink
          key={path}
          to={path}
          end={path === "/"}
          style={({ isActive }) => ({
            display: "flex",
            alignItems: "center",
            gap: "12px",
            margin: "0 12px",
            padding: "10px 12px",
            borderRadius: "8px",
            textDecoration: "none",
            fontSize: "14px",
            color: isActive ? "#FFFFFF" : MUTED,
            backgroundColor: isActive ? NAVY_ACTIVE : "transparent",
          })}
        >
          <Icon size={16} />
          {label}
        </NavLink>
      ))}
    </div>
  );
}

export default Sidebar;
