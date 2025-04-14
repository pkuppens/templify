"""
Example of using templify to create UPS shipments.

This script demonstrates how to use the templify library to efficiently create
UPS shipments, including splitting shipments when the number of packages exceeds
the limit.
"""

import json
from typing import Any

from templify import render_data

# UPS API payload template with placeholders
UPS_SHIPMENT_TEMPLATE = {
    "ShipmentRequest": {
        "Request": {"RequestOption": "nonvalidate", "TransactionReference": {"CustomerContext": "{customer_context}"}},
        "Shipment": {
            "Description": "{shipment_description}",
            "Shipper": {
                "Name": "{shipper_name}",
                "AttentionName": "{shipper_attention_name}",
                "TaxIdentificationNumber": "{shipper_tax_id}",
                "Phone": {"Number": "{shipper_phone}", "Extension": "{shipper_phone_ext}"},
                "ShipperNumber": "{shipper_number}",
                "Address": {
                    "AddressLine": ["{shipper_address_line1}", "{shipper_address_line2}"],
                    "City": "{shipper_city}",
                    "StateProvinceCode": "{shipper_state}",
                    "PostalCode": "{shipper_postal_code}",
                    "CountryCode": "{shipper_country_code}",
                },
            },
            "ShipTo": {
                "Name": "{ship_to_name}",
                "AttentionName": "{ship_to_attention_name}",
                "Phone": {"Number": "{ship_to_phone}", "Extension": "{ship_to_phone_ext}"},
                "Address": {
                    "AddressLine": ["{ship_to_address_line1}", "{ship_to_address_line2}"],
                    "City": "{ship_to_city}",
                    "StateProvinceCode": "{ship_to_state}",
                    "PostalCode": "{ship_to_postal_code}",
                    "CountryCode": "{ship_to_country_code}",
                },
            },
            "ShipFrom": {
                "Name": "{ship_from_name}",
                "AttentionName": "{ship_from_attention_name}",
                "Phone": {"Number": "{ship_from_phone}", "Extension": "{ship_from_phone_ext}"},
                "Address": {
                    "AddressLine": ["{ship_from_address_line1}", "{ship_from_address_line2}"],
                    "City": "{ship_from_city}",
                    "StateProvinceCode": "{ship_from_state}",
                    "PostalCode": "{ship_from_postal_code}",
                    "CountryCode": "{ship_from_country_code}",
                },
            },
            "PaymentInformation": {
                "ShipmentCharge": {"Type": "{payment_type}", "BillShipper": {"AccountNumber": {"Value": "{account_number}"}}}
            },
            "Service": {"Code": "{service_code}", "Description": "{service_description}"},
            "Package": "{packages}",
        },
        "LabelSpecification": {"LabelImageFormat": {"Code": "PDF"}, "HTTPUserAgent": "Mozilla/4.5"},
    }
}


def create_shipper_data() -> dict[str, Any]:
    """Create shipper data for the UPS shipment."""
    return {
        "shipper_name": "Bedrijf BV",
        "shipper_attention_name": "John Doe",
        "shipper_tax_id": "NL123456789B01",
        "shipper_phone": "+31612345678",
        "shipper_phone_ext": "",
        "shipper_number": "ABCD1234",
        "shipper_address_line1": "Hoofdstraat 123",
        "shipper_address_line2": "Suite 456",
        "shipper_city": "Amsterdam",
        "shipper_state": "NH",
        "shipper_postal_code": "1012AB",
        "shipper_country_code": "NL",
    }


def create_ship_to_data() -> dict[str, Any]:
    """Create ship to data for the UPS shipment."""
    return {
        "ship_to_name": "Klant Bedrijf",
        "ship_to_attention_name": "Jane Smith",
        "ship_to_phone": "+31687654321",
        "ship_to_phone_ext": "",
        "ship_to_address_line1": "Kerkstraat 456",
        "ship_to_address_line2": "Verdieping 3",
        "ship_to_city": "Rotterdam",
        "ship_to_state": "ZH",
        "ship_to_postal_code": "3011GH",
        "ship_to_country_code": "NL",
    }


def create_ship_from_data() -> dict[str, Any]:
    """Create ship from data for the UPS shipment."""
    return {
        "ship_from_name": "Bedrijf BV",
        "ship_from_attention_name": "John Doe",
        "ship_from_phone": "+31612345678",
        "ship_from_phone_ext": "",
        "ship_from_address_line1": "Hoofdstraat 123",
        "ship_from_address_line2": "Suite 456",
        "ship_from_city": "Amsterdam",
        "ship_from_state": "NH",
        "ship_from_postal_code": "1012AB",
        "ship_from_country_code": "NL",
    }


def create_payment_data() -> dict[str, Any]:
    """Create payment data for the UPS shipment."""
    return {
        "payment_type": "01",  # 01 = Prepaid
        "account_number": "ABCD1234",
    }


def create_service_data() -> dict[str, Any]:
    """Create service data for the UPS shipment."""
    return {
        "service_code": "01",  # 01 = UPS Next Day Air
        "service_description": "UPS Next Day Air",
    }


