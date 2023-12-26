import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.signal import medfilt
from scipy.interpolate import interp1d

rcParams['font.family'] = ['serif']
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = 16

def target_func(x):
    return 10+150*(x-0.1)**2

# Read data
with np.load("./data.npz") as data:
    time = data["time"]
    force = data["force"]
    params = data["params"]

force = medfilt(force, 5)
interplot_function = interp1d(time, force, kind="cubic")
time = np.linspace(np.min(time), np.max(time), 201)
force = interplot_function(time)

max_force = np.max(force, axis=1)
sorted_indices = np.argsort(max_force)

colormap = plt.get_cmap("autumn")
# Plot
for i, curve in enumerate(force):
    plt.plot(time/1e2, curve/1e4, color=colormap(i / 108.0), alpha=0.5)
# plt.ylim(0, 100)
plt.xlabel("Strain")
plt.ylabel("Stress (MPa)")

new_force = target_func(time/1e2)*1e4
plt.plot(time/1e2, new_force/1e4, label="Target Curve", linewidth=2, color="#1f77b4")
plt.ylim(-2,152)
plt.yticks(np.arange(0, 152, 25))

plt.show()
