# SEC IPO Detector

The **SEC IPO Detector** is a tool that helps track IPO filings from the SEC's EDGAR RSS feed in real time. By focusing on S-1 forms, this application detects IPO-related filings and saves them into a CSV file for easy monitoring.

## Story behind it:

Imagine you’re someone who needs to keep track of new IPO filings but don’t want to go through the hassle of manually checking SEC filings every day. This tool was built exactly for that. With just a few steps to set it up, it runs seamlessly in the background, ensuring that every new IPO-related filing is tracked, and you never miss out on important filings!

This `README.md` file provides instructions so that anyone can easily set up and use the tool. You just need to clone the repository, install the dependencies, and run the script to start populating your CSV with fresh IPO data!

## Features

- **Real-time tracking**: Polls the SEC RSS feed and monitors new filings as they happen.
- **IPO Detection**: Specifically looks for IPO-related filings, focusing on S-1 forms.
- **No duplicates**: Prevents duplicate entries by checking against existing records in a CSV file.
- **Export to CSV**: Detected IPO filings are automatically saved to a CSV file for record-keeping.

## Setup Instructions
To get started with the SEC IPO Detector, follow these steps:

### 1. Clone the Repository
Begin by cloning the repository to your local machine. Run the following commands in your terminal:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
Next, you’ll need to install the required Python dependencies for the project. To do this, simply run:
    
```bash
pip install -r requirements.txt
```

### 3. Running the Application
Once you've installed the dependencies, you're ready to run the IPO detector. To start the application, use the following command:
    
```bash
python3 -m src.detector
```
