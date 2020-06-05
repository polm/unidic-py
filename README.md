# unidic-py

This is a version of [UniDic](https://unidic.ninjal.ac.jp/) packaged for use
with pip. 

Currently it supports 2.3.0, the latest version of UniDic. **Note this will
take up 1GB on disk after install and can take a long time to download.** If
you want a small package, try
[unidic-lite](https://github.com/polm/unidic-lite).

After installing via pip, you need to download the dictionary using the
following command:

    python -m unidic download

Example use with [fugashi](https://github.com/polm/fugashi), though [mecab-python3](https://github.com/samurait/mecab-python3) works the same way:

    import fugashi
    import unidic
    tagger = fugashi.Tagger('-d{}'.format(unidic.DICDIR))
    # that's it!

# License

The modern Japanese UniDic is available under the GPL, LGPL, or BSD license,
[see here](https://unidic.ninjal.ac.jp/download#unidic_bccwj). UniDic is
developed by [NINJAL](https://www.ninjal.ac.jp/), the National Institute for
Japanese Language and Linguistics. UniDic is copyrighted by the UniDic
Consortium and is distributed here under the terms of the [BSD
License](./LICENSE.unidic).

The code in this repository is not written or maintained by NINJAL. The code is
available under the MIT or WTFPL License, as you prefer.
