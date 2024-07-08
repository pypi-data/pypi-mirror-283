
// generated from codegen/templates/_matrixtype.hpp

#ifndef E_MATH_MATRIXTYPE_HPP
#define E_MATH_MATRIXTYPE_HPP

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// glm
#include <glm/glm.hpp>
#include <glm/ext.hpp>

{% for name, column_size, row_size, c_type in types %}

typedef glm::tmat{{ row_size }}x{{ column_size }}<{{ c_type }}, glm::defaultp> {{ name }}Glm;

struct {{ name }}
{
    PyObject_HEAD
    PyObject *weakreflist;
    {{ name }}Glm *glm;
};

struct {{ name }}Array
{
    PyObject_HEAD
    PyObject *weakreflist;
    size_t length;
    {{ name }}Glm *glm;
};

{% endfor %}

#endif