# auto_struct
Python 3.8 module using annotations and dataclasses for easily writing parsers for binary data
- Parse packed binary data using declarative forms
- Easily validate parsed data
- Easily nest structs
- No Dependencies :)

### Usage example
See [this](https://github.com/Valmarelox/auto_struct/blob/master/examples/elf_header_parser.py)

### Contribution
Contributors are welcome!

### TODO:
- Method documentation (WIP)
- Documentation (WIP)
- More examples
- Tests
- Intermediate types/Binding two types - (E.g. in memory type vs how should it be used)
    - API Should probably be some `def twin(self)`?
    - 
- Dynamic sized structs (e.g. `struct a{ int len; char data[] };`)
