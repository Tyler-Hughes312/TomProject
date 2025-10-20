import React, { useState, useEffect } from 'react';

const SearchForm = ({ onSearch, loading }) => {
  const [formData, setFormData] = useState({
    location: '',
    business_type: '',
    radius: 25,
    max_results: 50
  });
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await fetch('/api/v1/categories/');
      const data = await response.json();
      setCategories(data.results || []);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.location.trim()) {
      onSearch(formData);
    } else {
      alert('Please enter a location');
    }
  };

  return (
    <div className="search-form">
      <h2>🔍 Search for Businesses</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="location">Location *</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="Enter city, state, or ZIP code"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="business_type">Business Type</label>
            <select
              id="business_type"
              name="business_type"
              value={formData.business_type}
              onChange={handleInputChange}
            >
              <option value="">All Business Types</option>
              {categories.map(category => (
                <option key={category.alias} value={category.alias}>
                  {category.title}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="radius">Search Radius (miles)</label>
            <input
              type="number"
              id="radius"
              name="radius"
              value={formData.radius}
              onChange={handleInputChange}
              min="1"
              max="100"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="max_results">Maximum Results</label>
          <input
            type="number"
            id="max_results"
            name="max_results"
            value={formData.max_results}
            onChange={handleInputChange}
            min="1"
            max="1000"
          />
        </div>

        <button 
          type="submit" 
          className="search-button"
          disabled={loading}
        >
          {loading ? '🔍 Searching...' : '🔍 Search Businesses'}
        </button>
      </form>
    </div>
  );
};

export default SearchForm;