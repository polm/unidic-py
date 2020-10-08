This is a description of the various tokenizer dictionaries hosted on AWS as
part of Amazon's Open Data Sponsorship Program. This file is distributed with
the main unidic-py package, but also describes other dictionaries.

This repository contains dictionaries for use with MeCab for tokenization and
morphological analysis of modern written Japanese.

## Background

Two main dictionaries are included in this repository: UniDic and IPADic.

UniDic is maintained by NINJAL, the National Institute for Japanese Language
and Lingusitics. It is the official dictionary of Japanese Universal
Dependencies. Based on the "School Grammar" model of Japanese, it uses the
"short unit word" as the base unit of tokenization, which results in highly
reproducible tokenizations suitable for many downstream tasks. 

In its default distribution, UniDic includes dictionary entries for individual
letters of the latin alphabet and some numbers. Because these can cause
unexpected tokenization results with the default configuration, they have been
removed. As a result strings of latin text or numbers will result in single
tokens.

This distribution of UniDic also adds entries for 令和 *Reiwa*, the name of the
new Imperial Era that began in 2019. 

Additionally, a smaller version UniDic called "unidic-lite" is provided. This
is based v2.1.2 of UniDic, which was much smaller in size than more recent
versions, but should still be accurate for many applications. In particular,
for first time use of MeCab it's more than enough to get started with Japanese
text analysis.

Besides UniDic, IPADic is also provided. IPADic is a dictionary based on an
original definition of the "word" and was built at the Nara Institute of
Science and Technology (NAIST), based on an older dictionary from the Institute
for New Generation Computer Technology (ICOT). IPADic has not been updated
since 2007, so using it is not recommended for new projects. However, IPADic
has been used for many old benchmarks and occasionally is used in newer
projects, so it's provided here for purposes of compatability. Unlike UniDic,
IPADic has not been modified for convenience or to make it more current in the
interest of providing maximum compatability with old benchmarks.

## Data Access

The various dictionaries are stored in the cloud on Amazon Web Services and can
be installed through pip. 

    pip install unidic
    pip install unidic-lite
    pip install ipadic

In the case of unidic, due to the large file size - 1GB after extraction - it
has an extra download step. Do this to download the dictionary data from S3:

    python -m unidic download aws

## Data Types and Structure

The dictionaries are provided as binary files for use with MeCab and you should
generally not need to access them directly.

The raw files used to compile the dictionaries are in CSV format. The fields
differ for each dictionary, except for the first four fields, which are defined
by MeCab.

- word: the literal word as it appears in text
- left_id: an internal ID (integer)
- right_id: an internal ID (integer). Ordinarily this is always the same as left_id.
- cost: (integer) Used in calculating tokenizations, low cost entries take priority over high cost entries.

### UniDic

UniDic fields are defined at [NINJAL's UniDic FAQ page][faq]. unidic-lite uses
a subset of the fields in the most recent version.

[faq]: https://unidic.ninjal.ac.jp/faq

IPADic fields are as follows:

- pos1: Broad part of speech
- pos2: part of speech
- pos3: part of speech
- ctype: conjugation type
- cform: the conjugation of the current token
- lemma: normalized form
- reading: standard kana representation
- pronuncation: as reading, but long vowels are differentiated (講師 is こーし, 子牛 is こうし)

## References

UniDic is developed by NINJAL. Here are some resources on UniDic:

- [UniDic home page](https://unidic.ninjal.ac.jp/faq)
- [Universal Dependencies for Japanese](https://www.semanticscholar.org/paper/Universal-Dependencies-for-Japanese-Tanaka-Miyao/064b601542d27471e397f8df811f0ddb54824113)

The MeCab documentation covers dictionary formats and tokenizer options. It
also has some discussion of IPADic, which does not have a home page.

- [MeCab documentation](https://taku910.github.io/mecab/)
