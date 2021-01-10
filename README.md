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

## Maintenance

When adding a new class, ensure it gets put into the the models map and any management commands.

Whenever changing how ingestion works, you need to re-ingest and create new test fixtures.
