from matplotlib.colors import LinearSegmentedColormap

FieldCMap = LinearSegmentedColormap.from_list('my_gradient', (
                 # Edit this gradient at https://eltos.github.io/gradient/#4C71FF-0025B3-000000-C7030D-FC4A53
                 (0.000, (0.298, 0.443, 1.000)),
                 (0.250, (0.000, 0.145, 0.702)),
                 (0.500, (0.000, 0.000, 0.000)),
                 (0.750, (0.780, 0.012, 0.051)),
                 (1.000, (0.988, 0.290, 0.325))))


np.set_printoptions(edgeitems=30, linewidth=100000)

plt.rcParams['axes.facecolor']='white'
plt.rcParams['savefig.facecolor']='white'

plt.rcParams["font.weight"] = "normal"
plt.rcParams["axes.labelweight"] = "medium"
plt.rcParams['xtick.major.pad']='25'
plt.rcParams['ytick.labelsize']='25'
plt.rcParams['xtick.labelsize']='25'
plt.rcParams["axes.grid"] = False
plt.rcParams["axes.labelsize"] = 30
plt.rcParams["axes.titlesize"] = 30

plt.rcParams["font.size"] = 10
plt.rcParams['legend.fontsize'] = 20
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['xtick.labelsize'] = 25
plt.rcParams['ytick.labelsize'] = 25
