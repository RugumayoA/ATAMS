import * as XLSX from "xlsx";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

// ---------- shared helpers ----------

const buildColumns = (data, columns) =>
  columns || Object.keys(data[0]).map((k) => ({ key: k, label: k }));

const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

// ---------- CSV ----------

const escapeCSV = (value) => {
  const s = value === null || value === undefined ? "" : String(value);
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};

export const exportCSV = (data, filename, columns = null) => {
  if (!data || data.length === 0) return;
  const cols = buildColumns(data, columns);

  const header = cols.map((c) => escapeCSV(c.label)).join(",");
  const rows = data.map((row) =>
    cols.map((c) => escapeCSV(row[c.key])).join(",")
  );
  const csv = "\uFEFF" + [header, ...rows].join("\n"); // BOM so Excel opens it cleanly

  downloadBlob(
    new Blob([csv], { type: "text/csv;charset=utf-8;" }),
    `${filename}.csv`
  );
};

// ---------- Excel ----------

export const exportExcel = (data, filename, columns = null) => {
  if (!data || data.length === 0) return;
  const cols = buildColumns(data, columns);

  // re-map each row so headers use your labels and column order is enforced
  const rows = data.map((row) => {
    const out = {};
    cols.forEach((c) => (out[c.label] = row[c.key] ?? ""));
    return out;
  });

  const worksheet = XLSX.utils.json_to_sheet(rows);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Report");
  XLSX.writeFile(workbook, `${filename}.xlsx`); // triggers the download itself
};

// ---------- PDF ----------

export const exportPDF = (data, filename, title, columns = null) => {
  if (!data || data.length === 0) return;
  const cols = buildColumns(data, columns);

  const doc = new jsPDF({ orientation: "landscape", format: "a4" });
  doc.setFontSize(14);
  doc.text(title, 14, 15);
  doc.setFontSize(9);
  doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 21);

  autoTable(doc, {
    startY: 26,
    head: [cols.map((c) => c.label)],
    body: data.map((row) => cols.map((c) => String(row[c.key] ?? ""))),
    styles: { fontSize: 8 },
    headStyles: { fillColor: [41, 98, 255] },
  });

  doc.save(`${filename}.pdf`);
};