
// generated from codegen/templates/math.h

#ifndef E_MATH_API_HPP
#define E_MATH_API_HPP

// stdlib
#include <stdbool.h>
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef PyTypeObject *(*EMathApi_GetType)();
typedef size_t (*EMathApi_GetArrayLength)(const PyObject *);

{% for type in vector_types %}
{% with c_type={
    "B": 'bool',
    "F": 'float',
    "D": 'double',
    "I": 'int',
    "I8": 'int8_t',
    "I16": 'int16_t',
    "I32": 'int32_t',
    "I64": 'int64_t',
    "U": 'unsigned int',
    "U8": 'uint8_t',
    "U16": 'uint16_t',
    "U32": 'uint32_t',
    "U64": 'uint64_t',
}[type[:type.find('V')]] %}
    typedef PyObject *(*EMathApi_Create{{ type }})(const {{ c_type }} *);
    typedef PyObject *(*EMathApi_Create{{ type }}Array)(size_t, const {{ c_type }} *);
    typedef const {{ c_type }} *(*EMathApi_Get{{ type }}ValuePointer)(const PyObject *);
{% endwith %}
{% endfor %}

{% for type in matrix_types %}
{% with c_type={
    "F": 'float',
    "D": 'double',
}[type[:type.find('M')]] %}
    typedef PyObject *(*EMathApi_Create{{ type }})(const {{ c_type }} *);
    typedef PyObject *(*EMathApi_Create{{ type }}Array)(size_t, const {{ c_type }} *);
    typedef {{ c_type }} *(*EMathApi_Get{{ type }}ValuePointer)(const PyObject *);
{% endwith %}
{% endfor %}

{% for type in quaternion_types %}
{% with c_type={
    "F": 'float',
    "D": 'double',
}[type[:type.find('Q')]] %}
    typedef PyObject *(*EMathApi_Create{{ type }})(const {{ c_type }} *);
    typedef PyObject *(*EMathApi_Create{{ type }}Array)(size_t, const {{ c_type }} *);
    typedef {{ c_type }} *(*EMathApi_Get{{ type }}ValuePointer)(const PyObject *);
{% endwith %}
{% endfor %}

{% for type in pod_types %}
{% with c_type={
    "B": 'bool',
    "F": 'float',
    "D": 'double',
    "I": 'int',
    "I8": 'int8_t',
    "I16": 'int16_t',
    "I32": 'int32_t',
    "I64": 'int64_t',
    "U": 'unsigned int',
    "U8": 'uint8_t',
    "U16": 'uint16_t',
    "U32": 'uint32_t',
    "U64": 'uint64_t',
}[type] %}
    typedef PyObject *(*EMathApi_Create{{ type }}Array)(size_t, const {{ c_type }} *);
    typedef {{ c_type }} *(*EMathApi_Get{{ type }}ValuePointer)(const PyObject *);
{% endwith %}
{% endfor %}


struct EMathApi
{
    const size_t version;
    {% for type in vector_types %}
        EMathApi_GetType {{ type }}_GetType;
        EMathApi_GetType {{ type }}Array_GetType;
        EMathApi_Create{{ type }} {{ type }}_Create;
        EMathApi_Create{{ type }}Array {{ type }}Array_Create;
        EMathApi_Get{{ type }}ValuePointer {{ type }}_GetValuePointer;
        EMathApi_Get{{ type }}ValuePointer {{ type }}Array_GetValuePointer;
        EMathApi_GetArrayLength {{ type }}Array_GetLength;
    {% endfor %}
    {% for type in matrix_types %}
        EMathApi_GetType {{ type }}_GetType;
        EMathApi_GetType {{ type }}Array_GetType;
        EMathApi_Create{{ type }} {{ type }}_Create;
        EMathApi_Create{{ type }}Array {{ type }}Array_Create;
        EMathApi_Get{{ type }}ValuePointer {{ type }}_GetValuePointer;
        EMathApi_Get{{ type }}ValuePointer {{ type }}Array_GetValuePointer;
        EMathApi_GetArrayLength {{ type }}Array_GetLength;
    {% endfor %}
    {% for type in quaternion_types %}
        EMathApi_GetType {{ type }}_GetType;
        EMathApi_GetType {{ type }}Array_GetType;
        EMathApi_Create{{ type }} {{ type }}_Create;
        EMathApi_Create{{ type }}Array {{ type }}Array_Create;
        EMathApi_Get{{ type }}ValuePointer {{ type }}_GetValuePointer;
        EMathApi_Get{{ type }}ValuePointer {{ type }}Array_GetValuePointer;
        EMathApi_GetArrayLength {{ type }}Array_GetLength;
    {% endfor %}
    {% for type in pod_types %}
        EMathApi_GetType {{ type }}Array_GetType;
        EMathApi_Create{{ type }}Array {{ type }}Array_Create;
        EMathApi_Get{{ type }}ValuePointer {{ type }}Array_GetValuePointer;
        EMathApi_GetArrayLength {{ type }}Array_GetLength;
    {% endfor %}
};

static struct EMathApi *
EMathApi_Get()
{
    if (!PyImport_ImportModule("emath._emath")){ return 0; }
    return (struct EMathApi *)PyCapsule_Import("emath._emath._api", 0);
}

static void
EMathApi_Release()
{
    PyObject *module = PyImport_ImportModule("emath._emath");
    if (!module){ return; }
    Py_DECREF(module);
    Py_DECREF(module);
}

#ifdef __cplusplus
}
#endif

#endif