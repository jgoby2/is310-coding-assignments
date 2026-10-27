# GETting Culture Across APIs: PokéAPI + Bulbapedia

`getting_culture.py` queries two APIs about Pokémon and connects them:

1. **Bulbapedia's MediaWiki Action API** (`https://bulbapedia.bulbagarden.net/w/api.php`). It prints the members of `Category:Generation I Pokémon`, then parses individual species articles for word count, internal links, and language links (the same measures used on the LOTR Fandom wiki in class).
2. **PokéAPI** (`https://pokeapi.co/api/v2`). It prints the raw `/pokemon-species/pikachu` response, then pulls each Pokémon's generation, types, legendary status, and official names in other languages.

**The connection:** PokéAPI's official English name is turned into a Bulbapedia title (`<Name> (Pokémon)`) and looked up there. I chose a few awkward names on purpose: `mr-mime`, `farfetchd`, and `nidoran-f` are PokéAPI's ASCII slugs for *Mr. Mime*, *Farfetch'd*, and *Nidoran♀*, so a naive match on the slug fails while a match on the official English name works. `missingno` (a famous glitch Pokémon) is not in PokéAPI at all, which tests the error handling.

**Output:** `pokeapi_bulbapedia_data.json` and `pokeapi_bulbapedia_data.csv` (item data only, no raw responses).

Run it with:

```
python -m pip install requests beautifulsoup4 rich
python getting_culture.py
```

No API keys are used.

## Comparing the two APIs

<!-- DRAFT: revise this in your own voice before submitting, then delete this line. -->

Both APIs didn't require a key or can account just a different user. PokeAPI doesn;t require anything, not even a user agent; it just has a simple fair use policy and asks users to cache locally on their machine. This api removed rate limiting when it switched to static hosting. The MediaWiki API is also open but sits behind Cloudflare and suggests a user-agent processing one request at a time; I could not find a published rate limit, so I paused a second between calls. The data shapes point the same way. PokeAPI returns JSON where a Pokemon is a set of game facts, which makes it easier to get one or all Pokemon, but doesn't really show anything about how people talk about them. Bulbapedia gives me HTML that I had to parse with BeautifulSoup, but there is a lot of valuable data in this HTML: Pikachu's article ran to 23,959 words and 1,782 unique internal links, eight times longer than the newest Pokémon I checked, Sprigatito (2,946 words). Suprising because PokeAPI describes both with the same set of fields. Every article linked to the same 6 other-language fan wikis. Connecting these two was not very easy. PokéAPI's identifiers are slugs like `farfetchd` and `nidoran-f`, while Bulbapedia titles uses the original symbols and punctuation, so identity only lined up once I used PokéAPI's official English name. Even that wasn't exact: PokéAPI spells Farfetch'd differently than Bulbapedia, so that match only worked because a wiki editor had set up a redirect. MissingNo., the famous glitch Pokémon, has a Bulbapedia article but returned a 404 from PokéAPI, because it exists in fan memory and not in the official dataset. The two are run completely different. PokéAPI is an open-source project funded by donations through Open Collective and GitHub Sponsors, but Bulbapedia is a fan community, running since 2005 kept free because of advertising; neither of these two are associated with Pokemon, so they could vanish in and instant, and my research would mean nothing. As for what's missing, PokéAPI only knows what the games define, so it covers the 12 languages the games were officially localized into (Japanese, English, French, German, Italian, Spanish, Korean, Chinese, and a few regional variants) and nothing about players, the anime's reception, or regional fan cultures. Bulbapedia is English-first, and its language links point to a plethora of different fan wikis.

### Sources for the facts above

- [PokéAPI v2 documentation and Fair Use Policy](https://pokeapi.github.io/pokeapi.co/v2/)
- [PokéAPI overview (API Evangelist)](https://github.com/api-evangelist/pokeapi)
- [Bulbapedia: About](https://bulbapedia.bulbagarden.net/wiki/Bulbapedia:About)
- [Bulbapedia main page (hosting partner)](https://m.bulbapedia.bulbagarden.net/wiki/Bulbapedia:About)


## AI Usage
Used Claude to help me fix my script when I kept getting an error message
Asked claude why I got an error 404
Claude helped me revise my writing for mistakes as well