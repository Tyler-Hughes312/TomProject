import React from 'react';
import LeadCard from './LeadCard';

const LeadList = ({ leads, onDeleteLead }) => {
  if (!leads || leads.length === 0) {
    return (
      <div className="lead-list">
        <div className="empty-state">
          <h3>📋 No leads yet</h3>
          <p>Search for businesses and create leads to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="lead-list">
      <div className="lead-list-header">
        <h3>📋 Your Leads ({leads.length})</h3>
        <p>Manage your business leads and track your progress</p>
      </div>
      
      <div className="lead-grid">
        {leads.map((lead) => (
          <LeadCard
            key={lead.leadid}
            lead={lead}
            onDeleteLead={onDeleteLead}
          />
        ))}
      </div>
    </div>
  );
};

export default LeadList;