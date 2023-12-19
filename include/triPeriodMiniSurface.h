#ifndef TRI_PERIOD_MINI_SURFACE_H
#define TRI_PERIOD_MINI_SURFACE_H

#include <memory>
#include <vector>

#include "vertex.h"

class vtkUnstructuredGrid;
class MPMfile;

class TPMS {
private:
    double alpha, beta, gamma;
    double c;
    double delta;
    double volume_fraction;
    const int factor = 100;

public:
    size_t Nx = 50, Ny = 50, Nz = 50;
    std::vector<Vertex> V;
    friend class vtkUnstructuredGrid;
    vtkUnstructuredGrid* vtk;
    friend class MPMfile;
    MPMfile* mpm;

    TPMS(double _alpha, double _beta, double _gamma, double _c, double _delta);
    ~TPMS()
    {
        V.clear();
        // delete vtk;
    };
    bool contain(Vertex v);
    void generate();
};

#endif