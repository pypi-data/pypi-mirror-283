
// generated from codegen/templates/_vector.hpp

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
#include <glm/gtx/compatibility.hpp>
#include <glm/ext.hpp>
// emath
#include "_modulestate.hpp"
#include "_quaterniontype.hpp"
#include "_vectortype.hpp"
#include "_type.hpp"


static PyObject *
{{ name }}__new__(PyTypeObject *cls, PyObject *args, PyObject *kwds)
{
    {% for i in range(component_count) %}
        {{ c_type }} c_{{ i }} = 0;
    {% endfor %}

    if (kwds && PyDict_Size(kwds) != 0)
    {
        PyErr_SetString(
            PyExc_TypeError,
            "{{ name }} does accept any keyword arguments"
        );
        return 0;
    }
    auto arg_count = PyTuple_GET_SIZE(args);
    switch (PyTuple_GET_SIZE(args))
    {
        case 0:
        {
            break;
        }
        case 1:
        {
            auto arg = PyTuple_GET_ITEM(args, 0);
            {{ c_type }} arg_c = pyobject_to_c_{{ c_type.replace(' ', '_') }}(arg);
            auto error_occurred = PyErr_Occurred();
            if (error_occurred){ return 0; }
            {% for i in range(component_count) %}
                c_{{ i }} = arg_c;
            {% endfor %}
            break;
        }
        {% if component_count != 1 %}
            case {{ component_count }}:
            {
                {% for i in range(component_count) %}
                {
                    auto arg = PyTuple_GET_ITEM(args, {{ i }});
                    c_{{ i }} = pyobject_to_c_{{ c_type.replace(' ', '_') }}(arg);
                    auto error_occurred = PyErr_Occurred();
                    if (error_occurred){ return 0; }
                }
                {% endfor %}
                break;
            }
        {% endif %}
        default:
        {
            PyErr_Format(
                PyExc_TypeError,
                "invalid number of arguments supplied to {{ name }}, expected "
                "0, 1 or {{ component_count }} (got %zd)",
                arg_count
            );
            return 0;
        }
    }

    {{ name }} *self = ({{ name }}*)cls->tp_alloc(cls, 0);
    if (!self){ return 0; }
    self->glm = new {{ name }}Glm(
        {% for i in range(component_count) %}
            c_{{ i }}{% if i != component_count - 1 %}, {% endif %}
        {% endfor %}
    );

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
    for ({{ name }}Glm::length_type i = 0; i < len; i++)
    {
        Py_uhash_t lane = std::hash<{{ c_type }}>{}((*self->glm)[i]);
        acc += lane * _HASH_XXPRIME_2;
        acc = _HASH_XXROTATE(acc);
        acc *= _HASH_XXPRIME_1;
    }
    acc += len ^ (_HASH_XXPRIME_5 ^ 3527539UL);

    if (acc == (Py_uhash_t)-1) {
        return 1546275796;
    }
    return acc;
}


static PyObject *
{{ name }}__repr__({{ name }} *self)
{
    PyObject *result = 0;
    {% for i in range(component_count) %}
        PyObject *py_{{ i }} = 0;
    {% endfor %}

    {% for i in range(component_count) %}
        py_{{ i }} = c_{{ c_type.replace(' ', '_') }}_to_pyobject((*self->glm)[{{ i }}]);
        if (!py_{{ i }}){ goto cleanup; }
    {% endfor %}
    result = PyUnicode_FromFormat(
        "{{ name }}("
        {% for i in range(component_count) %}
            "%R{% if i < component_count - 1 %}, {% endif %}"
        {% endfor %}
        ")",
        {% for i in range(component_count) %}
            py_{{ i }}{% if i < component_count - 1 %}, {% endif %}
        {% endfor %}
    );
cleanup:
    {% for i in range(component_count) %}
        Py_XDECREF(py_{{ i }});
    {% endfor %}
    return result;
}


static Py_ssize_t
{{ name }}__len__({{ name }} *self)
{
    return {{ component_count }};
}


