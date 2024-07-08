{% with component_type='float' if name.startswith('F') else ('bool' if name.startswith('B') else 'int') %}
{% with is_unsigned=name.startswith('U') %}
{% with ctypes_type={
    "B": 'ctypes.c_bool',
    "D": 'ctypes.c_double',
    "F": 'ctypes.c_float',
    "I8": 'ctypes.c_int8',
    "U8": 'ctypes.c_uint8',
    "I16": 'ctypes.c_int16',
    "U16": 'ctypes.c_uint16',
    "I32": 'ctypes.c_int32',
    "U32": 'ctypes.c_uint32',
    "I64": 'ctypes.c_int64',
    "U64": 'ctypes.c_uint64',
    "I": 'ctypes.c_int',
    "U": 'ctypes.c_uint',
}[name[:name.find('V')]] %}

..
    _ generated from codegen/templates/api_vector_array.rst

{{ name }}Array
===============

Python API
----------

.. py:class:: {{ name }}Array

    .. py:method:: __init__(*vectors: {{ name }})

        Initializes a {{ name }}Array composed of the vectors provided.


    .. py:method:: __hash__() -> int

        Generates a hash of the array.


    .. py:method:: __len__() -> int:

        Returns the number of vectors in the array.


    .. py:method:: __iter__() -> Iterator[{{ component_type }}]

        Iterate over each vector in the array.


    .. py:method:: __getitem__(index: int) -> {{ component_type }}

        Get the vector in the array at the position specified.


    .. py:method:: __getitem__(index: slice) -> {{ component_type }}Array
        :no-index:

        Slice the array, generating a new one.


    .. py:method:: __eq__(other: Any) -> bool

        Check if this array and the other object are equal.
        The other object must also be a :py:class:`{{ name }}Array` in order to pass as :code:`True`.


    .. py:method:: __bool__() -> {{ name }}

        Returns :code:`True` if the array is not empty.


    .. py:method:: __buffer__(flags: int) -> memoryview

        Generates a read-only memory view with access to the underyling array data.
        The C data-type equivalent for the buffer is :code:`{{ c_type }}[{{ component_count }} * length]`.


    .. py:method:: __release_buffer__(view: memoryview) -> None

        Releases the memory buffer returned by :py:meth:`__buffer__`.


    .. py:property:: pointer
        :type: ctypes._Pointer[{{ ctypes_type }}]

        :code:`ctypes` pointer to the data represented by the array.

    .. py:property:: size
        :type: int

        Return the size, in bytes, of the data represented by the array.


    .. py:method:: get_size() -> int
        :classmethod:

        Returns the size, in bytes, of the data represented by the vector.


    .. py:method:: get_component_type() -> type[{{ name }}]
        :classmethod:

        Returns the emath class used to create a vector for this array type.


    .. py:method:: from_buffer(buffer: Buffer, /) -> {{ name }}
        :classmethod:

        Create an array from an object supporting the buffer interface.
        The expected C data-type equivalent for the buffer is
        :code:`{{ c_type }}[{{ component_count }} * length]`.


C API
-----

.. c:function:: PyObject *{{ name }}Array_Create(size_t length, const {{ c_type }} *value)

    Returns a new :py:class:`{{ name }}Array` object or :code:`0` on failure.
    Data from the value pointer is copied.
    Note that the function reads :code:`{{ component_count }} * length` {{ c_type }}s from the pointer.


.. c:function:: const {{ c_type }} *{{ name }}Array_GetValuePointer(const PyObject *vector)

    Returns a pointer to the data represented by :py:class:`{{ name }}Array`. The lifetime of this
    pointer is tied to the :py:class:`{{ name }}Array` object.


.. c:function:: size_t {{ name }}Array_GetLength()

    Returns the number of vectors in the :py:class:`{{ name }}Array` object.


.. c:function:: PyTypeObject *{{ name }}Array_GetType()

    Returns the type object of :py:class:`{{ name }}Array`.

{% endwith %}
{% endwith %}
{% endwith %}