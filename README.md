# unidic-py

This is a version of [UniDic](https://unidic.ninjal.ac.jp/) packaged for use
with pip. 

Right now it only supports the somewhat old 2.1.2 version of UniDic.

Example use with [fugashi](https://github.com/polm/fugashi), though [mecab-python3](https://github.com/samurait/mecab-python3) works the same way:

    import fugashi
    import unidic
    tagger = fugashi.Tagger('-d{}'.format(unidic.DICDIR))
    # that's it!

# License

The modern Japanese UniDic is available under the GPL, LGPL, or BSD license,
[see here](https://unidic.ninjal.ac.jp/download#unidic_bccwj). UniDic is
developed by [NINJAL](https://www.ninjal.ac.jp/), the National Institute for
Japanese Language and Linguistics. 

The code in this repository is not written or maintained by NINJAL. The code is
available under the MIT or WTFPL License, as you prefer.
