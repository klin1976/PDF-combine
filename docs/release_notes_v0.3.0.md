# Release v0.3.0

This release significantly improves application startup time and refines CLI output encoding for Windows users.

## What's New & Changed
- **Performance Boost**: We now distribute the application using PyInstaller's `OneDir` layout by default instead of `OneFile`. This eliminates the lengthy decompression step on startup, reducing startup time from ~10+ seconds to just ~1-2 seconds.
- **Enhanced Encoding**: Fixed an `AttributeError` caused by `sys.stdout` being `None` in `--noconsole` mode. The standard output and error streams are now correctly configured to UTF-8 to prevent garbled Chinese characters in the Windows terminal.
- **Developer Tools**: Added `measure_windows_startup.ps1` for startup speed benchmarking, and updated `build_windows.ps1` to support different build layouts and a clean step.

## Assets
Please download the corresponding ZIP file for your needs:
- `PDF-Combine-GUI-v0.3.0-Windows.zip`: For the standard graphical user interface.
- `PDF-Combine-CLI-v0.3.0-Windows.zip`: For batch processing via the command line.
