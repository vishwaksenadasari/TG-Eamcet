# 🎓 TS EAMCET Portal

A modern, fast Streamlit-based web application for exploring TS EAMCET / TG EAPCET closing ranks across all colleges, branches, and categories in Telangana.

## ✨ Features

- **🔍 Search Ranks**: Find closing ranks for specific colleges, branches, categories, and genders
- **📊 Rank Checker**: Enter your rank to see all colleges and branches you can get admission into
- **⚖️ Compare Colleges**: Compare multiple colleges side-by-side for a specific branch
- **📋 Full Rank Profile**: View complete rank profiles for any college-branch combination across all categories
- **💰 Tuition Fee Toggle**: Show/hide tuition fee information in results
- **🏛️ District Filter**: Filter search results by district codes
- **📥 CSV Export**: Download results as CSV files for offline analysis
- **📱 Mobile Optimized**: Responsive design that works well on phones and tablets

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning)

### Installation

1. **Clone or download the repository:**
   ```bash
   git clone https://github.com/vishwaksenadasari/TS-EAMCET-PORTAL.git
   cd ts-eamcet-portal
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add data files:**
   - Place your Excel files containing rank data in the `data/raw/` directory
   - Files should be named with year and phase, e.g., `2023_phase1.xlsx`

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 📊 Data Format

The application expects Excel files with the following structure:

- **Year folders**: `data/raw/2023/`, `data/raw/2024/`, etc.
- **Phase files**: `phase1.xlsx`, `phase2.xlsx`, etc. within year folders
- **Required columns**: College Name, Branch, Category, Gender, Closing Rank, District Code, etc.

Example file structure:
```
data/raw/
├── 2023/
│   ├── phase1.xlsx
│   └── phase2.xlsx
└── 2024/
    ├── phase1.xlsx
    └── phase2.xlsx
```

## 🛠️ Development

### Project Structure

```
ts-eamcet-portal/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── data/
│   └── raw/              # Excel data files (not included)
├── src/
│   ├── __init__.py
│   ├── config.py         # Constants and configuration
│   ├── data_loader.py    # Data loading utilities
│   ├── filters.py        # Data filtering and search functions
│   └── utils.py          # Helper functions and formatting
└── README.md             # This file
```

### Adding New Features

1. Edit the relevant files in the `src/` directory
2. Update the UI in `app.py`
3. Test thoroughly with sample data
4. Update this README if needed

## 📋 Usage Guide

### Search Ranks
1. Select year and counselling phase from the sidebar
2. Choose your mode: "🔍 Search Ranks"
3. Select college, branch, category, and gender
4. Optionally filter by district
5. Click "🔍 Search" to view results

### Rank Checker
1. Choose "📊 Rank Checker" mode
2. Enter your rank, category, and gender
3. Click "🔍 Find My Colleges" to see eligible options

### Compare Colleges
1. Select "⚖️ Compare Colleges" mode
2. Choose a branch and multiple colleges
3. Click "⚖️ Compare" for side-by-side comparison

### Full Rank Profile
1. Choose "📋 Full Rank Profile" mode
2. Select college and branch
3. Click "📋 Show Profile" to view all category ranks

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for reference purposes only. Always verify information with official TSCHE (Telangana State Council of Higher Education) sources. Admission criteria and ranks may change.

## 🆘 Support

If you encounter issues:

1. Check that your Excel files are in the correct format
2. Ensure all required columns are present
3. Verify Python and dependencies are installed correctly
4. Check the browser console for any JavaScript errors

For bugs or feature requests, please open an issue on GitHub.

---