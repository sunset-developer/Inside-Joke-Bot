<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/286e9a6dcb1b472c85c0686bdd05b042)](https://app.codacy.com/manual/aidanstewart/ComediBot?utm_source=github.com&utm_medium=referral&utm_content=sunset-developer/ComediBot&utm_campaign=Badge_Grade_Dashboard)


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Comedibot</h3>

  <p align="center">
    The meme bot that's personal. 
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/sunset-developer/ComediBot/issues">Report Bug</a>
    ·
    <a href="https://github.com/sunset-developer/ComediBot/pulls">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

Comedibot is a customizable meme bot for content creators, communities, and groups of friends. 

Comedibot, unlike most meme bots, has the ability to be totally personalized to your sense of humor.

Comedibot responds to phrases or words detected in chat with a joke, meme, and even audio in ways that can be unexpected and have a very humorous result. What the bot responds too and with is up to you.

You can also tell Comedibot some stupid things your friend has said, always to remember and to bring up later when your friend denies saying something so dumb.

Comedibot is capable of being used in large servers due to administrator commands, role based permissions, and that individual users can rest assured that their jokes can't be tampered with.

So, would you rather a lame, probably unfunny, and personality free meme bot? Or do you want the next best thing to bring your friends and your community together with personalized humor and memes.

Personalized, Customized, Comedibot.


<!-- GETTING STARTED -->
## Getting Started

Comedibot is currently hosted on my servers, but if you'd like you can host it on your own!
It is recommended to use a linux server to host Comedibot.

### Prerequisites

* pip3
```sh
sudo apt-get install python3-pip
```

* mmpeg
```sh
sudo apt-get install mmpeg
```


* mysql

```sh
You must create a MySQL database and create a schema called comedibot.
```

* python 3.8

```sh
Any version below will not work.
```



### Installation

1. Clone the repo
```sh
git clone https://github.com/sunset-developer/ComediBot.git
```
2. Install pip packages
```sh
pip3 install -r requirements.txt
```

## Usage

Once installed, comedibot has a command-line interface allowing you to configure comedibot. Comedibot should be up and running if configured correctly.

* Example 
```sh
python3 app.py -pfx $ -tkn JJnKuNoiNInnU0.Z23PWK.k420jopBUIbu3-Hi_wjUWm87 -dbu root -dbp password -dbe 127.0.0.1
```

* Help
```sh
  -h, --help Show this help message and exit
  -pfx, --prefix Command prefix
  -tkn, --token Your bot token
  -dbu, --dbusername MySQL database username
  -dbp, --dbpassword MySQL database password
  -dbe, --dbendpoint MySQL database endpoint
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- CONTACT -->
## Contact

Aidan Stewart - aidanstewart@sunsetdeveloper.com

Project Link: [https://github.com/sunset-developer/ComediBot](https://github.com/sunset-developer/ComediBot)

Support Server: [https://discord.gg/wRTCcws](https://discord.gg/wRTCcws)

Discord: sunsetdev#6465



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Be the first! Submit a pull request.]()




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/sunset-developer/ComediBot.svg?style=flat-square
[contributors-url]: https://github.com/sunset-developer/ComediBot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sunset-developer/ComediBot.svg?style=flat-square
[forks-url]: https://github.com/sunset-developer/ComediBot/network/members
[stars-shield]: https://img.shields.io/github/stars/sunset-developer/ComediBot.svg?style=flat-square
[stars-url]: https://github.com/sunset-developer/ComediBot/stargazers
[issues-shield]: https://img.shields.io/github/issues/sunset-developer/ComediBot.svg?style=flat-square
[issues-url]: https://github.com/sunset-developer/ComediBot/issues
[product-screenshot]: images/screenshot.png
