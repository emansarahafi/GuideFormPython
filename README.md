# GuideForm (Python Tkinter Application)

![GuideForm](https://github.com/emansarahafi/GuideFormPython/assets/85173630/9fd5e911-7320-4f9a-9cb4-5ad9d5ff2b0c)

## Overview

GuideForm is a desktop application built with Python Tkinter for surveying senior engineering college students in Bahrain. The application is designed to support [Tashfeen Engineering Solutions](https://tashfeen.tech/) in expanding its presence in the Middle East by gathering insights about young engineers in the region.

The interface provides comprehensive functionality for accessing surveys, company information, and visualizing collected data through interactive graphs. More details can be found [by clicking here](https://www.geotashfeen.tech/Data_Extarction.php).

**Related Project**: [GuideForm Website](https://github.com/emansarahafi/GuideFormWebsite) - Web interface for the GuideForm survey system.

## Important Warnings

**Security Notice**: Never commit your `config.ini` file with real API credentials to version control. The `.gitignore` file is configured to exclude it.

**Data Privacy**: Survey data and Telegram session files are automatically excluded from git commits. Ensure compliance with data protection regulations when handling user information.

**Setup Required**: Before running the application, you must:

- Configure Telegram API credentials in `config.ini`
- Update the Telegram channel ID in `Interface.py` (replace `INSERT_CHAT_ID_HERE`)
- Set up a local web server for survey forms
- Place required image files in the `resources/` directory

**Network Requirements**: The application requires internet connectivity for:

- Telegram API access
- Web browser links to external resources
- Survey form access (localhost required)

## Features

- **Interactive GUI**: Clean and intuitive interface built with Tkinter
- **Survey Access**: Direct access to online surveys for engineering students
- **Data Visualization**: Real-time graph generation from survey responses including:
  - Age distribution
  - Gender demographics
  - University enrollment
  - Engineering majors
  - Career goals and next steps
  - Programming languages and frameworks
  - Learning methods and experience levels
- **Telegram Integration**: Automated data extraction from Telegram channels
- **External Links**: Quick access to company website, brochures, and application resources
- **Real-time Clock**: Display current date and time

## Prerequisites

- Python 3.x
- Telegram API credentials (api_id and api_hash)
- Local web server for accessing forms (e.g., localhost)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/emansarahafi/GuideFormPython.git
cd GuideFormPython
```

2. Install required packages:

```bash
pip install pillow matplotlib numpy telethon configparser
```

3. Place resource files in the `resources/` directory:
   - `GuideForm.png` - Application logo
   - `GuideForm.ico` - Application icon (optional)
   - `GuideForm.pdf` - Company brochure (optional)

4. Create your `config.ini` file from the template:

```bash
cp config.ini.template config.ini
```

5. Configure Telegram API credentials in `config.ini`:

```ini
[Telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH
phone = YOUR_PHONE_NUMBER
username = YOUR_USERNAME
```

6. Update Telegram channel ID in `Interface.py`:
   - Find and replace `INSERT_CHAT_ID_HERE` with your actual Telegram channel ID (appears twice in the code)

7. Set up local web server for survey forms (if using local hosting)

## Usage

Run the application:

```bash
python Interface.py
```

### Main Interface Features

1. **Access the Survey**: Opens the survey form in your default web browser
2. **Access the Links**: Dropdown menu with links to:
   - Application website
   - Company brochure
   - Tashfeen Engineering Solutions website
3. **Access the Data**: Dropdown menu for viewing different data visualizations:
   - Demographics (Age, Gender)
   - Academic information (University, Major)
   - Career insights (Next steps, Future goals)
   - Technical skills (Languages, Learning methods, Experience)

## Data Visualization

The application generates various types of charts:

- **Pie Charts**: Age distribution, gender demographics, learning duration, experience ratings, career relevance
- **Bar Charts**: Universities, majors, career paths, programming languages, learning methods

## Project Structure

```
GuideFormPython/
│
├── Interface.py           # Main application file
├── config.ini.template    # Template for Telegram API configuration
├── config.ini            # Your API credentials (excluded from git, create from template)
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
│
├── resources/            # Static resources
│   ├── GuideForm.png     # Application logo (excluded from git)
│   ├── GuideForm.ico     # Application icon (excluded from git)
│   ├── GuideForm.pdf     # Company brochure
│   └── README.md         # Resources directory documentation
│
└── data/                 # Generated data files (excluded from git)
    ├── .gitkeep          # Keeps directory in git
    ├── user_data.json    # Telegram user data (generated)
    ├── channel_messages.json  # Telegram messages (generated)
    └── channel_messages.txt   # Processed messages (generated)
```

**Note**: All files marked as "excluded from git" are listed in `.gitignore` to protect sensitive data and credentials.

## Configuration

### Telegram Setup

1. **Obtain API Credentials**: Visit [Telegram API Development Tools](https://my.telegram.org/apps)
   - Sign in with your phone number
   - Create a new application
   - Note your `api_id` and `api_hash`

2. **Configure credentials**: Update `config.ini` with your actual credentials
   - Use full phone number including + and country code
   - Username should be your Telegram username without @

3. **Set Channel ID**: In `Interface.py`, replace `INSERT_CHAT_ID_HERE` (appears twice) with your Telegram channel/group ID
   - You can get this using bots like @userinfobot or @RawDataBot

**Warning**: Telegram will create session files (`.session`) in the project directory. These contain authentication tokens and are automatically excluded from git.

### Local Resources Setup

The application expects files in the `resources/` directory. All resource files are excluded from git to keep the repository clean.

**Required:**

- `GuideForm.png` - Application logo (recommended size: 200x200px)

**Optional:**

- `GuideForm.ico` - Application icon for Windows
- `GuideForm.pdf` - Company brochure for sharing

### Web Server Setup

For local survey forms, ensure you have a web server running on localhost. The application expects forms at:

- `http://localhost/TashfeenUniForm/appsurvey.html`
- `http://localhost/TashfeenUniForm/appwebsite.html`
- `http://localhost/TashfeenUniForm/guideform.pdf`

You can use any local web server (Apache, Nginx, Python's http.server, etc.)

## About Tashfeen Engineering Solutions

Tashfeen Engineering Solutions is a geotechnical, civil engineering, and software development company established in 2020. The company has worked on several projects on national and international scales and is expanding its operations to the Middle East, beginning with Bahrain.

## License

© 2022 Tashfeen Engineering Solutions. All rights reserved.

## Contact

For inquiries, please visit [Tashfeen Engineering Solutions](https://tashfeen.tech/)

## Acknowledgments

- Built with Python and Tkinter
- Data visualization powered by Matplotlib
- Telegram integration via Telethon library
