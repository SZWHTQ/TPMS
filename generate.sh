#!/bin/zsh

genTPMS=/home/tengqing/Repository/TPMS/build/genTPMS

alpha_list=(2.0 2.5 3.0)
beta_list=(2.5 3.0 3.5)
gamma_list=(1.5 2.0 2.5)
c_list=(0.25 0.5)
delta_list=(0.5 1.0)

counter=0
for alpha in "${alpha_list[@]}"; do
   for beta in "${beta_list[@]}"; do
      for gamma in "${gamma_list[@]}"; do
         for c in "${c_list[@]}"; do
            for delta in "${delta_list[@]}"; do
               counter=$((counter+1))
               mkdir -p ${counter}
               cd ${counter}
               ${genTPMS} ${alpha} ${beta} ${gamma} ${c} ${delta}
               cd ..
            done
         done
      done
   done
done