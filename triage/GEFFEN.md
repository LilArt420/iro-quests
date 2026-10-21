# Geffen, chain by chain (2026-10-21)

The triage filed 231 quest-log entries under Geffen. Checked one chain at a time against the
live server's scripts (rAthena EP19 + every enabled mod), the iRO client's NPC table
(`navi_npc_us`) and iROWiki (Internet Archive copies), they come out as follows.

## Already in the game (other quest ids, or variables instead of the quest log)
| Ids | Chain | Where it already is |
|---|---|---|
| 19117-19129 | The Eye of Hellion | `npc/quests/eye_of_hellion.txt` (Welshyun, Grout'he, Tyus, Enoz), loaded |
| 1357-1361, 1394-1396 | Metz's / Jesqurienne's trials, Sobbing Starlight | the kRO rewrite of **The Sign**; rAthena's `the_sign_quest.txt` (Jesqurienne, Aaron) is loaded |

## Not live on iRO, or retired events
| Ids | Chain | Why it is left out |
|---|---|---|
| 7462-7463 | Lennon / Ken's stories | Valentine chocolate event (7454-7469) |
| 8532, 8579-8583 | Lavender, Dilfore, Sour Melons | Melon Festival event |
| 14386, 14394-14398 | Matchmaking, florist, seed | Valentine/White Day event (Chocolate Drink) |
| 17152 | Not everyone likes it | Snow Flower Festival event |
| 23323 | Strange Things at Abyss Lake | kRO collaboration event (Hiccup, Toothless) |
| 7181 | Karakas's ring | "available for some time": event |
| 60010-60017 | Derik Ver's Monster Investigation | iRO weekly event ("after the June 9th maintenance") |
| 62549-62554 | Jumping Janeway | iRO levelling event (iROWiki: "periodically visits"); in Izlude anyway |
| 62694-62702 | Undead Danielle | iRO seasonal event (Prontera church, Niflheim, Glast Heim) |
| 63042-63043, 297038-297040 | Pub Crawler, Spirit Cleansing | iRO events |
| 62423, 62432, 62504 | lab access, dice game, desocketing timers | cooldown entries of other systems |
| 21097-21118, 21167-21173 | Junior Wizard and Petite Boy dailies, "Bonus experience" | kRO's 2021 town quests: no Junior Wizard or Petite Boy in iRO's NPC table. The repeats already run from the Eden boards (mod eden-rework-2021, same ids) |

## Filed under Geffen, but belong to another area or pack
| Ids | Chain | Goes with |
|---|---|---|
| 5571-5705 | (A/B/C) Delivery quests | kRO delivery union, all over Rune-Midgard |
| 5117, 5477 | [Shelter] High Wizard, (Wanted) Fenrir | Biolab / Bounty Union (Dimensional Gap) |
| 3422 | Book of Illusion Vol. 2 | Illusion dungeons (Orc Dungeon) |
| 7490 | Mushroom soup | Morroc oasis |
| 8137-8138 | Keymaker, Blacksmith's request | Moscovia (Koschei) |
| 9267-9268, 9285-9289 | Strong Mage, Geffen Gangsters, Shoplifter | **Geffen Magic Tournament** instance (`1@gef`): rAthena ships it as `custom/official/GeffenMagicTournament.txt`, switched off |
| 11674-11683 | Elemental Master job change | 4th-job quests (map `job4_mag`, World Sync placeholders) |
| 21266-21267 | The Supplies Are Here | Prontera knights' subjugation chain |
| 21962-21964 | The Jewel of Helion 14-16 | the new-adventurer story (Izlude to Morroc) |
| 40002 | Ling Mynmei | iRO Lighthalzen pickpocket chain (40000-40026) |
| 50531-50535 | Overlook Water Dungeon | Izlude (`iz_dun00t`-`iz_dun03t`, World Sync placeholders) |
| 60301-60834 | Dragon, Orc Archer, Marionette... hunts | Gramps' weekly turn-ins (Eden Group) |
| 62424, 70041 | Yellow Plates | Amatsu |
| 62430-62431 | Orcs in the Sewers | Prontera Culvert |
| 62433-62548 | Adventurer's Guild Hunt | iROWiki: Alberta, Lighthalzen, Rachel, Allied Forces Post. The client text names no monsters, iROWiki lists them only for two of the four NPCs and has no EXP figures |
| 62494-62497 | Shady Sam's Carpet | no iROWiki page, no Trader Sam in iRO's NPC table |

## What is left for Geffen
Nothing that is both live on iRO and missing here. The one Geffen-map content that is
permanent on iRO (iROWiki, Dimensional Gap quests) and absent from this server is the
**Geffen Magic Tournament** instance, whose script rAthena ships switched off.
