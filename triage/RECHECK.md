# iRO quests, re-checked (2026-10-21)

The first triage counted 3,307 quest-log entries as "permanent and missing". Geffen showed
that most of them were not, so every chain was checked again on three things:

1. **Is it on iRO?** Its title or quest-giver appears on an iROWiki page (532 pages linked
   from the wiki's Quests index, read from the Internet Archive), or its giver is in the iRO
   client's NPC table (`navi_npc_us`).
2. **Is it permanent?** The iROWiki page is not under a year (event) or "Obsolete" heading.
3. **Is it already in the game?** A server or mod script names the chain, or has an NPC of
   the giver's name at the giver's spot.

## What is really missing (on iROWiki, permanent, and not on this server)

| Content | iROWiki page | Quest-log entries | Where |
|---|---|---:|---|
| **4th-job change quests** (and the expanded classes still missing) | the class pages (e.g. *Wizard* mentions Arch Mage) | ~97 | Path of Sky, Path of Ascetic, Path of the Soul Reaper, Path of the Inquisitor, Path of the Night Watch, Path to Becoming a Meister, Elemental Master, Arch Mage, Hyper Novice, Star Emperor... Only the Dragon Knight quest exists on the server. Maps `job4_*` already hold World Sync placeholders. |
| **Eye of the Beholder** | *Eye of the Beholder* (Other Quests, iRO-only) | 29 | 61001-61029 |
| **Criminal Activities Quest** | *Criminal Activities Quest* (Other Quests, iRO-only) | 27 | 40000-40026: Lighthalzen Pickpocket, Ling Mynmei, Howard Moon, Flood Control, Jymmy the Thumb... (Lighthalzen, Rock Ridge, Hugel, Rachel, Veins) |
| **Overlook Water Dungeon** | *Overlook Water Dungeon Quests* (Other Quests, iRO-only) | 5 | Aged-monster hunts at the dungeon signpost; maps `iz_dun00t`-`iz_dun03t`, World Sync placeholders |
| **Gramps' weekly turn-ins** | *Eden Group*, *Weekly Turn-In Events* (iRO-only) | 289 | rAthena's Gramps at the Eden Group is a talk-only stub |
| **Adventurer's Guild** | *Adventurer's Guild* (iRO-only) | 116 | Alberta, Lighthalzen, Rachel, Allied Forces Post. iROWiki lists the monsters for two of the four NPCs and no EXP; the client text names no monsters. Incomplete source. |

Unclear: **The Lion's Roar** (33 entries, 62260-62292). iROWiki files it under Other Quests, but
the page is the *Glast Heim Spotlight*, a temporary event.

## Already in the game (with other quest ids, or without the quest log)
Illusion of Abyss Turtle Island (rAthena's `quests_illusion_dungeons.txt`: Knight Aylvar, Narin, Leiphen, under kRO's quest ids, so the first check missed it),
The Eye of Hellion, The Sign (old version; the kRO rewrite with Metz Brayde is not here),
Help Mr. Zabaroo, Koschei the Immortal, Kiel Hyre, Seals of the God items, Sealed Shrine,
Geffen Magic Tournament (shipped switched off), Endless Tower, Old Glast Heim, Devil's Tower,
Ghost Palace, Sara's Memory, Memory of Professor Worm, Wolfchev's Laboratory, Bounty Boards (iro-quests 0.1.0).

## Not on iRO, or retired events
- Rebuilding the Destroyed Morroc (5253-5262): iROWiki marks it not implemented since Morroc was rebuilt in Episode 15.
- kRO's 2021 town and field quests (beyond the Eden boards that mod eden-rework-2021 already runs),
  the new-adventurer story (Leno, Jewel of Helion) and Criatura Academy's staff manual: their
  givers are mostly not in iRO's NPC table and iROWiki has no page for them.
- Every chain whose only iROWiki trace is an event page: Valentine, Lunar New Year, Snow Flower,
  Noodle Festival, Halloween, anniversaries, Pirate Day, Spotlights, collaborations.
- The rest of the "older kRO" entries (about 1,300): no trace on iROWiki or in iRO's NPC table.

Done in iro-quests 0.2.0: Criminal Activities, Eye of the Beholder, Overlook Water Dungeon.

So the real backlog is about **200 story/job entries** (now mostly the 4th-job quests) plus the two iRO hunting systems, not 3,307.
