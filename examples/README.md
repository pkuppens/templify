# Templify Examples

This directory contains examples of using the Templify library for various use cases.

## UPS Shipments Example

The file `ups_shipment_example.py` demonstrates how to use Templify to efficiently create UPS shipments, including splitting shipments when the number of packages exceeds the limit.

### Features

- Creating UPS shipment payloads with placeholders
- Reusing fixed parts of the shipment (shipper, delivery address, etc.)
- Automatically splitting shipments when the number of packages exceeds the limit
- Support for Dutch shipments (country code, currency, metric system)

### Usage

```bash
# Install templify
pip install templify

# Run the example
python ups_shipment_example.py
```

### Output

The script generates JSON files for each shipment:

- `shipment_1.json`: First shipment with maximum 20 packages
- `shipment_2.json`: Second shipment with the remaining packages

### Customization

You can customize the example by modifying the following functions:

- `create_shipper_data()`: Shipper information
- `create_ship_to_data()`: Delivery address information
- `create_ship_from_data()`: Sender address information
- `create_payment_data()`: Payment information
- `create_service_data()`: Service information
- `create_package_data()`: Package information

### Integration with UPS API

To integrate this example with the UPS API, you need to send the generated JSON files to the UPS API endpoint:

```python
import requests

# UPS API endpoint
url = "https://api.ups.com/api/shipments/v1/ship"

# API key and other authentication information
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

# Send the shipment to UPS
response = requests.post(url, json=shipment, headers=headers)

# Process the response
if response.status_code == 200:
    print("Shipment successfully created!")
    print(response.json())
else:
    print(f"Error creating shipment: {response.status_code}")
    print(response.text)
```

## More Examples

More examples coming soon! 