static PyObject *
{{ name }}__getitem__({{ name }} *self, Py_ssize_t index)
{
    if (index < 0 || index > {{ component_count - 1 }})
    {
        PyErr_Format(PyExc_IndexError, "index out of range");
        return 0;
    }
    auto c = (*self->glm)[({{ name }}Glm::length_type)index];
    return c_{{ c_type.replace(' ', '_') }}_to_pyobject(c);
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
        case Py_LT:
        {
            for ({{ name }}Glm::length_type i = 0; i < {{ component_count }}; i++)
            {
                if ((*self->glm)[i] < (*other->glm)[i])
                {
                    Py_RETURN_TRUE;
                }
                if ((*self->glm)[i] != (*other->glm)[i])
                {
                    Py_RETURN_FALSE;
                }
            }
            Py_RETURN_FALSE;
        }
        case Py_LE:
        {
            for ({{ name }}Glm::length_type i = 0; i < {{ component_count }}; i++)
            {
                if ((*self->glm)[i] < (*other->glm)[i])
                {
                    Py_RETURN_TRUE;
                }
                if ((*self->glm)[i] != (*other->glm)[i])
                {
                    Py_RETURN_FALSE;
                }
            }
            Py_RETURN_TRUE;
        }
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
        case Py_GE:
        {
            for ({{ name }}Glm::length_type i = 0; i < {{ component_count }}; i++)
            {
                if ((*self->glm)[i] > (*other->glm)[i])
                {
                    Py_RETURN_TRUE;
                }
                if ((*self->glm)[i] != (*other->glm)[i])
                {
                    Py_RETURN_FALSE;
                }
            }
            Py_RETURN_TRUE;
        }
        case Py_GT:
        {
            for ({{ name }}Glm::length_type i = 0; i < {{ component_count }}; i++)
            {
                if ((*self->glm)[i] > (*other->glm)[i])
                {
                    Py_RETURN_TRUE;
                }
                if ((*self->glm)[i] != (*other->glm)[i])
                {
                    Py_RETURN_FALSE;
                }
            }
            Py_RETURN_FALSE;
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

    {{ name }}Glm vector;
    if (Py_TYPE(left) == Py_TYPE(right))
    {
        vector = (*(({{name }} *)left)->glm) + (*(({{name }} *)right)->glm);
    }
    else
    {
        if (Py_TYPE(left) == cls)
        {
            auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            vector = (*(({{name }} *)left)->glm) + c_right;
        }
        else
        {
            auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            vector = c_left + (*(({{name }} *)right)->glm);
        }
    }

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(
        {% for i in range(component_count) %}
            vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
        {% endfor %}
    );

    return (PyObject *)result;
}


static PyObject *
{{ name}}__sub__(PyObject *left, PyObject *right)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ name }}_PyTypeObject;

    {{ name }}Glm vector;
    if (Py_TYPE(left) == Py_TYPE(right))
    {
        vector = (*(({{name }} *)left)->glm) - (*(({{name }} *)right)->glm);
    }
    else
    {
        if (Py_TYPE(left) == cls)
        {
            auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            vector = (*(({{name }} *)left)->glm) - c_right;
        }
        else
        {
            auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            vector = c_left - (*(({{name }} *)right)->glm);
        }
    }

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(
        {% for i in range(component_count) %}
            vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
        {% endfor %}
    );

    return (PyObject *)result;
}


static PyObject *
{{ name}}__mul__(PyObject *left, PyObject *right)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto cls = module_state->{{ name }}_PyTypeObject;

    {{ name }}Glm vector;
    if (Py_TYPE(left) == Py_TYPE(right))
    {
        vector = (*(({{name }} *)left)->glm) * (*(({{name }} *)right)->glm);
    }
    else
    {
        if (Py_TYPE(left) == cls)
        {
            auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            vector = (*(({{name }} *)left)->glm) * c_right;
        }
        else
        {
            auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
            if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
            vector = c_left * (*(({{name }} *)right)->glm);
        }
    }

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(
        {% for i in range(component_count) %}
            vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
        {% endfor %}
    );

    return (PyObject *)result;
}


