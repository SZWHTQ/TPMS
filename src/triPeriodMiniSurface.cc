#include <math.h>
#include <string>

#include "triPeriodMiniSurface.h"
#include "writeVtk.h"
#include "writeMPM.h"

TPMS::TPMS(double _alpha, double _beta, double _gamma, double _c, double _delta)
    : alpha(_alpha)
    , beta(_beta)
    , gamma(_gamma)
    , c(_c)
    , delta(_delta)
{
    vtk = new vtkUnstructuredGrid(this);
    mpm = new MPMfile(this);
}

bool TPMS::contain(Vertex v)
{
    double X = 2 * M_PI * alpha * v.x / factor;
    double Y = 2 * M_PI * beta * v.y / factor;
    double Z = 2 * M_PI * gamma * v.z / factor;
    return (sin(X) * cos(Y) + sin(Y) * cos(Z) + sin(Z) * cos(X) > c - delta * 0.5)
        && (sin(X) * cos(Y) + sin(Y) * cos(Z) + sin(Z) * cos(X) < c + delta * 0.5);
}

void TPMS::generate()
{
    double dx = 1.0 * factor / Nx, dy = 1.0 * factor / Ny, dz = 1.0 * factor / Nz;
    for (size_t i = 0; i < Nx; ++i) {
        double x = i * dx;
        for (size_t j = 0; j < Ny; ++j) {
            double y = j * dy;
            for (size_t k = 0; k < Nz; ++k) {
                double z = k * dz;
                Vertex v(x, y, z);
                if (contain(v)) {
                    V.push_back(v);
                }
            }
        }
    }
    volume_fraction = (double)V.size() / (Nx * Ny * Nz);
    std::string filename = "tpms" + std::to_string(alpha) + "_" + std::to_string(beta) + "_" + std::to_string(gamma) + "_" + std::to_string(c) + "_" + std::to_string(delta) + ".vtk";
    vtk->initialize(filename);
    vtk->write();
    mpm->initialize("gyroid.mpm");
    mpm->write();
}
