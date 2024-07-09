

class AnglePlotter:
    guideline_kwargs = {'color': 'grey', 'lw': .5, 'ls': '--'}
    thetaphinet_wedge_kwargs = {'color': 'C0', 'alpha': .6}

    def __init__(self, detector_pair, thetanet=1., phinet=.5,
                 z_cone=1.3):
        self.detector_pair = detector_pair
        self.thetanet = thetanet
        self.phinet = phinet
        self.z_cone = z_cone

        self.ax = None

    def __call__(self, figsize=(8, 5)):
        plt.figure()
        self.ax = plt.gca(projection='3d')

        # x, y, z axes
        for label, e_i in zip('zxy', np.eye(3)):
            plot_vector(ax, 3.35*e_i, -1.5*e_i, color='grey', lw=1)
            ax.text(*2*e_i, f'${label}$')
            
            
        # H, L detectors
        ax.scatter(np.array((-1, 1))*.8, (0, 0), (0, 0), c='k', alpha=1)

        self._plot_cone()
        self._plot_symmetric_solutions()
        self._plot_thetaphinet_wedges()

        ax.set_axis_off()
        ax.auto_scale_xyz(*[[-1, 1]]*2, [-.86, .86])  # Set aspect equal hack
        ax.view_init(28, 64)

    def _plot_symmetric_solutions(self):
        self.ax.scatter(1,
                        np.tan(self.thetanet) * np.cos(self.phinet),
                        np.tan(self.thetanet) * np.sin(self.phinet), c='C2')
        self.ax.scatter(1,
                        np.tan(self.thetanet) * np.cos(self.phinet),
                        -np.tan(self.thetanet) * np.sin(self.phinet), c='C2')
        self.ax.scatter(1,
                        -np.tan(self.thetanet) * np.cos(self.phinet),
                        np.tan(self.thetanet) * np.sin(self.phinet), c='C3')
        self.ax.scatter(1,
                        -np.tan(self.thetanet) * np.cos(self.phinet),
                        -np.tan(self.thetanet) * np.sin(self.phinet), c='C3')

    def _plot_vector(self, vec, origin=np.array([0,0,0]), **kwargs):
        self.ax.plot(*list(zip(origin, vec + origin)), **kwargs)

    def _plot_cone(self):
        znet_arr = np.linspace(0, self.z_cone, 50)
        phinet_arr = np.linspace(0, 2*np.pi, 100)
        zgrid, phigrid = np.meshgrid(znet_arr, phinet_arr, indexing='ij')
        xgrid = zgrid * np.cos(phigrid) * np.tan(self.thetanet)
        ygrid = zgrid * np.sin(phigrid) * np.tan(self.thetanet)

        # Conic surface
        ax.plot_surface(zgrid, xgrid, ygrid, color='w', alpha=.3)
        
        # Circle at edge of cone
        ax.plot(self.z_cone*np.ones_like(phinet_arr),
                np.cos(phinet_arr) * np.tan(self.thetanet),
                np.sin(phinet_arr) * np.tan(self.thetanet),
                **self.guideline_kwargs)
        
        # Horizontal line at edge of cone
        ax.plot([self.z_cone]*2,
                self.z_cone * np.tan(self.thetanet) * 1.5 * np.array([-1, 1]),
                [0]*2, **self.guideline_kwargs)

        # Vertical line at edge of cone
        ax.plot([self.z_cone]*2,
                [0]*2,
                self.z_cone * np.tan(self.thetanet) * 1.5 * np.array([-1, 1]),
                **self.guideline_kwargs)

    def _plot_thetaphinet_wedges():
        # thetanet wedge
        thetanet_wedge = Wedge((0, 0), .5, 0, np.rad2deg(self.thetanet),
                               **self.thetaphinet_wedge_kwargs)
        ax.add_patch(thetanet_wedge)
        art3d.pathpatch_2d_to_3d(thetanet_wedge, z=0, zdir="y")
        
        # thetanet line
        self.plot_vector((self.z_cone, 0, self.z_cone * np.tan(self.thetanet)),
                         **self.guideline_kwargs)

        # phinet wedge
        phinet_wedge = Wedge((0, 0), .5, 0, np.rad2deg(self.phinet),
                             **thetaphinet_wedge_kwargs)
        ax.add_patch(phinet_wedge)
        art3d.pathpatch_2d_to_3d(phinet_wedge, z=self.z_cone, zdir="x")

        # phinet line
        ax.plot((self.z_cone, self.z_cone),
                (0, self.z_cone * np.cos(self.phinet) * np.tan(self.thetanet)),
                (0, self.z_cone * np.sin(self.phinet) * np.tan(self.thetanet)),
                **self.guideline_kwargs)
