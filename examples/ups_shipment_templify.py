"""
UPS Shipment Example using Templify's advanced features.

This example demonstrates how Templify can simplify complex template workflows
by separating fixed and variable parts, using template composition, and
leveraging JMESPath for data transformation.
"""

import json
from typing import Dict, List, Any

from templify import render_data


# Base template with fixed parts (shipper, recipient, payment info)
BASE_SHIPMENT_TEMPLATE = {
    "ShipmentRequest": {
        "Request": {"RequestOption": "nonvalidate", "TransactionReference": {"CustomerContext": "{customer_context}"}},
        "Shipment": {
            "Description": "{shipment_description}",
            "Shipper": "{shipper}",
            "ShipTo": "{ship_to}",
            "ShipFrom": "{ship_from}",
            "PaymentInformation": "{payment}",
            "Service": "{service}",
            "Package": "{packages}",
        },
        "LabelSpecification": {"LabelImageFormat": {"Code": "PDF"}, "HTTPUserAgent": "Mozilla/4.5"},
    }
}

# Shipper template (fixed part)
SHIPPER_TEMPLATE = {
    "Name": "Company BV",
    "AttentionName": "John Doe",
    "TaxIdentificationNumber": "NL123456789B01",
    "Phone": {"Number": "+31612345678", "Extension": ""},
    "ShipperNumber": "ABCD1234",
    "Address": {
        "AddressLine": ["Main Street 123", "Suite 456"],
        "City": "Amsterdam",
        "StateProvinceCode": "NH",
        "PostalCode": "1012AB",
        "CountryCode": "NL",
    },
}

# Recipient template (fixed part)
RECIPIENT_TEMPLATE = {
    "Name": "Customer Company",
    "AttentionName": "Jane Smith",
    "Phone": {"Number": "+31687654321", "Extension": ""},
    "Address": {
        "AddressLine": ["Church Street 456", "Floor 3"],
        "City": "Rotterdam",
        "StateProvinceCode": "ZH",
        "PostalCode": "3011GH",
        "CountryCode": "NL",
    },
}

# Payment template (fixed part)
PAYMENT_TEMPLATE = {
    "ShipmentCharge": {
        "Type": "01",  # 01 = Prepaid
        "BillShipper": {"AccountNumber": {"Value": "ABCD1234"}},
    }
}

# Service template (fixed part)
SERVICE_TEMPLATE = {
    "Code": "01",  # 01 = UPS Next Day Air
    "Description": "UPS Next Day Air",
}

# Package template (variable part)
PACKAGE_TEMPLATE = {
    "PackagingType": {
        "Code": "02",  # 02 = Customer Packaging
        "Description": "Package",
    },
    "Dimensions": {"UnitOfMeasurement": {"Code": "CM"}, "Length": "{length}", "Width": "{width}", "Height": "{height}"},
    "PackageWeight": {"UnitOfMeasurement": {"Code": "KG"}, "Weight": "{weight}"},
    "PackageID": "{package_id}",
}


def create_package_data(
    package_id: int, weight: float = 2.5, length: float = 30.0, width: float = 20.0, height: float = 15.0
) -> Dict[str, Any]:
    """
    Create package data using the package template.

    This demonstrates how Templify can simplify data creation by using templates.
    """
    context = {
        "package_id": f"Package {package_id}",
        "weight": str(weight),
        "length": str(length),
        "width": str(width),
        "height": str(height),
    }

    return render_data(PACKAGE_TEMPLATE, context)


def create_packages_data(num_packages: int, start_id: int = 1) -> List[Dict[str, Any]]:
    """
    Create a list of package data.

    This demonstrates how Templify can be used to generate multiple data structures
    from a single template.
    """
    packages = []
    for i in range(num_packages):
        package_id = start_id + i
        packages.append(create_package_data(package_id))
    return packages


def create_shipment(customer_context: str, shipment_description: str, packages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a complete UPS shipment using template composition.

    This demonstrates how Templify can simplify complex data structures by
    composing smaller templates.
    """
    # Create the context with all the data
    context = {
        "customer_context": customer_context,
        "shipment_description": shipment_description,
        "shipper": SHIPPER_TEMPLATE,
        "ship_to": RECIPIENT_TEMPLATE,
        "ship_from": SHIPPER_TEMPLATE,  # Using same data for ship from
        "payment": PAYMENT_TEMPLATE,
        "service": SERVICE_TEMPLATE,
        "packages": packages,
    }

    # Render the complete shipment
    return render_data(BASE_SHIPMENT_TEMPLATE, context)


def create_shipments(
    customer_context: str, shipment_description: str, total_packages: int, packages_per_shipment: int = 20
) -> List[Dict[str, Any]]:
    """
    Create multiple shipments when the total number of packages exceeds the limit.

    This demonstrates how Templify can simplify complex business workflows by
    separating the template logic from the business logic.
    """
    # Calculate number of shipments needed
    num_shipments = (total_packages + packages_per_shipment - 1) // packages_per_shipment

    shipments = []
    for i in range(num_shipments):
        # Calculate start and end package indices for this shipment
        start_idx = i * packages_per_shipment + 1
        end_idx = min((i + 1) * packages_per_shipment, total_packages)
        num_packages_in_shipment = end_idx - start_idx + 1

        # Create packages for this shipment
        packages = create_packages_data(num_packages_in_shipment, start_idx)

        # Create shipment with unique customer context
        shipment = create_shipment(
            f"{customer_context}-{i+1}", f"{shipment_description} (Shipment {i+1} of {num_shipments})", packages
        )

        shipments.append(shipment)

    return shipments


def main():
    """Run the example to demonstrate Templify's capabilities."""
    # Example 1: Create a single shipment with 5 packages
    print("Example 1: Single shipment with 5 packages")
    packages = create_packages_data(5)
    shipment = create_shipment("Test Shipment 123", "Test Shipment", packages)
    print(json.dumps(shipment, indent=2))
    print("\n" + "-" * 80 + "\n")

    # Example 2: Create multiple shipments (30 packages split into 20+10)
    print("Example 2: Multiple shipments (30 packages split into 20+10)")
    shipments = create_shipments("Test Multiple Shipments 456", "Test Multiple Shipments", 30)
    print(f"Created {len(shipments)} shipments")
    print(f"First shipment has {len(shipments[0]['ShipmentRequest']['Shipment']['Package'])} packages")
    print(f"Second shipment has {len(shipments[1]['ShipmentRequest']['Shipment']['Package'])} packages")
    print("\n" + "-" * 80 + "\n")

    # Example 3: Create a shipment with custom package dimensions
    print("Example 3: Shipment with custom package dimensions")
    custom_packages = [
        create_package_data(1, weight=5.0, length=40.0, width=30.0, height=20.0),
        create_package_data(2, weight=3.0, length=25.0, width=15.0, height=10.0),
    ]
    custom_shipment = create_shipment("Custom Package Example 789", "Custom Package Dimensions", custom_packages)
    print(json.dumps(custom_shipment, indent=2))


if __name__ == "__main__":
    main()
