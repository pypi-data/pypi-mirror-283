
// generated from codegen/templates/_matrix.hpp

#ifndef E_MATH_{{ name.upper() }}_HPP
#define E_MATH_{{ name.upper() }}_HPP

// stdlib
#include <limits>
#include <functional>
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
// glm
#include <glm/glm.hpp>
#include <glm/ext.hpp>
// emath
#include "_modulestate.hpp"
#include "_vectortype.hpp"
#include "_matrixtype.hpp"
#include "_type.hpp"


static PyObject *
{{ name }}__new__(PyTypeObject *cls, PyObject *args, PyObject *kwds)
{
    if (kwds && PyDict_Size(kwds) != 0)
    {
        PyErr_SetString(
            PyExc_TypeError,
            "{{ name }} does accept any keyword arguments"
        );
        return 0;
    }

    {{ name }}Glm *glm = 0;
    auto arg_count = PyTuple_GET_SIZE(args);
    switch (PyTuple_GET_SIZE(args))
    {
        case 0:
        {
            glm = new {{ name }}Glm();
            break;
        }
        case 1:
        {
            auto arg = PyTuple_GET_ITEM(args, 0);
            {{ c_type }} arg_c = pyobject_to_c_{{ c_type.replace(' ', '_') }}(arg);
            auto error_occurred = PyErr_Occurred();
            if (error_occurred){ return 0; }
            glm = new {{ name }}Glm(arg_c);
            break;
        }
        case {{ row_size }}:
        {
            auto module_state = get_module_state();
            if (!module_state){ return 0; }
            auto column_cls = module_state->{{ column_type }}_PyTypeObject;
            {% for i in range(row_size) %}
                PyObject *p_{{ i }} = PyTuple_GET_ITEM(args, {{ i }});
                if (Py_TYPE(p_{{ i }}) != column_cls)
                {
                    PyErr_Format(
                        PyExc_TypeError,
                        "invalid column supplied, expected %R, (got %R)",
                        column_cls,
                        p_{{ i }}
                    );
                    return 0;
                }
            {% endfor %}
            glm = new {{ name }}Glm(
                {% for i in range(row_size) %}
                    *(({{ column_type }} *)p_{{ i }})->glm{% if i != row_size - 1 %}, {% endif %}
                {% endfor %}
            );

            break;
        }
        case {{ component_count }}:
        {
            {% for i in range(component_count) %}
                {{ c_type }} c_{{ i }} = 0;
            {% endfor %}
            {% for i in range(component_count) %}
            {
                auto arg = PyTuple_GET_ITEM(args, {{ i }});
                c_{{ i }} = pyobject_to_c_{{ c_type.replace(' ', '_') }}(arg);
                auto error_occurred = PyErr_Occurred();
                if (error_occurred){ return 0; }
            }
            {% endfor %}
            glm = new {{ name }}Glm(
                {% for i in range(component_count) %}
                    c_{{ i }}{% if i != component_count - 1 %}, {% endif %}
                {% endfor %}
            );
            break;
        }
        default:
        {
            PyErr_Format(
                PyExc_TypeError,
                "invalid number of arguments supplied to {{ name }}, expected "
                "0, 1, {{ row_size }} or {{ component_count }} (got %zd)",
                arg_count
            );
            return 0;
        }
    }

    {{ name }} *self = ({{ name }}*)cls->tp_alloc(cls, 0);
    if (!self)
    {
        delete glm;
        return 0;
    }
    self->glm = glm;

    return (PyObject *)self;
}


