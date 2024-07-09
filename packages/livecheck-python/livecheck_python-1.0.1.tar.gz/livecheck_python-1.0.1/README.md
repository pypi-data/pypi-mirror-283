## Quick Start
- Install the Python package named `livecheck_python` using `pip`.

```bash
pip install livecheck_python
```
- Import and initialize LiveCheck in your code using the `Your ID` and `Access Key` shown on the `LiveCheck+` app on your phone. Any bugs (i.e., exceptions) occurring in your code will be notified to your phone with just these two lines.

```python
from livecheck_python import LiveCheck

livecheck = LiveCheck(your_id='', access_key='')
```

- Save logs to the cloud over time to track and visualize them on your phone.

```python
livecheck.log(value={'loss': loss, 'val_loss': val_loss, 'accuracy': accuracy, 'val_accuracy': val_accuracy})
```

## User Guide
#### Constructor
```python
LiveCheck (
    your_id: str,
    access_key: str,
    project_name: Optional[str] = '',
    hyperparams: Optional[dict] = None,
    notification_period: Optional[float] = 0
) -> LiveCheck
```
|||||
|---|---|---|---|
|your_id|required|string|Your email used to log in to the mobile app|
|access_key|required|string|An access key shown in your account on the mobile app|
|project_name|optional|string|Set the project name to make it easier to distinguish logs of different projects on the mobile app|
|hyperparams|optional|dictionary|Hyperparameters used to train models in the run (e.g., learning rate)|
|notification_period|optional|float|The time in seconds between two consecutive notifications pushed to your mobile. A larger number means fewer notifications.|

#### Set Project Name
```python
set_project_name (
    value: str
) -> None
```

Instead of setting `project_name` when initializing LiveCheck using the constructor function above, you can call `livecheck.set_project_name()`.

#### Set Hyperparameters
```python
set_hyperparams (
    value: dict
) -> None
```

Instead of setting `hyperparams` when initializing LiveCheck using the constructor function above, you can call `livecheck.set_hyperparams()`.

!> Currently, the following types of hyperparameters are supported: `int`, `float`, `bool`, and `str`.

#### Set Notification Period
```python
set_notification_period (
    value: float
) -> None
```

Instead of setting `notification_period` when initializing LiveCheck using the constructor function above, you can call `livecheck.set_notification_period()`.

#### Notify Exception
After initializing a LiveCheck object using the constructor function above, any exceptions occurring in your code will be automatically notified to your mobile without needing to do anything else.

#### Save Logs
```python
log (
    value: dict,
    log_id: Optional[int] = None
) -> None
```

You can call `livecheck.log()` after each event (e.g., after each epoch) you want to save logs to check on the mobile app. You can set a custom `log_id` for each function call. Otherwise, the `log_id` will start from 1 and automatically increase by 1 after each function call. The logs saved to the cloud by calling this function will be notified and updated to the mobile app on your phone. Two consecutive notifications will be at least 30 seconds apart.

!> Currently, the following types of logs are supported: `int`, `float`, `bool`, and `str`.

## Notices
- Currently, the following types of logs and hyperparameters are supported: `int`, `float`, `bool`, and `str`.
- The maximum number of runs in one day is 1000.
- The maximum number of logs per run is 1000. If a run has more than 1000 logs, it is automatically separated and saved as a new run.
- The oldest run will be automatically deleted when a new run is saved to the cloud and the number of runs exceeds 10000.
- The minimum time between two `livecheck.log()` function calls is 0.2 seconds.
- The minimum time between two consecutive notifications to the mobile app on your phone is 30 seconds.

## Citation
If you use this for your work, please cite the manuscript mentioned below in the outcomes of your work (e.g., academic papers).

```bibtex
@misc{livecheck,
  title={LiveCheck: Check Program Bugs Anywhere - Track Your Logs On-the-Go},
  author={},
  journal={arXiv},
  year={2024}
}
```

## Contact
Please feel free to contact me at tuan.t.d@ieee.org for inquiries or collaboration opportunities.