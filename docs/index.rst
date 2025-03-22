Welcome to Templify's documentation!
================================

Templify is a powerful templating library that supports multiple template formats and data structures.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   examples
   contributing

Features
--------

* Multiple template format support:
  * Text templates with placeholders
  * JMESPath expressions
  * Jinja2 templates
* Data structure templating
* PDF generation support
* Extensible architecture

Installation
-----------

.. code-block:: bash

   pip install templify

Quick Start
----------

.. code-block:: python

   from templify import render_data

   # Simple text template
   template = "Hello, {{name}}!"
   context = {"name": "World"}
   result = render_data(template, context)
   print(result)  # Output: Hello, World!

   # JMESPath template
   template = "Top products: {{sort_by(@, &revenue)[-2:] | [*].name | join(', ', @)}}"
   context = {
       "products": [
           {"name": "Product A", "revenue": 100},
           {"name": "Product B", "revenue": 200},
           {"name": "Product C", "revenue": 300}
       ]
   }
   result = render_data(template, context)
   print(result)  # Output: Top products: Product B, Product C

   # Jinja2 template
   template = """
   {% if user.is_admin %}
       Welcome, Administrator {{ user.name }}!
   {% else %}
       Welcome, {{ user.name }}!
   {% endif %}
   """
   context = {
       "user": {
           "name": "Alice",
           "is_admin": True
       }
   }
   result = render_data(template, context)
   print(result)  # Output: Welcome, Administrator Alice!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