static void
{{ name }}__dealloc__({{ name }} *self)
{
    if (self->weakreflist)
    {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    delete self->glm;

    PyTypeObject *type = Py_TYPE(self);
    type->tp_free(self);
    Py_DECREF(type);
}


// this is roughly copied from how python hashes tuples in 3.11
#if SIZEOF_PY_UHASH_T > 4
#define _HASH_XXPRIME_1 ((Py_uhash_t)11400714785074694791ULL)
#define _HASH_XXPRIME_2 ((Py_uhash_t)14029467366897019727ULL)
#define _HASH_XXPRIME_5 ((Py_uhash_t)2870177450012600261ULL)
#define _HASH_XXROTATE(x) ((x << 31) | (x >> 33))  /* Rotate left 31 bits */
#else
#define _HASH_XXPRIME_1 ((Py_uhash_t)2654435761UL)
#define _HASH_XXPRIME_2 ((Py_uhash_t)2246822519UL)
#define _HASH_XXPRIME_5 ((Py_uhash_t)374761393UL)
#define _HASH_XXROTATE(x) ((x << 13) | (x >> 19))  /* Rotate left 13 bits */
#endif

static Py_hash_t
{{ name }}__hash__({{ name }} *self)
{
    Py_ssize_t len = {{ component_count }};
    Py_uhash_t acc = _HASH_XXPRIME_5;
    for ({{ name }}Glm::length_type c = 0; c < {{ column_size }}; c++)
    {
        for ({{ name }}Glm::length_type r = 0; r < {{ row_size }}; r++)
        {
            Py_uhash_t lane = std::hash<{{ c_type }}>{}((*self->glm)[r][c]);
            acc += lane * _HASH_XXPRIME_2;
            acc = _HASH_XXROTATE(acc);
            acc *= _HASH_XXPRIME_1;
        }
        acc += len ^ (_HASH_XXPRIME_5 ^ 3527539UL);
    }

    if (acc == (Py_uhash_t)-1) {
        return 1546275796;
    }
    return acc;
}


static PyObject *
{{ name }}__repr__({{ name }} *self)
{
    PyObject *result = 0;
    {% for c in range(column_size) %}
    {% for r in range(row_size) %}
        PyObject *py_{{ c }}_{{ r }} = 0;
    {% endfor %}
    {% endfor %}

    {% for c in range(column_size) %}
    {% for r in range(row_size) %}
        py_{{ c }}_{{ r }} = c_{{ c_type.replace(' ', '_') }}_to_pyobject((*self->glm)[{{ r }}][{{ c }}]);
        if (!py_{{ c }}_{{ r }}){ goto cleanup; }
    {% endfor %}
    {% endfor %}

    result = PyUnicode_FromFormat(
        "{{ name }}("
        {% for r in range(row_size) %}
        "("
        {% for c in range(column_size) %}
            "%R"
            {% if c != column_size - 1 %}", "{% endif %}
        {% endfor %}
        ")"
        {% if r != row_size - 1 %}
        ", "
        {% endif %}
        {% endfor %}
        ")",
        {% for r in range(row_size) %}
        {% for c in range(column_size) %}
            py_{{ c }}_{{ r }}
            {% if r == row_size - 1 and c == column_size - 1 %}{% else %}, {% endif %}
        {% endfor %}
        {% endfor %}
    );
cleanup:
    {% for c in range(column_size) %}
    {% for r in range(row_size) %}
        Py_XDECREF(py_{{ c }}_{{ r }});
    {% endfor %}
    {% endfor %}
    return result;
}


static Py_ssize_t
{{ name }}__len__({{ name }} *self)
{
    return {{ row_size }};
}


static PyObject *
{{ name }}__getitem__({{ name }} *self, Py_ssize_t index)
{
    if (index < 0 || index > {{ row_size - 1 }})
    {
        PyErr_Format(PyExc_IndexError, "index out of range");
        return 0;
    }
    const auto& v = (*self->glm)[({{ name }}Glm::length_type)index];
    return (PyObject *)create_{{ column_type }}_from_glm(v);
}


static PyObject *
{{ name}}__richcmp__({{ name }} *self, {{ name }} *other, int op)
{
    if (Py_TYPE(self) != Py_TYPE(other))
    {
        Py_RETURN_NOTIMPLEMENTED;
    }

    switch(op)
    {
        case Py_EQ:
        {
            if ((*self->glm) == (*other->glm))
            {
                Py_RETURN_TRUE;
            }
            else
            {
                Py_RETURN_FALSE;
            }
        }
        case Py_NE:
        {
            if ((*self->glm) != (*other->glm))
            {
                Py_RETURN_TRUE;
            }
            else
            {
                Py_RETURN_FALSE;
            }
        }
    }
    Py_RETURN_NOTIMPLEMENTED;
}


static PyObject *
{{ name}}__add__(PyObject *left, PyObject *right)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ name }}_PyTypeObject;

    {{ name }}Glm matrix;
    if (Py_TYPE(left) == Py_TYPE(right))
    {
        matrix = (*(({{ name }} *)left)->glm) + (*(({{ name }} *)right)->glm);
    }
    else
    {
        if (Py_TYPE(left) == cls)
        {
            auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            matrix = (*(({{ name }} *)left)->glm) + c_right;
        }
        else
        {
            auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            matrix = (*(({{ name }} *)right)->glm) + c_left;
        }
    }

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(matrix);

    return (PyObject *)result;
}


static PyObject *
{{ name}}__sub__(PyObject *left, PyObject *right)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ name }}_PyTypeObject;

    {{ name }}Glm matrix;
    if (Py_TYPE(left) == Py_TYPE(right))
    {
        matrix = (*(({{ name }} *)left)->glm) - (*(({{ name }} *)right)->glm);
    }
    else
    {
        if (Py_TYPE(left) == cls)
        {
            auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            matrix = (*(({{ name }} *)left)->glm) - c_right;
        }
        else
        {
            auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            {% if column_size == row_size %}
                matrix = c_left - (*(({{ name }} *)right)->glm);
            {% else %}
                matrix = {{ name }}Glm(
                    {% for i in range(component_count) %}
                        c_left{% if i < component_count - 1 %}, {% endif %}
                    {% endfor %}
                ) - (*(({{ name }} *)right)->glm);
            {% endif %}
        }
    }

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(matrix);

    return (PyObject *)result;
}


static PyObject *
{{ name}}__mul__(PyObject *left, PyObject *right)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ name }}_PyTypeObject;

    {{ name }}Glm matrix;
    if (Py_TYPE(left) == cls)
    {
        auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
        if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
        matrix = (*(({{name }} *)left)->glm) * c_right;
    }
    else
    {
        auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
        if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
        matrix = c_left * (*(({{name }} *)right)->glm);
    }

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(matrix);

    return (PyObject *)result;
}


static PyObject *
{{ name }}__matmul__(PyObject *left, PyObject *right)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ name }}_PyTypeObject;

    if (Py_TYPE(left) == cls)
    {
        {% for c in range(2, 5) %}
        {% with right_name=(('D' if c_type == 'double' else 'F') + 'Matrix' + str(c) + 'x' + str(row_size)) %}
        {% with result_name=(('D' if c_type == 'double' else 'F') + 'Matrix' + str(c) + 'x' + str(column_size)) %}
        {
            auto right_cls = module_state->{{ right_name }}_PyTypeObject;
            auto result_cls = module_state->{{ result_name }}_PyTypeObject;
            if (Py_TYPE(right) == right_cls)
            {
                {{ result_name }} *result = ({{ result_name }} *)result_cls->tp_alloc(result_cls, 0);
                if (!result){ return 0; }
                result->glm = new {{ result_name }}Glm(
                    (*(({{ name }} *)left)->glm) * (*(({{ right_name }} *)right)->glm)
                );
                return (PyObject *)result;
            }
        }
        {% endwith %}
        {% endwith %}
        {% endfor %}

        {% if row_size == 4 and column_size == 4 %}
        {
            auto vector3_cls = module_state->{{ name[0] }}Vector3_PyTypeObject;
            if (Py_TYPE(right) == vector3_cls)
            {
                auto result = ({{ name[0] }}Vector3 *)vector3_cls->tp_alloc(vector3_cls, 0);
                if (!result){ return 0; }
                result->glm = new {{ name[0] }}Vector3Glm(
                    (*(({{ name }} *)left)->glm) * {{ name[0] }}Vector4Glm(
                        *(({{ name[0] }}Vector3 *)right)->glm,
                        1
                    )
                );
                return (PyObject *)result;
            }
        }
        {% endif %}

        {
            auto row_cls = module_state->{{ row_type }}_PyTypeObject;
            auto column_cls = module_state->{{ column_type }}_PyTypeObject;
            if (Py_TYPE(right) == row_cls)
            {
                {{ column_type }} *result = ({{ column_type }} *)column_cls->tp_alloc(column_cls, 0);
                if (!result){ return 0; }
                result->glm = new {{ column_type }}Glm(
                    (*(({{ name }} *)left)->glm) * (*(({{ row_type }} *)right)->glm)
                );
                return (PyObject *)result;
            }
        }
    }
    else
    {
        {% if row_size == 4 and column_size == 4 %}
        {
            auto vector3_cls = module_state->{{ name[0] }}Vector3_PyTypeObject;
            if (Py_TYPE(left) == vector3_cls)
            {
                auto result = ({{ name[0] }}Vector3 *)vector3_cls->tp_alloc(vector3_cls, 0);
                if (!result){ return 0; }
                result->glm = new {{ name[0] }}Vector3Glm(
                     {{ name[0] }}Vector4Glm(
                        *(({{ name[0] }}Vector3 *)left)->glm,
                        1
                    ) * (*(({{ name }} *)right)->glm)
                );
                return (PyObject *)result;
            }
        }
        {% endif %}

        auto row_cls = module_state->{{ row_type }}_PyTypeObject;
        auto column_cls = module_state->{{ column_type }}_PyTypeObject;
        if (Py_TYPE(left) == column_cls)
        {
            {{ row_type }} *result = ({{ row_type }} *)row_cls->tp_alloc(row_cls, 0);
            if (!result){ return 0; }
            result->glm = new {{ row_type }}Glm(
                (*(({{ column_type }} *)left)->glm) * (*(({{ name }} *)right)->glm)
            );
            return (PyObject *)result;
        }
    }

    Py_RETURN_NOTIMPLEMENTED;
}

