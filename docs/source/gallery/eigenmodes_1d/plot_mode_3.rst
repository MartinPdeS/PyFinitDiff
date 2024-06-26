
.. DO NOT EDIT.
.. THIS FILE WAS AUTOMATICALLY GENERATED BY SPHINX-GALLERY.
.. TO MAKE CHANGES, EDIT THE SOURCE PYTHON FILE:
.. "gallery/eigenmodes_1d/plot_mode_3.py"
.. LINE NUMBERS ARE GIVEN BELOW.

.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        :ref:`Go to the end <sphx_glr_download_gallery_eigenmodes_1d_plot_mode_3.py>`
        to download the full example code

.. rst-class:: sphx-glr-example-title

.. _sphx_glr_gallery_eigenmodes_1d_plot_mode_3.py:


Example: 1D eigenmodes 2
========================

.. GENERATED FROM PYTHON SOURCE LINES 8-15

.. list-table:: 1D Finit-difference parameters
   :widths: 25
   :header-rows: 1

   * - boundaries: {left: anti-symmetric, right: anti-symmetric}
   * - derivative: 2
   * - accuracy: 6

.. GENERATED FROM PYTHON SOURCE LINES 15-62

.. code-block:: python3


    from scipy.sparse import linalg

    from MPSPlots.render2D import SceneList

    from PyFinitDiff.finite_difference_1D import FiniteDifference
    from PyFinitDiff.finite_difference_1D import get_circular_mesh_triplet
    from PyFinitDiff.finite_difference_1D import Boundaries


    n_x = 200
    sparse_instance = FiniteDifference(
        n_x=n_x,
        dx=1,
        derivative=2,
        accuracy=6,
        boundaries=Boundaries()
    )

    mesh_triplet = get_circular_mesh_triplet(
        n_x=n_x,
        radius=60,
        value_out=1,
        value_in=1.4444,
        x_offset=+100
    )

    dynamic_triplet = sparse_instance.triplet + mesh_triplet

    eigen_values, eigen_vectors = linalg.eigs(
        dynamic_triplet.to_dense(),
        k=4,
        which='LM',
        sigma=1.4444
    )

    figure = SceneList(unit_size=(3, 3), tight_layout=True, ax_orientation='horizontal')

    for i in range(4):
        Vector = eigen_vectors[:, i].real.reshape([sparse_instance.n_x])
        ax = figure.append_ax(title=f'eigenvalues: \n{eigen_values[i]:.3f}')
        _ = ax.add_line(y=Vector)

    figure.show()


    # -



