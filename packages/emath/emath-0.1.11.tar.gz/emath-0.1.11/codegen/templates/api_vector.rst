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
    _ generated from codegen/templates/api_vector.rst

{{ name }}
==========

Python API
----------

.. py:class:: {{ name }}

    .. py:method:: __init__()

        Initializes a {{ name }} with :code:`0` in all component positions.

{% if component_count > 1 %}
    .. py:method:: __init__(all: Number, /)
        :no-index:

        Initializes a {{ name }} with :code:`all` in all component positions.

{% if component_count == 2 %}
    .. py:method:: def __init__(x: Number, y: Number, /)
        :no-index:
{% endif %}
{% if component_count == 3 %}
    .. py:method:: __init__(x: Number, y: Number, z: Number, /)
        :no-index:
{% endif %}
{% if component_count == 4 %}
    .. py:method:: __init__(x: Number, y: Number, z: Number, w: Number, /)
        :no-index:
{% endif %}
{% else %}
    .. py:method:: __init__(x: Number, /)
        :no-index:
{% endif %}
        Initializes a {{ name }}.


    .. py:method:: __iter__() -> Iterator[{{ component_type }}]

        Iterate over each component of the vector.


    .. py:method:: __hash__() -> int

        Generates a hash of the vector.


    .. py:method:: __len__() -> int:

        Returns the number of components in the vector (always :code:`{{ component_count }}`).


    .. py:method:: __getitem__(key: int) -> {{ component_type }}

        Get the value of the vector component at the position specified.


    .. py:method:: __eq__(other: Any) -> bool

        Check if this vector and the other object are equal.
        The other object must also be a :py:class:`{{ name }}` in order to pass as :code:`True`.


    .. py:method:: __lt__(other: Any) -> bool

        Check if this vector is less than the other object.
        The other object must also be a :py:class:`{{ name }}` in order to pass as :code:`True`.
        Note this comparison operates the same as other Python container types.


    .. py:method:: __le__(other: Any) -> bool

        Check if this vector is less than or equal to the other object.
        The other object must also be a :py:class:`{{ name }}` in order to pass as :code:`True`.
        Note this comparison operates the same as other Python container types.


    .. py:method:: __gt__(other: Any) -> bool

        Check if this vector is greater than the other object.
        The other object must also be a :py:class:`{{ name }}` in order to pass as :code:`True`.
        Note this comparison operates the same as other Python container types.


    .. py:method:: __ge__(other: Any) -> bool

        Check if this vector is greater than or equal to the other object.
        The other object must also be a :py:class:`{{ name }}` in order to pass as :code:`True`.
        Note this comparison operates the same as other Python container types.


    .. py:method:: __buffer__(flags: int) -> memoryview

        Generates a read-only memory view with access to the underyling vector data.
        The C data-type equivalent for the buffer is :code:`{{ c_type }}[{{ component_count }}]`.


    .. py:method:: __release_buffer__(view: memoryview) -> None

        Releases the memory buffer returned by :py:meth:`__buffer__`.


    .. py:method:: __add__(other: {{ name }}) -> {{ name }}

        Add the two vectors together, component-wise.


    .. py:method:: __add__(other: Number) -> {{ name }}
        :no-index:

        Add the number to each component of the vector.


    .. py:method:: __sub__(other: {{ name }}) -> {{ name }}

        Subtract two vectors from each other, component-wise.


    .. py:method:: __sub__(other: Number) -> {{ name }}
        :no-index:

        Subtract the number from each component of the vector.


    .. py:method:: __mul__(other: {{ name }}) -> {{ name }}

        Multiple the two vectors, component-wise.


    .. py:method:: __mul__(other: Number) -> {{ name }}
        :no-index:

        Multiply each component in the vector by the number.

