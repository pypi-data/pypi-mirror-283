# amzn_jupyter_idle:

This package includes the JupyterLab extension built by Maxdome/Sagemaker team for checking last activity time comparing sessions and terminals. 

## Requirements
* Jupyter-server > 2.0.0
* tornado

## Installing the extension
To install the extension within local Jupyter environment, a Docker image/container or in SageMaker Studio, run:
```
pip install amzn_jupyter_idle-<version>-py3-none-any.whl`
```

## Uninstalling the extension
To uninstall this extension, run:
```
pip uninstall amzn_jupyter_idle`
```

## Troubleshooting
If you are unable to connect to the /api/idle endpoint, check that the server extension is enabled:

```
jupyter serverextension list
```

## See DEVELOPING.md for more instructions on dev setup and contributing guidelines
