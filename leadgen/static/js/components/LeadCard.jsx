import React from 'react';

const LeadCard = ({ lead, onDeleteLead }) => {
  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this lead?')) {
      onDeleteLead(lead.leadid);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    return new Date(dateString).toLocaleDateString();
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'new': return '#3498db';
      case 'contacted': return '#f39c12';
      case 'qualified': return '#27ae60';
      case 'closed': return '#e74c3c';
      default: return '#95a5a6';
    }
  };

  return (
    <div className="lead-card">
      <div className="lead-header">
        <h3 className="lead-business-name">
          {lead.business_name || 'Unknown Business'}
        </h3>
        <span 
          className="lead-status"
          style={{ backgroundColor: getStatusColor(lead.status) }}
        >
          {lead.status || 'New'}
        </span>
      </div>

      <div className="lead-info">
        {lead.business_address && (
          <div className="lead-address">
            📍 {lead.business_address}
          </div>
        )}
        {lead.business_phone && (
          <div className="lead-phone">
            📞 {lead.business_phone}
          </div>
        )}
        {lead.business_website && (
          <div className="lead-website">
            🌐 <a href={lead.business_website} target="_blank" rel="noopener noreferrer">
              Visit Website
            </a>
          </div>
        )}
        {lead.notes && (
          <div className="lead-notes">
            📝 {lead.notes}
          </div>
        )}
      </div>

      <div className="lead-meta">
        <span>Created: {formatDate(lead.created_at)}</span>
        {lead.updated_at && lead.updated_at !== lead.created_at && (
          <span>Updated: {formatDate(lead.updated_at)}</span>
        )}
      </div>

      <div className="lead-actions">
        <button 
          className="edit-lead-button"
          onClick={() => alert('Edit functionality coming soon!')}
        >
          ✏️ Edit
        </button>
        <button 
          className="delete-lead-button"
          onClick={handleDelete}
        >
          🗑️ Delete
        </button>
      </div>
    </div>
  );
};

export default LeadCard;