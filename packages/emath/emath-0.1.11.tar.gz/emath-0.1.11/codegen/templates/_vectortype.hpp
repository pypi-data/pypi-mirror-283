
// generated from codegen/templates/_vectortype.hpp

#ifndef E_MATH_VECTORTYPE_HPP
#define E_MATH_VECTORTYPE_HPP

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// glm
#include <glm/glm.hpp>
#include <glm/ext.hpp>

{% for name, component_count, c_type in types %}

typedef glm::vec<{{ component_count }}, {{ c_type }}, glm::defaultp> {{ name }}Glm;

struct {{ name }}
{
    PyObject_HEAD
    PyObject *weakreflist;
    {{ name }}Glm *glm;
};

static {{ name }} *
create_{{ name }}_from_glm(const {{ name }}Glm& glm);


struct {{ name }}Array
{
    PyObject_HEAD
    PyObject *weakreflist;
    size_t length;
    {{ name }}Glm *glm;
};

{% endfor %}

#endif