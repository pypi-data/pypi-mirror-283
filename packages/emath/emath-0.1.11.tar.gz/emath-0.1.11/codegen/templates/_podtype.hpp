
// generated from codegen/templates/_podtype.hpp

#ifndef E_MATH_PODTYPE_HPP
#define E_MATH_PODTYPE_HPP

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>

{% for name, c_type in types %}

struct {{ name }}Array
{
    PyObject_HEAD
    PyObject *weakreflist;
    size_t length;
    {{ c_type }} *pod;
};

{% endfor %}

#endif