static PyObject *
{{ name}}__truediv__(PyObject *left, PyObject *right)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ name }}_PyTypeObject;

    {{ name }}Glm matrix;
    if (Py_TYPE(left) == cls)
    {
        {% if row_size == column_size %}
        if (Py_TYPE(right) == cls)
        {
            {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
            if (!result){ return 0; }
            result->glm = new {{ name }}Glm(
                (*(({{ name }} *)left)->glm) / (*(({{ name }} *)right)->glm)
            );
            return (PyObject *)result;
        }

        {
            auto row_cls = module_state->{{ row_type }}_PyTypeObject;
            if (Py_TYPE(right) == row_cls)
            {
                {{ row_type }} *result = ({{ row_type }} *)row_cls->tp_alloc(row_cls, 0);
                if (!result){ return 0; }
                result->glm = new {{ row_type }}Glm(
                    (*(({{ name }} *)left)->glm) / (*(({{ row_type }} *)right)->glm)
                );
                return (PyObject *)result;
            }
        }
        {% endif %}

        auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
        if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
        matrix = (*(({{ name }} *)left)->glm) / c_right;
    }
    else
    {
        {% if row_size == column_size %}
        {
            auto row_cls = module_state->{{ row_type }}_PyTypeObject;
            if (Py_TYPE(left) == row_cls)
            {
                {{ row_type }} *result = ({{ row_type }} *)row_cls->tp_alloc(row_cls, 0);
                if (!result){ return 0; }
                result->glm = new {{ row_type }}Glm(
                    (*(({{ row_type }} *)left)->glm) / (*(({{ name }} *)right)->glm)
                );
                return (PyObject *)result;
            }
        }
        {% endif %}

        auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
        if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
        matrix = c_left / (*(({{ name }} *)right)->glm);
    }

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(matrix);

    return (PyObject *)result;
}


static PyObject *
{{ name}}__neg__({{ name }} *self)
{
    auto cls = Py_TYPE(self);

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(-(*self->glm));

    return (PyObject *)result;
}


static int
{{ name}}_getbufferproc({{ name }} *self, Py_buffer *view, int flags)
{
    if (flags & PyBUF_WRITABLE)
    {
        PyErr_SetString(PyExc_TypeError, "{{ name }} is read only");
        view->obj = 0;
        return -1;
    }
    if ((!(flags & PyBUF_C_CONTIGUOUS)) && flags & PyBUF_F_CONTIGUOUS)
    {
        PyErr_SetString(PyExc_BufferError, "{{ name }} cannot be made Fortran contiguous");
        view->obj = 0;
        return -1;
    }
    view->buf = glm::value_ptr(*self->glm);
    view->obj = (PyObject *)self;
    view->len = sizeof({{ c_type }}) * {{ component_count }};
    view->readonly = 1;
    view->itemsize = sizeof({{ c_type }});
    view->ndim = 2;
    if (flags & PyBUF_FORMAT)
    {
        view->format = "{{ struct_format }}";
    }
    else
    {
        view->format = 0;
    }
    if (flags & PyBUF_ND)
    {
        static Py_ssize_t shape[] = { {{ row_size }}, {{ column_size }} };
        view->shape = &shape[0];
    }
    else
    {
        view->shape = 0;
    }
    if (flags & PyBUF_STRIDES)
    {
        static Py_ssize_t strides[] = {
            sizeof({{ c_type }}) * {{ column_size }},
            sizeof({{ c_type }})
        };
        view->strides = &strides[0];
    }
    else
    {
        view->strides = 0;
    }
    view->suboffsets = 0;
    view->internal = 0;
    Py_INCREF(self);
    return 0;
}


static PyMemberDef {{ name }}_PyMemberDef[] = {
    {"__weaklistoffset__", T_PYSSIZET, offsetof({{ name }}, weakreflist), READONLY},
    {0}
};


static PyObject *
{{ name }}_pointer({{ name }} *self, void *)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto c_p = module_state->ctypes_c_{{ c_type.replace(' ', '_') }}_p;
    return PyObject_CallMethod(c_p, "from_address", "n", (Py_ssize_t)&self->glm);
}


static PyGetSetDef {{ name }}_PyGetSetDef[] = {
    {"pointer", (getter){{ name }}_pointer, 0, 0, 0},
    {0, 0, 0, 0, 0}
};


