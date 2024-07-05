# Auto Switch Providers

## Install

Install the latest auto-switch-providers release via **pip**

```bash
pip install auto-switch-providers
```

## How to use?

To use `auto-switch-providers`, you must first import it, like the following code:

```python
from auto_switch_providers import AutoSwitchProviders

# Import path from os to get template path
from os import path

# Define config
TEMPLATE_CONFIG = {
    "custom_api_provider": {
        "http_service": {
            "params": {
                "token": ""
            }
        }
    },
}

# Init service
service = AutoSwitchProviders(
    template_dir=f"{path.dirname(__file__)}/templates",
    config=TEMPLATE_CONFIG
)

# Process
service.process({
    "custom_param": "example"
})
```

## ©️ License

- [MIT](/LICENSE)
