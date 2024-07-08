
// generated from codegen/templates/_pod.hpp

#ifndef E_MATH_{{ name.upper() }}_HPP
#define E_MATH_{{ name.upper() }}_HPP

// stdlib
#include <limits>
#include <functional>
// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
// emath
#include "_modulestate.hpp"
#include "_podtype.hpp"
#include "_type.hpp"


static PyObject *
{{ name }}Array__new__(PyTypeObject *cls, PyObject *args, PyObject *kwds)
{
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
        self->pod = 0;
        return (PyObject *)self;
    }

    auto *self = ({{ name }}Array *)cls->tp_alloc(cls, 0);
    if (!self){ return 0; }
    self->length = arg_count;
    self->pod = new {{ c_type }}[arg_count];

    for (int i = 0; i < arg_count; i++)
    {
        auto arg = PyTuple_GET_ITEM(args, i);
        self->pod[i] = pyobject_to_c_{{ c_type.replace(' ', '_') }}(arg);
        if (PyErr_Occurred())
        {
            Py_DECREF(self);
            PyErr_Format(
                PyExc_TypeError,
                "invalid type %R, expected {{ c_type }}",
                arg
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

    delete self->pod;

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
{{ name }}Array__hash__({{ name }}Array *self)
{
    Py_ssize_t len = self->length;
    Py_uhash_t acc = _HASH_XXPRIME_5;
    for (Py_ssize_t i = 0; i < (Py_ssize_t)self->length; i++)
    {
        Py_uhash_t lane = std::hash<{{ c_type }}>{}(self->pod[i]);
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
    return c_{{ c_type.replace(' ', '_') }}_to_pyobject(self->pod[index]);
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
            result->pod = 0;
        }
        else
        {
            result->length = length;
            result->pod = new {{ c_type }}[length];
            for (Py_ssize_t i = 0; i < length; i++)
            {
                result->pod[i] = self->pod[start + (i * step)];
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

        return c_{{ c_type.replace(' ', '_') }}_to_pyobject(self->pod[index]);
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
                    if (self->pod[i] != other->pod[i])
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
                    if (self->pod[i] != other->pod[i])
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
    view->buf = self->pod;
    view->obj = (PyObject *)self;
    view->len = sizeof({{ c_type }}) * self->length;
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
        view->shape = new Py_ssize_t[1] {
            (Py_ssize_t)self->length
        };
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
    return PyObject_CallMethod(c_p, "from_address", "n", (Py_ssize_t)&self->pod);
}


static PyObject *
{{ name }}Array_size({{ name }}Array *self, void *)
{
    return PyLong_FromSize_t(sizeof({{ c_type }}) * self->length);
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
    if (view_length % sizeof({{ c_type }}))
    {
        PyBuffer_Release(&view);
        PyErr_Format(PyExc_BufferError, "expected buffer evenly divisible by %zd, got %zd", sizeof({{ c_type }}), view_length);
        return 0;
    }
    auto array_length = view_length / sizeof({{ c_type }});

    auto *result = ({{ name }}Array *)cls->tp_alloc(cls, 0);
    if (!result)
    {
        PyBuffer_Release(&view);
        return 0;
    }
    result->length = array_length;
    if (array_length > 0)
    {
        result->pod = new {{ c_type }}[array_length];
        std::memcpy(result->pod, view.buf, view_length);
    }
    else
    {
        result->pod = 0;
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
    {% if c_type in ['float', 'double'] %}
        Py_INCREF(&PyFloat_Type);
        return (PyObject *)&PyFloat_Type;
    {% elif c_type == 'bool' %}
        Py_INCREF(&PyBool_Type);
        return (PyObject *)&PyBool_Type;
    {% else %}
        Py_INCREF(&PyLong_Type);
        return (PyObject *)&PyLong_Type;
    {% endif %}
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
get_{{ name }}Array_type()
{
    auto module_state = get_module_state();
    if (!module_state){ return 0; }
    return module_state->{{ name }}Array_PyTypeObject;
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
        result->pod = new {{ c_type }}[length];
        for (size_t i = 0; i < length; i++)
        {
            result->pod[i] = value[i];
        }
    }
    else
    {
        result->pod = 0;
    }
    return (PyObject *)result;
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
    return (({{ name }}Array *)self)->pod;
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