{% if row_size == column_size %}
    static {{ name }} *
    {{ name }}_inverse({{ name }} *self, void*)
    {
        auto cls = Py_TYPE(self);
        auto matrix = glm::inverse(*self->glm);
        {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(matrix);
        return result;
    }
{% endif %}


{% if row_size == 4 and column_size == 4 %}
    static {{ name }} *
    {{ name }}_rotate({{ name }} *self, PyObject *const *args, Py_ssize_t nargs)
    {
        if (nargs != 2)
        {
            PyErr_Format(PyExc_TypeError, "expected 2 arguments, got %zi", nargs);
            return 0;
        }

        {{ c_type }} angle = ({{ c_type }})PyFloat_AsDouble(args[0]);
        if (PyErr_Occurred()){ return 0; }

        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto vector_cls = module_state->{{ name[0] }}Vector3_PyTypeObject;
        if (Py_TYPE(args[1]) != vector_cls)
        {
            PyErr_Format(PyExc_TypeError, "expected {{ name[0] }}Vector3, got %R", args[0]);
            return 0;
        }
        {{ name[0] }}Vector3 *vector = ({{ name[0] }}Vector3 *)args[1];

        auto matrix = glm::rotate(*self->glm, angle, *vector->glm);

        auto cls = Py_TYPE(self);
        auto *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(matrix);
        return result;
    }

    static {{ name }} *
    {{ name }}_scale({{ name }} *self, PyObject *const *args, Py_ssize_t nargs)
    {
        if (nargs != 1)
        {
            PyErr_Format(PyExc_TypeError, "expected 1 argument, got %zi", nargs);
            return 0;
        }

        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto vector_cls = module_state->{{ name[0] }}Vector3_PyTypeObject;
        if (Py_TYPE(args[0]) != vector_cls)
        {
            PyErr_Format(PyExc_TypeError, "expected {{ name[0] }}Vector3, got %R", args[0]);
            return 0;
        }
        {{ name[0] }}Vector3 *vector = ({{ name[0] }}Vector3 *)args[0];

        auto matrix = glm::scale(*self->glm, *vector->glm);

        auto cls = Py_TYPE(self);
        auto *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(matrix);
        return result;
    }

    static {{ name }} *
    {{ name }}_translate({{ name }} *self, PyObject *const *args, Py_ssize_t nargs)
    {
        if (nargs != 1)
        {
            PyErr_Format(PyExc_TypeError, "expected 1 argument, got %zi", nargs);
            return 0;
        }

        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto vector_cls = module_state->{{ name[0] }}Vector3_PyTypeObject;
        if (Py_TYPE(args[0]) != vector_cls)
        {
            PyErr_Format(PyExc_TypeError, "expected {{ name[0] }}Vector3, got %R", args[0]);
            return 0;
        }
        {{ name[0] }}Vector3 *vector = ({{ name[0] }}Vector3 *)args[0];

        auto matrix = glm::translate(*self->glm, *vector->glm);

        auto cls = Py_TYPE(self);
        auto *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(matrix);
        return result;
    }

    static {{ name }} *
    {{ name }}_perspective(PyTypeObject *cls, PyObject *const *args, Py_ssize_t nargs)
    {
        if (nargs != 4)
        {
            PyErr_Format(PyExc_TypeError, "expected 4 argument, got %zi", nargs);
            return 0;
        }

        double fov = PyFloat_AsDouble(args[0]);
        if (PyErr_Occurred()){ return 0; }
        double aspect = PyFloat_AsDouble(args[1]);
        if (PyErr_Occurred()){ return 0; }
        double near = PyFloat_AsDouble(args[2]);
        if (PyErr_Occurred()){ return 0; }
        double far = PyFloat_AsDouble(args[3]);
        if (PyErr_Occurred()){ return 0; }

        auto *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(glm::perspective(fov, aspect, near, far));
        return result;
    }

    static {{ name }} *
    {{ name }}_orthographic(PyTypeObject *cls, PyObject *const *args, Py_ssize_t nargs)
    {
        if (nargs != 6)
        {
            PyErr_Format(PyExc_TypeError, "expected 6 argument, got %zi", nargs);
            return 0;
        }

        double left = PyFloat_AsDouble(args[0]);
        if (PyErr_Occurred()){ return 0; }
        double right = PyFloat_AsDouble(args[1]);
        if (PyErr_Occurred()){ return 0; }
        double bottom = PyFloat_AsDouble(args[2]);
        if (PyErr_Occurred()){ return 0; }
        double top = PyFloat_AsDouble(args[3]);
        if (PyErr_Occurred()){ return 0; }
        double near = PyFloat_AsDouble(args[4]);
        if (PyErr_Occurred()){ return 0; }
        double far = PyFloat_AsDouble(args[5]);
        if (PyErr_Occurred()){ return 0; }

        auto *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(glm::ortho(left, right, bottom, top, near, far));
        return result;
    }

    static {{ name }} *
    {{ name }}_look_at(PyTypeObject *cls, PyObject *const *args, Py_ssize_t nargs)
    {
        if (nargs != 3)
        {
            PyErr_Format(PyExc_TypeError, "expected 3 argument, got %zi", nargs);
            return 0;
        }

        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto vec3_cls = module_state->{{ name[0] }}Vector3_PyTypeObject;

        if (Py_TYPE(args[0]) != vec3_cls)
        {
            PyErr_Format(PyExc_TypeError, "expected {{ name[0] }}Vector3 for eye, got %R", args[0]);
            return 0;
        }
        auto eye = ({{ name[0] }}Vector3 *)args[0];
        if (Py_TYPE(args[1]) != vec3_cls)
        {
            PyErr_Format(PyExc_TypeError, "expected {{ name[0] }}Vector3 for center, got %R", args[1]);
            return 0;
        }
        auto center = ({{ name[0] }}Vector3 *)args[1];
        if (Py_TYPE(args[2]) != vec3_cls)
        {
            PyErr_Format(PyExc_TypeError, "expected {{ name[0] }}Vector3 for up, got %R", args[2]);
            return 0;
        }
        auto up = ({{ name[0] }}Vector3 *)args[2];

        auto *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(glm::lookAt(*eye->glm, *center->glm, *up->glm));
        return result;
    }

    static {{ name[0] }}Matrix3x3 *
    {{ name }}_to_matrix3({{ name }} *self, void*)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->{{ name[0] }}Matrix3x3_PyTypeObject;

        auto *result = ({{ name[0] }}Matrix3x3 *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name[0] }}Matrix3x3Glm(*self->glm);
        return result;
    }
{% endif %}


