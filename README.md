# Templify

Templify is a templating library designed for scenarios where data structures need to be managed independently from the code that generates them. This is particularly useful when dealing with external API specifications that may change over time.

## Example: UPS Shipment Creation

We've implemented two versions of the UPS shipment creation system:
1. Traditional approach (`examples/ups_shipment.py`)
2. Templify approach (`examples/ups_shipment_templify.py`)

### Key Differences

#### 1. Template Definition vs. Direct Construction

**Traditional Approach:**
```python
def create_shipment(customer_context, shipment_description, packages):
    return {
        "ShipmentRequest": {
            "Request": {
                "RequestOption": "nonvalidate",
                "TransactionReference": {
                    "CustomerContext": customer_context
                }
            },
            "Shipment": {
                "Description": shipment_description,
                "Shipper": {
                    "Name": "Company BV",
                    "AttentionName": "John Doe",
                    # ... many more fields ...
                },
                # ... more nested structures ...
            }
        }
    }
```

**Templify Approach:**
```python
# Define templates once
BASE_SHIPMENT_TEMPLATE = {
    "ShipmentRequest": {
        "Request": {
            "RequestOption": "nonvalidate",
            "TransactionReference": {
                "CustomerContext": "{customer_context}"
            }
        },
        "Shipment": {
            "Description": "{shipment_description}",
            "Shipper": "{shipper}",
            "ShipTo": "{ship_to}",
            # ... more placeholders ...
        }
    }
}

# Use templates with simple context
def create_shipment(customer_context, shipment_description, packages):
    context = {
        "customer_context": customer_context,
        "shipment_description": shipment_description,
        "shipper": SHIPPER_TEMPLATE,
        "ship_to": RECIPIENT_TEMPLATE,
        "packages": packages
    }
    return render_data(BASE_SHIPMENT_TEMPLATE, context)
```

### When to Use Templify

Templify is particularly valuable when:

1. **API Specifications Change Frequently**
   - New API versions require different payload structures
   - Fields need to be added, removed, or modified
   - Templates can be updated without changing code
   - Changes can be managed by non-developers

2. **Template Management is External**
   - Templates are stored in files or databases
   - Templates are managed by a separate team
   - Templates need to be version controlled independently
   - Templates can be updated without deployment

3. **Data Sources are Fixed**
   - Database queries are already defined
   - Business logic for data collection is stable
   - Only the output format needs to change
   - Data transformation rules are well-defined

### When to Use Traditional Approach

The traditional approach might be better when:

1. **Performance is Critical**
   - Direct dictionary construction is faster
   - No template parsing overhead
   - No string interpolation needed
   - Lower memory usage

2. **Type Safety is Important**
   - Python's static type checking works directly
   - IDE autocomplete works better
   - Compile-time error detection
   - Better refactoring support

3. **Simple, Stable Structures**
   - Payload structure rarely changes
   - Changes are always handled by developers
   - No need for external template management
   - Business logic and structure are tightly coupled

### Real-World Example: UPS API Version Update

Consider a scenario where UPS updates their API:

**Traditional Approach:**
```python
# Need to modify code and redeploy
def create_shipment_v2(customer_context, shipment_description, packages):
    return {
        "ShipmentRequest": {
            "Request": {
                "RequestOption": "nonvalidate",
                "TransactionReference": {
                    "CustomerContext": customer_context,
                    "NewField": "value"  # New field added
                }
            },
            # ... rest of the structure
        }
    }
```

**Templify Approach:**
```python
# Just update the template file
BASE_SHIPMENT_TEMPLATE_V2 = {
    "ShipmentRequest": {
        "Request": {
            "RequestOption": "nonvalidate",
            "TransactionReference": {
                "CustomerContext": "{customer_context}",
                "NewField": "{new_field}"  # New field added
            }
        },
        # ... rest of the template
    }
}

# Code remains unchanged
def create_shipment(customer_context, shipment_description, packages):
    context = {
        "customer_context": customer_context,
        "shipment_description": shipment_description,
        "shipper": SHIPPER_TEMPLATE,
        "ship_to": RECIPIENT_TEMPLATE,
        "packages": packages,
        "new_field": "value"  # Just add new field to context
    }
    return render_data(BASE_SHIPMENT_TEMPLATE_V2, context)
```

### Getting Started

1. Install Templify:
```bash
pip install templify
```

2. Define your templates:
```python
MY_TEMPLATE = {
    "field1": "{value1}",
    "field2": "{value2}"
}
```

3. Use the templates:
```python
from templify import render_data

context = {
    "value1": "Hello",
    "value2": "World"
}

result = render_data(MY_TEMPLATE, context)
```

### Advanced Features

1. **JMESPath Support**
```python
template = "{{ data | jmespath('items[?type==`book`]') }}"
```

2. **Missing Value Handling**
```python
result = render_data(template, context, handle_missing=MissingKeyHandling.DEFAULT)
```

3. **Type Preservation**
```python
# Returns actual dict/list objects when appropriate
result = render_data("{complex_object}", context)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
