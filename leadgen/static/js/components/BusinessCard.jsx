import React from 'react';

const BusinessCard = ({ business, onCreateLead }) => {
  const handleCreateLead = () => {
    if (business.businessid || business.yelp_id) {
      onCreateLead(business.businessid || business.yelp_id);
    }
  };

  const formatAddress = () => {
    const parts = [
      business.address,
      business.city,
      business.state,
      business.zip_code
    ].filter(Boolean);
    return parts.join(', ');
  };

  const formatPhone = (phone) => {
    if (!phone) return 'No phone number';
    return phone;
  };

  const formatWebsite = (website) => {
    if (!website) return null;
    if (website.startsWith('http')) return website;
    return `https://${website}`;
  };

  return (
    <div className="business-card">
      <div className="business-header">
        <h3 className="business-name">{business.name}</h3>
        <div className="business-rating">
          ⭐ {business.rating || 'N/A'} ({business.review_count || 0} reviews)
        </div>
      </div>

      <div className="business-info">
        <div className="business-address">
          📍 {formatAddress()}
        </div>
        <div className="business-phone">
          📞 {formatPhone(business.phone)}
        </div>
        {business.website && (
          <div className="business-website">
            🌐 <a href={formatWebsite(business.website)} target="_blank" rel="noopener noreferrer">
              Visit Website
            </a>
          </div>
        )}
      </div>

      <div className="business-details">
        {business.business_type && (
          <span className="business-type">{business.business_type}</span>
        )}
        {business.price_level && (
          <span className="price-level">{business.price_level}</span>
        )}
        {business.review_count > 0 && (
          <span className="review-count">{business.review_count} reviews</span>
        )}
      </div>

      <div className="business-actions">
        <button 
          className="create-lead-button"
          onClick={handleCreateLead}
        >
          ➕ Create Lead
        </button>
        {business.yelp_url && (
          <a 
            href={business.yelp_url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="yelp-link"
          >
            View on Yelp
          </a>
        )}
      </div>
    </div>
  );
};

export default BusinessCard;