#include "writeMPM.h"
#include "triPeriodMiniSurface.h"

void MPMfile::initialize(std::string _filename = "demo.mpm")
{
    dx = 1.0 * tpms->factor / tpms->Nx;
    filename = _filename;
    content.open(filename.c_str());
    content << "mpm3d *** test simulation" << std::endl;
    content << "! Unit: mm g N ms MPa" << std::endl;
    content << "nbco " << 3 << std::endl;
    content << "nbbo " << 3 << std::endl;
    content << "nbmp " << 2 * (102 / dx * 102 / dx * 6 / dx) + tpms->V.size() << std::endl;
    content << "nmat " << 2 << std::endl;
};

void MPMfile::write()
{
    // Grid Span & cell size
    content << std::endl;
    content << "spx " << 0 - 0.5 * dx << " " << 100 + 0.5 * dx << std::endl;
    content << "spy " << -10 - 0.5 * dx << " " << 110 + 0.5 * dx << std::endl;
    content << "spz " << 0 - 0.5 * dx << " " << 100 + 0.5 * dx << std::endl;
    content << "dcell " << dx * dCellScale << std::endl;

    // Boundary Condition
    content << std::endl;
    content << "fixed "
            << 2 << " " // left   (min.x) symmetry
            << 2 << " " // right  (max.x) symmetry
            << 1 << " " // bottom (min.y) fixed
            << 1 << " " // top    (max.y) fixed
            << 2 << " " // back   (min.z) symmetry
            << 2 // front  (max.z) symmetry
            << std::endl;

    // Material
    content << std::endl;
    content << "material" << std::endl;
    //  Gyroid TPMS
    //     content << 1 << " elas "
    //             << 1.2e-3 << " " // density
    //             << 29 << " " // Elastic Modulus
    //             << 0.39 // Poisson's Ratio
    //             << std::endl;
    content << 1 << " jcst "
            << 2.8e-3 << " " // Density
            << 6.89e4 << " " // Young's Modulus
            << 0.33 << " " // Poisson's Ratio
            << 295 << " " // A, Yield Stress
            << 635 << " " // B, Strength Coefficient
            << 0.9 << " " // n, Hardening Exponent
            << 0.0075 << " " // C, Strain Rate Strength Coefficient
            << 1.429 << " " // m, Temperature Exponent
            << 293 << " " // Room Temperature
            << 863 << " " // Melting Temperature
            << 8.8e2 << " " // Specific Heat Capacity
            << 1e-6 << " " // Reference Strain Rate
            << 0.116 << " " // D1
            << 0.211 << " " // D2
            << -2.172 << " " // D3
            << 0.012 << " " // D4
            << -0.01256 << " " // D5
            << 1 << " " // Failure strain factor
            << std::endl;
    // block
    content << 2 << " elas "
            << 7.85e-3 << " " // density
            << 2e3 << " " // Elastic Modulus
            << 0.3 // Poisson's Ratio
            << std::endl;
    // EoS
    //  Mie-Gruneisen EoS for TPMS
    content << "seos "
            << 1 << " "
            << 4 << " "
            << 4909 << " " // C
            << 2.03 << " " // S1
            << 0 << " " // S2
            << 0 << " " // S3
            << 1.97 << " " // gamma0
            << 0 << " " // a
            << 0 << " " // E0
            << 0 << std::endl; // V0

    // PostProcess Parameter
    content << std::endl;
    content << "para" << std::endl;

    // Time Step
    content << std::endl;
    content << "dtscale " << dtScale << std::endl;
    content << "endt " << endTime << std::endl;
    content << "outtime " << outTime << std::endl;
    content << "rpttime " << rptTime << std::endl;

    // Algorithm
    content << "gimp "
            << "on" << std::endl;
    content << "musl "
            << "on" << std::endl;
    content << "jaum "
            << "on" << std::endl;
    // Contact Algorithm
    content << "contact" << std::endl;
    content << "lagr "
            << 0.00 << " "
            << 2 << std::endl;

    int count = 0;
    // Gyroid TPMS
    content << std::endl;
    content << "Particle "
            << "point " << 1 << " " << tpms->V.size() << std::endl;
    for (auto v : tpms->V) {
        ++count;
        content << count << " "
                << 1 << " "
                << 1.2e-3 * (dx * dx * dx) << " "
                << v.x << " " << v.y << " " << v.z
                << std::endl;
    }
    // Up
    content << std::endl;
    content << "Particle "
            << "block " << 2 << std::endl;
    content << 2 << " "
            << 7.85e-3 * (dx * dx * dx) << " "
            << dx << " "
            << -1 << " " << 100 << " " << -1 << " "
            << 102 / dx << " " << 6 / dx << " " << 102 / dx
            << std::endl;
    // Down
    content << std::endl;
    content << "Particle "
            << "block " << 3 << std::endl;
    content << 2 << " "
            << 7.85e-3 * (dx * dx * dx) << " "
            << dx << " "
            << -1 << " " << -6 << " " << -1 << " "
            << 102 / dx << " " << 6 / dx << " " << 102 / dx
            << std::endl;

    content << std::endl;
    content << "velo " << std::endl;
    content << "m_bo " << 2 << " "
            << 0 << " " << -1e0 << " " << 0 << std::endl;
    content << "endv" << std::endl;

    content << std::endl;
    content << "endi" << std::endl;
}