{% if (row_size == 4 and column_size == 4) or (row_size == 3 and column_size == 3) %}
    static {{ name[0] }}Quaternion *
    {{ name }}_to_quaternion({{ name }} *self, void*)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->{{ name[0] }}Quaternion_PyTypeObject;

        auto *result = ({{ name[0] }}Quaternion *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name[0] }}QuaternionGlm(glm::quat_cast(*self->glm));
        return result;
    }
{% endif %}


static {{ row_type }} *
{{ name }}_get_row({{ name }} *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (nargs != 1)
    {
        PyErr_Format(PyExc_TypeError, "expected 1 argument, got %zi", nargs);
        return 0;
    }

    auto index = PyLong_AsLong(args[0]);
    if (PyErr_Occurred()){ return 0; }
    if (index < 0 || index > {{ column_size - 1 }})
    {
        PyErr_Format(PyExc_IndexError, "index out of range");
        return 0;
    }

    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto row_cls = module_state->{{ row_type }}_PyTypeObject;

    auto *result = ({{ row_type }} *)row_cls->tp_alloc(row_cls, 0);
    if (!result){ return 0; }
    auto row = glm::row(*self->glm, index);
    result->glm = new {{ row_type }}Glm(row);
    return result;
}


{% with transpose_name=(('D' if c_type == 'double' else 'F') + 'Matrix' + str(column_size) + 'x' + str(row_size)) %}
static {{ transpose_name }} *
{{ name }}_transpose({{ name }} *self, void*)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ transpose_name }}_PyTypeObject;

    {{ transpose_name }}Glm matrix = glm::transpose(*self->glm);
    {{ transpose_name }} *result = ({{ transpose_name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ transpose_name }}Glm(matrix);
    return result;
}
{% endwith %}


static PyObject *
{{ name }}_get_size({{ name }} *cls, void *)
{
    return PyLong_FromSize_t(sizeof({{ c_type }}) * {{ component_count }});
}


static PyObject *
{{ name }}_get_limits({{ name }} *self, void *)
{
    auto c_min = std::numeric_limits<{{ c_type }}>::lowest();
    auto c_max = std::numeric_limits<{{ c_type }}>::max();
    auto py_min = c_{{ c_type.replace(' ', '_') }}_to_pyobject(c_min);
    if (!py_min){ return 0; }
    auto py_max = c_{{ c_type.replace(' ', '_') }}_to_pyobject(c_max);
    if (!py_max)
    {
        Py_DECREF(py_min);
        return 0;
    }
    auto result = PyTuple_New(2);
    if (!result)
    {
        Py_DECREF(py_min);
        Py_DECREF(py_max);
        return 0;
    }
    PyTuple_SET_ITEM(result, 0, py_min);
    PyTuple_SET_ITEM(result, 1, py_max);
    return result;
}


static PyObject *
{{ name }}_from_buffer(PyTypeObject *cls, PyObject *buffer)
{
    static Py_ssize_t expected_size = sizeof({{ c_type }}) * {{ component_count }};
    Py_buffer view;
    if (PyObject_GetBuffer(buffer, &view, PyBUF_SIMPLE) == -1){ return 0; }
    auto view_length = view.len;
    if (view_length < expected_size)
    {
        PyBuffer_Release(&view);
        PyErr_Format(PyExc_BufferError, "expected buffer of size %zd, got %zd", expected_size, view_length);
        return 0;
    }

    auto *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result)
    {
        PyBuffer_Release(&view);
        return 0;
    }
    result->glm = new {{ name }}Glm();
    std::memcpy(result->glm, view.buf, expected_size);
    PyBuffer_Release(&view);
    return (PyObject *)result;
}


