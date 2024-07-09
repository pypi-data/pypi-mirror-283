# sopel-pronouns

Pronoun-sharing plugin for Sopel IRC bots

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-pronouns
```

## Configuring

The easiest way to configure `sopel-pronouns` is via Sopel's
configuration wizard—simply run `sopel-plugins configure pronouns`
and enter the values for which it prompts you.

Options are:

* `fetch_complete_list`: Whether to download the complete list of supported
  pronoun sets at startup
  * `fetch_url`: An optional custom fetch URL for the complete list (see below)
* `link_base_url`: An optional custom base URL for links in the plugin's output

The `link_base_url` option allows you to use your own domain to host your own
instance of [our pronoun service][pronoun-service] hosted at
[`pronouns.sopel.chat`][pronouns-instance], which is itself a fork of Lucas
Eduardo's [lovely little Svelte project][original-pronoun-service].

If you want to customize the available pronoun sets, set the `fetch_url` to your
own instance's `pronouns.tab` file or an equivalent tab-delimited data source.

[pronoun-service]: https://github.com/sopel-irc/pronoun-service
[pronouns-instance]: https://pronouns.sopel.chat/
[original-pronoun-service]: https://github.com/lucasew/svelte-pronounisland

## Credits

`sopel-pronouns` is based on the `pronouns.py` plugin that was built into Sopel
from version 6.5.1 through 8.0. Special thanks to Elsie Powell and other
contributors to the original code, whose work can be viewed in the main Sopel
repository's [commit history][original-history].

[original-history]: https://github.com/sopel-irc/sopel/commits/d4a0efde1a4bdea03be265d5e23591b553a0ce76/sopel/modules/pronouns.py
