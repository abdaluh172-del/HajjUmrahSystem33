# -*- coding: utf-8 -*-
"""manual_sources — admin manual-entry-by-URL path (v15.9).

    Manual link  ->  manual_external.py  ->  ai_pipeline.py

The admin pastes an external post URL (X or Reddit) plus the comment text;
we validate the URL, derive a stable external_id from it (so the same link
can't be added twice), tag it with the right source_type, and hand the text
to the SAME AI pipeline every other source uses.
"""
