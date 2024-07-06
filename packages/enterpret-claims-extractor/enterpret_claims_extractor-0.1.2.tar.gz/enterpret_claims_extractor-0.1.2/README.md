# Enterpret-Claims-Extractor

Enterpret-Claims-Extractor is a  Python library designed to extract verifiable atomic claims from various types of records. These records can include conversations, feedback, surveys, or any similar textual data. The library provides an efficient way to analyze and extract meaningful information from unstructured text.

## Features

- Extract atomic claims from various types of records
- Support for CSV file input
- Custom record definition
- Visualization of extracted claims and their sources

## Installation

Install Claims Extractor using pip:

```sh
pip install enterpret-claims-extractor
```

## Usage

### Importing the Package

```python
from enterpret_claims_extractor.extractor import ClaimsExtractor
from enterpret_claims_extractor.utils import read_records_from_csv
```

### Extracting Claims

There are two main ways to use the Claims Extractor:

1. Reading records from a CSV file
2. Defining records manually

#### 1. Reading Records from a CSV File

```python
# Initialize the extractor
extractor = ClaimsExtractor()

# Read records from a CSV file
records = read_records_from_csv('./data/main_df.csv', row_ids=['3c5dfb85-23bb-5cd6-bc75-f652802d3721'])
```

#### 2. Defining Records Manually

You can also define records manually as a list of dictionaries:

```python
# Define records manually
records = [
    {
        "id": "3c5dfb85-23bb-5cd6-bc75-f652802d3721",
        "url": "https://abcd.com/1",
        "type": "RecordTypeConversation",
        "source": "Example Source 1",
        "timestamp": "2023-07-04T12:00:00Z",
        "content": "User: Hello\nAgent: Hi there! How can I assist you today?\nUser: I'm having trouble with my order.\nAgent: I'm sorry to hear that. Can you provide me with your order number?"
    },
]
```

##### Extract Claims from Records with Claim Indices

```python
# Extract claims
results = extractor.extract_claims(records)

# Print results
print(results)
```

#### Output

```
[
  {
    'record_id': '3c5dfb85-23bb-5cd6-bc75-f652802d3721',
    'claim_indices': [2, 3, 5]
  }
]
```

#### View extracted Claims and retrieve their indices

Use the record Id to view the extracted claims

```python
extracted_claims = extractor.view_extracted_claims("3c5dfb85-23bb-5cd6-bc75-f652802d3721")
print(extracted_claims)
```

#### Output

```
{
  2: 'Expansion to multi-channel + multi-modal feedback analysis',
  3: 'Setup of relevant dashboards and training sessions',
  5: 'Backfill not counting towards consumption quota'
}
```

#### View Sources in Record from where Claims were extracted

```python
claims_sources = extractor.view_claim_source("3c5dfb85-23bb-5cd6-bc75-f652802d3721")
print(claims_sources)
```

#### Output

```
{
  2: 'We are thrilled to expand the value of Enterpret from multi-channel textual feedback to multi-channel + multi-modal feedback analysis for the HopSkipDrive team.',
  3: "We'll get started on the Amazon Connect integration in our next sprint only (starts next Wednesday), and work with you closely for questions and clarifications to get that live, before setting up relevant dashboards and training sessions on the support call data.",
  5: 'Also, confirming, that as part of building the integration, we will backfill all support calls from January to March 2024, which will not count towards the consumption quota.'
}
```

#### View the Tokenized/Splitted Record

```python
tokenized_input = extractor.tokenized_inputs['3c5dfb85-23bb-5cd6-bc75-f652802d3721']
print(tokenized_input)
```

#### Output
```
{
  1: 'Agent: Hi Corey McMahon - Confirming that our partnership amendment to include the support calls is now fully executed.',
  2: 'We are thrilled to expand the value of Enterpret from multi-channel textual feedback to multi-channel + multi-modal feedback analysis for the HopSkipDrive team.',
  3: "We'll get started on the Amazon Connect integration in our next sprint only (starts next Wednesday), and work with you closely for questions and clarifications to get that live, before setting up relevant dashboards and training sessions on the support call data.",
  4: 'Matt Miller will coordinate from our end throughout the process.',
  5: 'Also, confirming, that as part of building the integration, we will backfill all support calls from January to March 2024, which will not count towards the consumption quota.',
  6: 'User: Matt Miller I will be OOO next week, so if there is anything you need ahead of time let me know.',
  7: 'Otherwise, we can discuss when I get back.'
}
```

### `ClaimsExtractor`

The main class for extracting claims from records.

#### Methods:

- `extract_claims(records)`: Extracts claims from the given records.
- `view_extracted_claims(record_id)`: Returns the extracted claims for a specific record.
- `view_claim_source(record_id)`: Returns the source of the claims based on their indices.

#### `read_records_from_csv`

A utility function to read records from a CSV file.

#### Parameters:

- `file_path`: Path to the CSV file.
- `row_ids`: (Optional) List of specific row IDs to read from the CSV.
