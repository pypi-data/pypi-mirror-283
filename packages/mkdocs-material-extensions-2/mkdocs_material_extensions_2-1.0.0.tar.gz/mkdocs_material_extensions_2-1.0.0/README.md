# [MkDocs Material Extensions 2](https://materialy.danling.org)

## Introduction

Better emoji support for [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Usage

=== "EmojiOne"

```yaml
- pymdownx.emoji:
    emoji_index: !!python/name:materialy.emoji1
    emoji_generator: !!python/name:materialy.to_svg
```

=== "Twemoji"

```yaml
- pymdownx.emoji:
    emoji_index: !!python/name:materialy.twemoji
    emoji_generator: !!python/name:materialy.to_svg
```

=== "Gemoji"

```yaml
- pymdownx.emoji:
    emoji_index: !!python/name:materialy.gemoji
    emoji_generator: !!python/name:materialy.to_png
```

## Installation

=== "Install the most recent stable version on pypi"

    ```shell
    pip install mkdocs-material-extensions-2
    ```

=== "Install the latest version from source"

    ```shell
    pip install git+https://github.com/ZhiyuanChen/mkdocs-material-extensions-2
    ```

## License

mkdocs-material-extensions-2 is licensed under the AGPLv3+ license:

`SPDX-License-Identifier: AGPL-3.0-or-later`
