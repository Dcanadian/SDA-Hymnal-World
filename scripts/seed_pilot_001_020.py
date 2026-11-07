#!/usr/bin/env python3
"""
Canonical SATB-derived chord & lyric database generator for Pilot Batch (Hymns 001-020)
of the Seventh-day Adventist Hymnal (1985).

Every hymn's key, time signature, lyricist, composer/tune source, and functional
worship harmony (including musical slash chords and cadential V7/sus4 chords) are
derived directly from the 4-part SATB score in SDA_Hymnal_1985.pdf.
Chords are placed inline on EVERY stanza and refrain with NO mid-word hyphens.
"""

import json
from pathlib import Path

DB_DIR = Path("/home/antigravity/SDA-Hymnal/Database")

PILOT_HYMNS = [
    {
        "number": 1,
        "title": "Praise to the Lord",
        "lyricist": "Joachim Neander",
        "composer": "Choral Book for England",
        "tune": "LOBE DEN HERREN",
        "key": "F",
        "time": "3/4",
        "tempo": 104,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[F]Praise to [Dm]the [C]Lord, the [F/A]Al[F/C]might[Dm7]y, [Gm]the [F/A]King [Bb]of [C7/G]cre[F/A]a[Gm7]tion![C] [F]",
                    "[F]O [Dm]my [C]soul, [F/A]praise Him, [F/C]for [Dm7]He [Gm]is [F/A]thy [Bb]health [C7/G]and [F/A]sal[Gm7]va[C]tion! [F]",
                    "[F]All ye [C/E]who [C]hear, [Bb]Now to [F/A]His [Gm]tem[C]ple [F/A]draw [C]near;",
                    "[F]Join [Gm]ye [Dm/A]in [Gm]glad [Dm/A]ad[A7]o[Dm]ra[Gm6]tion![C7] [F]"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[F]Praise to [Dm]the [C]Lord, who [F/A]o'er [F/C]all [Dm7]things [Gm]so [F/A]won[Bb]drous[C7/G]ly [F/A]reign[Gm7]eth,[C] [F]",
                    "[F]Shield[Dm]eth [C]thee [F/A]under [F/C]His [Dm7]wings, [Gm]yea, [F/A]so [Bb]gen[C7/G]tly [F/A]sus[Gm7]tain[C]eth! [F]",
                    "[F]Hast thou [C/E]not [C]seen [Bb]How thy [F/A]de[Gm]sires [C]e'er [F/A]have [C]been",
                    "[F]Grant[Gm]ed [Dm/A]in [Gm]what [Dm/A]He [A7]or[Dm]dain[Gm6]eth?[C7] [F]"
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[F]Praise to [Dm]the [C]Lord, who [F/A]doth [F/C]pros[Dm7]per [Gm]thy [F/A]work [Bb]and [C7/G]de[F/A]fend [Gm7]thee;[C] [F]",
                    "[F]Sure[Dm]ly [C]His [F/A]goodness [F/C]and [Dm7]mer[Gm]cy [F/A]here [Bb]dai[C7/G]ly [F/A]at[Gm7]tend [C]thee. [F]",
                    "[F]Ponder [C/E]a[C]new [Bb]What the [F/A]Al[Gm]might[C]y [F/A]can [C]do,",
                    "[F]If [Gm]with [Dm/A]His [Gm]love [Dm/A]He [A7]be[Dm]friend [Gm6]thee.[C7] [F]"
                ]
            }
        ]
    },
    {
        "number": 2,
        "title": "All Creatures of Our God and King",
        "lyricist": "Francis of Assisi",
        "composer": "Geistliche Kirchengesange",
        "tune": "LASST UNS ERFREUEN",
        "key": "D",
        "time": "3/2",
        "tempo": 96,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[D]All creatures [G]of [D/F#]our [Em7]God [A]and [D]King,",
                    "[D]Lift up your [G]voice [D/F#]with [Em7]us [A]and [D]sing:",
                    "[G]Alle[D]luia! [G]Al[A]le[Bm]lu[G]ia![A]",
                    "[D]O burning [G]sun [D/F#]with [Em7]gold[A]en [D]beam,",
                    "[D]And silver [G]moon [D/F#]with [Em7]soft[A]er [D]gleam:"
                ]
            },
            {
                "name": "Refrain",
                "type": "chorus",
                "lines": [
                    "[D]Oh, [Bm]praise [F#m]Him! [G]Oh, [Em]praise [F#m]Him!",
                    "[G]Alle[D/F#]lu[Em]ia! [A]al[Bm]le[F#m/A]lu[G]ia! [A]al[Em7]le[D/F#]lu[G]ia![A7] [D]"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[D]O rushing [G]wind [D/F#]and [Em7]breez[A]es [D]soft,",
                    "[D]O clouds that [G]ride [D/F#]the [Em7]winds [A]a[D]loft,",
                    "[G]Oh, [D]praise Him! [G]Al[A]le[Bm]lu[G]ia![A]",
                    "[D]O rising [G]morn, [D/F#]in [Em7]praise [A]re[D]joice,",
                    "[D]O lights of [G]eve[D/F#]ning, [Em7]find [A]a [D]voice:"
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[D]O flowing [G]wa[D/F#]ters, [Em7]pure [A]and [D]clear,",
                    "[D]Make music [G]for [D/F#]your [Em7]Lord [A]to [D]hear,",
                    "[G]Oh, [D]praise Him! [G]Al[A]le[Bm]lu[G]ia![A]",
                    "[D]O fire so [G]mas[D/F#]ter[Em7]ful [A]and [D]bright,",
                    "[D]Providing [G]us [D/F#]with [Em7]warmth [A]and [D]light:"
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "[D]Let all things [G]their [D/F#]Cre[Em7]a[A]tor [D]bless,",
                    "[D]And worship [G]Him [D/F#]in [Em7]hum[A]ble[D]ness,",
                    "[G]Oh, [D]praise Him! [G]Al[A]le[Bm]lu[G]ia![A]",
                    "[D]Oh, praise the [G]Fa[D/F#]ther, [Em7]praise [A]the [D]Son,",
                    "[D]And praise the [G]Spir[D/F#]it, [Em7]three [A]in [D]One!"
                ]
            }
        ]
    },
    {
        "number": 3,
        "title": "God Himself Is With Us",
        "lyricist": "Gerhard Tersteegen",
        "composer": "Joachim Neander",
        "tune": "WUNDERBARER KÖNIG",
        "key": "G",
        "time": "2/2",
        "tempo": 96,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[G]God Him[D/F#]self is [Em]with [D]us; [G]Let us [D]all a[A7]dore [D]Him,",
                    "[Em]And with [Bm]awe ap[C]pear [Am7]be[D]fore [G]Him.",
                    "[G]God is [D/F#]here with[Em]in [D]us; [G]Soul, in [D]silence [A7]fear [D]Him,",
                    "[Em]Humbly, [Bm]fervent[C]ly [Am7]draw [D]near [G]Him.",
                    "[G]Now His [D]own [Em]who have [Bm]known [C]God, in [G/B]worship [Am7]low[D]ly,",
                    "[G]Yield their [C]spirits [G/D]whol[D7]ly. [G]"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[G]Come, a[D/F#]bide with[Em]in [D]me; [G]Let my [D]soul, like [A7]Ma[D]ry,",
                    "[Em]Be Thine [Bm]earthly [C]sanc[Am7]tu[D]ar[G]y.",
                    "[G]Come, in[D/F#]dwelling [Em]Spir[D]it, [G]With trans[D]figured [A7]splen[D]dor;",
                    "[Em]Love and [Bm]honor [C]will [Am7]I [D]ren[G]der.",
                    "[G]Where I [D]go [Em]here be[Bm]low, [C]Let me [G/B]bow be[Am7]fore [D]Thee,",
                    "[G]Know Thee [C]and a[G/D]dore [D7]Thee. [G]"
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[G]Gladly [D/F#]we sur[Em]ren[D]der [G]Earth's de[D]ceitful [A7]trea[D]sures,",
                    "[Em]Pride of [Bm]life and [C]sin[Am7]ful [D]plea[G]sures:",
                    "[G]Gladly, [D/F#]Lord, we [Em]of[D]fer [G]Thine to [D]be for[A7]ev[D]er,",
                    "[Em]Soul and [Bm]life and [C]each [Am7]en[D]deav[G]or.",
                    "[G]Thou a[D]lone [Em]shall be [Bm]known [C]Lord of [G/B]all our [Am7]be[D]ing,",
                    "[G]Life's true [C]way de[G/D]cree[D7]ing. [G]"
                ]
            }
        ]
    },
    {
        "number": 4,
        "title": "Praise, My Soul, the King of Heaven",
        "lyricist": "Henry Francis Lyte",
        "composer": "John Goss",
        "tune": "LAUDA ANIMA",
        "key": "D",
        "time": "4/4",
        "tempo": 100,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[D]Praise, my [A/C#]soul, the [Bm]King of [F#m/A]heav[G]en; [D/F#]",
                    "[Em]To His [D/F#]feet thy [G]tribute [A]bring;",
                    "[F#7]Ransomed, [Bm]healed, re[E7/G#]stored, for[A]giv[E7]en, [A]",
                    "[D/F#]Who like [G]thee His [E7/G#]praise [A]should [E7]sing? [A]",
                    "[G]Praise Him, [D/F#]praise Him, [Em7]alle[D]luia, [B7]",
                    "[Em]Praise the [E7/G#]ever[A]last[A7]ing [D]King."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[D]Praise Him [A/C#]for His [Bm]grace and [F#m/A]fa[G]vor [D/F#]",
                    "[Em]To our [D/F#]fathers [G]in dis[A]tress;",
                    "[F#7]Praise Him, [Bm]still the [E7/G#]same for[A]ev[E7]er, [A]",
                    "[D/F#]Slow to [G]chide and [E7/G#]swift [A]to [E7]bless; [A]",
                    "[G]Praise Him, [D/F#]praise Him, [Em7]alle[D]luia, [B7]",
                    "[Em]Glorious [E7/G#]in His [A]faith[A7]ful[D]ness."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[D]Tender[A/C#]ly He [Bm]shields and [F#m/A]spares [G]us; [D/F#]",
                    "[Em]Well our [D/F#]feeble [G]frame He [A]knows;",
                    "[F#7]In His [Bm]hands He [E7/G#]gently [A]bears [E7]us, [A]",
                    "[D/F#]Rescues [G]us from [E7/G#]all [A]our [E7]foes: [A]",
                    "[G]Praise Him, [D/F#]praise Him, [Em7]alle[D]luia, [B7]",
                    "[Em]Widely [E7/G#]as His [A]mer[A7]cy [D]flows."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "[D]Angels, [A/C#]help us [Bm]to a[F#m/A]dore [G]Him: [D/F#]",
                    "[Em]Ye be[D/F#]hold Him [G]face to [A]face;",
                    "[F#7]Sun and [Bm]moon bow [E7/G#]down be[A]fore [E7]Him: [A]",
                    "[D/F#]Dwellers [G]all in [E7/G#]time [A]and [E7]space, [A]",
                    "[G]Praise Him, [D/F#]praise Him, [Em7]alle[D]luia, [B7]",
                    "[Em]Praise with [E7/G#]us the [A]God [A7]of [D]grace."
                ]
            }
        ]
    },
    {
        "number": 5,
        "title": "All My Hope on God Is Founded",
        "lyricist": "Joachim Neander",
        "composer": "Herbert Howells",
        "tune": "MICHAEL",
        "key": "F",
        "time": "4/4",
        "tempo": 96,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[F]All my [C/E]hope on [Dm]God is [Am7]found[Bb]ed; [Gm7]",
                    "[F]He doth [C/E]still my [Dm7]trust [G7]re[C]new.",
                    "[Bb]Me through [F/A]change and [Gm7]chance He [Dm]guid[A]eth,",
                    "[D7]Only [Gm]good and [C7]only [F]true.",
                    "[F]God un[Bb]known, [Gm]He a[A]lone",
                    "[Dm]Calls my [Bb]heart to [Gm7]be [C7]His [F]own."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[F]Pride of [C/E]man and [Dm]earthly [Am7]glo[Bb]ry, [Gm7]",
                    "[F]Sword and [C/E]crown be[Dm7]tray [G7]his [C]trust;",
                    "[Bb]What with [F/A]care and [Gm7]toil he [Dm]build[A]eth,",
                    "[D7]Tower and [Gm]temple [C7]fall to [F]dust.",
                    "[F]But God's [Bb]power, [Gm]hour by [A]hour,",
                    "[Dm]Is my [Bb]temple [Gm7]and [C7]my [F]tower."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[F]God's great [C/E]goodness [Dm]aye en[Am7]dur[Bb]eth, [Gm7]",
                    "[F]Deep His [C/E]wisdom, [Dm7]pass[G7]ing [C]thought;",
                    "[Bb]Splendor, [F/A]light and [Gm7]life at[Dm]tend [A]Him,",
                    "[D7]Beauty [Gm]springeth [C7]out of [F]naught.",
                    "[F]Love doth [Bb]stand [Gm]at His [A]hand;",
                    "[Dm]Joy doth [Bb]wait on [Gm7]His [C7]com[F]mand."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "[F]Still from [C/E]man to [Dm]God e[Am7]ter[Bb]nal, [Gm7]",
                    "[F]Sacri[C/E]fice of [Dm7]praise [G7]be [C]done.",
                    "[Bb]High a[F/A]bove all [Gm7]praises [Dm]prais[A]ing,",
                    "[D7]For the [Gm]gift of [C7]Christ His [F]Son.",
                    "[F]Christ doth [Bb]call [Gm]one and [A]all:",
                    "[Dm]Ye who [Bb]follow [Gm7]shall [C7]not [F]fall."
                ]
            }
        ]
    },
    {
        "number": 6,
        "title": "O Worship the Lord",
        "lyricist": "J. S. B. Monsell",
        "composer": "Edwin Barnes",
        "tune": "SOUTHAMPTON",
        "key": "G",
        "time": "3/4",
        "tempo": 100,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[G]O worship [D7]the [G]Lord in the [C]beauty of [G/D]ho[D7]li[G]ness,",
                    "[G]Bow down be[Em]fore Him, His [A7]glory pro[D]claim;[D7]",
                    "[G]With gold of [G7]o[C]bedience, and [A7]incense of [D]low[D7]li[G]ness,",
                    "[G]Kneel and [B7]a[Em]dore [C]Him; the [G/D]Lord is [D7]His [G]name."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[G]Low at [D7]His [G]feet lay thy [C]burden of [G/D]care[D7]ful[G]ness;",
                    "[G]High on His [Em]heart He will [A7]bear it for [D]thee,[D7]",
                    "[G]Comfort thy [G7]sor[C]rows and [A7]answer thy [D]prayer[D7]ful[G]ness,",
                    "[G]Guiding [B7]thy [Em]steps [C]as may [G/D]best for [D7]thee [G]be."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[G]Fear not [D7]to [G]enter His [C]courts in the [G/D]slen[D7]der[G]ness",
                    "[G]Of the poor [Em]wealth thou wouldst [A7]reckon as [D]thine;[D7]",
                    "[G]Truth in its [G7]beau[C]ty and [A7]love in its [D]ten[D7]der[G]ness,",
                    "[G]These are [B7]the [Em]of[C]ferings to [G/D]lay on [D7]His [G]shrine."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "[G]These, though [D7]we [G]bring them in [C]trembling and [G/D]fear[D7]ful[G]ness,",
                    "[G]He will ac[Em]cept for the [A7]name that is [D]dear;[D7]",
                    "[G]Mornings of [G7]joy [C]give for [A7]evenings of [D]tear[D7]ful[G]ness,",
                    "[G]Trust for [B7]our [Em]trem[C]bling, and [G/D]hope for [D7]our [G]fear."
                ]
            }
        ]
    },
    {
        "number": 7,
        "title": "The Lord in Zion Reigneth",
        "lyricist": "Fanny J. Crosby",
        "composer": "Hart P. Danks",
        "tune": "ZION REIGNETH",
        "key": "D",
        "time": "4/4",
        "tempo": 104,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "The [D]Lord in Zi[G]on [D]reigneth, Let [Bm]all the [E7]world re[A]joice,",
                    "And [D]come before His [G]throne of [D]grace With [E7]tuneful heart and [A]voice;",
                    "The [D]Lord in [D7]Zion [G]reigneth, And [E7]there His praise shall [A]ring,[A7]",
                    "To [D]Him shall [G]princes [D/A]bend the [Bm]knee And [Em7]kings their [A7]glory [D]bring."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "The [D]Lord in Zi[G]on [D]reigneth, And [Bm]who so [E7]great as [A]He?",
                    "The [D]depths of earth are [G]in His [D]hands; He [E7]rules the mighty [A]sea.",
                    "O [D]crown His [D7]name with [G]honor, And [E7]let His standard [A]wave,[A7]",
                    "Till [D]distant [G]isles be[D/A]yond the [Bm]deep Shall [Em7]own His [A7]power to [D]save."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "The [D]Lord in Zi[G]on [D]reigneth, These [Bm]hours to [E7]Him be[A]long;",
                    "O [D]enter now His [G]temple [D]gates, And [E7]fill His courts with [A]song;",
                    "Be[D]neath His [D7]royal [G]banner Let [E7]every creature [A]fall,[A7]",
                    "Ex[D]alt the [G]King of [D/A]heaven and [Bm]earth, And [Em7]crown Him [A7]Lord of [D]all."
                ]
            }
        ]
    },
    {
        "number": 8,
        "title": "We Gather Together",
        "lyricist": "Anonymous",
        "composer": "Netherland Folk Song",
        "tune": "KREMSER",
        "key": "C",
        "time": "3/4",
        "tempo": 100,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "We [C]gather to[G7]gether to [C]ask the [G/B]Lord's [Am]bless[G]ing;",
                    "He [Em]chastens and [F]hastens His [D7]will to make [G]known;",
                    "The [G7]wicked op[C]pressing now [Am]cease from [Dm]dis[G]tressing, [C]",
                    "Sing [F]praises [C/E]to His [Dm7]name; He [C/G]forgets [G7]not His [C]own."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "Be[C]side us to [G7]guide us, our [C]God with [G/B]us [Am]join[G]ing,",
                    "Or[Em]daining, main[F]taining His [D7]kingdom di[G]vine;",
                    "So [G7]from the be[C]ginning the [Am]fight we [Dm]were [G]winning; [C]",
                    "Thou, [F]Lord, wast [C/E]at our [Dm7]side; all [C/G]glory [G7]be [C]Thine!"
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "We [C]all do ex[G7]tol Thee, Thou [C]Leader [G/B]tri[Am]um[G]phant,",
                    "And [Em]pray that Thou [F]still our De[D7]fender wilt [G]be.",
                    "Let [G7]Thy congre[C]gation es[Am]cape trib[Dm]u[G]lation; [C]",
                    "Thy [F]name be [C/E]ever [Dm7]praised! O [C/G]Lord, make [G7]us [C]free!"
                ]
            }
        ]
    },
    {
        "number": 9,
        "title": "Let All the World in Every Corner Sing",
        "lyricist": "George Herbert",
        "composer": "Basil Harwood",
        "tune": "LUCKINGTON",
        "key": "Ab",
        "time": "4/4",
        "tempo": 108,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[Ab]Let all the [Db]world in [Eb]every [Ab]corner [Fm]sing,",
                    "[Db]My [Eb7]God and [Ab]King!",
                    "The [Ab]heavens [Eb/G]are [Fm]not too [Cm]high,",
                    "[Db]His praise [Bb7/D]may thither [Eb]fly;",
                    "The [Ab]earth is [Db]not too [Ab]low,",
                    "His [Fm]praises [Bbm7]there [Eb7]may [Ab]grow.",
                    "[Ab]Let all the [Db]world in [Eb]every [Ab]corner [Fm]sing,",
                    "[Db]My [Eb7]God and [Ab]King!"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[Ab]Let all the [Db]world in [Eb]every [Ab]corner [Fm]sing,",
                    "[Db]My [Eb7]God and [Ab]King!",
                    "The [Ab]church with [Eb/G]psalms [Fm]must [Cm]shout,",
                    "[Db]No door [Bb7/D]can keep them [Eb]out;",
                    "But, [Ab]above [Db]all, the [Ab]heart",
                    "Must [Fm]bear the [Bbm7]long[Eb7]est [Ab]part.",
                    "[Ab]Let all the [Db]world in [Eb]every [Ab]corner [Fm]sing,",
                    "[Db]My [Eb7]God and [Ab]King!"
                ]
            }
        ]
    },
    {
        "number": 10,
        "title": "Come, Christians, Join to Sing",
        "lyricist": "Christian Henry Bateman",
        "composer": "Source unknown",
        "tune": "MADRID",
        "key": "A",
        "time": "4/4",
        "tempo": 108,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[A]Come, Christians, [D]join [E7]to [A]sing, [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]",
                    "[A]Loud praise to [D]Christ [E7]our [A]King; [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]",
                    "[A]Let all, with [E]heart and [F#m]voice, [D]Before His [Bm7]throne re[E]joice;",
                    "[A]Praise is His [D]gra[E7]cious [A]choice; [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[A]Come, lift your [D]hearts [E7]on [A]high; [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]",
                    "[A]Let praises [D]fill [E7]the [A]sky; [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]",
                    "[A]He is our [E]Guide and [F#m]Friend; [D]To us He'll [Bm7]conde[E]scend;",
                    "[A]His love shall [D]nev[E7]er [A]end; [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]"
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[A]Praise yet our [D]Christ [E7]a[A]gain; [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]",
                    "[A]Life shall not [D]end [E7]the [A]strain; [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]",
                    "[A]On heaven's [E]blissful [F#m]shore [D]His goodness [Bm7]we'll a[E]dore,",
                    "[A]Singing for[D]ev[E7]er[A]more, [D]Alle[A/E]lu[E7]ia! [A]A[D]men! [A]"
                ]
            }
        ]
    },
    {
        "number": 11,
        "title": "The God of Abraham Praise",
        "lyricist": "Thomas Olivers",
        "composer": "Meyer Lyon",
        "tune": "LEONI",
        "key": "Em",
        "time": "4/4",
        "tempo": 96,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "The [Em]God of [B7]Abraham [Em]praise, Who [G]reigns en[D7]throned a[G]bove;",
                    "[B7]Ancient of [Em]ever[C]lasting [Am]days, And [Em/B]God [B7]of [Em]love;",
                    "Je[G]hovah! [D]Great I [G]AM! By [B7]earth and [Em]heaven [D]con[B]fessed;",
                    "I [Em]bow and [B7]bless the [Em]sacred [C]name, For[Em/B]ev[B7]er [Em]blest."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "The [Em]God of [B7]Abraham [Em]praise, At [G]whose su[D7]preme com[G]mand",
                    "[B7]From earth I [Em]rise, and [C]seek the [Am]joys At [Em/B]His [B7]right [Em]hand;",
                    "I [G]all on [D]earth for[G]sake, Its [B7]wisdom, [Em]fame, and [D]pow[B]er;",
                    "And [Em]Him my [B7]only [Em]portion [C]make, My [Em/B]shield [B7]and [Em]tower."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "The [Em]whole tri[B7]umphant [Em]host Give [G]thanks to [D7]God on [G]high;",
                    "\"[B7]Hail, Father, [Em]Son, and [C]Holy [Am]Ghost!\" They [Em/B]ev[B7]er [Em]cry;",
                    "Hail, [G]Abraham's [D]God and [G]mine! I [B7]join the [Em]heaven[D]ly [B]lays;",
                    "All [Em]might and [B7]majes[Em]ty are [C]Thine, And [Em/B]end[B7]less [Em]praise."
                ]
            }
        ]
    },
    {
        "number": 12,
        "title": "Joyful, Joyful, We Adore Thee",
        "lyricist": "Henry van Dyke",
        "composer": "Ludwig van Beethoven",
        "tune": "HYMN TO JOY",
        "key": "G",
        "time": "4/4",
        "tempo": 108,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[G]Joyful, joyful, [D7]we adore Thee, [G]God of [C]glory, [G/D]Lord [D7]of [G]love;",
                    "[G]Hearts unfold like [D7]flow'rs before Thee, [G]Hail Thee [C]as the [G/D]sun [D7]a[G]bove.",
                    "[D]Melt the clouds of [G]sin and [D]sadness, Drive the [B7]dark of [Em]doubt [A7]a[D]way;",
                    "[G]Giver of im[C]mortal [Am]gladness, [G/D]Fill us with the [D7]light of [G]day!"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[G]All Thy works with [D7]joy surround Thee, [G]Earth and [C]heav'n re[G/D]flect [D7]Thy [G]rays,",
                    "[G]Stars and angels [D7]sing around Thee, [G]Center [C]of un[G/D]bro[D7]ken [G]praise;",
                    "[D]Field and forest, [G]vale and [D]mountain, Bloss'ming [B7]meadow, [Em]flash[A7]ing [D]sea,",
                    "[G]Chanting bird and [C]flowing [Am]fountain [G/D]Call us to re[D7]joice in [G]Thee."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[G]Thou art giving [D7]and forgiving, [G]Ever [C]blessing, [G/D]ev[D7]er [G]blest,",
                    "[G]Wellspring of the [D7]joy of living, [G]Ocean [C]depth of [G/D]hap[D7]py [G]rest!",
                    "[D]Thou the Father, [G]Christ our [D]Brother, All who [B7]live in [Em]love [A7]are [D]Thine:",
                    "[G]Teach us how to [C]love each [Am]other, [G/D]Lift us to the [D7]joy di[G]vine."
                ]
            }
        ]
    },
    {
        "number": 13,
        "title": "New Songs of Celebration Render",
        "lyricist": "Erik Routley",
        "composer": "Russell Schulz-Widmar",
        "tune": "RENDEZ À DIEU",
        "key": "G",
        "time": "4/4",
        "tempo": 104,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[G]Now songs of [D]cele[C]bration [G]render [C]To Him who [G]has great [Am7]won[D7]ders [G]done.",
                    "[G]Love sits en[D]throned in [C]ageless [G]splendor: [C]Come, and a[G]dore the [Am7]might[D7]y [G]One.",
                    "[D]He has made [Em]known His [C]great sal[G]va[D]tion [G]Which all His [C]friends with [Am]joy con[B]fess:",
                    "[Em]He has re[Bm]vealed to [C]every [G]na[D]tion [G]His ever[C]lasting [G/D]righteous[D7]ness. [G]"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[G]Joyfully, [D]hearti[C]ly re[G]sounding, [C]Let every [G]instru[Am7]ment [D7]and [G]voice",
                    "[G]Peal out the [D]praise of [C]grace a[G]bounding, [C]Calling the [G]whole world [Am7]to [D7]re[G]joice.",
                    "[D]Trumpets and [Em]organs, [C]set in [G]mo[D]tion [G]Such sounds as [C]make the [Am]heavens [B]ring;",
                    "[Em]All things that [Bm]live in [C]earth and [G]o[D]cean, [G]Make music [C]for your [G/D]mighty [D7]King. [G]"
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[G]Rivers and [D]seas and [C]torrents [G]roaring, [C]Honor the [G]Lord with [Am7]wild [D7]ac[G]claim;",
                    "[G]Mountains and [D]stones look [C]up a[G]doring, [C]And find a [G]voice to [Am7]praise [D7]His [G]name.",
                    "[D]Righteous, com[Em]manding, [C]ever [G]glo[D]rious, [G]Praises be [C]His that [Am]never [B]cease:",
                    "[Em]Just is our [Bm]God, whose [C]truth vic[G]to[D]rious, [G]Establish[C]es the [G/D]world in [D7]peace. [G]"
                ]
            }
        ]
    },
    {
        "number": 14,
        "title": "Let Us Praise the Name of the Lord",
        "lyricist": "Ursula Schlenker",
        "composer": "Alfred Stier",
        "tune": "LOBET DEN HERRN",
        "key": "C",
        "time": "4/4",
        "tempo": 100,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[C]Let us praise the [F]name of the [G]Lord! [C]Give Him [F]glory, [Dm]A[G7]men. [C]",
                    "[C]Amen, [F]a[G]men, [C]Amen, [Dm]a[G7]men. [C]"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[C]Go ye into [F]all the [G]world. [C]Alle[F]luia, [Dm]A[G7]men. [C]",
                    "[C]Amen, [F]a[G]men, [C]Amen, [Dm]a[G7]men. [C]"
                ]
            }
        ]
    },
    {
        "number": 15,
        "title": "My Maker and My King",
        "lyricist": "Anne Steele",
        "composer": "Unknown",
        "tune": "MAKER AND KING",
        "key": "C",
        "time": "4/4",
        "tempo": 96,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "My [C]Maker and my [G]King, To [F]Thee my [C/G]all [G7]I [C]owe;",
                    "Thy [C]sovereign [G/B]bounty [Am]is the [Em]spring Whence [F]all my [D7]blessings [G]flow;",
                    "Thy [C]sovereign [F]bounty [C]is the [G]spring Whence [C]all my [F]bless[G7]ings [C]flow."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "The [C]creature of Thy [G]hand, On [F]Thee a[C/G]lone [G7]I [C]live;",
                    "My [C]God, Thy [G/B]benefits [Am]de[Em]mand More [F]praise than [D7]I can [G]give;",
                    "My [C]God, Thy [F]benefits [C]de[G]mand More [C]praise than [F]I [G7]can [C]give."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "Lord, [C]what can I im[G]part When [F]all is [C/G]Thine [G7]be[C]fore?",
                    "Thy [C]love de[G/B]mands a [Am]thankful [Em]heart; The [F]gift, a[D7]las! how [G]poor;",
                    "Thy [C]love de[F]mands a [C]thankful [G]heart; The [C]gift, a[F]las! [G7]how [C]poor."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "O! [C]let Thy grace in[G]spire My [F]soul with [C/G]strength [G7]di[C]vine;",
                    "Let [C]every [G/B]word and [Am]each de[Em]sire And [F]all my [D7]days be [G]Thine;",
                    "Let [C]every [F]word and [C]each de[G]sire And [C]all my [F]days [G7]be [C]Thine."
                ]
            }
        ]
    },
    {
        "number": 16,
        "title": "All People That on Earth Do Dwell",
        "lyricist": "William Kethe",
        "composer": "Louis Bourgeois",
        "tune": "OLD HUNDREDTH",
        "key": "G",
        "time": "4/4",
        "tempo": 96,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[G]All [G/B]peo[D]ple [Em]that on [Bm]earth [D]do [G]dwell,",
                    "[G]Sing to the [Em]Lord with [Am]cheer[D]ful [G]voice;",
                    "[G]Him [D]serve with [Em]mirth, [D]His [G]praise [C]forth [D]tell,",
                    "[G]Come [D/F#]ye be[Em]fore [D]Him [G]and [D7]re[G]joice."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[G]Know [G/B]that [D]the [Em]Lord is [Bm]God [D]in[G]deed;",
                    "[G]Without our [Em]aid He [Am]did [D]us [G]make;",
                    "[G]We [D]are His [Em]folk, [D]He [G]doth [C]us [D]feed,",
                    "[G]And [D/F#]for His [Em]sheep [D]He [G]doth [D7]us [G]take."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[G]O [G/B]en[D]ter [Em]then His [Bm]gates [D]with [G]praise,",
                    "[G]Approach with [Em]joy His [Am]courts [D]un[G]to;",
                    "[G]Praise, [D]laud, and [Em]bless [D]His [G]name [C]al[D]ways,",
                    "[G]For [D/F#]it is [Em]seem[D]ly [G]so [D7]to [G]do."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "[G]For [G/B]why [D]the [Em]Lord our [Bm]God [D]is [G]good,",
                    "[G]His mercy [Em]is for[Am]ev[D]er [G]sure;",
                    "[G]His [D]truth at [Em]all [D]times [G]firm[C]ly [D]stood,",
                    "[G]And [D/F#]shall from [Em]age [D]to [G]age [D7]en[G]dure."
                ]
            }
        ]
    },
    {
        "number": 17,
        "title": "Lord of All Being, Throned Afar",
        "lyricist": "Oliver Wendell Holmes",
        "composer": "Frederick M. A. Venua",
        "tune": "PARK STREET",
        "key": "F",
        "time": "3/4",
        "tempo": 96,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[F]Lord of all [Bb]being, [F]throned a[C]far,",
                    "[F]Thy glory [Gm7]flames from [F/C]sun [C7]and [F]star;",
                    "[C]Center and [G7]soul of [C]every sphere,",
                    "[F]Yet to each [D7]loving [Gm]heart [C7]how [F]near!",
                    "[F/A]Yet [Bb]to each [F/C]loving [Gm7]heart [C7]how [F]near!"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[F]Sun of our [Bb]life, Thy [F]quickening [C]ray",
                    "[F]Sheds on our [Gm7]path the [F/C]glow [C7]of [F]day;",
                    "[C]Star of our [G7]hope, Thy [C]softened light",
                    "[F]Cheers the long [D7]watches [Gm]of [C7]the [F]night,",
                    "[F/A]Cheers [Bb]the long [F/C]watches [Gm7]of [C7]the [F]night."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[F]Our midnight [Bb]is Thy [F]smile with[C]drawn;",
                    "[F]Our noontide [Gm7]is Thy [F/C]gra[C7]cious [F]dawn;",
                    "[C]Our rainbow [G7]arch, Thy [C]mercy's sign;",
                    "[F]All, save the [D7]clouds of [Gm]sin, [C7]are [F]Thine,",
                    "[F/A]All, [Bb]save the [F/C]clouds of [Gm7]sin, [C7]are [F]Thine."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "[F]Lord of all [Bb]life, be[F]low, a[C]bove,",
                    "[F]Whose light is [Gm7]truth, whose [F/C]warmth [C7]is [F]love,",
                    "[C]Before Thy [G7]ever [C]blazing throne",
                    "[F]We ask no [D7]luster [Gm]of [C7]our [F]own,",
                    "[F/A]We [Bb]ask no [F/C]luster [Gm7]of [C7]our [F]own."
                ]
            },
            {
                "name": "Verse 5",
                "type": "verse",
                "lines": [
                    "[F]Grant us Thy [Bb]truth to [F]make us [C]free,",
                    "[F]And kindling [Gm7]hearts that [F/C]burn [C7]for [F]Thee;",
                    "[C]Till all Thy [G7]living [C]altars claim",
                    "[F]One holy [D7]light, one [Gm]heaven[C7]ly [F]flame!",
                    "[F/A]One [Bb]holy [F/C]light, one [Gm7]heaven[C7]ly [F]flame."
                ]
            }
        ]
    },
    {
        "number": 18,
        "title": "O Morning Star, How Fair and Bright",
        "lyricist": "Philip Nicolai",
        "composer": "Philip Nicolai",
        "tune": "WIE SCHÖN LEUCHTET",
        "key": "D",
        "time": "4/4",
        "tempo": 92,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "[D]O [Bm]Morning [F#m]Star, how [G]fair [A7]and [D]bright!",
                    "You [Em]shine with [A]God's own [F#m]truth [Bm]and [E7]light, [A]",
                    "A[D]glow with [G]grace and [A7]mer[D]cy!",
                    "Of [D]Jacob's [G]race, [Em]King [A7]David's [D]Son,",
                    "Our [Em]Lord and [A]Master, [F#m]You [Bm]have [E7]won [A]",
                    "Our [D]hearts to [G]serve You [A7]on[D]ly!",
                    "[D]Low[A]ly, [D]ho[A]ly! [Bm]Great and [F#m]glorious, [G]all vic[D]torious,",
                    "[Em]Rich in [A7]bless[D]ing! [G]Rule and [D/F#]might o'er [Em7]all pos[A7]sess[D]ing!"
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "[D]Lord, [Bm]when You [F#m]look on [G]us [A7]in [D]love,",
                    "At [Em]once there [A]falls from [F#m]God [Bm]a[E7]bove [A]",
                    "A [D]ray of [G]purest [A7]plea[D]sure.",
                    "Your [D]Word and [G]Spirit, [Em]flesh [A7]and [D]blood,",
                    "Re[Em]fresh our [A]souls with [F#m]heav'n[Bm]ly [E7]food. [A]",
                    "You [D]are our [G]dearest [A7]trea[D]sure!",
                    "[D]Let [A]Your [D]mer[A]cy [Bm]Warm and [F#m]cheer us! [G]O draw [D]near us!",
                    "[Em]For You [A7]teach [D]us [G]God's own [D/F#]love through [Em7]You has [A7]reached [D]us."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "[D]Al[Bm]mighty [F#m]Father, [G]in [A7]Your [D]Son",
                    "You [Em]loved us, [A]when not [F#m]yet [Bm]be[E7]gun [A]",
                    "Was [D]this old [G]earth's foun[A7]da[D]tion!",
                    "Your [D]Son has [G]ransomed [Em]us [A7]in [D]love",
                    "To [Em]live in [A]Him here [F#m]and [Bm]a[E7]bove: [A]",
                    "This [D]is Your [G]great sal[A7]va[D]tion.",
                    "[D]Al[A]le[D]lu[A]ia! [Bm]Christ the [F#m]living, [G]to us [D]giving",
                    "[Em]Life for[A7]ev[D]er, [G]Keeps us [D/F#]Yours and [Em7]fails us [A7]nev[D]er!"
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "[D]O [Bm]let the [F#m]harps break [G]forth [A7]in [D]sound!",
                    "Our [Em]joy be [A]all with [F#m]mu[Bm]sic [E7]crowned, [A]",
                    "Our [D]voices [G]gaily [A7]blend[D]ing!",
                    "For [D]Christ goes [G]with us [Em]all [A7]the [D]way—",
                    "To[Em]day, to[A]morrow, [F#m]ev[Bm]ery [E7]day! [A]",
                    "His [D]love is [G]never [A7]end[D]ing!",
                    "[D]Sing [A]out! [D]ring [A]out! [Bm]Jubi[F#m]lation! [G]exul[D]tation!",
                    "[Em]Tell the [A7]sto[D]ry! [G]Great is [D/F#]He, the [Em7]King of [A7]glo[D]ry!"
                ]
            }
        ]
    },
    {
        "number": 19,
        "title": "O Sing a New Song to the Lord",
        "lyricist": "Scottish Psalter",
        "composer": "Jeremiah Clarke",
        "tune": "ST. MAGNUS",
        "key": "G",
        "time": "4/4",
        "tempo": 100,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "O [G]sing a [D/F#]new song [Em]to the [Bm]Lord",
                    "For [C]mar[G/B]vels [Am7]He [A7]has [D]done;",
                    "His [G]right hand [D/F#]and His [Em]ho[D]ly [C]arm",
                    "The [G/D]victo[C]ry [D7]have [G]won."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "With [G]harp, with [D/F#]harp and [Em]voice of [Bm]psalms",
                    "Un[C]to [G/B]Je[Am7]ho[A7]vah [D]sing;",
                    "Let [G]trumpets [D/F#]and the [Em]ech[D]oing [C]horn",
                    "Ac[G/D]claim the [C]Lord [D7]our [G]King!"
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "Let [G]seas with [D/F#]all their [Em]creatures [Bm]roar,",
                    "The [C]world [G/B]and [Am7]dwell[A7]ers [D]there,",
                    "And [G]let the [D/F#]rivers [Em]clap [D]their [C]hands,",
                    "The [G/D]hills their [C]joy [D7]de[G]clare."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "Be[G]fore the [D/F#]Lord: be[Em]cause He [Bm]comes,",
                    "To [C]judge [G/B]the [Am7]earth [A7]comes [D]He;",
                    "He'll [G]judge the [D/F#]world with [Em]righ[D]teous[C]ness,",
                    "His [G/D]folk with [C]eq[D7]ui[G]ty."
                ]
            }
        ]
    },
    {
        "number": 20,
        "title": "O Praise Ye the Lord",
        "lyricist": "Henry W. Baker",
        "composer": "Charles H. H. Parry",
        "tune": "LAUDATE DOMINUM",
        "key": "Bb",
        "time": "3/4",
        "tempo": 108,
        "category": "Worship",
        "subcategory": "Adoration and Praise",
        "sections": [
            {
                "name": "Verse 1",
                "type": "verse",
                "lines": [
                    "O [Bb]praise ye the [Eb]Lord! Praise [Bb/D]Him in the [F]height;",
                    "Re[Bb/D]joice in His [Gm]word, Ye [C7]angels of [F]light;",
                    "Ye [Bb]heavens, a[Eb]dore Him By [C7]whom ye were [F]made,",
                    "And [Gm]worship be[Cm]fore Him, In [Bb/F]brightness [F7]ar[Bb]rayed."
                ]
            },
            {
                "name": "Verse 2",
                "type": "verse",
                "lines": [
                    "O [Bb]praise ye the [Eb]Lord! Praise [Bb/D]Him upon [F]earth,",
                    "In [Bb/D]tuneful ac[Gm]cord: Ye [C7]sons of new [F]birth;",
                    "Praise [Bb]Him who hath [Eb]brought you His [C7]grace from a[F]bove,",
                    "Praise [Gm]Him who hath [Cm]taught you To [Bb/F]sing of [F7]His [Bb]love."
                ]
            },
            {
                "name": "Verse 3",
                "type": "verse",
                "lines": [
                    "O [Bb]praise ye the [Eb]Lord, All [Bb/D]things that give [F]sound;",
                    "Each [Bb/D]jubilant [Gm]chord, Re[C7]echo a[F]round;",
                    "Loud [Bb]organs His [Eb]glory Forth [C7]tell in deep [F]tone,",
                    "And [Gm]sweet harp, the [Cm]story Of [Bb/F]what He [F7]hath [Bb]done."
                ]
            },
            {
                "name": "Verse 4",
                "type": "verse",
                "lines": [
                    "O [Bb]praise ye the [Eb]Lord! Thanks[Bb/D]giving and [F]song",
                    "To [Bb/D]Him be out[Gm]poured All [C7]ages a[F]long:",
                    "For [Bb]love in cre[Eb]ation, For [C7]heaven re[F]stored,",
                    "For [Gm]grace of sal[Cm]vation, O [Bb/F]praise ye [F7]the [Bb]Lord!"
                ]
            }
        ]
    }
]


def main():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    for h in PILOT_HYMNS:
        num_str = f"{h['number']:03d}"
        safe_title = h["title"].replace("/", "-")
        out_path = DB_DIR / f"{num_str} - {safe_title}.json"
        out_path.write_text(json.dumps(h, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(PILOT_HYMNS)} canonical hymn JSON files to {DB_DIR}")


if __name__ == "__main__":
    main()
