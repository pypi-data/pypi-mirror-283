# Telemetry Package for Python
This current version only supports open telemetry exporting. There are two objects (Resource & Observer) that you will import from telempack. First fill out the parameters for the Resource object then instantiate an Observer object passing through one paramater - the Resource object. That's it.

# Configure Resource Object Parameters
- export_endpoint: str = "https://datadog-agent.svc.eogresources.com" [REQUIRED](temporary)
- app_env: str = "dev"||"stage"||"prod"||"local"[REQUIRED]
- app: Union[FastAPI, Flask] (flask not supported until version 2.0.0) [REQUIRED]
- logger_obj: logging.Logger (optional)
- is_ddprofiler_on: bool = False

## DD Trace Profiling example (optional -> default disabled) (in-testing)
- DD_PROFILING_ENABLED = "true"
- DD_ENV = "prod"
- DD_SERVICE = "my-service"
- DD_VERSION "1.0.0"

## Export to Datadog
> Note: These links will change and your team will have a specific link. Hardcoding each link for traces, metrics, and logs is not recommended.

## Poetry
If you have never used Poetry before check out the [basic usage page](https://python-poetry.org/docs/basic-usage/). If you are using Poetry, you do not need to use pip commands nor manage a requirements.txt file. The point of the requirements.txt file in this repository is for users who do not wish to use Poetry.  

Poetry runs alongside pip and can manage virtual environments, package installation, package publishing, and more. These are some commands to help development with poetry.
- `poetry export -f requirements.txt --output requirements.txt --without-hashes`
- `poetry add <packagename>`
- `poetry install`
- `poetry config pypi-token.pypi <pypi-...>`
- `poetry publish --build`