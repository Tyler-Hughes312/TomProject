# 📊 Lead Generator

A web-based system that uses AI to find and manage business leads with Yelp and Google APIs, making business prospecting accessible to everyone.

## 🚀 Features

* **🔍 AI-Powered Search**: Uses Yelp Fusion API for accurate business data
* **📍 Location-based Search**: Search by city, state, or ZIP code
* **🏢 Business Type Filtering**: Filter by specific business categories
* **📏 Customizable Radius**: Set search radius in miles
* **📊 Excel Export**: Clean, formatted Excel files with auto-adjusted columns
* **📈 Summary Statistics**: Additional sheet with business statistics
* **🎯 Interactive Interface**: User-friendly React-based interface
* **🔧 Programmatic API**: Use in your own scripts

## 🛠 Tech Stack

* **Backend**: Python Flask with SQLAlchemy
* **Frontend**: React with Webpack
* **Database**: SQLite (development)
* **APIs**: Yelp Fusion API, Google Maps API
* **Authentication**: Flask sessions
* **Export**: Excel files with openpyxl

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* Node.js 16+ (for frontend)
* API Keys (see Configuration section)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/lead-generator.git
cd lead-generator
```

2. **Run the installer**

```bash
./bin/leadgeninstall
```

3. **Configure environment variables**

```bash
# Copy the example configuration
cp env_template.txt .env

# Edit .env with your API keys
nano .env
```

4. **Start the application**

```bash
# Start everything at once
./bin/leadgenrun

# Or start components separately
./bin/leadgendb reset    # Initialize database
npx webpack             # Build frontend
python -m leadgen       # Start backend
```

5. **Access the application**
* **Main App**: http://localhost:5000/
* **API Health**: http://localhost:5000/api/v1/

## 📁 Project Structure

```
LeadGenerator/
├── leadgen/                    # Flask backend
│   ├── __init__.py            # Main Flask application
│   ├── static/                # Static assets
│   │   ├── css/               # Stylesheets
│   │   └── js/                # JavaScript bundles
│   ├── templates/             # HTML templates
│   └── views/                 # Flask routes
├── bin/                       # Executable scripts
│   ├── leadgeninstall         # Installation script
│   ├── leadgenrun            # Development server
│   ├── leadgentest           # Testing script
│   └── leadgendb             # Database management
├── tests/                     # Test files
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
├── webpack.config.js         # Webpack configuration
├── env_template.txt          # Environment variables template
└── README.md                # This file
```

## 🔑 Configuration

### Required API Keys

The application requires the following API keys for full functionality:

1. **Yelp Fusion API Key** (Required for business search)  
   * Get from: https://www.yelp.com/developers/documentation/v3/authentication  
   * Used for: Business search and data retrieval
2. **Google Maps API Key** (Required for business verification)  
   * Get from: https://developers.google.com/maps/documentation/javascript/get-api-key  
   * Used for: Business verification and additional data

### Environment Setup

1. Copy the example configuration:

```bash
cp env_template.txt .env
```

2. Edit `.env` with your actual API keys:

```bash
# Required API Keys
YELP_API_KEY=your_yelp_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Optional Configuration
DATABASE_URL=var/leadgen.sqlite3
SECRET_KEY=your_secret_key_here
```

**⚠️ Security Note**: Never commit your `.env` file to version control!

## 🎯 Features

### 🔐 Authentication

* Simple session-based authentication
* User registration with location fields
* Secure password hashing with Werkzeug

### 🔍 Business Search

* **Yelp Integration**: Yelp Fusion API integration
* **Google Verification**: Google Maps API integration
* **Location Filtering**: Based on user's city, state, county
* **Category Filtering**: Filter by business type
* **Radius Search**: Customizable search radius

### 📊 Lead Management

* **Lead Creation**: Convert businesses to leads
* **Lead Tracking**: Track lead status and progress
* **Lead Export**: Export leads to Excel format
* **Lead Analytics**: Summary statistics and insights

### 📈 Export Features

* **Excel Export**: Clean, formatted Excel files
* **Multiple Sheets**: Business data, summary statistics
* **Custom Formatting**: Auto-adjusted columns and styling
* **Data Validation**: Ensures data integrity

## 🧪 Development

### Running Tests

```bash
# Run all tests
./bin/leadgentest

# Run specific test suites
python -m pytest tests/test_setup.py
python tests/test_setup.py
```

### Database Schema

The system uses SQLite with the following key tables:

* `businesses`: Business data from Yelp API
* `leads`: User's business leads
* `users`: User accounts
* `exports`: Export history

### API Endpoints

* `GET /api/v1/` - API health check
* `GET /api/v1/businesses/` - List businesses
* `GET /api/v1/businesses/search/` - Search businesses
* `POST /api/v1/leads/` - Create lead
* `GET /api/v1/leads/` - List leads
* `POST /api/v1/exports/` - Export data
* `GET /api/v1/categories/` - Business categories

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use production secrets
2. **Database**: Consider PostgreSQL for production
3. **API Keys**: Rotate keys regularly
4. **Security**: Use HTTPS and secure headers
5. **Monitoring**: Add logging and error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

* **Yelp** for Fusion API capabilities
* **Google** for Maps API integration
* **Flask** and **React** communities for excellent frameworks
* **LegislationForDumbies** for the project structure inspiration

## 🆘 Troubleshooting

### Common Issues

1. **"API key is required" error**: Make sure your `.env` file exists and contains the required API keys
2. **"No businesses found"**: Check your location spelling, try a larger search radius, or verify the business category exists
3. **Rate limit errors**: The application automatically handles rate limits, wait a few minutes and try again
4. **Excel file not created**: Check that the output directory exists and you have write permissions

### Getting Help

1. Check the API documentation for Yelp and Google
2. Verify your API keys are active
3. Test with a simple location first
4. Check the browser console for JavaScript errors
5. Review the Flask application logs

## 📊 Performance

* **Parallel Processing**: Uses ThreadPoolExecutor for fast business processing
* **Caching**: Google API results are cached to reduce API calls
* **Rate Limiting**: Built-in rate limiting to respect API limits
* **Pagination**: Automatic handling of large result sets

## 🔧 Customization

### Adding New Business Categories

Edit `config.py` to add new business categories:

```python
BUSINESS_CATEGORIES = {
    'your_category': 'yelp_category_alias',
    # ... existing categories
}
```

### Modifying Excel Output

Edit `config.py` to change Excel columns:

```python
EXCEL_COLUMNS = [
    'Business Name',
    'Address',
    # ... add or remove columns
]
```

### Adjusting Search Parameters

Modify default values in `config.py`:

```python
DEFAULT_LIMIT = 50  # Results per request
MAX_RESULTS = 1000  # Maximum total results
```