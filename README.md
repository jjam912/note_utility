# NoteUtil

NoteUtil is a library to turn "notes" into usable data structures. "Notes" are used in a sense here as any structured
document of information. NoteUtil identifies different parts of the document based on how you configure it and organizes
itself so that it maintains the same structure. This makes retrieving information through code as easy and simple as 
looking at the document itself. It also makes searching through loads of information more automated and effortless. 
In addition to storing information, NoteUtil also contains separate data structures that handles studying the 
information (See [Quiz](https://github.com/JJamesWWang/noteutil/RULES.md#quiz-rules), [Leitner](https://github.com/JJamesWWang/noteutil/RULES.md#leitner-rules)). 

## Getting Started

### Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the noteutil library.

```bash
python3 -m pip install noteutil
```
### Usage

NoteUtil requires a configuration file in order to work properly. Please see [RULES.md](RULES.md) for an in-depth
tutorial on writing notes that satisfy NoteUtil's note creation process and correctly completing the config file. 
A config file template can be found at [CONFIG.txt](CONFIG.txt) 

## Testing

Tests using [pytest](https://docs.pytest.org/en/latest/) are currently in development. 

## Contributing

Contact me at [JJamesWWang@gmail.com](mailto:JJamesWWang@gmail.com).

## License

This project is licensed under the [GPL 3.0 License](LICENSE)

## Acknowledgments

NoteUtil arose from the need for a better way to study for my history classes starting sophomore year;  I wish to thank
Mr. Brennan and Mr. Sima for the inspiration of this project.