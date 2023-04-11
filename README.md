# Rust Type Layout Helper

## Development

To set up a development environment:

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pip install -r dev-requirements.txt
python $PATH_TO_BINARY_NINJA_INSTALLATION/scripts/install_api.py
```

For formatting and linting (optional), install [Nox](https://nox.thea.codes/en/stable/tutorial.html), then:

```
nox -s format
nox -s lint
```

To test the plugin, create a symbolic link between your development folder, and the [Binary Ninja user plugins folder](https://docs.binary.ninja/guide/index.html#user-folder), so that your development folder is loaded by Binary Ninja on startup as a plugin.

- MacOS:

    ```sh
    ln -s --relative . ~/Library/Application\ Support/Binary\ Ninja/plugins/rust_type_layout_helper
    ```

- Linux:

    ```sh
    ln -s --relative . ~/.binaryninja/plugins/rust_type_layout_helper
    ```

- Windows (Powershell):
    ```powershell
    New-Item -ItemType Junction -Value . -Path "$env:APPDATA\Binary Ninja\plugins\rust_type_layout_helper"
    ```