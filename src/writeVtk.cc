#include "writeVtk.h"
#include "triPeriodMiniSurface.h"
#include <iostream>

void vtkUnstructuredGrid::initialize(std::string _filename = "demo.vtk")
{
    filename = _filename;
    content.open(filename.c_str());
    content << "# vtk DataFile Version 2.0" << std::endl;
    content << "TPMS, Volume Fraction=" << tpms->volume_fraction << std::endl;
    content << "ASCII" << std::endl;
    content << "DATASET UNSTRUCTURED_GRID" << std::endl;
};

void vtkUnstructuredGrid::write()
{
    content << "POINTS " << tpms->V.size() << " double\n";
    int count = 0;
    for (auto v : tpms->V) {
        content << v.x << " " << v.y << " " << v.z << "\n";
    }
    content << "CELLS 0 0\n";
}