{% if c_type != 'float' %}
    static F{{ name[1:] }} *
    {{ name }}_to_fmatrix({{ name }} *self, void*)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->F{{ name[1:] }}_PyTypeObject;

        auto *result = (F{{ name[1:] }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new F{{ name[1:] }}Glm(*self->glm);
        return result;
    }
{% endif %}


{% if c_type != 'double' %}
    static D{{ name[1:] }} *
    {{ name }}_to_dmatrix({{ name }} *self, void*)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->D{{ name[1:] }}_PyTypeObject;

        auto *result = (D{{ name[1:] }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new D{{ name[1:] }}Glm(*self->glm);
        return result;
    }
{% endif %}


static PyObject *
{{ name }}_get_array_type(PyTypeObject *cls, void*)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto array_type = module_state->{{ name }}Array_PyTypeObject;
    Py_INCREF(array_type);
    return (PyObject *)array_type;
}


static PyMethodDef {{ name }}_PyMethodDef[] = {
    {% if row_size == column_size %}
        {"inverse", (PyCFunction){{ name }}_inverse, METH_NOARGS, 0},
    {% endif %}
    {% if row_size == 4 and column_size == 4 %}
        {"rotate", (PyCFunction){{ name }}_rotate, METH_FASTCALL, 0},
        {"scale", (PyCFunction){{ name }}_scale, METH_FASTCALL, 0},
        {"translate", (PyCFunction){{ name }}_translate, METH_FASTCALL, 0},
        {"perspective", (PyCFunction){{ name }}_perspective, METH_CLASS | METH_FASTCALL, 0},
        {"orthographic", (PyCFunction){{ name }}_orthographic, METH_CLASS | METH_FASTCALL, 0},
        {"look_at", (PyCFunction){{ name }}_look_at, METH_CLASS | METH_FASTCALL, 0},
        {"to_matrix3", (PyCFunction){{ name }}_to_matrix3, METH_NOARGS, 0},
    {% endif %}
    {% if (row_size == 4 and column_size == 4) or (row_size == 3 and column_size == 3) %}
        {"to_quaternion", (PyCFunction){{ name }}_to_quaternion, METH_NOARGS, 0},
    {% endif %}
    {% if c_type != 'float' %}
        {"to_fmatrix", (PyCFunction){{ name }}_to_fmatrix, METH_NOARGS, 0},
    {% endif %}
    {% if c_type != 'double' %}
        {"to_dmatrix", (PyCFunction){{ name }}_to_dmatrix, METH_NOARGS, 0},
    {% endif %}
    {"get_row", (PyCFunction){{ name }}_get_row, METH_FASTCALL, 0},
    {"transpose", (PyCFunction){{ name }}_transpose, METH_NOARGS, 0},
    {"get_limits", (PyCFunction){{ name }}_get_limits, METH_NOARGS | METH_STATIC, 0},
    {"get_size", (PyCFunction){{ name }}_get_size, METH_NOARGS | METH_STATIC, 0},
    {"get_array_type", (PyCFunction){{ name }}_get_array_type, METH_NOARGS | METH_STATIC, 0},
    {"from_buffer", (PyCFunction){{ name }}_from_buffer, METH_O | METH_CLASS, 0},
    {0, 0, 0, 0}
};


static PyType_Slot {{ name }}_PyType_Slots [] = {
    {Py_tp_new, (void*){{ name }}__new__},
    {Py_tp_dealloc, (void*){{ name }}__dealloc__},
    {Py_tp_hash, (void*){{ name }}__hash__},
    {Py_tp_repr, (void*){{ name }}__repr__},
    {Py_sq_length, (void*){{ name }}__len__},
    {Py_sq_item, (void*){{ name }}__getitem__},
    {Py_tp_richcompare, (void*){{ name }}__richcmp__},
    {Py_nb_add, (void*){{ name }}__add__},
    {Py_nb_subtract, (void*){{ name }}__sub__},
    {Py_nb_multiply, (void*){{ name }}__mul__},
    {Py_nb_matrix_multiply, (void*){{ name }}__matmul__},
    {Py_nb_true_divide, (void*){{ name }}__truediv__},
    {Py_nb_negative, (void*){{ name }}__neg__},
    {Py_bf_getbuffer, (void*){{ name }}_getbufferproc},
    {Py_tp_getset, (void*){{ name }}_PyGetSetDef},
    {Py_tp_members, (void*){{ name }}_PyMemberDef},
    {Py_tp_methods, (void*){{ name }}_PyMethodDef},
    {0, 0},
};


static PyType_Spec {{ name }}_PyTypeSpec = {
    "emath.{{ name }}",
    sizeof({{ name }}),
    0,
    Py_TPFLAGS_DEFAULT,
    {{ name }}_PyType_Slots
};


static PyTypeObject *
define_{{ name }}_type(PyObject *module)
{
    PyTypeObject *type = (PyTypeObject *)PyType_FromModuleAndSpec(
        module,
        &{{ name }}_PyTypeSpec,
        0
    );
    if (!type){ return 0; }
    // Note:
    // Unlike other functions that steal references, PyModule_AddObject() only
    // decrements the reference count of value on success.
    if (PyModule_AddObject(module, "{{ name }}", (PyObject *)type) < 0)
    {
        Py_DECREF(type);
        return 0;
    }
    return type;
}



static PyObject *
{{ name }}Array__new__(PyTypeObject *cls, PyObject *args, PyObject *kwds)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto element_cls = module_state->{{ name }}_PyTypeObject;

    if (kwds && PyDict_Size(kwds) != 0)
    {
        PyErr_SetString(
            PyExc_TypeError,
            "{{ name }} does accept any keyword arguments"
        );
        return 0;
    }

    auto arg_count = PyTuple_GET_SIZE(args);
    if (arg_count == 0)
    {
        auto self = ({{ name }}Array *)cls->tp_alloc(cls, 0);
        if (!self){ return 0; }
        self->length = 0;
        self->glm = 0;
        return (PyObject *)self;
    }

    auto *self = ({{ name }}Array *)cls->tp_alloc(cls, 0);
    if (!self){ return 0; }
    self->length = arg_count;
    self->glm = new {{ name }}Glm[arg_count];

    for (int i = 0; i < arg_count; i++)
    {
        auto arg = PyTuple_GET_ITEM(args, i);
        if (Py_TYPE(arg) == element_cls)
        {
            self->glm[i] = *((({{ name }}*)arg)->glm);
        }
        else
        {
            Py_DECREF(self);
            PyErr_Format(
                PyExc_TypeError,
                "invalid type %R, expected %R",
                arg,
                element_cls
            );
            return 0;
        }
    }

    return (PyObject *)self;
}


static void
{{ name }}Array__dealloc__({{ name }}Array *self)
{
    if (self->weakreflist)
    {
        PyObject_ClearWeakRefs((PyObject *)self);
    }

    delete self->glm;

    PyTypeObject *type = Py_TYPE(self);
    type->tp_free(self);
    Py_DECREF(type);
}


static Py_hash_t
{{ name }}Array__hash__({{ name }}Array *self)
{
    Py_ssize_t len = self->length * {{ component_count }};
    Py_uhash_t acc = _HASH_XXPRIME_5;
    for (Py_ssize_t i = 0; i < (Py_ssize_t)self->length; i++)
    {
        for ({{ name }}Glm::length_type c = 0; c < {{ column_size }}; c++)
        {
            for ({{ name }}Glm::length_type r = 0; r < {{ row_size }}; r++)
            {
                Py_uhash_t lane = std::hash<{{ c_type }}>{}(self->glm[i][r][c]);
                acc += lane * _HASH_XXPRIME_2;
                acc = _HASH_XXROTATE(acc);
                acc *= _HASH_XXPRIME_1;
            }
            acc += len ^ (_HASH_XXPRIME_5 ^ 3527539UL);
        }
    }

    if (acc == (Py_uhash_t)-1) {
        return 1546275796;
    }
    return acc;
}


static PyObject *
{{ name }}Array__repr__({{ name }}Array *self)
{
    return PyUnicode_FromFormat("{{ name }}Array[%zu]", self->length);
}


