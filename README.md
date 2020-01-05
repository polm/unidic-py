# unidic-py

This is a version of [UniDic](https://unidic.ninjal.ac.jp/) packaged for use
with pip. 

This is based on UniDic 2.1.2, which is roughly 55MB zipped or 300MB unzipped.
There are more recent versions of UniDic but they're significantly larger,
which makes packaging difficult.

This package distributes only the files necessary for using UniDic with MeCab.
The large files are gzipped for distribution and unzipped the first time the
library is imported. It would be better for MeCab to unzip on the fly when
reading from disk but it doesn't support that.

Example use with [fugashi](https://github.com/polm/fugashi), though [mecab-python3](https://github.com/samurait/mecab-python3) works the same way:

    import fugashi
    import unidic
    tagger = fugashi.Tagger('-d{}'.format(unidic.DICDIR))
    # that's it!

# License

The modern Japanese UniDic is available under the GPL, LGPL, or BSD license,
[see here](https://unidic.ninjal.ac.jp/download#unidic_bccwj) or [the included
BSD license](https://github.com/polm/unidic-py/blob/master/unidic/dicdir/BSD).
UniDic is developed by [NINJAL](https://www.ninjal.ac.jp/), the National
Institute for Japanese Language and Linguistics. 

The code in this repository is not written or maintained by NINJAL. The code is
available under the MIT or WTFPL License, as you prefer.
