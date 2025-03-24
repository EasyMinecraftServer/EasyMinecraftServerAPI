<br/>
<div align="center">
<a href="https://github.com/ShaanCoding/ReadME-Generator">
<img src="https://minecraft.wiki/images/Crafter_JE4_BE3.png?3996e&format=original" alt="Logo" width="80" height="80">
</a>
<h3 align="center">EasyMinecraftServerAPI</h3>
<p align="center">
A FastAPI application to download JAR files
<br/>
<br/>
<!-- <a href="https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/wiki"><strong>Explore the docs »</strong></a> -->
<br/>
<br/>
<a href="https://api.nucceteere.xyz">View Demo</a>  
<a href="https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/issues/new">Report Bug</a>
<a href="https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/issues/new">Request Feature</a>
</p>
</div>

## About The Project

![EasyMinecraftServer's configure command being used to create a settings file in the users home directory](https://cdn.nucc.tr/assets/emc-demo.png)

This is a simple project that lets you create Minecraft Server with ease. This API handles the serving of JARs and configuration files. It is being used for EasyMinecraftServer and you can use it in your own projects as long as you notify me of such usage.

### Built With

- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- Poetry (Linux)
  ```sh
  curl -sSL https://install.python-poetry.org | python3 -
  ```
- Poetry (Windows)
  ```sh
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
  ```

### Installation

1. Clone the repo

   ```sh
   git clone https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServer.git
   ```

2. Activate Virtual Enviroment

   Bash / Zsh / Csh

   ```sh
   eval $(poetry env activate)
   ```

   Fish

   ```sh
   eval (poetry env activate)
   ```

3. Install dependencies

   ```sh
   poetry install
   ```

4. Run the web server
   ```sh
   fastapi run
   ```

## Roadmap

See the [open issues](https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/issues) for a full list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

All commits must follow the Conventional Commits specification and any version bumps must follow the SemVer specification

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the AGPLv3 License. See [AGPLv3 License](https://www.gnu.org/licenses/agpl-3.0.en.html) for more information.

## Contact

Rüzgar Engür - [@nucceteere.xyz](https://bsky.app/profile/nucceteere.xyz) - ruzgar@nucceteere.xyz

Project Link: [Funtimes909 Git](https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI)

## Acknowledgments

- [makeread.me by ShaanCoding](https://github.com/ShaanCoding/ReadME-Generator)
- [NodeJS Minecraft Versions by Nixinova](https://github.com/Nixinova/Minecraft-Versions)
- setup.md - [Docs](https://www.setup.md/docs) - [API](https://www.setup.md/services#server-jar-api)
- [Minecraft Server Software by LeStegii](https://github.com/LeStegii/server-software)
