"""
Tests for the UPS shipment example using Templify.

This test file demonstrates how Templify simplifies testing by separating
template logic from business logic.
"""

from examples.ups_shipment_templify import (
    create_package_data,
    create_packages_data,
    create_shipment,
    create_shipments,
    BASE_SHIPMENT_TEMPLATE,
    SHIPPER_TEMPLATE,
    RECIPIENT_TEMPLATE,
    PAYMENT_TEMPLATE,
    SERVICE_TEMPLATE,
)
from templify import render_data


def test_package_template():
    """Test that the package template is correctly structured."""
    # Create a package with default values
    package = create_package_data(1)

    # Verify the package structure
    assert package["PackagingType"]["Code"] == "02"
    assert package["Dimensions"]["UnitOfMeasurement"]["Code"] == "CM"
    assert package["PackageWeight"]["UnitOfMeasurement"]["Code"] == "KG"
    assert package["PackageID"] == "Package 1"
    assert package["Dimensions"]["Length"] == "30.0"
    assert package["Dimensions"]["Width"] == "20.0"
    assert package["Dimensions"]["Height"] == "15.0"
    assert package["PackageWeight"]["Weight"] == "2.5"


def test_custom_package_dimensions():
    """Test creating packages with custom dimensions."""
    # Create a package with custom dimensions
    package = create_package_data(1, weight=5.0, length=40.0, width=30.0, height=20.0)

    # Verify the custom dimensions
    assert package["Dimensions"]["Length"] == "40.0"
    assert package["Dimensions"]["Width"] == "30.0"
    assert package["Dimensions"]["Height"] == "20.0"
    assert package["PackageWeight"]["Weight"] == "5.0"


def test_create_multiple_packages():
    """Test creating multiple packages."""
    # Create 3 packages
    packages = create_packages_data(3)

    # Verify the number of packages
    assert len(packages) == 3

    # Verify each package has the correct ID
    for i, package in enumerate(packages):
        assert package["PackageID"] == f"Package {i+1}"


def test_create_shipment():
    """Test creating a complete shipment."""
    # Create a shipment with 2 packages
    packages = create_packages_data(2)
    shipment = create_shipment("Test Shipment 123", "Test Shipment", packages)

    # Verify the shipment structure
    assert shipment["ShipmentRequest"]["Request"]["TransactionReference"]["CustomerContext"] == "Test Shipment 123"
    assert shipment["ShipmentRequest"]["Shipment"]["Description"] == "Test Shipment"
    assert shipment["ShipmentRequest"]["Shipment"]["Shipper"] == SHIPPER_TEMPLATE
    assert shipment["ShipmentRequest"]["Shipment"]["ShipTo"] == RECIPIENT_TEMPLATE
    assert shipment["ShipmentRequest"]["Shipment"]["ShipFrom"] == SHIPPER_TEMPLATE
    assert shipment["ShipmentRequest"]["Shipment"]["PaymentInformation"] == PAYMENT_TEMPLATE
    assert shipment["ShipmentRequest"]["Shipment"]["Service"] == SERVICE_TEMPLATE

    # Verify the packages
    assert len(shipment["ShipmentRequest"]["Shipment"]["Package"]) == 2
    assert shipment["ShipmentRequest"]["Shipment"]["Package"][0]["PackageID"] == "Package 1"
    assert shipment["ShipmentRequest"]["Shipment"]["Package"][1]["PackageID"] == "Package 2"


def test_create_multiple_shipments():
    """Test creating multiple shipments when exceeding package limit."""
    # Create 30 packages (should be split into 2 shipments)
    shipments = create_shipments("Test Multiple Shipments 456", "Test Multiple Shipments", 30)

    # Verify the number of shipments
    assert len(shipments) == 2

    # Verify the first shipment has 20 packages
    first_shipment = shipments[0]["ShipmentRequest"]["Shipment"]["Package"]
    assert len(first_shipment) == 20

    # Verify the second shipment has 10 packages
    second_shipment = shipments[1]["ShipmentRequest"]["Shipment"]["Package"]
    assert len(second_shipment) == 10

    # Verify the customer context is unique for each shipment
    context1 = "Test Multiple Shipments 456-1"
    context2 = "Test Multiple Shipments 456-2"
    assert shipments[0]["ShipmentRequest"]["Request"]["TransactionReference"]["CustomerContext"] == context1
    assert shipments[1]["ShipmentRequest"]["Request"]["TransactionReference"]["CustomerContext"] == context2

    # Verify the shipment descriptions include the shipment number
    first_desc = shipments[0]["ShipmentRequest"]["Shipment"]["Description"]
    second_desc = shipments[1]["ShipmentRequest"]["Shipment"]["Description"]
    assert "Shipment 1 of 2" in first_desc
    assert "Shipment 2 of 2" in second_desc

    # Verify package IDs are sequential across shipments
    assert first_shipment[0]["PackageID"] == "Package 1"
    assert first_shipment[19]["PackageID"] == "Package 20"
    assert second_shipment[0]["PackageID"] == "Package 21"
    assert second_shipment[9]["PackageID"] == "Package 30"


def test_template_composition():
    """Test that Templify correctly composes templates."""
    # Create a simple context
    context = {
        "customer_context": "Test Context",
        "shipment_description": "Test Description",
        "shipper": SHIPPER_TEMPLATE,
        "ship_to": RECIPIENT_TEMPLATE,
        "ship_from": SHIPPER_TEMPLATE,
        "payment": PAYMENT_TEMPLATE,
        "service": SERVICE_TEMPLATE,
        "packages": [create_package_data(1)],
    }

    # Render the template
    result = render_data(BASE_SHIPMENT_TEMPLATE, context)

    # Verify the result
    assert result["ShipmentRequest"]["Request"]["TransactionReference"]["CustomerContext"] == "Test Context"
    assert result["ShipmentRequest"]["Shipment"]["Description"] == "Test Description"
    assert result["ShipmentRequest"]["Shipment"]["Shipper"] == SHIPPER_TEMPLATE
    assert result["ShipmentRequest"]["Shipment"]["ShipTo"] == RECIPIENT_TEMPLATE
    assert result["ShipmentRequest"]["Shipment"]["ShipFrom"] == SHIPPER_TEMPLATE
    assert result["ShipmentRequest"]["Shipment"]["PaymentInformation"] == PAYMENT_TEMPLATE
    assert result["ShipmentRequest"]["Shipment"]["Service"] == SERVICE_TEMPLATE
    assert len(result["ShipmentRequest"]["Shipment"]["Package"]) == 1
    assert result["ShipmentRequest"]["Shipment"]["Package"][0]["PackageID"] == "Package 1"
