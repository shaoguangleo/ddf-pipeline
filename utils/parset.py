from getcpus import getcpus

option_list = ( ( 'machine', 'NCPU_DDF', int, getcpus(),
                  'Number of CPUS to use for DDF'),
                ( 'machine', 'NCPU_killms', int, getcpus(),
                  'Number of CPUS to use for KillMS' ),
                ( 'data', 'mslist', str, None,
                  'Initial measurement set list to use -- must be specified' ),
                ( 'data', 'full_mslist', str, None,
                  'Full-bandwidth measurement set to use for final step, if any' ),
                ( 'data', 'colname', str, 'CORRECTED_DATA', 'MS column to use' ),
                ( 'solutions', 'ndir', int, 45, 'Number of directions' ),
                ( 'solutions', 'SolsDir', str, "SOLSDIR", 'Directory for solutions' ),
                ( 'solutions', 'NChanSols', int, 1, 'NChanSols for killMS' ),
                ( 'solutions', 'NChanSols_di', int, 2, 'NChanSols for DI killMS' ),
                ( 'solutions', 'dt_slow', float, 1., 'Time interval for killMS (minutes)' ),
                ( 'solutions', 'dt_di', float, 0.5, 'Time interval for DI killMS (minutes)' ),
                ( 'solutions', 'dt_fast', float, 0.5, 'Time interval for full-bandwidth killMS (minutes)' ),
                ( 'solutions', 'LambdaKF', float, 0.5, 'Kalman filter lambda for killMS' ),
                ( 'solutions', 'NIterKF', list, [1, 6, 6], 'Kalman filter iterations for killMS for the three self-cal steps' ),
                ( 'solutions', 'PowerSmooth', float, 0.0, 'Underweighting factor for missing baseliness in killMS'),
                ( 'solutions', 'normalize', list, ['BLBased', 'BLBased', 'SumBLBased'], 'How to normalize solutions for the three self-cal steps' ),
                ( 'solutions', 'uvmin', float, None, 'Minimum baseline length to use in self-calibration (km)' ),
                ( 'solutions', 'wtuv', float, None, 'Factor to apply to fitting weights of data below uvmin. None implies, effectively, zero.'),
                ( 'solutions', 'robust', float, None, 'Briggs robustness to use in killMS. If None, natural weighting is used.'),
                ( 'solutions', 'smoothing', int, None, 'Smoothing interval for amplitudes, in units of dt. Must be odd.'),
                ( 'image', 'imsize', int, 20000, 'Image size in pixels' ),
                ( 'image', 'cellsize', float, 1.5, 'Pixel size in arcsec' ),
                ( 'image', 'robust', float, -0.15, 'Imaging robustness' ),
                ( 'image', 'final_robust', float, -0.5, 'Final imaging robustness' ),
                ( 'image', 'psf_arcsec', float, 12.0, 'Force restore with this PSF size in arcsec if set, otherwise use default' ),
                ( 'image', 'final_psf_arcsec', float, 6.0, 'Final image restored with this PSF size in arcsec' ),
                ( 'image', 'final_psf_minor_arcsec', float, None, 'Final image restored with this PSF minor axis in arcsec' ),
                ( 'image', 'final_psf_pa_deg', float, None, 'Final image restored with PSF with this PA in degrees' ),
                ( 'image', 'final_rmsfactor', float, 1.0, 'Final image RMS factor for cleaning' ),
                ( 'image', 'low_psf_arcsec', float, None, 'Low-resolution restoring beam in arcsec. If None, no image will be made.' ),
                ( 'image', 'low_robust', float, -0.20, 'Low-resolution image robustness' ),
                ( 'image', 'low_cell', float, 4.5, 'Low-resolution image pixel size in arcsec' ),
                ( 'image', 'low_imsize', int, None, 'Low-resolution image size in pixels' ),
                ( 'image', 'do_decorr', bool, True, 'Use DDF\'s decorrelation mode' ),
                ( 'image', 'HMPsize', int, 10, 'Island size to use HMP initialization' ),
                ( 'image', 'uvmin', float, 0.1, 'Minimum baseline length to use in imaging (km)'),
                ( 'image', 'uvmax', float, 1000.0, 'Maximum baseline length to use in imaging (km)'),
                ( 'image', 'apply_weights', list, [False, True, True, True], 'Use IMAGING_WEIGHT column from killms'),
                ( 'image', 'clusterfile', str, None, 'User-defined cluster file to use'),
                ( 'masking', 'thresholds', list, [15,10,10,5],
                  'sigmas to use in (auto)masking for initial clean and 3 self-cals'),
                ( 'masking', 'tgss', str, None, 'Path to TGSS catalogue file' ),
                ( 'masking', 'tgss_radius', float, 8.0, 'TGSS mask radius in pixels' ), 
                ( 'masking', 'tgss_flux', float, 300, 'Use TGSS components with peak flux in catalogue units (mJy) above this value' ),
                ( 'masking', 'tgss_extended', bool, False, 'Make extended regions for non-pointlike TGSS sources' ),
                ( 'masking', 'tgss_pointlike', float, 30, 'TGSS source considered pointlike if below this size in arcsec' ),
                ( 'masking', 'region', str, None, 'ds9 region to merge with mask'),
                ( 'masking', 'extended_size', int, None,
                  'If generating a mask from the bootstrap low-res images, use islands larger than this size in pixels' ),
                ( 'masking', 'extended_rms', float, 3.0,
                  'Threshold value defining an island in the extended mask'),
                ( 'masking', 'rmsfacet', bool, False, 'If True calculate one rms per facet rather than per image when making the extended rms maps' ),  
                ( 'control', 'quiet', bool, False, 'If True, do not log to screen' ),
                ( 'control', 'nobar', bool, False, 'If True, do not print progress bars' ),
                ( 'control', 'logging', str, 'logs', 'Name of directory to save logs to, or \'None\' for no logging' ),
                ( 'control', 'dryrun', bool, False, 'If True, don\'t run anything, just print what would be run' ),
                ( 'control', 'restart', bool, True, 'If True, skip steps that would re-generate existing files' ),
                ( 'control', 'cache_dir', str, None, 'Directory for ddf cache files -- default is working directory'),
                ( 'control', 'clearcache', bool, True, 'If True, clear all DDF cache before running' ),
                ( 'control', 'clearcache_end', bool, True, 'If True, clear all DDF cache at successful end of the pipeline' ),
                ( 'control', 'bootstrap', bool, False, 'If True, do bootstrap' ),
                ( 'control', 'catch_signal', bool, True, 'If True, catch SIGUSR1 as graceful exit signal -- stops when control returns to the pipeline.'),
                ( 'control', 'exitafter', str, None, 'Step to exit after -- dirin, dirin_di, bootstrap, phase, ampphase, fulllow'),
                ( 'control', 'redofrom', str, None, 'Step to redo from after -- start, dirin, phase, ampphase, fulllow, full'),
                ( 'control', 'archive_dir', str, 'old', 'Directory to archive to if redofrom is set'),
                ( 'control', 'msss_mode', bool, False, 'Work in "MSSS mode" where a smooth beam and spectral cube are computed in the ampphase1 step' ),
                ( 'control', 'remove_columns', bool, False, 'Remove all pipeline-generated columns before the run.' ),
                ( 'bootstrap', 'catalogues', list, None, 'File names of catalogues for doing bootstrap' ),
                ( 'bootstrap', 'groups', list, None, 'Group numbers for catalogues. At least one match must be found in each group. Optional -- if not present each catalogue is in a different group.' ), 
                ( 'bootstrap', 'frequencies', list, None, 'Frequencies for catalogues (Hz)' ), 
                ( 'bootstrap', 'names', list, None, 'Short names for catalogues' ), 
                ( 'bootstrap', 'radii', list, None, 'Crossmatch radii for catalogues (arcsec)' ),
                ( 'offsets', 'method', str, None, 'Offset correction method to use. None -- no correction'),
                ( 'offsets', 'fit', str, 'mcmc', 'Histogram fit method' ),
                ( 'offsets', 'mode', str, 'normal', 'Mode of operation: normal or test' ),
                ( 'spectra', 'do_dynspec', bool, True, 'Do dynamic spectra') )