.. image-sg:: /gallery/eigenmodes_1d/images/sphx_glr_plot_mode_3_001.png
   :alt: , eigenvalues:  1.442+0.000j, eigenvalues:  1.434+0.000j, eigenvalues:  1.421+0.000j, eigenvalues:  1.403+0.000j
   :srcset: /gallery/eigenmodes_1d/images/sphx_glr_plot_mode_3_001.png
   :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 .. code-block:: none


    SceneList(unit_size=(3, 3), tight_layout=True, transparent_background=False, title='', padding=1.0, axis_list=[Axis(row=0, col=0, x_label=None, y_label=None, title='eigenvalues: \n1.442+0.000j', show_grid=True, show_legend=False, legend_position='best', x_scale='linear', y_scale='linear', x_limits=None, y_limits=None, equal_limits=False, projection=None, font_size=16, tick_size=14, y_tick_position='left', x_tick_position='bottom', show_ticks=True, show_colorbar=None, legend_font_size=14, line_width=None, line_style=None, x_scale_factor=None, y_scale_factor=None, aspect_ratio='auto', _artist_list=[Line(y=array([ 1.26015503e-17,  2.36905816e-17, -1.19795244e-17,  4.20613803e-18,
           -3.29125378e-17,  1.40141403e-17, -5.29139551e-17, -5.55512817e-18,
           -3.87693967e-18,  5.58755970e-18,  1.20145766e-17, -3.16194066e-20,
           -1.08365076e-17, -5.18460432e-18, -2.60383782e-18, -2.14413345e-18,
           -3.92460641e-18,  3.67890922e-17,  4.58976785e-18,  3.96404857e-19,
           -1.17018662e-17,  1.74034541e-19, -7.49316342e-19,  3.52413614e-20,
           -1.19225241e-17,  2.13850166e-17, -1.70080854e-17,  9.33237021e-18,
           -1.04748635e-17, -1.72463097e-17, -5.06292355e-18,  1.69437359e-17,
           -5.97832851e-18,  4.82971056e-18,  5.53272032e-20,  1.60065975e-17,
            1.95785491e-17, -4.31251191e-18, -1.61428648e-17,  2.53171776e-19,
            2.51231035e-19, -1.70737952e-18,  7.82702770e-18, -6.16031319e-18,
            1.11727562e-19,  2.66537079e-17, -1.71017330e-18,  3.92499660e-17,
            1.63364270e-17,  6.95848119e-18,  2.93265193e-17, -1.12209984e-17,
            2.96946762e-18, -7.54990485e-19, -3.73804224e-17, -8.07685221e-18,
            3.18294674e-18, -2.71826077e-19, -3.88865421e-18, -4.41000943e-18,
            6.92315505e-18, -2.47723868e-17, -2.18814369e-18,  1.35136724e-18,
           -2.83387269e-18,  1.82985281e-17,  1.51566862e-17, -6.13141362e-18,
           -2.68861872e-18, -7.47501825e-19, -4.52859585e-20,  2.86208225e-17,
            7.96235697e-18,  3.15009376e-17, -6.19559450e-19, -5.74810492e-19,
           -1.95416721e-17,  1.19096930e-17,  2.74237556e-19, -1.30372337e-17,
           -1.35275061e-17, -2.11253998e-18,  1.14664942e-17, -9.90213468e-18,
           -1.43932012e-17,  1.34212434e-17,  1.28233653e-17, -9.71345962e-18,
           -4.36286161e-17, -3.72435724e-17, -7.23830213e-17, -1.42594354e-16,
           -2.37099030e-16, -5.19775354e-16, -1.02185611e-15, -1.98106947e-15,
           -3.86014858e-15, -7.50930831e-15, -1.45962761e-14, -2.83389197e-14,
           -5.51038168e-14, -1.07063112e-13, -2.08094344e-13, -4.04526240e-13,
           -7.86333647e-13, -1.52851203e-12, -2.97106727e-12, -5.77515930e-12,
           -1.12257695e-11, -2.18207106e-11, -4.24152245e-11, -8.24469297e-11,
           -1.60260770e-10, -3.11515771e-10, -6.05525997e-10, -1.17702467e-09,
           -2.28790681e-09, -4.44724545e-09, -8.64457939e-09, -1.68033795e-08,
           -3.26624985e-08, -6.34895385e-08, -1.23411303e-07, -2.39887549e-07,
           -4.66294695e-07, -9.06386112e-07, -1.76183815e-06, -3.42467039e-06,
           -6.65689255e-06, -1.29397032e-05, -2.51522640e-05, -4.88911055e-05,
           -9.50347967e-05, -1.84729133e-04, -3.59076772e-04, -6.97968884e-04,
           -1.35671903e-03, -2.63791756e-03, -5.13511369e-03, -9.98776533e-03,
           -1.86865363e-02, -2.77175408e-02, -3.66815181e-02, -4.55481908e-02,
           -5.42974422e-02, -6.29071281e-02, -7.13551309e-02, -7.96197354e-02,
           -8.76796996e-02, -9.55143074e-02, -1.03103422e-01, -1.10427538e-01,
           -1.17467831e-01, -1.24206205e-01, -1.30625342e-01, -1.36708742e-01,
           -1.42440770e-01, -1.47806694e-01, -1.52792722e-01, -1.57386039e-01,
           -1.61574838e-01, -1.65348354e-01, -1.68696888e-01, -1.71611834e-01,
           -1.74085699e-01, -1.76112125e-01, -1.77685903e-01, -1.78802989e-01,
           -1.79460512e-01, -1.79656781e-01, -1.79391293e-01, -1.78664728e-01,
           -1.77478956e-01, -1.75837023e-01, -1.73743150e-01, -1.71202718e-01,
           -1.68222258e-01, -1.64809428e-01, -1.60973002e-01, -1.56722839e-01,
           -1.52069864e-01, -1.47026035e-01, -1.41604317e-01, -1.35818644e-01,
           -1.29683886e-01, -1.23215813e-01, -1.16431047e-01, -1.09347028e-01,
           -1.01981962e-01, -9.43547802e-02, -8.64850855e-02, -7.83931049e-02,
           -7.00996365e-02, -6.16259965e-02, -5.29939646e-02, -4.42257312e-02,
           -3.53438042e-02, -2.63702502e-02, -1.73225543e-02, -8.24407218e-03]), x=array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
            13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,
            26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,
            39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
            52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,
            65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,
            78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,
           104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
           117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
           130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
           143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
           156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
           169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181,
           182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194,
           195, 196, 197, 198, 199]), label='', color=None, line_style='-', line_width=1, x_scale_factor=1, y_scale_factor=1, layer_position=1, mappable=[<matplotlib.lines.Line2D object at 0x130fe3390>])], mpl_ax=<Axes: title={'center': 'eigenvalues: \n1.442+0.000j'}>, colorbar=Colorbar(artist=None, discreet=False, position='right', colormap=<matplotlib.colors.LinearSegmentedColormap object at 0x125418050>, orientation='vertical', symmetric=False, log_norm=False, numeric_format=None, n_ticks=None, label_size=None, width='10%', padding=0.1, norm=None, label='', mappable=None)), Axis(row=0, col=1, x_label=None, y_label=None, title='eigenvalues: \n1.434+0.000j', show_grid=True, show_legend=False, legend_position='best', x_scale='linear', y_scale='linear', x_limits=None, y_limits=None, equal_limits=False, projection=None, font_size=16, tick_size=14, y_tick_position='left', x_tick_position='bottom', show_ticks=True, show_colorbar=None, legend_font_size=14, line_width=None, line_style=None, x_scale_factor=None, y_scale_factor=None, aspect_ratio='auto', _artist_list=[Line(y=array([-5.16646271e-18,  4.26755125e-18, -1.95137079e-18,  6.47422135e-18,
           -1.27066269e-18,  7.73186303e-18,  2.10655556e-18,  4.23248084e-18,
           -8.90569549e-18, -5.91083334e-18, -9.25109095e-18, -7.35565608e-18,
           -1.07989096e-17, -1.94111201e-17, -2.74510569e-18, -1.00219206e-17,
           -1.22887331e-18, -9.32050203e-19, -6.90214073e-18,  8.08743675e-18,
            1.43757585e-18,  5.67172370e-18,  1.22719597e-18,  2.38899369e-18,
            2.08282292e-18,  1.01119900e-17,  7.36832639e-18,  1.19312584e-17,
           -8.12599545e-19, -2.66597006e-18,  1.86748506e-18, -5.77954953e-19,
           -4.83078417e-18, -5.96889269e-19, -6.66241991e-18,  4.82053515e-19,
           -1.44852621e-18, -2.26100627e-18,  7.14362445e-19, -1.05839699e-18,
           -2.75681665e-18,  6.01266298e-18, -6.49115901e-18, -4.62257677e-18,
           -3.24219918e-18, -4.09909451e-18, -1.30922225e-17, -9.32349954e-18,
           -7.91009371e-18, -9.40537191e-18, -1.00138291e-17, -7.54438928e-18,
           -7.80050995e-20,  2.50351605e-18,  3.61704226e-18,  4.69893825e-18,
            1.11020032e-17,  4.59345235e-18, -8.78814866e-19,  1.72566940e-18,
            1.12088410e-17, -8.82016643e-18,  5.22387003e-18,  6.81652839e-20,
           -1.51716744e-17,  3.24503717e-19,  5.45417701e-18, -8.10732409e-18,
            6.95778328e-18,  1.01929747e-18, -7.19305159e-18, -6.60223906e-18,
           -9.99172270e-18, -5.02331142e-18, -4.73284905e-18,  3.16749354e-18,
            1.99121160e-18,  2.93849129e-18,  6.18567556e-18,  5.11305318e-18,
            7.56176991e-18,  6.19469743e-18,  1.01709534e-17, -1.20423354e-18,
           -8.40267631e-18, -2.37768930e-18, -1.19601051e-17, -2.55600441e-17,
           -5.47430707e-17, -8.95864431e-17, -1.89014341e-16, -3.64430421e-16,
           -7.16661229e-16, -1.36910124e-15, -2.66120794e-15, -5.13820699e-15,
           -9.93474841e-15, -1.91769165e-14, -3.70987438e-14, -7.16769850e-14,
           -1.38540982e-13, -2.67731006e-13, -5.17390164e-13, -9.99877093e-13,
           -1.93228673e-12, -3.73418587e-12, -7.21639547e-12, -1.39458299e-11,
           -2.69506194e-11, -5.20826279e-11, -1.00650743e-10, -1.94509613e-10,
           -3.75893778e-10, -7.26422388e-10, -1.40382604e-09, -2.71292237e-09,
           -5.24277769e-09, -1.01317745e-08, -1.95798604e-08, -3.78384786e-08,
           -7.31236297e-08, -1.41312902e-07, -2.73090058e-07, -5.27752093e-07,
           -1.01989166e-06, -1.97096137e-06, -3.80892295e-06, -7.36082110e-06,
           -1.42249365e-05, -2.74899792e-05, -5.31249441e-05, -1.02665037e-04,
           -1.98402283e-04, -3.83416424e-04, -7.40958647e-04, -1.43190485e-03,
           -2.76719239e-03, -5.34908876e-03, -1.03521560e-02, -2.00176095e-02,
           -3.72345261e-02, -5.48306167e-02, -7.18719055e-02, -8.81688059e-02,
           -1.03559246e-01, -1.17885809e-01, -1.31001339e-01, -1.42771099e-01,
           -1.53074176e-01, -1.61804728e-01, -1.68873067e-01, -1.74206579e-01,
           -1.77750474e-01, -1.79468345e-01, -1.79342544e-01, -1.77374365e-01,
           -1.73584025e-01, -1.68010464e-01, -1.60710938e-01, -1.51760434e-01,
           -1.41250901e-01, -1.29290303e-01, -1.16001511e-01, -1.01521040e-01,
           -8.59976473e-02, -6.95908040e-02, -5.24690570e-02, -3.48082974e-02,
           -1.67899535e-02,  1.40087287e-03,  1.95773082e-02,  3.75526265e-02,
            5.51421682e-02,  7.21652366e-02,  8.84469542e-02,  1.03820060e-01,
            1.18126626e-01,  1.31219682e-01,  1.42964723e-01,  1.53241093e-01,
            1.61943223e-01,  1.68981716e-01,  1.74284268e-01,  1.77796403e-01,
            1.79482043e-01,  1.79323871e-01,  1.77323512e-01,  1.73501515e-01,
            1.67897143e-01,  1.60567971e-01,  1.51589291e-01,  1.41053339e-01,
            1.29068352e-01,  1.15757451e-01,  1.01257379e-01,  8.57171036e-02,
            6.92962124e-02,  5.21618759e-02,  3.44789889e-02,  1.64694471e-02]), x=array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
            13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,
            26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,
            39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
            52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,
            65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,
            78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,
           104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
           117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
           130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
           143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
           156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
           169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181,
           182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194,
           195, 196, 197, 198, 199]), label='', color=None, line_style='-', line_width=1, x_scale_factor=1, y_scale_factor=1, layer_position=1, mappable=[<matplotlib.lines.Line2D object at 0x131198890>])], mpl_ax=<Axes: title={'center': 'eigenvalues: \n1.434+0.000j'}>, colorbar=Colorbar(artist=None, discreet=False, position='right', colormap=<matplotlib.colors.LinearSegmentedColormap object at 0x125418050>, orientation='vertical', symmetric=False, log_norm=False, numeric_format=None, n_ticks=None, label_size=None, width='10%', padding=0.1, norm=None, label='', mappable=None)), Axis(row=0, col=2, x_label=None, y_label=None, title='eigenvalues: \n1.421+0.000j', show_grid=True, show_legend=False, legend_position='best', x_scale='linear', y_scale='linear', x_limits=None, y_limits=None, equal_limits=False, projection=None, font_size=16, tick_size=14, y_tick_position='left', x_tick_position='bottom', show_ticks=True, show_colorbar=None, legend_font_size=14, line_width=None, line_style=None, x_scale_factor=None, y_scale_factor=None, aspect_ratio='auto', _artist_list=[Line(y=array([ 1.57792126e-17,  2.50818775e-17, -6.34053985e-18, -1.64437963e-18,
           -1.22068696e-17,  1.69454497e-17, -3.55826519e-17,  7.69336566e-18,
           -5.57636392e-18, -3.23154773e-18,  1.41571604e-17,  2.34829806e-18,
            6.76286676e-17, -1.45457229e-17,  6.01659711e-18, -2.19796722e-18,
            3.52022056e-18,  1.91961409e-17, -1.54809628e-17,  1.90815296e-18,
           -2.16192949e-17, -2.22433811e-18, -3.25853461e-19,  1.93729956e-18,
           -1.03786440e-17,  1.21890563e-17, -1.57149788e-17,  1.23983626e-17,
           -3.15695587e-17, -1.87711085e-17, -1.61328791e-17,  1.71093997e-17,
            4.17673224e-17,  1.72394624e-17, -1.08485944e-18, -3.49008444e-18,
            5.58672049e-18,  4.92306701e-18, -6.38196920e-18, -2.53888061e-18,
            2.81254807e-18,  2.51318416e-17, -6.14994674e-18, -5.66496813e-18,
            7.53730486e-18,  1.13951926e-17, -1.53872490e-17,  2.65399764e-17,
            3.94884395e-17,  1.79799644e-17,  1.70103082e-17, -7.09128930e-18,
            2.12703269e-18, -6.29485000e-18, -1.18338005e-17, -7.48422258e-18,
            3.54626207e-18, -5.78143943e-18, -2.33919699e-17, -5.16766901e-18,
            2.20190819e-17, -2.65293547e-17,  7.40201176e-18,  2.98352343e-17,
           -5.60099221e-18,  1.95479380e-17,  3.51384998e-18, -3.60456559e-17,
            1.15317770e-18, -2.78989984e-17, -1.81179286e-17,  1.79416668e-17,
            4.07294814e-17,  4.61502081e-18,  2.67747210e-18,  5.56051252e-18,
           -1.70982306e-17, -2.53038398e-17,  6.99412501e-18, -1.71772759e-17,
           -2.78301513e-17, -2.60591156e-17, -5.86298663e-18, -9.95308790e-18,
           -2.23250425e-17,  2.82216600e-18, -5.19352295e-18, -7.06415401e-17,
           -1.38310244e-16, -2.38930770e-16, -4.86878606e-16, -8.89648859e-16,
           -1.73186550e-15, -3.24742962e-15, -6.23131882e-15, -1.19155713e-14,
           -2.28106998e-14, -4.36275825e-14, -8.35657308e-14, -1.59828538e-13,
           -3.05874350e-13, -5.85308194e-13, -1.12005959e-12, -2.14339710e-12,
           -4.10171272e-12, -7.84923966e-12, -1.50205581e-11, -2.87439514e-11,
           -5.50055857e-11, -1.05260904e-10, -2.01431600e-10, -3.85467778e-10,
           -7.37646978e-10, -1.41159160e-09, -2.70127978e-09, -5.16927993e-09,
           -9.89214662e-09, -1.89300185e-08, -3.62252615e-08, -6.93221496e-08,
           -1.32657715e-07, -2.53859258e-07, -4.85795512e-07, -9.29638262e-07,
           -1.77899400e-06, -3.40435604e-06, -6.51471568e-06, -1.24668277e-05,
           -2.38570341e-05, -4.56538012e-05, -8.73649908e-05, -1.67185240e-04,
           -3.19932564e-04, -6.12236072e-04, -1.17159805e-03, -2.24199924e-03,
           -4.29039348e-03, -8.21240652e-03, -1.57377544e-02, -3.01333363e-02,
           -5.55035233e-02, -8.07379273e-02, -1.04121367e-01, -1.25092151e-01,
           -1.43174205e-01, -1.57951148e-01, -1.69081896e-01, -1.76309500e-01,
           -1.79467112e-01, -1.78481842e-01, -1.73376433e-01, -1.64268742e-01,
           -1.51369012e-01, -1.34975027e-01, -1.15465230e-01, -9.32899930e-02,
           -6.89612165e-02, -4.30405149e-02, -1.61262507e-02,  1.11602775e-02,
            3.81891780e-02,  6.43365059e-02,  8.89986671e-02,  1.11606351e-01,
            1.31637675e-01,  1.48630228e-01,  1.62191748e-01,  1.72009176e-01,
            1.77855884e-01,  1.79596903e-01,  1.77192043e-01,  1.70696819e-01,
            1.60261170e-01,  1.46125995e-01,  1.28617595e-01,  1.08140141e-01,
            8.51663422e-02,  6.02265330e-02,  3.38964331e-02,  6.78385596e-03,
           -2.04853221e-02, -4.72816098e-02, -7.29864320e-02, -9.70064095e-02,
           -1.18787057e-01, -1.37825581e-01, -1.53682491e-01, -1.65991740e-01,
           -1.74469177e-01, -1.78919105e-01, -1.79238801e-01, -1.75420885e-01,
           -1.67553491e-01, -1.55818233e-01, -1.40486014e-01, -1.21910779e-01,
           -1.00521242e-01, -7.68088928e-02, -5.13045076e-02, -2.46572912e-02]), x=array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
            13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,
            26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,
            39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
            52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,
            65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,
            78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,
           104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
           117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
           130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
           143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
           156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
           169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181,
           182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194,
           195, 196, 197, 198, 199]), label='', color=None, line_style='-', line_width=1, x_scale_factor=1, y_scale_factor=1, layer_position=1, mappable=[<matplotlib.lines.Line2D object at 0x13111e590>])], mpl_ax=<Axes: title={'center': 'eigenvalues: \n1.421+0.000j'}>, colorbar=Colorbar(artist=None, discreet=False, position='right', colormap=<matplotlib.colors.LinearSegmentedColormap object at 0x125418050>, orientation='vertical', symmetric=False, log_norm=False, numeric_format=None, n_ticks=None, label_size=None, width='10%', padding=0.1, norm=None, label='', mappable=None)), Axis(row=0, col=3, x_label=None, y_label=None, title='eigenvalues: \n1.403+0.000j', show_grid=True, show_legend=False, legend_position='best', x_scale='linear', y_scale='linear', x_limits=None, y_limits=None, equal_limits=False, projection=None, font_size=16, tick_size=14, y_tick_position='left', x_tick_position='bottom', show_ticks=True, show_colorbar=None, legend_font_size=14, line_width=None, line_style=None, x_scale_factor=None, y_scale_factor=None, aspect_ratio='auto', _artist_list=[Line(y=array([-4.35309042e-17, -5.94939258e-19, -5.98641394e-18,  6.84180576e-18,
            2.54273414e-18,  2.73440828e-17, -3.46675400e-18,  8.56572796e-18,
           -2.18215101e-17, -5.52266374e-17, -4.95245184e-17, -6.38462460e-17,
           -1.06914718e-17, -4.08163881e-18, -2.75579795e-18, -1.33214916e-17,
           -1.57015205e-17, -1.44594648e-17,  1.07636294e-17,  8.02282796e-18,
           -1.65884260e-17,  1.07439910e-17,  2.02505401e-17,  1.51819088e-17,
           -2.17888626e-17,  1.99316974e-17, -8.54726000e-18,  9.14531044e-17,
            2.37868154e-17,  2.09129574e-17,  6.92234546e-18, -8.44022166e-18,
           -5.68213920e-17, -4.81377120e-17, -4.48751528e-17, -4.43227117e-17,
           -2.49771895e-17, -2.06435451e-17,  1.24323433e-17,  7.58004226e-18,
           -1.43080553e-17,  1.76493106e-18, -6.61617209e-20, -1.84744645e-18,
           -1.72601587e-17, -1.95126134e-17, -3.88862744e-17, -2.82567482e-17,
           -7.90512721e-17, -9.78932653e-17, -4.47871791e-17, -3.38307413e-17,
           -1.48327580e-18,  2.86500915e-17,  4.62891394e-17,  3.35214851e-17,
            2.36925964e-17,  3.86287573e-17, -5.42753043e-18, -5.99241326e-18,
            2.84552992e-17, -4.38969452e-17, -3.28874359e-19, -1.58814439e-17,
           -4.30015636e-17, -7.26305943e-18,  2.33361037e-17, -2.08668003e-17,
            5.11425326e-17,  2.43100139e-17,  2.68187698e-17,  2.32935660e-18,
           -3.43360766e-17, -4.80215769e-17, -2.32583683e-17,  1.81889230e-17,
            3.41123410e-17,  2.70497462e-17,  4.43136540e-17,  1.14428046e-17,
            3.53888107e-17,  3.08199373e-17,  4.06218001e-17,  8.04063762e-17,
            6.87161505e-17,  6.39614511e-17,  6.05394879e-17,  1.75972700e-16,
            3.67035569e-16,  6.81534009e-16,  1.26799472e-15,  2.37037080e-15,
            4.41573636e-15,  8.30879567e-15,  1.56751663e-14,  2.95759608e-14,
            5.57928230e-14,  1.05310142e-13,  1.98690336e-13,  3.74937086e-13,
            7.07475579e-13,  1.33502667e-12,  2.51925999e-12,  4.75395944e-12,
            8.97100592e-12,  1.69287354e-11,  3.19453424e-11,  6.02824160e-11,
            1.13755950e-10,  2.14663333e-10,  4.05080728e-10,  7.64408192e-10,
            1.44247766e-09,  2.72202960e-09,  5.13660994e-09,  9.69304751e-09,
            1.82912797e-08,  3.45165867e-08,  6.51345765e-08,  1.22912300e-07,
            2.31941839e-07,  4.37686193e-07,  8.25936383e-07,  1.55858449e-06,
            2.94112918e-06,  5.55006221e-06,  1.04732532e-05,  1.97635680e-05,
            3.72948706e-05,  7.03773412e-05,  1.32805667e-04,  2.50611134e-04,
            4.72916136e-04,  8.92417052e-04,  1.68403421e-03,  3.17783450e-03,
            5.99675430e-03,  1.13189972e-02,  2.13886175e-02,  4.03824088e-02,
            7.33489558e-02,  1.04843808e-01,  1.32061098e-01,  1.53856472e-01,
            1.69347799e-01,  1.77901863e-01,  1.79168299e-01,  1.73095221e-01,
            1.59931406e-01,  1.40216102e-01,  1.14756934e-01,  8.45968210e-02,
            5.09712527e-02,  1.52576792e-02, -2.10809154e-02, -5.65559437e-02,
           -8.97141935e-02, -1.19197358e-01, -1.43797678e-01, -1.62507418e-01,
           -1.74560143e-01, -1.79462123e-01, -1.77012550e-01, -1.67311771e-01,
           -1.50757170e-01, -1.28026897e-01, -1.00052083e-01, -6.79786994e-02,
           -3.31206109e-02,  3.09424238e-03,  3.91823420e-02,  7.36653618e-02,
            1.05130727e-01,  1.32289478e-01,  1.54029074e-01,  1.69458967e-01,
            1.77947080e-01,  1.79145704e-01,  1.73005737e-01,  1.59778699e-01,
            1.40006429e-01,  1.14498883e-01,  8.43009631e-02,  5.06497075e-02,
            1.49236187e-02, -2.14138067e-02, -5.68740291e-02, -9.00044428e-02,
           -1.19447881e-01, -1.43998213e-01, -1.62649749e-01, -1.74638441e-01,
           -1.79473180e-01, -1.76955913e-01, -1.67189762e-01, -1.50574807e-01,
           -1.27791554e-01, -9.97702910e-02, -6.76368952e-02, -3.27884598e-02]), x=array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
            13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,
            26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,
            39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
            52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,
            65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,
            78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,
           104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
           117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
           130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
           143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
           156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
           169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181,
           182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194,
           195, 196, 197, 198, 199]), label='', color=None, line_style='-', line_width=1, x_scale_factor=1, y_scale_factor=1, layer_position=1, mappable=[<matplotlib.lines.Line2D object at 0x130f86910>])], mpl_ax=<Axes: title={'center': 'eigenvalues: \n1.403+0.000j'}>, colorbar=Colorbar(artist=None, discreet=False, position='right', colormap=<matplotlib.colors.LinearSegmentedColormap object at 0x125418050>, orientation='vertical', symmetric=False, log_norm=False, numeric_format=None, n_ticks=None, label_size=None, width='10%', padding=0.1, norm=None, label='', mappable=None))], _mpl_figure=<Figure size 1200x300 with 4 Axes>, mpl_axis_generated=False, axis_generated=True, ax_orientation='horizontal')




.. rst-class:: sphx-glr-timing

   **Total running time of the script:** (0 minutes 0.393 seconds)


.. _sphx_glr_download_gallery_eigenmodes_1d_plot_mode_3.py:

.. only:: html

  .. container:: sphx-glr-footer sphx-glr-footer-example




    .. container:: sphx-glr-download sphx-glr-download-python

      :download:`Download Python source code: plot_mode_3.py <plot_mode_3.py>`

    .. container:: sphx-glr-download sphx-glr-download-jupyter

      :download:`Download Jupyter notebook: plot_mode_3.ipynb <plot_mode_3.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
