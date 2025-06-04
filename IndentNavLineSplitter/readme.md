## When upgrading python version or adjusting build settings

In Visual Studio 2022 go to Solution explorer, then right click on the project and click settings. Then:

* c/C++ > General > Additional Include Directories
    * `C:\Python311-32\include`
* Linker > General > Additional Library Directories
    * `C:\Python311-32\libs`
* Linker > Input > Additional dependencies
    * `python311.lib`
    