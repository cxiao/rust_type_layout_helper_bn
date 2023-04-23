# Binary Ninja Rust Type Layout Helper Plugin 🦀

An extremely experimental Binary Ninja importer for the type layout information emitted by the [`-Zprint-type-sizes` flag](https://nnethercote.github.io/perf-book/type-sizes.html) of the Rust compiler.

This plugin is meant to help reverse engineers with the following:
- Getting a sense of how, in general, Rust data structures are laid out in memory.
- Getting more comfortable with certain core data structures which appear in Rust binaries.

![A screenshot of Binary Ninja's Types view in the sidebar, showing the imported definitions and layouts of several Rust types from `std::sys::windows`.](images/std-sys-windows-types-border.png)

## How to use this plugin

Compile some Rust code with the following options:

MacOS / Linux:

```sh
RUSTFLAGS=-Zprint-type-sizes cargo +nightly build -j 1 > type-sizes.txt
```

Windows (Powershell):

```powershell
$env:RUSTFLAGS="-Zprint-type-sizes"; cargo +nightly build -j 1 > type-sizes.txt
```

The following options are all necessary for this to work:
- `-Zprint-type-sizes` in the `RUSTFLAGS` passed to rustc.
- `+nightly` passed to cargo, as the `print-type-sizes` flag is only supported on nightly toolchain builds.
- `-j 1` to avoid shuffled lines in the output.

You should see output like this in the generated `type-sizes.txt` file:

```
print-type-size type: `core::num::dec2flt::decimal::Decimal`: 784 bytes, alignment: 8 bytes
print-type-size     field `.digits`: 768 bytes
print-type-size     field `.num_digits`: 8 bytes
print-type-size     field `.decimal_point`: 4 bytes
print-type-size     field `.truncated`: 1 bytes
print-type-size     end padding: 3 bytes
print-type-size type: `std::result::Result<std::sys::windows::fs::ReadDir, std::io::Error>`: 616 bytes, alignment: 8 bytes
print-type-size     variant `Ok`: 616 bytes
print-type-size         field `.0`: 616 bytes
print-type-size     variant `Err`: 8 bytes
print-type-size         field `.0`: 8 bytes
print-type-size type: `std::sys::windows::fs::ReadDir`: 616 bytes, alignment: 8 bytes
print-type-size     field `.handle`: 8 bytes
print-type-size     field `.root`: 8 bytes
print-type-size     field `.first`: 596 bytes
print-type-size     end padding: 4 bytes
print-type-size type: `std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>`: 608 bytes, alignment: 8 bytes
print-type-size     discriminant: 8 bytes
print-type-size     variant `Some`: 600 bytes
print-type-size         field `.0`: 600 bytes
print-type-size     variant `None`: 0 bytes
[...]
```

You can now use the _Plugins > Rust Type Layout Helper - Load File..._ command to import the contents of this file into Binary Ninja. The following types in Binary Ninja wil be created from the types shown in the example above:

```c
struct core::num::dec2flt::decimal::Decimal __packed
{
    char .digits[0x300];
    int64_t .num_digits;
    int32_t .decimal_point;
    char .truncated;
    char _padding[0x3];
};
struct std::result::Result<std::sys::windows::fs::ReadDir, std::io::Error> __packed
{
    union __packed
    {
        struct std::result::Result<std::sys::windows::fs::ReadDir, std::io::Error>::Ok Ok;
        struct std::result::Result<std::sys::windows::fs::ReadDir, std::io::Error>::Err Err;
    } std::result::Result<std::sys::windows::fs::ReadDir, std::io::Error>::variants;
};

struct std::result::Result<std::sys::windows::fs::ReadDir, std::io::Error>::Err __packed
{
    int64_t .0;
};

struct std::result::Result<std::sys::windows::fs::ReadDir, std::io::Error>::Ok __packed
{
    char .0[0x268];
};
struct std::sys::windows::fs::ReadDir __packed
{
    int64_t .handle;
    int64_t .root;
    char .first[0x254];
    int32_t _padding;
};
struct std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>> __packed
{
    enum std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::discriminant discriminant;
    union __packed
    {
        struct std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::Some Some;
        struct std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::None None;
    } std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::variants;
};

struct std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::None __packed
{
};

struct std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::Some __packed
{
    char .0[0x258];
};

enum std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::discriminant : uint64_t
{
};
```

## Caveats and future work

There are some caveats to using this:
- The layout of data types is not stable, and can change between compilations!
- Only the nightly builds of rustc supports the `print-type-sizes` flag.
- Binary Ninja's support for working with unions in the decompilation is currently quite poor (see [Vector35/binaryninja-api#1013](https://github.com/Vector35/binaryninja-api/issues/1013), [Vector35/binaryninja-api#4218](https://github.com/Vector35/binaryninja-api/issues/4218)). This may make it difficult to work with the generated `variants` unions, such as `std::option::Option<std::result::Result<std::fs::DirEntry, std::io::Error>>::variants` in the example above.

In the future it would be nice to:
- Add scripts / plugins to import the type information into IDA and Ghidra.
- Use a Rust compiler plugin to emit better type information than we get from `-Zprint-type-sizes`? Maybe a combination of the information we get from `-Zprint-type-sizes` and `#[rustc_layout(...)]`. It would also be nice to emit the type information in a format which is slightly easier to parse (e.g. JSON).

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

## Acknowledgements and resources

The compilation instructions for emitting type information are taken from the instructions in the [`top-type-sizes` crate, by Paul Loyd](https://github.com/loyd/top-type-sizes).