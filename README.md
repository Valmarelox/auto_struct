# auto_struct
Python 3.8 module using annotations and dataclasses for easily writing parsers for binary data
- Parse packed binary data using declarative forms
- Easily validate parsed data
- Easily nest structs
- No Dependencies :)

### Usage example
See [this](examples/elf_header_parser.py)

### Contribution
Contributers are welcome!

### TODO:
- Method documentation
- Documentation
- More examples
- Tests
- Enums
  - Bit flags types
- Dynamic sized structs (e.g. `struct a{ int len; char data[] };`)
