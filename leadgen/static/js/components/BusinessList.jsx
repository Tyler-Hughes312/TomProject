import React from 'react';
import BusinessCard from './BusinessCard';

const BusinessList = ({ businesses, onCreateLead, loading }) => {
  if (loading) {
    return (
      <div className="business-list">
        <div className="loading-spinner">
          <h3>🔍 Searching for businesses...</h3>
          <p>This may take a few moments</p>
        </div>
      </div>
    );
  }

  if (!businesses || businesses.length === 0) {
    return (
      <div className="business-list">
        <div className="empty-state">
          <h3>No businesses found</h3>
          <p>Try adjusting your search criteria or expanding your search radius</p>
        </div>
      </div>
    );
  }

  return (
    <div className="business-list">
      <div className="business-list-header">
        <h3>📋 Found {businesses.length} businesses</h3>
      </div>
      
      <div className="business-grid">
        {businesses.map((business) => (
          <BusinessCard
            key={business.businessid || business.yelp_id}
            business={business}
            onCreateLead={onCreateLead}
          />
        ))}
      </div>
    </div>
  );
};

export default BusinessList;