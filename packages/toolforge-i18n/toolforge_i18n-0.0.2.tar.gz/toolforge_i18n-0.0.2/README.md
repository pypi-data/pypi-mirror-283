# Toolforge I18n

A **work in progress** library for making Wikimedia Toolforge tools written in Python+Flask translatable.

## Features

- Make your tool translatable into dozens,
  potentially hundreds of languages!

- Easy integration with [translatewiki.net][]
  by reusing MediaWiki message file syntax.

- Full support for the [magic words][]
  `{{GENDER:}}` and `{{PLURAL:}}`,
  as well as for hyperlink syntax (`[url text]`)
  and list formatting.

- By default, support for a MediaWiki-like
  `?uselang=` URL parameter,
  including `?uselang=qqx` to see message keys.

- Correct conversion between MediaWiki language codes
  and HTML language codes / IETF BCP 47 language tags;
  for instance, `?uselang=simple` produces `<html lang="en-simple">`.

- Correct `lang=` and `dir=` in the face of language fallback:
  messages that (due to language fallback) don’t match the surrounding markup
  are automatically wrapped in a `<span>` with the right attributes.
  (Even MediaWiki doesn’t do this!
  Though, admittedly, MediaWiki doesn’t have the luxury of assuming
  that every message can be wrapped in a `<span>` –
  many MediaWiki messages are block elements that would rather need a `<div>`.)

- Includes tests that check all the translations
  for unexpected elements (e.g. `<script>`)
  or attributes (e.g. `onclick=`),
  to protect against XSS attacks from translations.
  The tests are automatically registered via a pytest plugin;
  you must set up CI to run `pytest`,
  e.g. in GitLab CI or GitHub actions,
  even if you have no other tests of your own.

## How to use it

The library is still a work in progress, so preferably don’t use it yet :)
but if you’re feeling adventurous, the rough steps should be:

- Add the library to your tool’s dependencies.
  (As the library is still in its early stages,
  and there may be breaking changes,
  I recommend pinning your dependencies using [pip-tools][] or something similar.)

- In your tool’s source code,
  add a file `tool_translations_config.py` with at least the following contents:

  ```python
  from toolforge_i18n.translations import TranslationsConfig

  config = TranslationsConfig()
  ```

  Later, you may want to customize parts of the translations config,
  such as the message `variables`;
  see the class documentation for details.

- Create an `i18n/` directory,
  with `en.json` and `qqq.json` files,
  just like for MediaWiki extensions.
  `en.json` contains English messages,
  while `qqq.json` contains message documentation;
  both contain a JSON object mapping the message key to the text / documentation.

- In your tool’s source code (probably `app.py`),
  add the following import:

  ```python
  from toolforge_i18n.flask_things import ToolforgeI18n, message
  ```

  And add this line shortly after creating the `app`
  (which usually looks like `app = flask.Flask(__name__)`):

  ```python
  i18n = ToolforgeI18n(app)
  ```

- Use `message('message-key')` for any message that should be translatable,
  either in a Jinja2 template (`{{ message('message-key') }}`)
  or directly in the Python code.
  For messages with parameters, use kwargs syntax like
  `message('message-key', arg1='X', arg2='Y')`
  and define the variable names in `tool_translations_config`
  (as mentioned above).

That should be it, but I might have forgotten some steps.
Also, at some point I’ll surely flesh this out more.

## License

BSD-3-Clause

[translatewiki.net]: https://translatewiki.net/
[magic words]: https://www.mediawiki.org/wiki/Special:MyLanguage/Help:Magic_words
[pip-tools]: https://pip-tools.readthedocs.io/en/latest/
