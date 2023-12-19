#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>

#include "triPeriodMiniSurface.h"
#include "vertex.h"

int main()
{
    std::vector<double> alpha_list = { /* 3.5, 2.5,  */ 2 /* , 1 */ };
    std::vector<double> beta_list = { /* 3.5, 2.5,  */ 2 /* , 1 */ };
    std::vector<double> gamma_list = { /* 3.5, 2.5,  */ 2 /* , 1 */ };
    std::vector<double> c_list = { /* 1,  */ 0.5 };
    std::vector<double> delta_list = { /* 1,  */ 1 };

    auto start = std::chrono::steady_clock::now();
    for (auto alpha : alpha_list) {
        for (auto beta : beta_list) {
            for (auto gamma : gamma_list) {
                for (auto c : c_list) {
                    for (auto delta : delta_list) {
                        TPMS tpms(alpha, beta, gamma, c, delta);
                        tpms.generate();
                    }
                }
            }
        }
    }
    auto end = std::chrono::steady_clock::now();
    std::cout << "Elapsed time in seconds : "
              << std::chrono::duration_cast<std::chrono::seconds>(end - start).count()
              << " s" << std::endl;

    return 0;
}