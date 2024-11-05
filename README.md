# MBOX Attachments Extractor

This Python script extracts attachments from MBOX files and saves them to a specified directory, setting their last modified dates to match the email dates. Upon name collissions the file will be appended with a datetime stamp. The script checks for UTF-8 and Latin encoding.

## Prerequisites

- Python 3.7 or higher
- `pip` (Python package installer)
- `virtualenv` (optional, but recommended for creating an isolated Python environment)

## Setup

### 1. Clone the Repository

Clone this repository to your local machine using:

```sh
git clone https://github.com/yourusername/mbox-attachments-extractor.git
cd mbox-attachments-extractor
```

### 2. Create a Virtual Environment (Optional but Recommended)

Create a virtual environment to keep dependencies isolated:

```sh
python -m venv venv
```

Activate the virtual environment:

- On Windows:
```sh
.\venv\Scripts\activate
```
- On macOS and Linux:
```sh
source venv/bin/activate
```

### 3. Install Requirements
```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a .env file in the root directory of the project and add the following environment variables:
```env
MBOX_DIR=path/to/your/mbox/directory
ATTACHMENTS_DIR=path/to/save/attachments
```

Replace `path/to/your/mbox/directory` and `path/to/save/attachments` with your actual directory paths.

## Usage
Run the script to process MBOX files and extract attachments:
```sh
owner@hostname >python extract_attachments.py
```
The script will print the directories where MBOX files are read from and where attachments are saved.
License