static Py_ssize_t
{{ name }}Array__len__({{ name }}Array *self)
{
    return self->length;
}


static PyObject *
{{ name }}Array__sq_getitem__({{ name }}Array *self, Py_ssize_t index)
{
    if (index < 0 || index > (Py_ssize_t)self->length - 1)
    {
        PyErr_Format(PyExc_IndexError, "index out of range");
        return 0;
    }

    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto element_cls = module_state->{{ name }}_PyTypeObject;

    {{ name }} *result = ({{ name }} *)element_cls->tp_alloc(element_cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(self->glm[index]);

    return (PyObject *)result;
}


static PyObject *
{{ name }}Array__mp_getitem__({{ name }}Array *self, PyObject *key)
{
    if (PySlice_Check(key))
    {
        Py_ssize_t start;
        Py_ssize_t stop;
        Py_ssize_t step;
        Py_ssize_t length;
        if (PySlice_GetIndicesEx(key, self->length, &start, &stop, &step, &length) != 0)
        {
            return 0;
        }
        auto cls = Py_TYPE(self);
        auto *result = ({{ name }}Array *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        if (length == 0)
        {
            result->length = 0;
            result->glm = 0;
        }
        else
        {
            result->length = length;
            result->glm = new {{ name }}Glm[length];
            for ({{ name }}Glm::length_type i = 0; i < length; i++)
            {
                result->glm[i] = self->glm[start + (i * step)];
            }
        }
        return (PyObject *)result;
    }
    else if (PyLong_Check(key))
    {
        auto index = PyLong_AsSsize_t(key);
        if (PyErr_Occurred()){ return 0; }
        if (index < 0)
        {
            index = (Py_ssize_t)self->length + index;
        }
        if (index < 0 || index > (Py_ssize_t)self->length - 1)
        {
            PyErr_Format(PyExc_IndexError, "index out of range");
            return 0;
        }
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto element_cls = module_state->{{ name }}_PyTypeObject;

        {{ name }} *result = ({{ name }} *)element_cls->tp_alloc(element_cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(self->glm[index]);

        return (PyObject *)result;
    }
    PyErr_Format(PyExc_TypeError, "expected int or slice");
    return 0;
}


static PyObject *
{{ name}}Array__richcmp__(
    {{ name }}Array *self,
    {{ name }}Array *other,
    int op
)
{
    if (Py_TYPE(self) != Py_TYPE(other))
    {
        Py_RETURN_NOTIMPLEMENTED;
    }

    switch(op)
    {
        case Py_EQ:
        {
            if (self->length == other->length)
            {
                for (size_t i = 0; i < self->length; i++)
                {
                    if (self->glm[i] != other->glm[i])
                    {
                        Py_RETURN_FALSE;
                    }
                }
                Py_RETURN_TRUE;
            }
            else
            {
                Py_RETURN_FALSE;
            }
        }
        case Py_NE:
        {
            if (self->length != other->length)
            {
                Py_RETURN_TRUE;
            }
            else
            {
                for (size_t i = 0; i < self->length; i++)
                {
                    if (self->glm[i] != other->glm[i])
                    {
                        Py_RETURN_TRUE;
                    }
                }
                Py_RETURN_FALSE;
            }
        }
    }
    Py_RETURN_NOTIMPLEMENTED;
}


static int
{{ name}}Array__bool__({{ name }}Array *self)
{
    return self->length ? 1 : 0;
}


static int
{{ name}}Array_getbufferproc({{ name }}Array *self, Py_buffer *view, int flags)
{
    if (flags & PyBUF_WRITABLE)
    {
        PyErr_SetString(PyExc_TypeError, "{{ name }} is read only");
        view->obj = 0;
        return -1;
    }
    if ((!(flags & PyBUF_C_CONTIGUOUS)) && flags & PyBUF_F_CONTIGUOUS)
    {
        PyErr_SetString(PyExc_BufferError, "{{ name }} cannot be made Fortran contiguous");
        view->obj = 0;
        return -1;
    }
    view->buf = self->glm;
    view->obj = (PyObject *)self;
    view->len = sizeof({{ c_type }}) * {{ component_count }} * self->length;
    view->readonly = 1;
    view->itemsize = sizeof({{ c_type }});
    view->ndim = 3;
    if (flags & PyBUF_FORMAT)
    {
        view->format = "{{ struct_format }}";
    }
    else
    {
        view->format = 0;
    }
    if (flags & PyBUF_ND)
    {
        view->shape = new Py_ssize_t[3] {
            (Py_ssize_t)self->length,
            {{ row_size }},
            {{ column_size }}
        };
    }
    else
    {
        view->shape = 0;
    }
    if (flags & PyBUF_STRIDES)
    {
        static Py_ssize_t strides[] = {
            sizeof({{ c_type }}) * {{ component_count }},
            sizeof({{ c_type }}) * {{ column_size }},
            sizeof({{ c_type }})
        };
        view->strides = &strides[0];
    }
    else
    {
        view->strides = 0;
    }
    view->suboffsets = 0;
    view->internal = 0;
    Py_INCREF(self);
    return 0;
}


static void
{{ name}}Array_releasebufferproc({{ name }}Array *self, Py_buffer *view)
{
    delete view->shape;
}


static PyMemberDef {{ name }}Array_PyMemberDef[] = {
    {"__weaklistoffset__", T_PYSSIZET, offsetof({{ name }}Array, weakreflist), READONLY},
    {0}
};


static PyObject *
{{ name }}Array_pointer({{ name }}Array *self, void *)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto c_p = module_state->ctypes_c_{{ c_type.replace(' ', '_') }}_p;
    return PyObject_CallMethod(c_p, "from_address", "n", (Py_ssize_t)&self->glm);
}


static PyObject *
{{ name }}Array_size({{ name }}Array *self, void *)
{
    return PyLong_FromSize_t(sizeof({{ c_type }}) * {{ component_count }} * self->length);
}


static PyGetSetDef {{ name }}Array_PyGetSetDef[] = {
    {"pointer", (getter){{ name }}Array_pointer, 0, 0, 0},
    {"size", (getter){{ name }}Array_size, 0, 0, 0},
    {0, 0, 0, 0, 0}
};


static PyObject *
{{ name }}Array_from_buffer(PyTypeObject *cls, PyObject *buffer)
{
    static Py_ssize_t expected_size = sizeof({{ c_type }});
    Py_buffer view;
    if (PyObject_GetBuffer(buffer, &view, PyBUF_SIMPLE) == -1){ return 0; }
    auto view_length = view.len;
    if (view_length % (sizeof({{ c_type }}) * {{ component_count }}))
    {
        PyBuffer_Release(&view);
        PyErr_Format(PyExc_BufferError, "expected buffer evenly divisible by %zd, got %zd", sizeof({{ c_type }}), view_length);
        return 0;
    }
    auto array_length = view_length / (sizeof({{ c_type }}) * {{ component_count }});

    auto *result = ({{ name }}Array *)cls->tp_alloc(cls, 0);
    if (!result)
    {
        PyBuffer_Release(&view);
        return 0;
    }
    result->length = array_length;
    if (array_length > 0)
    {
        result->glm = new {{ name }}Glm[array_length];
        std::memcpy(result->glm, view.buf, view_length);
    }
    else
    {
        result->glm = 0;
    }
    PyBuffer_Release(&view);
    return (PyObject *)result;
}


static PyObject *
{{ name }}Array_get_component_type(PyTypeObject *cls, PyObject *const *args, Py_ssize_t nargs)
{
    if (nargs != 0)
    {
        PyErr_Format(PyExc_TypeError, "expected 0 arguments, got %zi", nargs);
        return 0;
    }
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto component_type = module_state->{{ name }}_PyTypeObject;
    Py_INCREF(component_type);
    return (PyObject *)component_type;
}


static PyMethodDef {{ name }}Array_PyMethodDef[] = {
    {"from_buffer", (PyCFunction){{ name }}Array_from_buffer, METH_O | METH_CLASS, 0},
    {"get_component_type", (PyCFunction){{ name }}Array_get_component_type, METH_FASTCALL | METH_CLASS, 0},
    {0, 0, 0, 0}
};


static PyType_Slot {{ name }}Array_PyType_Slots [] = {
    {Py_tp_new, (void*){{ name }}Array__new__},
    {Py_tp_dealloc, (void*){{ name }}Array__dealloc__},
    {Py_tp_hash, (void*){{ name }}Array__hash__},
    {Py_tp_repr, (void*){{ name }}Array__repr__},
    {Py_sq_length, (void*){{ name }}Array__len__},
    {Py_sq_item, (void*){{ name }}Array__sq_getitem__},
    {Py_mp_subscript, (void*){{ name }}Array__mp_getitem__},
    {Py_tp_richcompare, (void*){{ name }}Array__richcmp__},
    {Py_nb_bool, (void*){{ name }}Array__bool__},
    {Py_bf_getbuffer, (void*){{ name }}Array_getbufferproc},
    {Py_bf_releasebuffer, (void*){{ name }}Array_releasebufferproc},
    {Py_tp_getset, (void*){{ name }}Array_PyGetSetDef},
    {Py_tp_members, (void*){{ name }}Array_PyMemberDef},
    {Py_tp_methods, (void*){{ name }}Array_PyMethodDef},
    {0, 0},
};


static PyType_Spec {{ name }}Array_PyTypeSpec = {
    "emath.{{ name }}Array",
    sizeof({{ name }}Array),
    0,
    Py_TPFLAGS_DEFAULT,
    {{ name }}Array_PyType_Slots
};


static PyTypeObject *
define_{{ name }}Array_type(PyObject *module)
{
    PyTypeObject *type = (PyTypeObject *)PyType_FromModuleAndSpec(
        module,
        &{{ name }}Array_PyTypeSpec,
        0
    );
    if (!type){ return 0; }
    // Note:
    // Unlike other functions that steal references, PyModule_AddObject() only
    // decrements the reference count of value on success.
    if (PyModule_AddObject(module, "{{ name }}Array", (PyObject *)type) < 0)
    {
        Py_DECREF(type);
        return 0;
    }
    return type;
}


static PyTypeObject *
get_{{ name }}_type()
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    return module_state->{{ name }}_PyTypeObject;
}


static PyTypeObject *
get_{{ name }}Array_type()
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    return module_state->{{ name }}Array_PyTypeObject;
}


