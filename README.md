# autoDFT

autoDFT needs UltraNest installed. Follow the instructions on https://johannesbuchner.github.io/UltraNest/index.html

run autoDFT

```
from autoDFT import autoDFT
autoDFT(filename, frange, iter_max, df_factor=3, snr_box=2, write_res=False, plots=False, path='',os=5, write_spec=False):
```
Input:
| Parameter | Description |
| --- | --- |
|```<filename>```| file that contains the timeseries. Currently, a 3-column format is required with x, y, y_err. If a different format should be used, adopt the function read_ts()|
|```frange=[f_min, f_max]```| frequency range (in units of 1/x) that is considered in the analysis|
|```iter_max```| number of prewithening steps (default=10)|
|```write_res```| write residual time series after iter_max steps (default=False)|
|```plots```| create standard UltraNEst plots for each prewithening step (default=False)|
|```os```| oversampling factor for computation of the Fourier amplitude spectra (default=5)|
|```snr_box```| Frequency box size in which the local Fourier noise around found frequency is computed (default=2)|
|```write_spec```| write Fourier amplitude spectrum for each prewithening step (default=False)|
|```path```| path to folder in which all input and output is located (default='')|
