#ifndef WRITE_VTK_H
#define WRITE_VTK_H

#include <fstream>
#include <memory>
#include <string>
#include <vector>

#include "vertex.h"

class TPMS;

class vtkUnstructuredGrid {
private:
    friend class TPMS;
    TPMS* tpms;
    std::string filename;
    std::ofstream content;

public:
    vtkUnstructuredGrid(TPMS* _tpms)
        : tpms(_tpms) {};
    void initialize(std::string _filename);
    ~vtkUnstructuredGrid() {
        // delete tpms;
    };
    void write();
};

#endif