
// generated from codegen/templates/_quaterniontype.hpp

#ifndef E_MATH_QUATERNIONTYPE_HPP
#define E_MATH_QUATERNIONTYPE_HPP

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// glm
#include <glm/glm.hpp>
#include <glm/ext.hpp>

{% for name, c_type in types %}

typedef glm::tquat<{{ c_type }}> {{ name }}Glm;

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