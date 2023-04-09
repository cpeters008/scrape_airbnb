# Airbnb Scraper

This project is designed to scrape Airbnb listings data. The main entry point for this project is `main.py`.

## Prerequisites

- Python 3.8 or higher
- Git
- A virtual environment tool (e.g., `venv`)

## Setup Instructions

1. Clone the repository:

```
git clone https://github.com/cpeters008/scrape_airbnb.git
cd scrape_airbnb
```

2. Create a virtual environment:

```
python3 -m venv venv
```

3. Activate the virtual environment:

- On macOS and Linux:

  ```
  source venv/bin/activate
  ```

- On Windows:

  ```
  .\venv\Scripts\activate
  ```

4. Install the required packages:

```
./install_requirements.sh
```

If you encounter permission issues, try running `chmod +x install_requirements.sh` and then run the script again.

## Usage

To run the Airbnb scraper, use the following command:

```
python3 main.py
```

You can customize the scraper's behavior by modifying the parameters in `main.py` or the configuration settings in `config.ini`.

## Outputs

There are two outputs can you produce using this script:

1. A csv file that contains the conversationId, sender, content, and timestamp of each message in all conversations scraped
2. A json file that has an array of json objects which contains the sender and content only. It is formatted for use in finetuning an openai model. 

The content is always scraped to remove PII and attempts to fix typos.

## Troubleshooting

If you encounter any issues, please refer to the error messages for guidance or consult the project documentation. If you need further assistance, feel free to open an issue on the GitHub repository.

