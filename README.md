# autoDFT

autoDFT needs UltraNest installed. Follow the instructions on https://johannesbuchner.github.io/UltraNest/index.html

run autoDFT

```
from autoDFT import autoDFT
autoDFT(<filename>,frange=[f_min,f_max],iter_max=int, write_res=True/False, plots=True/False)
```
Input:
```<filename>``` ... file that contains the timeseries. Currently, a 3-column format is required with x, y, y_err. If a different format should be used, adopt the function read_ts()
