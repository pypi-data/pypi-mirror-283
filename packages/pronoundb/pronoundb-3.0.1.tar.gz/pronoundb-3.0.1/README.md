# PronounDB Python API

![PyPI](https://img.shields.io/pypi/v/pronoundb?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pronoundb?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/pronoundb?style=flat-square)

API wrapper for the pronoundb.org API.

## Installation

```bash
pip install pronoundb
```

## Setup

You need to create a client to be able to use the pronoundb wrapper. Make sure to use a [descriptive user agent](https://pronoundb.org/wiki/api-docs).

```py
from pronoundb import Client

pronoundb_client = Client(user_agent="Example for Python PronounDB API Wrapper")
```

## Examples

Lookup someone's pronouns by their discord id:

```py
from pronoundb import Client, Platform

pronoundb_client = Client(user_agent="Example for Python PronounDB API Wrapper")
pronoundb_client.get_pronouns_by_platform_ids(Platform.DISCORD, 123456789012345678)
# -> {123456789012345678: ["he", "him"]}
```

Lookup someone's pronouns by their minecraft (java) uuid:

```py
from pronoundb import Client, Platform

pronoundb_client = Client(user_agent="Example for Python PronounDB API Wrapper")
pronoundb_client.get_pronouns_by_platform_ids(Platform.MINECRAFT, "12345678-1234-1234-1234-123456789012")
# -> {"12345678-1234-1234-1234-123456789012": ["they", "them"]}
```

Lookup multiple users pronouns by their discord id:

```py
from pronoundb import Client, Platform

pronoundb_client = Client(user_agent="Example for Python PronounDB API Wrapper")
pronoundb_client.get_pronouns_by_platform_ids(Platform.DISCORD, [123456789012345678, 987654321098765432])
# -> {123456789012345678: ["he", "him"], 987654321098765432: ["she", "her"]}
```

## Supported Platforms

- Discord
- GitHub
- Minecraft (Java)
- Twitch
- Twitter

## Custom Pronouns (Version 2.0.0)

Beginning with version 2.0.0, you can give the client a list of pronouns to translate them, for example.

```py
from pronoundb import Client, Platform

pronoundb_client = Client(user_agent="Example for Python PronounDB API Wrapper", pronouns={
    "unspecified": [],
    "he": ["Er", "Ihn"],
    "she": ["Sie", "Ihr"],
    "it": ["Es", "Seine"],
    "they": ["They", "Them"],
    "any": ["Jede"],
    "other": ["Anderes"],
    "ask": ["Frag"],
    "avoid": ["Nutz Name"],
})

pronoundb_client.get_pronouns_by_platform_ids(Platform.DISCORD, 123456789012345678)
# -> {123456789012345678: ["Er", "Ihn"]}
```

You can also use one of the included translation pronouns (`english_pronouns` and `german_pronouns`).
AND when forgejo supports that, you can contribute translations as well! :D

> Notice, that currently in some languages some translations like the "They/Them" are still in active debate about how to translate them, so dear developer:
> Think about if the way the presets do it is good.
> - If it's good, ignore the deprecation warning and use the preset.
> - If not, make your own.

## Decorations (Version 3.0.0)

Decorations are a new feature of pronoundb and currently in Beta.
If you want to use them, you can do that like this:

```py
from pronoundb import Client, Platform

pronoundb_client = Client(user_agent="Example for Python PronounDB API Wrapper")
pronoundb_client.get_decorations_by_platform_ids(Platform.DISCORD, 123456789012345678)
# -> {123456789012345678: "donator_aurora"}
```

## Contributing

Contributions to this library are always welcome and highly encouraged.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
