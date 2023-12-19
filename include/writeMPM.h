#ifndef WRITE_MPM_H
#define WRITE_MPM_H

#include <fstream>
#include <memory>
#include <string>
#include <vector>

class TPMS;

class MPMfile {
private:
    friend class TPMS;
    TPMS* tpms;
    std::string filename;
    std::ofstream content;

    double dx = 0;
    const double dCellScale = 2;
    const double endTime = 6e1;
    const double outTime = 2e0;
    const double rptTime = 5e-1;
    const double dtScale = 0.5;

public:
    MPMfile(TPMS* _tpms)
        : tpms(_tpms) {};
    void initialize(std::string _filename);
    ~MPMfile() {
        // delete tpms;
    };
    void write();
};

#endif