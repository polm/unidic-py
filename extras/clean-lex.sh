#!/bin/bash
# Remove entries from lex.csv that can make weird tokenizations

# usage:
#     ./clean-lex.sh [lex.csv] > lex.fix.csv
# Make sure to delete the original lex.csv before building a dictionary.

# Types of entries to remove:
# 1. Single latin letters. These can cause short unknown words to break up,
# like "fish" as "f i s h".
# 2. Number-only entries of any length. These can cause strange pronunciations,
# like 10 as "ten".

# Note it is extremely important that the character ranges are broken up like
# this to avoid including punctuation. 
grep -Ev '^([A-Za-zＡ-Ｚａ-ｚ]|[0-9０-９]*),' "$1"

# In Unidic 2.3.0 this removes 232 entries.
