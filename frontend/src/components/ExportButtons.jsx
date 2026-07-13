import { exportCSV, exportExcel, exportPDF } from "../utils/exportUtils";

const ExportButtons = ({ data, filename, title, columns }) => {
  const disabled = !data || data.length === 0;

  return (
    <div className="export-buttons">
      <button disabled={disabled} onClick={() => exportCSV(data, filename, columns)}>
        Export CSV
      </button>
      <button disabled={disabled} onClick={() => exportExcel(data, filename, columns)}>
        Export Excel
      </button>
      <button disabled={disabled} onClick={() => exportPDF(data, filename, title, columns)}>
        Export PDF
      </button>
    </div>
  );
};

export default ExportButtons;