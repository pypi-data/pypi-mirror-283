# Telemetry Package for Python
TODO: setup instructions and where to look

# Configure Environment Variables
- APP_ENV = "dev"||"stage"||"prod"||"local"

## DD Trace Profiling example (optional -> default disabled)
- DD_PROFILING_ENABLED = "true"
- DD_ENV = "prod"
- DD_SERVICE = "my-service"
- DD_VERSION "1.0.0"

## Open Telemetry to datadog
> Note: These links will change and your team will have a specific link. Hardcoding the each link for traces, metrics, and logs is not recommended.

- OTEL_EXPORTER_OTLP_ENDPOINT="https://datadog-agent.svc.eogresources.com"

## Poetry
If you have never used Poetry before check out the [basic usage page](https://python-poetry.org/docs/basic-usage/). If you are using Poetry, you do not need to use pip commands nor manage a requirements.txt file. The point of the requirements.txt file in this repository is for users who do not wish to use Poetry.  

Poetry runs alongside pip and can manage virtual environments, package installation, package publishing, and more. These are some commands to help development with poetry.
- `poetry export -f requirements.txt --output requirements.txt --without-hashes`
- `poetry add <packagename>`