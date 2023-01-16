# autoDFT

autoDFT needs UltraNest installed. Follow the instructions on https://johannesbuchner.github.io/UltraNest/index.html

run autoDFT

```
from autoDFT import autoDFT
autoDFT(filename, frange, <iter_max, df_factor, snr_box, write_res, plots, path='',os, write_spec>)
```
Input:
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

Output:
The main output of autoDFT is a list of the found frequencies ```<filename>.flist```
