set(dir "${CMAKE_CURRENT_SOURCE_DIR}")

list(
    APPEND srcs
    "${dir}/main.cc"
    "${dir}/triPeriodMiniSurface.cc"
    "${dir}/writeMPM.cc"
    "${dir}/writeVtk.cc"
)

set(srcs "${srcs}" PARENT_SCOPE)