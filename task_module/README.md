# Task Model Module

## Overview

The Task Model module for Odoo is designed to integrate with an external XML-RPC API to perform specific operations. This module provides functionality to connect to an external service, retrieve necessary authentication details, and send data dynamically to the service. The module is built to ensure seamless interaction between the Odoo environment and external systems through structured XML-RPC calls.

## Features

- **Connect to External Service**: Establish a connection with an external service to retrieve authentication details.
- **Send Data via XML-RPC**: Dynamically construct and send XML-RPC requests with data from Odoo models.
- **Error Handling**: Comprehensive error handling to manage connection and data transmission issues.
- **Notification System**: User-friendly notifications to indicate the success or failure of operations.

## Installation

To install this module, follow these steps:

1. Place the module folder in the Odoo addons directory.
2. Update the Odoo app list.
3. Install the module from the Odoo Apps interface.

## Usage

### Fields

The module defines the following fields in the `task.model`:

- `state`: Char field to store the state of the task.
- `task_name`: Char field to store the name of the task.
- `task_description`: Text field to store the description of the task.
- `priority`: Integer field to store the priority of the task.

### Methods

#### `button_connect_and_send`

This method handles both the connection to the external service and the subsequent data transmission via XML-RPC.

**Process Flow:**

1. **Connection and UID Retrieval**:
    - Sends a POST request to the `/task/connect` endpoint.
    - Parses the response JSON to extract the XML containing the UID.
    - Extracts the UID from the XML response.

2. **XML-RPC Data Transmission**:
    - Constructs an XML body dynamically with the retrieved UID and data from the `task.model`.
    - Sends a POST request to the XML-RPC endpoint to transmit the data.
    - Handles the response and provides appropriate notifications based on the success or failure of the operation.