{% if c_type in ['float', 'double'] %}
    static PyObject *
    {{ name }}__matmul__({{ name }} *left, {{ name }} *right)
    {
        auto cls = Py_TYPE(left);
        if (Py_TYPE(left) != Py_TYPE(right)){ Py_RETURN_NOTIMPLEMENTED; }
        auto c_result = glm::dot(*left->glm, *right->glm);
        return c_{{ c_type.replace(' ', '_') }}_to_pyobject(c_result);
    }


    static PyObject *
    {{ name}}__mod__(PyObject *left, PyObject *right)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->{{ name }}_PyTypeObject;

        {{ name }}Glm vector;
        if (Py_TYPE(left) == Py_TYPE(right))
        {
            vector = glm::mod(
                *(({{name }} *)left)->glm,
                *(({{name }} *)right)->glm
            );
        }
        else
        {
            if (Py_TYPE(left) == cls)
            {
                auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
                if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
                vector = glm::mod(*(({{name }} *)left)->glm, c_right);
            }
            else
            {
                auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
                if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
                vector = glm::mod({{ name }}Glm(c_left), *(({{name }} *)right)->glm);
            }
        }

        {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(
            {% for i in range(component_count) %}
                vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
            {% endfor %}
        );

        return (PyObject *)result;
    }


    static PyObject *
    {{ name}}__pow__(PyObject *left, PyObject *right)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->{{ name }}_PyTypeObject;

        {{ name }}Glm vector;
        if (Py_TYPE(left) == Py_TYPE(right))
        {
            vector = glm::pow(
                *(({{name }} *)left)->glm,
                *(({{name }} *)right)->glm
            );
        }
        else
        {
            if (Py_TYPE(left) == cls)
            {
                auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
                if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
                vector = glm::pow(*(({{name }} *)left)->glm, {{ name }}Glm(c_right));
            }
            else
            {
                auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
                if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
                vector = glm::pow({{ name }}Glm(c_left), *(({{name }} *)right)->glm);
            }
        }

        {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(
            {% for i in range(component_count) %}
                vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
            {% endfor %}
        );

        return (PyObject *)result;
    }
{% endif %}


{% if c_type != 'bool' %}

    static PyObject *
    {{ name}}__truediv__(PyObject *left, PyObject *right)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->{{ name }}_PyTypeObject;

        {{ name }}Glm vector;
        if (Py_TYPE(left) == Py_TYPE(right))
        {
            {% if c_type not in ['float', 'double'] %}
                if (
                    {% for i in range(component_count) %}
                        (*(({{name }} *)right)->glm)[{{ i }}] == 0{% if i < component_count - 1 %} || {% endif %}
                    {% endfor %}
                )
                {
                    PyErr_SetString(PyExc_ZeroDivisionError, "divide by zero");
                    return 0;
                }
            {% endif %}
            vector = (*(({{name }} *)left)->glm) / (*(({{name }} *)right)->glm);
        }
        else
        {
            if (Py_TYPE(left) == cls)
            {
                auto c_right = pyobject_to_c_{{ c_type.replace(' ', '_') }}(right);
                if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
                {% if c_type not in ['float', 'double'] %}
                    if (c_right == 0)
                    {
                        PyErr_SetString(PyExc_ZeroDivisionError, "divide by zero");
                        return 0;
                    }
                {% endif %}
                vector = (*(({{name }} *)left)->glm) / c_right;
            }
            else
            {
                auto c_left = pyobject_to_c_{{ c_type.replace(' ', '_') }}(left);
                if (PyErr_Occurred()){ PyErr_Clear(); Py_RETURN_NOTIMPLEMENTED; }
                {% if c_type not in ['float', 'double'] %}
                    if (
                        {% for i in range(component_count) %}
                            (*(({{name }} *)right)->glm)[{{ i }}] == 0{% if i < component_count - 1 %} || {% endif %}
                        {% endfor %}
                    )
                    {
                        PyErr_SetString(PyExc_ZeroDivisionError, "divide by zero");
                        return 0;
                    }
                {% endif %}
                vector = c_left / (*(({{name }} *)right)->glm);
            }
        }

        {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(
            {% for i in range(component_count) %}
                vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
            {% endfor %}
        );

        return (PyObject *)result;
    }
{% endif %}


