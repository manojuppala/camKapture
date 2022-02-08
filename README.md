# camKapture

camKapture is an open source application that allows users to access their webcam device and take pictures or create videos.

<p>
  <img src="assets/camkapture.png" alt="camKapture" width="150"/>
&nbsp; &nbsp; &nbsp; &nbsp;
  <img src="assets/camkapture1.png" alt="camKapture" width="150"/>
</p>

## Clone and Install

Clone the repository

```
git clone https://github.com/manojuppala/camKapture.git
```

Create and activate virtual env  
**Linux and Mac**

```
python3 venv -m <env_name>
source <env_name>/bin/activate
```

**Windows**

```
python3 -m venv <env_name>
.\<env_name>\Scripts\activate
```

Install dependencies

```
cd camKapture
pip install -r requirements.txt
```

Run using python3

```
python3 camKapture.py
```

## Features

- Cross-platform (GNU/Linux, Mac, Windows)
- Take pictures and record videos with the webcam.
- Keyboard based application
- Written in Python and OpenCV.
- Burst mode to capture multiple images.
- Timer mode to capture image after 10 secs

## Usage

`s` - capture image  
`v` - start recording video  
`b` - enable burst mode  
`t` - enable timer mode  
`f` - enable full screen mode  
`e` - enable effects screen mode or selct effect  
`Shift`+`]` - next effect in effects mode  
`Shift`+`[` - previous effect in effects mode  
`Backspace` - return from any mode  
`Space` - pause and unpause video capture  
`Esc` - quit

## License

```
camKapture is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

camKapture is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with camKapture. If not, see <http://www.gnu.org/licenses/>.
```

[![License](https://www.gnu.org/graphics/gplv3-with-text-136x68.png)](https://github.com/manojuppala/camKapture/blob/main/LICENSE)