{% if component_type == 'float' %}
    .. py:method:: __matmul__(other: {{ name }}) -> {{ name }}

        Computes the dot product of the two vectors.


    .. py:method:: __mod__(other: {{ name }}) -> {{ name }}

        Computes the modulus, component-wise.


    .. py:method:: __mod__(other: Number) -> {{ name }}
        :no-index:

        Computes the modulus for each component using the number.


    .. py:method:: __pow__(other: {{ name }}) -> {{ name }}

        Computes the power of each component in the vector by the other's component.


    .. py:method:: __pow__(other: Number) -> {{ name }}
        :no-index:

        Computes the power of each component in the vector by the number.
{% endif %}

{% if component_type != 'bool' %}
    .. py:method:: __truediv__(other: {{ name }}) -> {{ name }}

        Divide the two vectors, component-wise.


    .. py:method:: __truediv__(other: Number) -> {{ name }}
        :no-index:

        Divide each component in the vector by the number.
{% endif %}

{% if is_unsigned %}
    .. py:method:: __neg__() -> {{ name }}

        Returns a new vector with each component's sign flipped.
{% endif %}

    .. py:method:: __abs__() -> {{ name }}

        Returns a new vector with each component's sign made positive.


    .. py:method:: __bool__() -> {{ name }}

        Returns :code:`True` if all components of the vector are not :code:`0`.

{% if component_type == 'float' %}
    .. py:property:: magnitude
        :type: {{ component_type }}

        The magnitude of the vector.

{% if component_count == 3 %}
    .. py:method:: cross(other: {{ name }}, /) -> {{ name }}

        Calculates the cross product between the two vectors.


    .. py:method:: to_quaternion() -> {{ name[0] }}Quaternion

        Converts the vector, where the components represent pitch, raw and roll in radians,
        to a quaternion
{% endif %}

    .. py:method:: normalize() -> {{ name }}

        Computes a normalized vector.


    .. py:method:: distance(other: {{ name }}, /) -> {{ component_type }}

        Computes the distance between the two vectors.


    .. py:method:: lerp(other: {{ name }}, t: {{ component_type }}, /) -> {{ name }}

        Calculate the point on the linear interpolant between the two vectors using t as the
        time between the two vectors. Note that t is not bound between :code:`0` and :code:`1`.
        That is, this method may be used to extrapolate.
{% endif %}

    .. py:method:: min(n: Number, /) -> {{ name }}

        Creates a vector where each component is at most equal to the input.


    .. py:method:: max(n: Number, /) -> {{ name }}

        Creates a vector where each component is at least equal to the input.


    .. py:method:: clamp(min: Number, max: Number, /) -> {{ name }}

        Creates a vector where each component is at most equal to min and at least equal to max.


    .. py:method:: get_limits() -> tuple[{{ component_type }}, {{ component_type }}]
        :classmethod:

        Returns a tuple describing the minimum and maximum (respectively) values that vector can
        store per component.


    .. py:property:: pointer
        :type: ctypes._Pointer[{{ ctypes_type }}]

        :code:`ctypes` pointer to the data represented by the vector.


    .. py:method:: get_size() -> int
        :classmethod:

        Returns the size, in bytes, of the data represented by the vector.


    .. py:method:: get_array_type() -> type[{{ name }}Array]
        :classmethod:

        Returns the emath class used to create an array of this vector type.


    .. py:method:: from_buffer(buffer: Buffer, /) -> {{ name }}
        :classmethod:

        Create a vector from an object supporting the buffer interface.
        The expected C data-type equivalent for the buffer is
        :code:`{{ c_type }}[{{ component_count }}]`.


C API
-----

.. c:function:: PyObject *{{ name }}_Create(const {{ c_type }} *value)

    Returns a new :py:class:`{{ name }}` object or :code:`0` on failure.
    Data from the value pointer is copied.
    Note that the function reads {{ component_count }} {{ c_type }}{% if component_count > 1 %}s{% endif %} from the pointer.


.. c:function:: const {{ c_type }} *{{ name }}_GetValuePointer(const PyObject *vector)

    Returns a pointer to the data represented by :py:class:`{{ name }}`. The lifetime of this
    pointer is tied to the :py:class:`{{ name }}` object.


.. c:function:: PyTypeObject *{{ name }}_GetType()

    Returns the type object of :py:class:`{{ name }}`.

{% endwith %}
{% endwith %}
{% endwith %}