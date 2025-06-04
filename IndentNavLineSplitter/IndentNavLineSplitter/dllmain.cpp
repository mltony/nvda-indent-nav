#include "pch.h"
#include <Python.h>
#include <memory>
#include "thread_pool.h"
static std::unique_ptr<ThreadPool> global_thread_pool;

static PyObject* hello(PyObject* self, PyObject* args) {
    return PyUnicode_FromString("Hello from C++!");
}

static std::vector<Py_ssize_t> worker_func(PyObject* s, Py_ssize_t start, Py_ssize_t end) {
    std::vector<Py_ssize_t> line_offsets;
    if (start == 0) {
        line_offsets.push_back(0);
    }
    bool sawCarriageReturn = false;
    for (Py_ssize_t i = start; i < end; i++) {
        auto c = PyUnicode_ReadChar(s, i);
        if (c == '\n') {
            line_offsets.push_back(i + 1);
            sawCarriageReturn = false;
        } 
        else if (c == '\r') {
            if (sawCarriageReturn) {
                // Detected two \r\r in a row - the document must be formatted using \r character only
                line_offsets.push_back(i);
            }
            sawCarriageReturn = true;
        }
        else if (sawCarriageReturn) {
            line_offsets.push_back(i);
            sawCarriageReturn = false;
        }
    }
    if (sawCarriageReturn) {
        line_offsets.push_back(end);
    }
    return line_offsets;
}

#define CHUNK_SIZE 500000

static PyObject* find_line_offsets(PyObject* self, PyObject* args) {
    PyObject* py_str = nullptr;

    // Parse a single positional argument, expecting a str object
    if (!PyArg_ParseTuple(args, "U", &py_str)) {
        // "U" format code ensures it's a Unicode object
        return nullptr;  // TypeError is automatically raised
    }
    std::vector<Py_ssize_t> all_offsets;
    Py_ssize_t length = PyUnicode_GetLength(py_str);
    if (length == 0) {
        all_offsets.push_back(0);
    }
    else {
        std::vector< std::future<std::vector<Py_ssize_t>>> futures;
        Py_ssize_t start = 0;
        while (start < length) {
            Py_ssize_t end = start + CHUNK_SIZE;
            if (end >= length) {
                end = length;
            }
            else {
                auto c = PyUnicode_ReadChar(py_str, end);
                if (c == '\n') {
                    end += 1;
                }
            }
            auto future_result = global_thread_pool->enqueue(worker_func, py_str, start, end);
            futures.push_back(std::move(future_result));
            start = end;
        }
        for (auto& future : futures) {
            try {
                std::vector<Py_ssize_t> result = future.get();  // Waits for task to complete
                all_offsets.insert(all_offsets.end(), result.begin(), result.end());
            }
            catch (const std::exception& ex) {
                PyErr_SetString(PyExc_Exception, ex.what());
                return nullptr;
            }
        }
    }
    PyObject* py_list = PyList_New(all_offsets.size());
    if (!py_list) return nullptr;

    for (Py_ssize_t i = 0; i < static_cast<Py_ssize_t>(all_offsets.size()); ++i) {
        PyObject* num = PyLong_FromSsize_t(all_offsets[i]);
        if (!num) {
            Py_DECREF(py_list);
            return nullptr;
        }
        PyList_SET_ITEM(py_list, i, num);  // Steals reference to num
    }

    return py_list;
}


// Method definition object
static PyMethodDef MyMethods[] = {
    {"hello", hello, METH_NOARGS, "Returns a hello string."},
    {"find_line_offsets", find_line_offsets, METH_VARARGS, "Finds line offsets in a large string."},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef mymodule = {
    PyModuleDef_HEAD_INIT,
    "IndentNavLineSplitter",         // name of module
    "C++ code for fast splitting text into lines for IndentNav NVDA add-on.", // module documentation
    -1,
    MyMethods
};

void cleanup() {
    global_thread_pool.reset();
}

// Module initialization function
PyMODINIT_FUNC PyInit_IndentNavLineSplitter(void) {
    Py_AtExit(cleanup);
    if (!global_thread_pool) {
        size_t n = std::thread::hardware_concurrency();
        if (n == 0) n = 4;
        global_thread_pool = std::make_unique<ThreadPool>(n);
    }
    return PyModule_Create(&mymodule);
}
