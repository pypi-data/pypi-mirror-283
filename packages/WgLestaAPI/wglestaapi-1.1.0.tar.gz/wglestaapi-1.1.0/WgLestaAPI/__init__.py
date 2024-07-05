"""
# WgLestaAPI

Unofficial Python library that facilitates working with API Lesta Games and API Wargaming.net functionality via Python. 

By downloading this library you fully agree with all official documents Lesta Games and Wargaming.net about Lesta Games and Wargaming.net products. The author of the library (Alexander Podstrechny) is not responsible for your actions performed with the help of this program code.

## Installing the library

Run the command below at the command line

```powershell
pip install --upgrade WgLestaAPI
```

## Library functionality

The library implements the basic functions of API Lesta Games and API Wargaming.net. All requests are made through your application, which you previously created on [Lesta Games](https://developers.lesta.ru/applications/) or on [Wargaming.net](https://developers.wargaming.net/applications/). Some features are listed below:
- Getting information about the player, his equipment and medals.
- Obtaining information about the clan.
- Getting information about equipment, equipment mauls.
- And other methods that do not require user authorization.

## The main advantages

* The presence of synchronous and asynchronous methods of working with the API;
* The ability to use any available methods of the official API through this single library;
* The ability to run a single `*.py` program in several different regions;
* Built-in constants to designate all games and regions;
* One App class with all the necessary library methods.


## Quickstart

More examples you can find on the [GitHub](https://github.com/tankalxat34/WgLestaAPI)

### 1. Get an `application_id`
1. Choice your API provider;
2. Log in to the official API provider service;
3. Create a new application by clicking on the button **Add application** or use the existing;
4. Copy ID field from webpage;

### 2. Write a synchron variant of the "Hello world" example

```python
from WgLestaAPI.Application import App
from WgLestaAPI.Constants import REGION, GAMENAMES
import json

# init your app
wgApp = App(
    application_id = "YOUR_APPLICATION_ID",
    region = REGION.EU,
    game_shortname = GAMENAMES.SHORTNAMES.WOT
)

# make a query
data = wgApp.account.info(account_id=563982544)
# processing the response
print(json.dumps(data, indent=2))
```

## Copyright Notice

- 2024 © Alexander Podstrechnyy. 
    - [tankalxat34@gmail.com](mailto:tankalxat34@gmail.com?subject=lestagamesapi)
    - [VKontakte](https://vk.com/tankalxat34)
    - [Telegram](https://tankalxat34.t.me)
    - [GitHub](https://github.com/tankalxat34/wglestaapi)

- 2024 © Wargaming.net. All rights reserved.
    - [User Support Center](http://support.wargaming.net/)
    - [Official website](https://wargaming.net/)
    - [License Agreement](https://eu.wargaming.net/user_agreement/)
    - [Privacy Policy](https://eu.wargaming.net/privacy_policy/)
    
- 2024 © Lesta Games. All rights reserved. 
    - [User Support Center](https://lesta.ru/support/)
    - [Official website](https://lesta.ru/)
    - [License Agreement](https://developers.lesta.ru/documentation/rules/agreement/)
    - [Privacy Policy](https://legal.lesta.ru/privacy-policy/)

This program code is not a product of Lesta Games and was developed according to Lesta Games DPP rules.

This program code is not a product of Wargaming.net and is developed according to WG DPP rules.
"""

__author__ = "Alexander Podstrechnyy"
__email__ = "tankalxat34@gmail.com"
__license__ = "MIT"
__apiholders__ = ["Wargaming.net <https://wargaming.net>", "Lesta Games <https://lesta.ru>"]