# Minecraft Wiki Mob Scraper

## Wiki and Question

I scraped the [Minecraft Wiki](https://minecraft.wiki), a community-run wiki that moved off Fandom.com in 2023 and is now hosted independently by Weird Gloop. I chose this because I used to be very into Minecraft as a kid, and I wanted to do some scraping on the mobs in the game.

**Research question:** Do hostile mobs receive more documentation on the Minecraft Wiki than passive mobs?

This data is interesting for users because it really dives into the fandom of Minecraft. Users can learn what fans think about mobs and how fans display their ideas with data.

## How the Scraper Works

`wiki_scraping.py` scrapes two levels of pages:

1. **Category pages:** [Category:Hostile_mobs](https://minecraft.wiki/w/Category:Hostile_mobs) and [Category:Passive_mobs](https://minecraft.wiki/w/Category:Passive_mobs). It collects every mob link listed in the `mw-pages` section.
2. **Mob pages:** For each mob, it measures the main article content (`#mw-content-text .mw-parser-output`):
   - `word_count`: number of whitespace-separated words
   - `character_count`: number of characters, including spaces and punctuation
   - `internal_link_count`: every link to another wiki page, including repeats
   - `unique_internal_link_count`: each distinct wiki page linked, counted once

The scraper sends an honest User-Agent that identifies me, waits one second after every request, and only parses pages that return a `200` status code. It skips any page whose name contains a colon. That excludes editors' `User:` sandbox drafts, which robots.txt disallows, and `Dungeons II:` pages, which belong to a spin-off game. Mobs listed in both categories are downloaded once but appear in both groups, flagged in the `in_both_categories` column.

The results are saved in `minecraft_mobs.csv`.

## robots.txt and Site Policies

**robots.txt:** https://minecraft.wiki/robots.txt

The robots.txt allows general crawlers to access regular article pages under `/w/`, but disallows File, User, Special, and Bucket pages, the API (`api.php` and REST endpoints), and URLs with query parameters such as `?action=`, `?oldid=`, `?search=`, and `?pagefrom=`. It fully blocks a long list of named SEO and AI crawlers. It does not set a crawl delay, but my scraper waits one second between requests anyway.

The wiki's content is licensed under [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/) unless otherwise noted (see [Weird Gloop's licensing page](https://meta.weirdgloop.org/w/Licensing)). The wiki also links to Weird Gloop's [Terms of Use](https://weirdgloop.org/terms).

## Results

| Type | Pages | Avg Words | Avg Characters | Avg All Links | Avg Unique Links |
|---|---|---|---|---|---|
| Hostile | 46 | 5,935 | 34,722 | 1,295 | 543 |
| Passive | 41 | 5,931 | 35,132 | 1,270 | 600 |

Both hostile and passive mobs recieve the same amount of text on average. Hostile pages have more links, while passive pages have more nested links. This might show us hostile pages repeat the same links with different mobs. The longest page is Villager with (18207) words. This is probably due to all the Villager trading capabilities. In regards to hostile mobs Zombie has the most text with (13799). This is possibly because it seems to be the most known mob in the game, in my opinion. 

## Reflection

My measurements are proxies for "documentation," not for how much fans care about a mob or how important it is in the game. The clearest example came from my first run: the hostile category included 15 short pages for Minecraft Dungeons II mobs, which made passive mobs look much better documented. Once I removed them, the difference disappeared. The answer depended on what editors had placed in the category, not just on how much they wrote, so the categories themselves are part of the evidence rather than neutral containers. Word count also shows a lot about a mob and what an editor thinks about a specific mob. Villager, for examplle the largest page with text because it has the capability of trading with the user. Link counts are inflated by navigation boxes that appear on every page, so much of each count is shared template rather than writing about that specific mob. The groups also include entries that are not ordinary mobs, such as joke, removed, and Education Edition entries (Pink Wither, Giant, Camera), and three mobs appear in both categories. This could be inflating the data slightly. Someone would be wrong to conclude from my data that fans care equally about hostile and passive mobs, or that either type is more popular with players. To make claims like that, I would need other evidence, such as edit histories, page view counts, or talk page discussions.

## AI Usage
helped me active the virtual enviroment, for some reason it wasn't working
helped further explain the robots.txt as it didn't make total sense at first 
helped me troubleshoot my scrape file as it was running correctly but i could tell the data was wrong