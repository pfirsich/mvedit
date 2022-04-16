# mvedit

This is essentially a Python implementation of [pipe-rename](https://github.com/marcusbuffett/pipe-rename).

This adds the possibility of having a command in the EDITOR variable instead of a path to an executable. This makes it possible to include CLI flags.

Also it's not 🚀blazing fast and memory-safe🚀, but it also doesn't have 40 (that is the actual number) dependencies that download and compile for literally minutes (not counting a compilation error inbetween that required a `rustup update`). Of course Python is not very lightweight either, but it is installed everywhere anyways.