{% if 'unsigned' not in c_type and not (c_type.startswith('u') and c_type.endswith('_t')) %}
    static PyObject *
    {{ name}}__neg__({{ name }} *self)
    {
        auto cls = Py_TYPE(self);
        {% if c_type == 'bool' %}
            {{ name }}Glm vector = (*self->glm);
        {% else %}
            {{ name }}Glm vector = -(*self->glm);
        {% endif %}

        {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(
            {% for i in range(component_count) %}
                vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
            {% endfor %}
        );

        return (PyObject *)result;
    }
{% endif %}


static PyObject *
{{ name}}__abs__({{ name }} *self)
{
    auto cls = Py_TYPE(self);
    {{ name }}Glm vector = glm::abs(*self->glm);

    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(
        {% for i in range(component_count) %}
            vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
        {% endfor %}
    );

    return (PyObject *)result;
}


static int
{{ name}}__bool__({{ name }} *self)
{
    {% for i in range(component_count) %}
        if ((*self->glm)[{{ i }}] == 0)
        {
            return 0;
        }
    {% endfor %}
    return 1;
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
    view->buf = self->glm;
    view->obj = (PyObject *)self;
    view->len = sizeof({{ c_type }}) * {{ component_count }};
    view->readonly = 1;
    view->itemsize = sizeof({{ c_type }});
    view->ndim = 1;
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
        static Py_ssize_t shape = {{ component_count }};
        view->shape = &shape;
    }
    else
    {
        view->shape = 0;
    }
    if (flags & PyBUF_STRIDES)
    {
        view->strides = &view->itemsize;
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


{% for i in range(component_count) %}
    static PyObject *
    {{ name }}_Getter_{{ i }}({{ name }} *self, void *)
    {
        auto c = (*self->glm)[{{ i }}];
        return c_{{ c_type.replace(' ', '_') }}_to_pyobject(c);
    }
{% endfor %}


{% if c_type in ['float', 'double'] %}
    static PyObject *
    {{ name }}_magnitude({{ name }} *self, void *)
    {
        auto magnitude = glm::length(*self->glm);
        return c_{{ c_type.replace(' ', '_') }}_to_pyobject(magnitude);
    }
{% endif %}


static PyObject *
{{ name }}_pointer({{ name }} *self, void *)
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    auto c_p = module_state->ctypes_c_{{ c_type.replace(' ', '_') }}_p;
    return PyObject_CallMethod(c_p, "from_address", "n", (Py_ssize_t)&self->glm);
}


static PyGetSetDef {{ name }}_PyGetSetDef[] = {
    {"x", (getter){{ name }}_Getter_0, 0, 0, 0},
    {"r", (getter){{ name }}_Getter_0, 0, 0, 0},
    {"s", (getter){{ name }}_Getter_0, 0, 0, 0},
    {"u", (getter){{ name }}_Getter_0, 0, 0, 0},
    {% if component_count > 1 %}
        {"y", (getter){{ name }}_Getter_1, 0, 0, 0},
        {"g", (getter){{ name }}_Getter_1, 0, 0, 0},
        {"t", (getter){{ name }}_Getter_1, 0, 0, 0},
        {"v", (getter){{ name }}_Getter_1, 0, 0, 0},
    {% endif %}
    {% if component_count > 2 %}
        {"z", (getter){{ name }}_Getter_2, 0, 0, 0},
        {"b", (getter){{ name }}_Getter_2, 0, 0, 0},
        {"p", (getter){{ name }}_Getter_2, 0, 0, 0},
    {% endif %}
    {% if component_count > 3 %}
        {"w", (getter){{ name }}_Getter_3, 0, 0, 0},
        {"a", (getter){{ name }}_Getter_3, 0, 0, 0},
        {"q", (getter){{ name }}_Getter_3, 0, 0, 0},
    {% endif %}
    {% if c_type in ['float', 'double'] %}
        {"magnitude", (getter){{ name }}_magnitude, 0, 0, 0},
    {% endif %}
    {"pointer", (getter){{ name }}_pointer, 0, 0, 0},
    {0, 0, 0, 0, 0}
};

{% for swizzle_count in range(2, 5) %}
{% with result_type=name[:name.index('V')] + 'Vector' + str(swizzle_count) %}
    static PyObject *
    swizzle_{{ swizzle_count }}_{{ name }}({{name}} *self, PyObject *py_attr)
    {
        const char *attr = PyUnicode_AsUTF8(py_attr);
        if (!attr){ return 0; }

        {{ result_type }}Glm vec;
        for (int i = 0; i < {{ swizzle_count }}; i++)
        {
            char c_name = attr[i];
            int glm_index;
            switch(c_name)
            {
                case 'o':
                    vec[i] = 0;
                    continue;
                case 'l':
                    vec[i] = 1;
                    continue;
                case 'x':
                case 'r':
                case 's':
                case 'u':
                    glm_index = 0;
                    break;
                {% if component_count > 1 %}
                    case 'y':
                    case 'g':
                    case 't':
                    case 'v':
                        glm_index = 1;
                        break;
                {% endif %}
                {% if component_count > 2 %}
                    case 'z':
                    case 'b':
                    case 'p':
                        glm_index = 2;
                        break;
                {% endif %}
                {% if component_count > 3 %}
                    case 'w':
                    case 'a':
                    case 'q':
                        glm_index = 3;
                        break;
                {% endif %}
                default:
                {
                    PyErr_Format(
                        PyExc_AttributeError,
                        "invalid swizzle: %R", py_attr
                    );
                    return 0;
                }
            }
            vec[i] = (*self->glm)[glm_index];
        }

        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->{{ result_type }}_PyTypeObject;

        {{ result_type }} *result = ({{ result_type }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ result_type }}Glm(vec);

        return (PyObject *)result;
    }
{% endwith %}
{% endfor %}


static PyObject *
{{ name }}__getattr__({{name}} *self, PyObject *py_attr)
{
    PyObject *result = PyObject_GenericGetAttr((PyObject *)self, py_attr);
    if (result != 0){ return result; }

    auto attr_length = PyUnicode_GET_LENGTH(py_attr);
    switch(attr_length)
    {
        case 2:
        {
            PyErr_Clear();
            return swizzle_2_{{ name }}(self, py_attr);
        }
        case 3:
        {
            PyErr_Clear();
            return swizzle_3_{{ name }}(self, py_attr);
        }
        case 4:
        {
            PyErr_Clear();
            return swizzle_4_{{ name }}(self, py_attr);
        }
    }
    return 0;
}


static PyMemberDef {{ name }}_PyMemberDef[] = {
    {"__weaklistoffset__", T_PYSSIZET, offsetof({{ name }}, weakreflist), READONLY},
    {0}
};


{% if c_type in ['float', 'double'] %}
    {% if component_count == 3 %}
        static {{ name }} *
        {{ name }}_cross({{ name }} *self, {{ name }} *other)
        {
            auto cls = Py_TYPE(self);
            if (Py_TYPE(other) != cls)
            {
                PyErr_Format(PyExc_TypeError, "%R is not {{ name }}", other);
                return 0;
            }
            auto vector = glm::cross(*self->glm, *other->glm);
            {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
            if (!result){ return 0; }
            result->glm = new {{ name }}Glm(
                {% for i in range(component_count) %}
                    vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
                {% endfor %}
            );
            return result;
        }

        static {{ name[0] }}Quaternion *
        {{ name }}_to_quaternion({{ name }} *self, void*)
        {
            auto module_state = get_module_state();
            if (!module_state){ return 0; }
            auto cls = module_state->{{ name[0] }}Quaternion_PyTypeObject;

            auto result = ({{ name[0] }}Quaternion *)cls->tp_alloc(cls, 0);
            if (!result){ return 0; }
            result->glm = new {{ name[0] }}QuaternionGlm(*self->glm);
            return result;
        }
    {% endif %}


    static PyObject *
    {{ name }}_lerp({{ name }} *self, PyObject *const *args, Py_ssize_t nargs)
    {
        if (nargs != 2)
        {
            PyErr_Format(PyExc_TypeError, "expected 2 arguments, got %zi", nargs);
            return 0;
        }

        auto cls = Py_TYPE(self);
        if (Py_TYPE(args[0]) != cls)
        {
            PyErr_Format(PyExc_TypeError, "%R is not {{ name }}", args[0]);
            return 0;
        }
        auto other = ({{ name }} *)args[0];

        auto c_x = pyobject_to_c_{{ c_type.replace(' ', '_') }}(args[1]);
        if (PyErr_Occurred()){ return 0; }

        {% if component_count == 1 %}
            auto vector = glm::lerp<{{ c_type }}>(*({{ c_type }} *)self->glm, *({{ c_type }} *)other->glm, c_x);
        {% else %}
            auto vector = glm::lerp(*self->glm, *other->glm, c_x);
        {% endif %}
        auto result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(vector);
        return (PyObject *)result;
    }


    static {{ name }} *
    {{ name }}_normalize({{ name }} *self, void*)
    {
        auto cls = Py_TYPE(self);
        auto vector = glm::normalize(*self->glm);
        {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(
            {% for i in range(component_count) %}
                vector[{{ i }}]{% if i < component_count - 1 %}, {% endif %}
            {% endfor %}
        );
        return result;
    }

    static PyObject *
    {{ name }}_distance({{ name }} *self, {{ name }} *other)
    {
        auto cls = Py_TYPE(self);
        if (Py_TYPE(other) != cls)
        {
            PyErr_Format(PyExc_TypeError, "%R is not {{ name }}", other);
            return 0;
        }
        auto result = glm::distance(*self->glm, *other->glm);
        return c_{{ c_type.replace(' ', '_') }}_to_pyobject(result);
    }

{% endif %}


static PyObject *
{{ name }}_min({{ name }} *self, PyObject *min)
{
    auto c_min = pyobject_to_c_{{ c_type.replace(' ', '_') }}(min);
    if (PyErr_Occurred()){ return 0; }
    auto cls = Py_TYPE(self);
    auto vector = glm::min(*self->glm, c_min);
    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(vector);
    return (PyObject *)result;
}


static PyObject *
{{ name }}_max({{ name }} *self, PyObject *max)
{
    auto c_max = pyobject_to_c_{{ c_type.replace(' ', '_') }}(max);
    if (PyErr_Occurred()){ return 0; }
    auto cls = Py_TYPE(self);
    auto vector = glm::max(*self->glm, c_max);
    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(vector);
    return (PyObject *)result;
}


static PyObject *
{{ name }}_clamp({{ name }} *self, PyObject *const *args, Py_ssize_t nargs)
{
    if (nargs != 2)
    {
        PyErr_Format(PyExc_TypeError, "expected 2 arguments, got %zi", nargs);
        return 0;
    }
    auto c_min = pyobject_to_c_{{ c_type.replace(' ', '_') }}(args[0]);
    if (PyErr_Occurred()){ return 0; }
    auto c_max = pyobject_to_c_{{ c_type.replace(' ', '_') }}(args[1]);
    if (PyErr_Occurred()){ return 0; }

    auto cls = Py_TYPE(self);
    auto vector = glm::clamp(*self->glm, c_min, c_max);
    {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
    if (!result){ return 0; }
    result->glm = new {{ name }}Glm(vector);
    return (PyObject *)result;
}


static PyObject *
{{ name }}_get_size({{ name }} *cls, void *)
{
    return PyLong_FromSize_t(sizeof({{ c_type }}) * {{ component_count }});
}


static PyObject *
{{ name }}_get_limits({{ name }} *cls, void *)
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
    {% if c_type in ['float', 'double'] %}
        {% if component_count == 3 %}
            {"cross", (PyCFunction){{ name }}_cross, METH_O, 0},
            {"to_quaternion", (PyCFunction){{ name }}_to_quaternion, METH_NOARGS, 0},
        {% endif %}
        {"lerp", (PyCFunction){{ name }}_lerp, METH_FASTCALL, 0},
        {"normalize", (PyCFunction){{ name }}_normalize, METH_NOARGS, 0},
        {"distance", (PyCFunction){{ name }}_distance, METH_O, 0},
    {% endif %}
    {"min", (PyCFunction){{ name }}_min, METH_O, 0},
    {"max", (PyCFunction){{ name }}_max, METH_O, 0},
    {"clamp", (PyCFunction){{ name }}_clamp, METH_FASTCALL, 0},
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
    {% if c_type in ['float', 'double'] %}
        {Py_nb_matrix_multiply, (void*){{ name }}__matmul__},
        {Py_nb_remainder, (void*){{ name }}__mod__},
        {Py_nb_power, (void*){{ name }}__pow__},
    {% endif %}
    {% if c_type != 'bool' %}
        {Py_nb_true_divide, (void*){{ name }}__truediv__},
    {% endif %}
    {% if 'unsigned' not in c_type and not (c_type.startswith('u') and c_type.endswith('_t')) %}
        {Py_nb_negative, (void*){{ name }}__neg__},
    {% endif %}
    {Py_nb_absolute, (void*){{ name }}__abs__},
    {Py_nb_bool, (void*){{ name }}__bool__},
    {Py_bf_getbuffer, (void*){{ name }}_getbufferproc},
    {Py_tp_getset, (void*){{ name }}_PyGetSetDef},
    {Py_tp_getattro, (void*){{ name }}__getattr__},
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

{% if c_type in ['float', 'double'] %}
    static {{ name }} *
    create_{{ name }}_from_glm(const {{ name }}Glm& glm)
    {
        auto module_state = get_module_state();
        if (!module_state){ return 0; }
        auto cls = module_state->{{ name }}_PyTypeObject;

        {{ name }} *result = ({{ name }} *)cls->tp_alloc(cls, 0);
        if (!result){ return 0; }
        result->glm = new {{ name }}Glm(glm);

        return result;
    }
{% endif %}


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
        for ({{ name }}Glm::length_type j = 0; j < {{ component_count }}; j++)
        {
            Py_uhash_t lane = std::hash<{{ c_type }}>{}(self->glm[i][j]);
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
        PyErr_SetString(PyExc_BufferError, "{{ name }} is read only");
        view->obj = 0;
        return -1;
    }
    {% if component_count != 1 %}
        if ((!(flags & PyBUF_C_CONTIGUOUS)) && flags & PyBUF_F_CONTIGUOUS)
        {
            PyErr_SetString(PyExc_BufferError, "{{ name }} cannot be made Fortran contiguous");
            view->obj = 0;
            return -1;
        }
    {% endif %}
    view->buf = self->glm;
    view->obj = (PyObject *)self;
    view->len = sizeof({{ c_type }}) * {{ component_count }} * self->length;
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
        view->shape = new Py_ssize_t[2] {
            (Py_ssize_t)self->length,
            {{ component_count }}
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


static const {{ c_type }} *
get_{{ name }}_value_ptr(const PyObject *self)
{
    if (Py_TYPE(self) != get_{{ name }}_type())
    {
        PyErr_Format(PyExc_TypeError, "expected {{ name }}, got %R", self);
        return 0;
    }
    return ({{ c_type }} *)(({{ name }} *)self)->glm;
}


static const {{ c_type }} *
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
