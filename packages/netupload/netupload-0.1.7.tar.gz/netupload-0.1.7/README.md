# netupload

<br>
<a href="https://pypi.org/project/netupload/">
    <img src="https://img.shields.io/pypi/v/netupload" alt="PyPI - Version">
</a>
<a href="https://github.com/zpg6/netupload">
    <img src="https://img.shields.io/pypi/l/netupload" alt="PyPI - License">
</a>
<a href="https://github.com/zpg6/netupload">
    <img src="https://img.shields.io/badge/github-zpg6/netupload-black" alt="GitHub Repo">
</a>
<br><br>

Simple file upload server for when you need to send files around on your local network.
Sometimes you don't want to login to your email and don't have a USB so this can be a quick way to transfer files.

![How it works](https://github.com/zpg6/netupload/raw/main/docs/how_it_works.png)

## Usage

```
pip install netupload
```

```
netupload
```

![Webpage Screenshot](https://github.com/zpg6/netupload/raw/main/docs/webpage_screenshot.png)

## Options

```
netupload --host=0.0.0.0 --port=4000 --save-dir=./uploads
```

| Option     | Description                      | Default   |
| ---------- | -------------------------------- | --------- |
| --host     | Host to run the server on        | 0.0.0.0   |
| --port     | Port to run the server on        | 4000      |
| --save-dir | Directory to save uploaded files | ./uploads |
