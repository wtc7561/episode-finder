# Art is Change Episode Finder

A searchable guide to every episode of the *Art is Change* podcast from the Center for the Study of Art & Community, hosted by Bill Cleveland.

- `index.html` is the search page.
- `episodes.json` holds the episode data. It is exported from the Art is Change Airtable base and refreshed each Wednesday after the new episode is added.
- `tools/build_episodes.py` builds `episodes.json` from the Airtable CSV export.
