#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "pixhom.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

void change_sign(double* arr, size_t size) {
    for (size_t i = 0; i < size; ++i) {
        arr[i] = -arr[i];
    }
}


py::object py_computePH(py::array_t<double> input_array, bool return_index = false, int maxdim = 0) {
    // Ensure the input array is contiguous and 2D
    py::buffer_info buf_info = input_array.request();
    if (buf_info.ndim != 2) {
        throw std::runtime_error("Input should be a 2D NumPy array");
    }

    int numRows = buf_info.shape[0];
    int numCols = buf_info.shape[1];

    // Call the computePH function (dim = 0)
    Result res;
    try {
        res = computePH((double*)buf_info.ptr, numRows, numCols);
    } catch (const std::exception& e) {
        throw std::runtime_error(std::string("Error in computePH (dim = 0): ") + e.what());
    }

    // Create numpy arrays to return
    py::array_t<double> data_array_0({res.length / 2, 2});
    auto data_buf = data_array_0.request();
    std::copy(res.data.begin(), res.data.end(), (double *)data_buf.ptr);

    py::array_t<int> posix_array_0({res.length / 2, 4});
    auto posix_buf = posix_array_0.request();
    for (size_t i = 0; i < (res.posix.size() * 2); i += 4) {
        ((int*)posix_buf.ptr)[i] = res.posix[i / 2] % numCols;
        ((int*)posix_buf.ptr)[i + 1] = res.posix[i / 2] / numCols;
        ((int*)posix_buf.ptr)[i + 2] = res.posix[(i / 2) + 1] % numCols;
        ((int*)posix_buf.ptr)[i + 3] = res.posix[(i / 2) + 1] / numCols;
    }
    freemem();


    if (maxdim == 0){
        if (return_index) {
            return py::make_tuple(data_array_0, posix_array_0);
        } else {
            return data_array_0;
        }
    } else if(maxdim == 1){
        // Call the computePH function (dim = 0)
        Result res;
        try {
            change_sign((double*)buf_info.ptr, numRows * numCols);
            res = computePH((double*)buf_info.ptr, numRows, numCols);
            change_sign((double*)buf_info.ptr, numRows * numCols);
        } catch (const std::exception& e) {
            throw std::runtime_error(std::string("Error in computePH (dim = 0): ") + e.what());
        }

        // Create numpy arrays to return
        py::array_t<double> data_array_1({res.length / 2, 2});
        auto data_buf = data_array_1.request();
        change_sign(res.data.data(), res.data.size());
        //std::copy(res.data.begin(), res.data.end(), (double *)data_buf.ptr);
        for (size_t i = 0; i < res.data.size(); i += 2) {
            ((double*)data_buf.ptr)[i] = res.data[i + 1];
            ((double*)data_buf.ptr)[i + 1] = res.data[i];
        }
        py::array_t<int> posix_array_1({res.length / 2, 4});
        auto posix_buf = posix_array_1.request();
        for (size_t i = 0; i < (res.posix.size() * 2); i += 4) {
            ((int*)posix_buf.ptr)[i] = res.posix[(i / 2) + 1] % numCols;
            ((int*)posix_buf.ptr)[i + 1] = res.posix[(i / 2) + 1] / numCols;
            ((int*)posix_buf.ptr)[i + 2] = res.posix[i / 2] % numCols;
            ((int*)posix_buf.ptr)[i + 3] = res.posix[i / 2] / numCols;

        }
        freemem();

        if (return_index) {
            return py::make_tuple(py::make_tuple(data_array_0, data_array_1), py::make_tuple(posix_array_0, posix_array_1));
        } else {
            return py::make_tuple(data_array_0, data_array_1);
        }

    }
}

PYBIND11_MODULE(pixhomology, m) {
    m.doc() = "PixHomology is an open-source software for image processing and analysis focused on persistent homology computation. It provides a set of tools and algorithms to explore the topological features of 2D images, enabling users to extract meaningful information about the underlying structures."; // Optional module docstring

    m.def("computePH", &py_computePH,
      "A function that computes Persistent Homology (PH) on 2D image data.\n\n"
      "Parameters:\n"
      "  input_array (numpy.ndarray): A 2D array representing the input image data on which Persistent Homology is to be computed.\n"
      "  return_index (bool, optional): A flag indicating whether to return indices of the features. Defaults to False.\n"
      "  maxdim (int, optional): The maximum dimension of homology to compute. Defaults to 0.\n\n"
      "Returns:\n"
      "  numpy.ndarray or tuple:\n"
      "    - dgms (numpy.ndarray or list of numpy.ndarray): If maxdim=0, an (N, 2) array with birth and death values of dimension zero. If maxdim=1, a list of arrays for dimension 0 and dimension 1.\n"
      "    - indexes (numpy.ndarray or list of numpy.ndarray): If return_index=True. If maxdim=0, an (N, 4) array with x_birth, y_birth, x_death, y_death coordinates in pixels of dimension zero PH. If maxdim=1, a list of arrays for dimension 0 and dimension 1.",
      py::arg("input_array"),
      py::arg("return_index") = false,
      py::arg("maxdim") = 0);

    #ifdef VERSION_INFO
        m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
    #else
        m.attr("__version__") = "dev";
    #endif
}
