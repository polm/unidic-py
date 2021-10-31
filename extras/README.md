# Extras

unidic-py distributes a slightly modified version of UniDic for ease of use. To
build this dictionary yourself, perform the following steps:

1. Download the official latest UniDic from the [homepage](https://ccd.ninjal.ac.jp/unidic/)
2. Use `clean-lex.sh` to rewrite `lex.csv`
3. Copy the appropriate `reiwa.csv` to your dictionary directory (the number is the field count)
4. Run the normal mecab dictionary build command

That's it.

The normal MeCab dictionary building command is:

    /usr/local/libexec/mecab/mecab-dict-index -d . -o . -f utf8 -t utf8

Note that depending on your MeCab install the path may be different.