static PyObject *
create_{{ name }}(const {{ c_type }} *value)
{

    auto cls = get_{{ name }}_type();
    auto result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(*({{ name }}Glm *)value);
    return (PyObject *)result;
}


static PyObject *
create_{{ name }}Array(size_t length, const {{ c_type }} *value)
{
    auto cls = get_{{ name }}Array_type();
    auto result = ({{ name }}Array *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->length = length;
    if (length > 0)
    {
        result->glm = new {{ name }}Glm[length];
        for (size_t i = 0; i < length; i++)
        {
            result->glm[i] = (({{ name }}Glm *)value)[i];
        }
    }
    else
    {
        result->glm = 0;
    }
    return (PyObject *)result;
}


static {{ c_type }} *
get_{{ name }}_value_ptr(const PyObject *self)
{
    if (Py_TYPE(self) != get_{{ name }}_type())
    {
        PyErr_Format(PyExc_TypeError, "expected {{ name }}, got %R", self);
        return 0;
    }
    return ({{ c_type }} *)(({{ name }} *)self)->glm;
}


static {{ c_type }} *
get_{{ name }}Array_value_ptr(const PyObject *self)
{
    if (Py_TYPE(self) != get_{{ name }}Array_type())
    {
        PyErr_Format(
            PyExc_TypeError,
            "expected {{ name }}Array, got %R",
            self
        );
        return 0;
    }
    return ({{ c_type }} *)(({{ name }}Array *)self)->glm;
}


static size_t
get_{{ name }}Array_length(const PyObject *self)
{
    if (Py_TYPE(self) != get_{{ name }}Array_type())
    {
        PyErr_Format(
            PyExc_TypeError,
            "expected {{ name }}Array, got %R",
            self
        );
        return 0;
    }
    return (({{ name }}Array *)self)->length;
}

#endif
