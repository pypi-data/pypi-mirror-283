API Reference
=============

.. py:data:: Number

    Type alias for int, float and bool compatible python objects.


.. toctree::
   :maxdepth: 1

{% for type in vector_types %}
   api_{{ type.lower() }}
   api_{{ type.lower() }}_array
{% endfor %}