# Changelog

## [0.2.0](https://github.com/cxiao/rust_type_layout_helper_bn/compare/v0.1.0...v0.2.0) (2023-04-27)


### Features

* Add basic parsing of print-type-size output ([ed88c48](https://github.com/cxiao/rust_type_layout_helper_bn/commit/ed88c48bd4d19022ad416e475091ee7d03721472))
* Add basic struct and field parsing ([84494f6](https://github.com/cxiao/rust_type_layout_helper_bn/commit/84494f6bd2d2a4ea72dfee84ea79904b41432bc4))
* Add Binary Ninja plugin import stub in module __init__.py ([e15e5df](https://github.com/cxiao/rust_type_layout_helper_bn/commit/e15e5dfa84028b5616cefc423317efd0a3ddc5c5))
* Add discriminant entries to corresponding created enum type ([768b848](https://github.com/cxiao/rust_type_layout_helper_bn/commit/768b8488182c0434dc708b84738526e3779e0397))
* Add plugin action to add types from Rust type layout file ([75b99ea](https://github.com/cxiao/rust_type_layout_helper_bn/commit/75b99ea8bc088d899011d4d4a747495288b440ba))
* Add support for offset in fields ([2d440ed](https://github.com/cxiao/rust_type_layout_helper_bn/commit/2d440ed4191f4c29c30b0a1ea94a5c39f4a46904))
* Expose parsing interface ([2cc1469](https://github.com/cxiao/rust_type_layout_helper_bn/commit/2cc1469491687e8308cc6039974ddcdc2537a383))
* Make parse.py into a utility for printing parsed data ([12c6e56](https://github.com/cxiao/rust_type_layout_helper_bn/commit/12c6e563798a3c6e5ebc77f20a7f867210432e67))
* Parse into predefined dataclass types ([f006c92](https://github.com/cxiao/rust_type_layout_helper_bn/commit/f006c92049eebd26ff247bc0b8dc196b3381a446))
* Parse lists of multiple types ([da76be8](https://github.com/cxiao/rust_type_layout_helper_bn/commit/da76be848ec82af44be6e92dc35a1025e219705a))
* Parse variants ([adb2b0b](https://github.com/cxiao/rust_type_layout_helper_bn/commit/adb2b0b48271c4f420d53849c4445430079f9fe6))
* Remove redundant usage of `pyparsing.Group` ([7a1aa70](https://github.com/cxiao/rust_type_layout_helper_bn/commit/7a1aa706a8188ba8dfaea8e24317112f92d4b275))
* Support creating types containing Variant, Discriminant ([c405c33](https://github.com/cxiao/rust_type_layout_helper_bn/commit/c405c332202b7470f99b91a18ffdb625a67cb8a5))


### Bug Fixes

* Make real integers when parsing variants ([cb7223c](https://github.com/cxiao/rust_type_layout_helper_bn/commit/cb7223c0a573bad5490dba811c9e7ffd7e96ad1a))
* Only consider parsing a success if all contents of file are parsed ([94329c4](https://github.com/cxiao/rust_type_layout_helper_bn/commit/94329c4dcce0583591a43b509d9273e67c172e40))
