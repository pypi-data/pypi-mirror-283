
// generated from codegen/templates/_modulestate.hpp

#ifndef E_MATH_MODULESTATE_HPP
#define E_MATH_MODULESTATE_HPP

// python
#define PY_SSIZE_T_CLEAN
#include <Python.h>
// emath
#include "_module.hpp"

struct ModuleState
{
    PyObject *ctypes_c_bool_p;
    PyObject *ctypes_c_int8_t_p;
    PyObject *ctypes_c_uint8_t_p;
    PyObject *ctypes_c_int16_t_p;
    PyObject *ctypes_c_uint16_t_p;
    PyObject *ctypes_c_int32_t_p;
    PyObject *ctypes_c_uint32_t_p;
    PyObject *ctypes_c_int64_t_p;
    PyObject *ctypes_c_uint64_t_p;
    PyObject *ctypes_c_int_p;
    PyObject *ctypes_c_unsigned_int_p;
    PyObject *ctypes_c_float_p;
    PyObject *ctypes_c_double_p;
    {% for type in types %}
        PyTypeObject *{{ type }}_PyTypeObject;
        PyTypeObject *{{ type }}Array_PyTypeObject;
    {% endfor %}
    {% for pod_type in pod_types %}
        PyTypeObject *{{ pod_type }}Array_PyTypeObject;
    {% endfor %}
};


static int
ModuleState_traverse(
    struct ModuleState *self,
    visitproc visit,
    void *arg
)
{
    Py_VISIT(self->ctypes_c_bool_p);
    Py_VISIT(self->ctypes_c_int8_t_p);
    Py_VISIT(self->ctypes_c_uint8_t_p);
    Py_VISIT(self->ctypes_c_int16_t_p);
    Py_VISIT(self->ctypes_c_uint16_t_p);
    Py_VISIT(self->ctypes_c_int32_t_p);
    Py_VISIT(self->ctypes_c_uint32_t_p);
    Py_VISIT(self->ctypes_c_int64_t_p);
    Py_VISIT(self->ctypes_c_uint64_t_p);
    Py_VISIT(self->ctypes_c_int_p);
    Py_VISIT(self->ctypes_c_unsigned_int_p);
    Py_VISIT(self->ctypes_c_float_p);
    Py_VISIT(self->ctypes_c_double_p);
    {% for type in types %}
        Py_VISIT(self->{{ type }}_PyTypeObject);
        Py_VISIT(self->{{ type }}Array_PyTypeObject);
    {% endfor %}
    {% for pod_type in pod_types %}
        Py_VISIT(self->{{ pod_type }}Array_PyTypeObject);
    {% endfor %}
    return 0;
}


static int
ModuleState_clear(struct ModuleState *self)
{
    Py_CLEAR(self->ctypes_c_bool_p);
    Py_CLEAR(self->ctypes_c_int8_t_p);
    Py_CLEAR(self->ctypes_c_uint8_t_p);
    Py_CLEAR(self->ctypes_c_int16_t_p);
    Py_CLEAR(self->ctypes_c_uint16_t_p);
    Py_CLEAR(self->ctypes_c_int32_t_p);
    Py_CLEAR(self->ctypes_c_uint32_t_p);
    Py_CLEAR(self->ctypes_c_int64_t_p);
    Py_CLEAR(self->ctypes_c_uint64_t_p);
    Py_CLEAR(self->ctypes_c_int_p);
    Py_CLEAR(self->ctypes_c_unsigned_int_p);
    Py_CLEAR(self->ctypes_c_float_p);
    Py_CLEAR(self->ctypes_c_double_p);
    {% for type in types %}
        Py_CLEAR(self->{{ type }}_PyTypeObject);
        Py_CLEAR(self->{{ type }}Array_PyTypeObject);
    {% endfor %}
    {% for pod_type in pod_types %}
        Py_CLEAR(self->{{ pod_type }}Array_PyTypeObject);
    {% endfor %}
    return 0;
}


static ModuleState *
get_module_state()
{
    PyObject *module = get_module();
    if (!module){ return 0; }
    return (ModuleState *)PyModule_GetState(module);
}

#endif