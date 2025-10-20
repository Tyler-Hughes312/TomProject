import React, { useState, useEffect } from 'react';
import SearchForm from './SearchForm';
import BusinessList from './BusinessList';
import LeadList from './LeadList';
import ExportPanel from './ExportPanel';

const LeadGenerator = () => {
  const [businesses, setBusinesses] = useState([]);
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('search');
  const [searchResults, setSearchResults] = useState([]);

  useEffect(() => {
    // Load initial data
    loadBusinesses();
    loadLeads();
  }, []);

  const loadBusinesses = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/v1/businesses/');
      const data = await response.json();
      setBusinesses(data.results || []);
    } catch (error) {
      console.error('Error loading businesses:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadLeads = async () => {
    try {
      const response = await fetch('/api/v1/leads/');
      const data = await response.json();
      setLeads(data.results || []);
    } catch (error) {
      console.error('Error loading leads:', error);
    }
  };

  const handleSearch = async (searchParams) => {
    try {
      setLoading(true);
      const queryParams = new URLSearchParams(searchParams);
      const response = await fetch(`/api/v1/businesses/search/?${queryParams}`);
      const data = await response.json();
      setSearchResults(data.results || []);
      setBusinesses(data.results || []);
    } catch (error) {
      console.error('Error searching businesses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateLead = async (businessId) => {
    try {
      const response = await fetch('/api/v1/leads/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          business_id: businessId,
          user_id: 1,
          notes: 'Created from Lead Generator'
        })
      });

      if (response.ok) {
        loadLeads(); // Refresh leads list
        alert('Lead created successfully!');
      } else {
        alert('Error creating lead');
      }
    } catch (error) {
      console.error('Error creating lead:', error);
      alert('Error creating lead');
    }
  };

  const handleDeleteLead = async (leadId) => {
    try {
      const response = await fetch(`/api/v1/leads/${leadId}/`, {
        method: 'DELETE'
      });

      if (response.ok) {
        loadLeads(); // Refresh leads list
        alert('Lead deleted successfully!');
      } else {
        alert('Error deleting lead');
      }
    } catch (error) {
      console.error('Error deleting lead:', error);
      alert('Error deleting lead');
    }
  };

  return (
    <div className="lead-generator">
      <header className="header">
        <div className="header-content">
          <h1>📊 Lead Generator</h1>
          <p>Find and manage business leads with AI-powered search</p>
        </div>
        <nav className="tabs">
          <button 
            className={activeTab === 'search' ? 'active' : ''}
            onClick={() => setActiveTab('search')}
          >
            🔍 Search Businesses
          </button>
          <button 
            className={activeTab === 'leads' ? 'active' : ''}
            onClick={() => setActiveTab('leads')}
          >
            📋 My Leads ({leads.length})
          </button>
          <button 
            className={activeTab === 'export' ? 'active' : ''}
            onClick={() => setActiveTab('export')}
          >
            📊 Export Data
          </button>
        </nav>
      </header>

      <main className="main-content">
        {activeTab === 'search' && (
          <div className="search-tab">
            <SearchForm onSearch={handleSearch} loading={loading} />
            <BusinessList 
              businesses={searchResults} 
              onCreateLead={handleCreateLead}
              loading={loading}
            />
          </div>
        )}

        {activeTab === 'leads' && (
          <div className="leads-tab">
            <LeadList 
              leads={leads} 
              onDeleteLead={handleDeleteLead}
            />
          </div>
        )}

        {activeTab === 'export' && (
          <div className="export-tab">
            <ExportPanel 
              businesses={businesses} 
              leads={leads} 
            />
          </div>
        )}
      </main>
    </div>
  );
};

export default LeadGenerator;