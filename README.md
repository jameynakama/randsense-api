# Randsense
        verb_types = [
            "intran",
            "tran",
            "ditran",
            "link"
        ]

        pronoun_types = [
            "dem",
            "obj",
            "subj",
            "poss",  # their
            "possnom",  # theirs
            "refl",
            "poss",
            "univ",
            "indef(assert)",
            "indef(neg)",
            "indef(nonassert)",
        ]

## Usage

You must have docker installed to run this app (the easy way).

You also must have a lexicon to ingest. I don't include it in the repo because it's
very large, so please just ask me for it if you'd like to play with the app yourself.

First time:

```bash
$ docker-compose build --pull
$ docker-compose run --rm manage ingest_lexicon LEXICON.xml
# Run this next command for each word class.
# Words with a rank of 0 will not be returned by queries.
$ docker-compose run --rm manage rank_words_by_frequency --word-class=noun unigram_freq.csv
$ docker-compose run --rm manage rank_words_by_frequency --word-class=verb unigram_freq.csv
$ docker-compose run --rm manage rank_words_by_frequency --word-class=adjective unigram_freq.csv
# Etc. etc.
```

General running:

```bash
$ docker-compose up web
```

## Maintenance

When adding a new class, ensure it gets put into the the models map and any management commands.

Whenever changing how ingestion works, you need to re-ingest and create new test fixtures.
