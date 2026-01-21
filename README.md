# PyPomodoro

## Features

- Pomodoro cycles with short and long breaks.
- Configurable durations, theme, and language (Portuguese and English).
- System notifications and default alert sound (`wood.mp3`).
- Native desktop UI.

## Build executables (Windows and macOS)

### 1) Prepare the environment

- Create and activate a virtual environment (optional, recommended).
- Install project dependencies:

```
pip install -r requirements.txt
```

### 2) Build the package

Use the preconfigured spec file:

```
pyinstaller pypomodoro.spec
```

### 3) Where the generated files are

- Windows: `dist/PyPomodoroWin/PyPomodoroWin.exe`
- macOS: `dist/PyPomodoroMac.app`

### Important notes

- Build the executable on each operating system. You cannot generate a `.app` on Windows or a `.exe` on macOS.
- If a dependency is missing, install it with `pip` and run again.
- The Windows executable icon uses `src/tomato.ico`. For macOS, use a `.icns` icon.

## License

MIT License

Copyright (c) 2026 PyPomodoro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