def create_package_data(package_id: int, weight: float, length: float, width: float, height: float) -> dict[str, Any]:
    """Create package data for the UPS shipment."""
    return {
        "PackagingType": {
            "Code": "02",  # 02 = Customer Packaging
            "Description": "Package",
        },
        "Dimensions": {"UnitOfMeasurement": {"Code": "CM"}, "Length": str(length), "Width": str(width), "Height": str(height)},
        "PackageWeight": {"UnitOfMeasurement": {"Code": "KG"}, "Weight": str(weight)},
        "PackageID": f"Package {package_id}",
    }


def create_packages_data(num_packages: int, start_id: int = 1) -> list[dict[str, Any]]:
    """Create packages data for the UPS shipment."""
    packages = []
    for i in range(num_packages):
        package_id = start_id + i
        # Example dimensions and weight - in a real scenario these would vary
        weight = 2.5
        length = 30.0
        width = 20.0
        height = 15.0
        packages.append(create_package_data(package_id, weight, length, width, height))
    return packages


def create_shipment_context(
    customer_context: str,
    shipment_description: str,
    packages: list[dict[str, Any]],
    shipper_data: dict[str, Any],
    ship_to_data: dict[str, Any],
    ship_from_data: dict[str, Any],
    payment_data: dict[str, Any],
    service_data: dict[str, Any],
) -> dict[str, Any]:
    """Create the complete context for the UPS shipment."""
    context = {
        "customer_context": customer_context,
        "shipment_description": shipment_description,
        "packages": packages,
        **shipper_data,
        **ship_to_data,
        **ship_from_data,
        **payment_data,
        **service_data,
    }
    return context


def create_ups_shipment(
    customer_context: str,
    shipment_description: str,
    packages: list[dict[str, Any]],
    shipper_data: dict[str, Any],
    ship_to_data: dict[str, Any],
    ship_from_data: dict[str, Any],
    payment_data: dict[str, Any],
    service_data: dict[str, Any],
) -> dict[str, Any]:
    """Create a complete UPS shipment payload."""
    context = create_shipment_context(
        customer_context, shipment_description, packages, shipper_data, ship_to_data, ship_from_data, payment_data, service_data
    )

    return render_data(UPS_SHIPMENT_TEMPLATE, context)


def create_multiple_shipments(
    customer_context: str,
    shipment_description: str,
    total_packages: int,
    packages_per_shipment: int = 20,
    shipper_data: dict[str, Any] = None,
    ship_to_data: dict[str, Any] = None,
    ship_from_data: dict[str, Any] = None,
    payment_data: dict[str, Any] = None,
    service_data: dict[str, Any] = None,
) -> list[dict[str, Any]]:
    """
    Create multiple UPS shipments when the total number of packages exceeds the limit.

    Args:
        customer_context: Customer context for the shipment
        shipment_description: Description of the shipment
        total_packages: Total number of packages to ship
        packages_per_shipment: Maximum number of packages per shipment (default: 20)
        shipper_data: Shipper data (optional)
        ship_to_data: Ship to data (optional)
        ship_from_data: Ship from data (optional)
        payment_data: Payment data (optional)
        service_data: Service data (optional)

    Returns:
        List of UPS shipment payloads
    """
    # Use default data if not provided
    if shipper_data is None:
        shipper_data = create_shipper_data()
    if ship_to_data is None:
        ship_to_data = create_ship_to_data()
    if ship_from_data is None:
        ship_from_data = create_ship_from_data()
    if payment_data is None:
        payment_data = create_payment_data()
    if service_data is None:
        service_data = create_service_data()

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
        shipment = create_ups_shipment(
            f"{customer_context}-{i+1}",
            f"{shipment_description} (Shipment {i+1} of {num_shipments})",
            packages,
            shipper_data,
            ship_to_data,
            ship_from_data,
            payment_data,
            service_data,
        )

        shipments.append(shipment)

    return shipments


def main():
    """Main function for the example."""
    # Create test data
    customer_context = "Order 12345"
    shipment_description = "Customer Order #12345"
    total_packages = 30

    # Create shipments
    shipments = create_multiple_shipments(customer_context, shipment_description, total_packages)

    # Display results
    print(f"Number of shipments: {len(shipments)}")

    for i, shipment in enumerate(shipments):
        print(f"\nShipment {i+1}:")
        print(f"Number of packages: {len(shipment['ShipmentRequest']['Shipment']['Package'])}")
        print(f"Customer context: {shipment['ShipmentRequest']['Request']['TransactionReference']['CustomerContext']}")
        print(f"Description: {shipment['ShipmentRequest']['Shipment']['Description']}")

        # Display package IDs
        package_ids = [p["PackageID"] for p in shipment["ShipmentRequest"]["Shipment"]["Package"]]
        print(f"Package IDs: {', '.join(package_ids)}")

        # Save shipment to JSON file
        with open(f"shipment_{i+1}.json", "w") as f:
            json.dump(shipment, f, indent=2)

        print(f"Shipment saved to shipment_{i+1}.json")


if __name__ == "__main__":
    main()
