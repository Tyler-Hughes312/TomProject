import React, { useState } from 'react';

const ExportPanel = ({ businesses, leads }) => {
  const [exportFormat, setExportFormat] = useState('excel');
  const [includeBusinesses, setIncludeBusinesses] = useState(true);
  const [includeLeads, setIncludeLeads] = useState(true);
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    try {
      setExporting(true);
      
      const exportData = {
        format: exportFormat,
        include_businesses: includeBusinesses,
        include_leads: includeLeads,
        businesses: includeBusinesses ? businesses : [],
        leads: includeLeads ? leads : []
      };

      const response = await fetch('/api/v1/exports/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(exportData)
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `lead_generator_export_${new Date().toISOString().split('T')[0]}.${exportFormat === 'excel' ? 'xlsx' : 'csv'}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        alert('Export completed successfully!');
      } else {
        alert('Error creating export');
      }
    } catch (error) {
      console.error('Error exporting data:', error);
      alert('Error exporting data');
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="export-panel">
      <h2>📊 Export Data</h2>
      
      <div className="export-form">
        <div className="form-group">
          <label htmlFor="export-format">Export Format</label>
          <select
            id="export-format"
            value={exportFormat}
            onChange={(e) => setExportFormat(e.target.value)}
          >
            <option value="excel">Excel (.xlsx)</option>
            <option value="csv">CSV (.csv)</option>
          </select>
        </div>

        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={includeBusinesses}
              onChange={(e) => setIncludeBusinesses(e.target.checked)}
            />
            Include Businesses ({businesses.length})
          </label>
        </div>

        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={includeLeads}
              onChange={(e) => setIncludeLeads(e.target.checked)}
            />
            Include Leads ({leads.length})
          </label>
        </div>

        <button 
          className="export-button"
          onClick={handleExport}
          disabled={exporting || (!includeBusinesses && !includeLeads)}
        >
          {exporting ? '📊 Exporting...' : '📊 Export Data'}
        </button>
      </div>

      <div className="export-info">
        <h3>📈 Export Summary</h3>
        <div className="info-grid">
          <div className="info-item">
            <strong>Total Businesses:</strong> {businesses.length}
          </div>
          <div className="info-item">
            <strong>Total Leads:</strong> {leads.length}
          </div>
          <div className="info-item">
            <strong>Export Format:</strong> {exportFormat.toUpperCase()}
          </div>
          <div className="info-item">
            <strong>File Size:</strong> ~{Math.round((businesses.length + leads.length) * 0.5)}KB
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExportPanel;