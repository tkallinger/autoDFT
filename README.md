# autoDFT

autoDFT needs UltraNest installed. Follow the instructions on https://johannesbuchner.github.io/UltraNest/index.html

run autoDFT

```
from autoDFT import autoDFT
autoDFT(filename, frange, <iter_max, df_factor, snr_box, write_res, plots, path='',os, write_spec>)
```
| Parameter | Description |
| --- | --- |
|```<filename>```| file that contains the timeseries. Currently, a 3-column format is required with x, y, y_err. If a different format should be used, adopt the function read_ts()|
|```frange=[f_min, f_max]```| frequency range (in units of 1/x) that is considered in the analysis|
|```iter_max```| number of prewithening steps (default=10)|
|```os```| oversampling factor for computation of the Fourier amplitude spectra (default=5)|
|```snr_box```| Frequency box size in which the local Fourier noise around found frequency is computed (default=2)|
|```df_factor```| sets the frequency parameter limits for the UltraNest fits. In units of formal frequency resolution, 1/T (default=3)|
|```write_spec```| write Fourier amplitude spectrum for each prewithening step (default=False)|
|```write_res```| write residual time series after iter_max steps (default=False)|
|```plots```| create standard UltraNEst plots for each prewithening step (default=False)|
|```path```| path to folder in which all input and output is located (default='')|

The main output of autoDFT is a list of all found frequencies ```<filename>.flist```

```
file: <filename>
frange: <f_min> - <f_max> 
phase 0 at: <x_phase=0>
local SNR: +/-<snr_box>

     f                 f_err             a               a_err            p               p_err           ev              globalSNR       localSNR
--------------------------------------------------------------------------------------------------------------------------------------------------
       0.446666        0.000019          1.2392          0.0026           0.308           0.000           1.000           17.93           13.78
```

```phase 0 at``` gives the point in time at which the phase of all fitted frequencies is 0. Currently it is set to the centre of the time series. ```f```, ```a```, and ```p``` are the frequency, amplitude, and phase of the individual fitted frequencies with their corresponding 1-sigma uncertainties (```_err```). ```ev``` is the Bayesian evidence that a peak is real, i.e. not due to noise. ```globalSNR``` and ```localSNR``` are the signal to noise ratios of a given peak with respect to the full considered frequency range (```frange```) and locally around (```snr_box```) the peak. 
