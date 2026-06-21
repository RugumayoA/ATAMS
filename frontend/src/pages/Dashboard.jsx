import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import {
  Users,
  UserCheck,
  UserX,
  CalendarClock,
  Plane,
  BarChart3,
} from "lucide-react";

const COLORS = {
  ink: "#101826",
  navy: "#1e3a5f", // matches Sidebar.jsx
  sky: "#2C72B0",
  runway: "#F3F5F7",
  cloud: "#FFFFFF",
  green: "#F2820D",
  amber: "#FBB94C",
  red: "#DC3A2D",
  mute: "#6B7785",
  border: "#E4E7EB",
};

const MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace";

const TOTAL_STAFF = 15;
const PRESENT = 12;
const ABSENT = 2;
const ON_LEAVE = 3;

const DEPT_DATA = [
  { name: "Air Traffic Ctrl", present: 3, absent: 0, leave: 1 },
  { name: "Engineering", present: 3, absent: 0, leave: 0 },
  { name: "Security", present: 2, absent: 1, leave: 0 },
  { name: "Admin", present: 2, absent: 0, leave: 1 },
  { name: "Cargo Ops", present: 2, absent: 0, leave: 0 },
];

const BREAKDOWN_DATA = [
  { name: "Present", value: PRESENT, color: COLORS.green },
  { name: "Absent", value: ABSENT, color: COLORS.red },
  { name: "On Leave", value: ON_LEAVE, color: COLORS.amber },
];

const cardStyle = {
  borderRadius: 12,
  padding: 20,
  display: "flex",
  flexDirection: "column",
  gap: 12,
  backgroundColor: COLORS.cloud,
  border: `1px solid ${COLORS.border}`,
};

function StatCard({ icon: Icon, label, value, sub, color }) {
  return (
    <div style={cardStyle}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <div style={{ borderRadius: 8, padding: 8, backgroundColor: `${color}1A`, display: "flex" }}>
          <Icon size={18} color={color} />
        </div>
        <span style={{ fontSize: 13, color: COLORS.mute }}>{label}</span>
      </div>
      <div style={{ fontFamily: MONO, fontVariantNumeric: "tabular-nums", fontSize: 34, fontWeight: 600, color: COLORS.ink }}>
        {value}
      </div>
      <div style={{ fontSize: 12, color: COLORS.mute }}>{sub}</div>
    </div>
  );
}

function ChartPanel({ icon: Icon, title, children }) {
  return (
    <div style={cardStyle}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <Icon size={17} color={COLORS.sky} />
        <h3 style={{ fontWeight: 600, fontSize: 15, color: COLORS.ink, margin: 0 }}>{title}</h3>
      </div>
      {children}
    </div>
  );
}

function LegendChip({ color, label, value }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 13 }}>
      <span style={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: color }} />
      <span style={{ color: COLORS.mute }}>{label}</span>
      {value !== undefined && (
        <span style={{ fontFamily: MONO, fontVariantNumeric: "tabular-nums", fontWeight: 500, color: COLORS.ink }}>
          {value}
        </span>
      )}
    </div>
  );
}

export default function Dashboard() {
  const presentRate = Math.round((PRESENT / TOTAL_STAFF) * 100);

  return (
    <div style={{ padding: 24, display: "flex", flexDirection: "column", gap: 20, backgroundColor: COLORS.runway, minHeight: "100vh" }}>
      {/* Header */}
      <div
        style={{
          borderRadius: 12,
          padding: 24,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: `linear-gradient(110deg, ${COLORS.navy} 0%, ${COLORS.sky} 100%)`,
        }}
      >
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <Plane size={22} color="#FFFFFF" />
            <h1 style={{ color: "#FFFFFF", fontSize: 20, fontWeight: 600, margin: 0 }}>
              ATAMS Dashboard
            </h1>
          </div>
          <p style={{ fontSize: 13, marginTop: 4, marginBottom: 0, color: "#C7D7E5" }}>
            Uganda Civil Aviation Authority Attendance Overview
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, justifyContent: "flex-end" }}>
            <span style={{ width: 6, height: 6, borderRadius: "50%", backgroundColor: COLORS.green }} />
            <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)", fontFamily: MONO, letterSpacing: "0.04em" }}>
              LIVE
            </span>
          </div>
          <p style={{ fontSize: 11, marginTop: 4, marginBottom: 0, fontFamily: MONO, color: "#C7D7E5" }}>
            Sat 20 Jun 2026
          </p>
        </div>
      </div>

      {/* Stat cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
        <StatCard icon={Users} label="Total Staff" value={TOTAL_STAFF} sub="Across 5 departments" color={COLORS.sky} />
        <StatCard icon={UserCheck} label="Present" value={PRESENT} sub={`${presentRate}% of total staff`} color={COLORS.green} />
        <StatCard icon={UserX} label="Absent" value={ABSENT} sub={`${Math.round((ABSENT / TOTAL_STAFF) * 100)}% of total staff`} color={COLORS.red} />
        <StatCard icon={CalendarClock} label="On Leave" value={ON_LEAVE} sub={`${Math.round((ON_LEAVE / TOTAL_STAFF) * 100)}% of total staff`} color={COLORS.amber} />
      </div>

      {/* Charts */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
        <ChartPanel icon={BarChart3} title="Attendance by Department">
          <div style={{ width: "100%", height: 230 }}>
            <ResponsiveContainer>
              <BarChart data={DEPT_DATA} barSize={22}>
                <CartesianGrid vertical={false} stroke={COLORS.border} strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: COLORS.mute }} axisLine={false} tickLine={false} />
                <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: COLORS.mute }} axisLine={false} tickLine={false} width={24} />
                <Tooltip contentStyle={{ borderRadius: 8, border: `1px solid ${COLORS.border}`, fontSize: 12 }} />
                <Bar dataKey="present" stackId="a" fill={COLORS.green} />
                <Bar dataKey="absent" stackId="a" fill={COLORS.red} />
                <Bar dataKey="leave" stackId="a" fill={COLORS.amber} radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div style={{ display: "flex", justifyContent: "center", gap: 20, marginTop: 12 }}>
            <LegendChip color={COLORS.green} label="Present" />
            <LegendChip color={COLORS.red} label="Absent" />
            <LegendChip color={COLORS.amber} label="Leave" />
          </div>
        </ChartPanel>

        <ChartPanel icon={UserCheck} title="Attendance Breakdown">
          <div style={{ position: "relative", width: "100%", height: 230 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={BREAKDOWN_DATA}
                  dataKey="value"
                  innerRadius={68}
                  outerRadius={96}
                  paddingAngle={3}
                  cornerRadius={4}
                  stroke="none"
                >
                  {BREAKDOWN_DATA.map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                pointerEvents: "none",
              }}
            >
              <span style={{ fontFamily: MONO, fontVariantNumeric: "tabular-nums", fontSize: 28, fontWeight: 700, color: COLORS.ink }}>
                {presentRate}%
              </span>
              <span style={{ fontSize: 10, textTransform: "uppercase", letterSpacing: "0.05em", color: COLORS.mute, marginTop: 2 }}>
                Present rate
              </span>
            </div>
          </div>
          <div style={{ display: "flex", justifyContent: "center", gap: 20, marginTop: 12 }}>
            <LegendChip color={COLORS.green} label="Present" value={PRESENT} />
            <LegendChip color={COLORS.red} label="Absent" value={ABSENT} />
            <LegendChip color={COLORS.amber} label="Leave" value={ON_LEAVE} />
          </div>
        </ChartPanel>
      </div>
    </div>
  );
}