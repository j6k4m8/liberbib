# liberbib

An open-source bibliography-management tool.

Intended to fuel projects like [remarkabib](/https://github.com/j6k4m8/remarkabib) and an [upcoming] web app.

## Usage

```bash
uv run liberbib --mailto liberbib@example.com search --bibtex "ten simple rules"
```

> Note: The 'mailto' flag is required to use the search command; this puts you in the "polite" pool for OpenAlex, the API used to search for papers. This is good practice and helps us support our community.

```
@article{MenshTen2017,
    author = {Brett D. Mensh and Konrad Körding},
    title = {Ten simple rules for structuring papers},
    year = {2017},
    journal = {PLoS Computational Biology},
}
```
