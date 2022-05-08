import lightbulb
from bs4 import BeautifulSoup
import requests
import hikari
bot = lightbulb.BotApp(
    token='',
    default_enabled_guilds=971049013203845150
)


class Champ:
    def __init__(self, primary, secondary, stats) -> None:
        self.primary = primary
        self.secondary = secondary
        self.stats = stats

    def getRunes(self):
        return (self.primary + "\n" + self.secondary + "\n" + self.stats)


def removelist(page, runes):  # removes the list and puts it in a string
    str = runes[0]
    for rune in runes[1:]:
        str = str + ' \n ' + rune

    query = str
    stopwords = ['The', 'Rune', 'Shard', 'Keystone']  # removing these words
    querywords = query.split()

    # removes the words from the string
    resultwords = [word for word in querywords if word not in stopwords]
    result = ' '.join(resultwords)

    l = [
        ("Absolute Focus", "<:absolutefocus:972593966396637225>"),
        ("Aftershock", "<:aftershock:972594579855536188>"),
        ("Approach Velocity", "<:approachvelocity:972594579733893200>"),
        ("Arcane Comet", "<:arcanecomet:972594579905867786>"),
        ("Biscuit Delivery", "<:biscuitdelivery:972594579863912538>"),
        ("Bone Plating", "<:boneplating:972594579763240990>"),
        ("Celerity", "<:celerity:972594579855515668>"),
        ("Cheap Shot", "<:cheapshot:972591275826085988>"),
        ("Conditioning", "<:conditioning:972594579834564708>"),
        ("Conqueror", "<:conqueror:972597065169395802>"),
        ("Cosmic Insight", "<:cosmicinsight:972594579842928760>"),
        ("Coup de Grace", "<:coupdegrace:972594579859722300>"),
        ("Cut Down", "<:cutdown:972594579507413033>"),
        ("Dark Harvest", "<:darkharvest:972591276136484954>"),
        ("Demolish", "<:demolish:972594811590815834>"),
        ("Electrocute", "<:electrocute:972594579901661196>"),
        ("Eyeball Collection", "<:eyeballcollection:972591275800940554>"),
        ("First Strike", "<:firststrike:972594579981369374>"),
        ("Fleet Footwork", "<:fleetfootwork:972594579918450709>"),
        ("Font of Life", "<:fontoflife:972594579842937003>"),
        ("Future's Market", "<:futuresmarket:972594579826155560>"),
        ("Gathering Storm", "<:gatheringstorm:972594579880706118>"),
        ("Ghost Poro", "<:ghostporo:972594579842953286>"),
        ("Glacial Augment", "<:glacialaugment:972594579893276682>"),
        ("Grasp of the Undying", "<:graspoftheundying:972594579914248202>"),
        ("Guardian", "<:guardian:972594579884892250>"),
        ("Hail of Blades", "<:hailofblades:972594580044279828>"),
        ("Hextech Flashtraption", "<:hextechflashtraption:972594580002316319>"),
        ("Ingenious Hunter", "<:ingenioushunter:972594580023308338>"),
        ("Last Stand", "<:laststand:972594579947786260>"),
        ("Legend: Alacrity", "<:legendalacrity:972594580014907462>"),
        ("Legend: Bloodline", "<:legendbloodline:972594580232994846>"),
        ("Legend: Tenacity", "<:legendtenacity:972594579700338728>"),
        ("Lethal Tempo", "<:lethaltempo:972595166173102130>"),
        ("Magical Footwear", "<:magicalfootwear:972595166227611698>"),
        ("Manaflow Band", "<:manaflowband:972595166185660476>"),
        ("Minion Dematerializer", "<:miniondematerializer:972595166097592340>"),
        ("Nimbus Cloak", "<:nimbuscloak:972595166168891412>"),
        ("Nullifying Orb", "<:nullifyingorb:972595166240190506>"),
        ("Overgrowth", "<:overgrowth:972595166064042014>"),
        ("Overheal", "<:overheal:972595166080811038>"),
        ("Perfect Timing", "<:perfecttiming:972595166223417394>"),
        ("Phase Rush", "<:phaserush:972595307110092810>"),
        ("Predator", "<:predator:972595166269550602>"),
        ("Presence of Mind", "<:presenceofmind:972595166122737664>"),
        ("Press the Attack", "<:presstheattack:972595166244372560>"),
        ("Relentless Hunter", "<:relentlesshunter:972595166152122398>"),
        ("Revitalize", "<:revitalize:972595166324084847>"),
        ("Scorch", "<:scorch:972595633204633670>"),
        ("Second Wind", "<:secondwind:972597076737261598>"),
        ("Shield Bash", "<:shieldbash:972597071481802803>"),
        ("Sudden Impact", "<:suddenimpact:972599188623851540>"),
        ("Summon Aery", "<:summonaery:972599188523200512>"),
        ("Taste of Blood", "<:tasteofblood:972599188196044851>"),
        ("Time Warp Tonic", "<:timewarptonic:972599188728729692>"),
        ("Transcendence", "<:transcendence:972599188636438578>"),
        ("Treasure Hunter", "<:treasurehunter:972599188611297290>"),
        ("Triumph", "<:Triumph:972599188531597372>"),
        ("Ultimate Hunter", "<:ultimatehunter:972591275763195995>"),
        ("Unflinching", "<:unflinching:972599188607094884>"),
        ("Unsealed Spellbook", "<:unsealedspellbook:972599188623859802>"),
        ("Waterwalking", "<:waterwalking:972599188636442754>"),
        ("Zombie Ward", "<:zombieward:972599188443525290>"),
        ("Attack Speed", "<:attackspeed:972600670366597130>"),
        ("Adaptive Force", "<:adaptiveforce:972600670391771216>"),
        ("Armor", "<:armor:972600670395969566>"),
        ("Scaling CDR", "<:cooldown:972600670458875924>"),
        ("Magic Resist", "<:magicresist:972600670270132224>"),
        ("Scaling Bonus Health", "<:health:972600670261739660>"),

    ]
    for word, emoji in l:
        result = result.replace(word, emoji)

    return (page + ": \n" + result)


def runes(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    # gets the primary runes and secondary runes
    primarytree = soup.find('div', class_='perk-style-title').text
    secondarytree = soup.find('div', class_='secondary-tree').text
    # gets the main rune and the other runes that follow and does not allow duplicates
    keystone = [a.find('img').get('alt') for a in soup.find_all(
        "div", {"class": "perk keystone perk-active"}) if a.find('img')]

    actualrunes = [a.find('img').get('alt') for a in soup.find_all(
        "div", {"class": "perk perk-active"}) if a.find('img')]

    statsrunes = [a.find('img').get('alt') for a in soup.find_all(
        "div", {"class": "shard shard-active"}) if a.find('img')][:3]

    primary = removelist(primarytree, keystone[1:] + actualrunes[:3])
    secondary = removelist(secondarytree, actualrunes[3:5])
    stats = removelist('Stats', statsrunes)

    champ1 = Champ(primary, secondary, stats)

    return champ1.getRunes()


@bot.command
@lightbulb.option('champion', 'champion name')
@lightbulb.command("rift", "Runes for rift")
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_rift(ctx: lightbulb.SlashContext) -> None:
    champion = ctx.options.champion.capitalize()
    embed = hikari.Embed(
        title="Chanaram Bot",
        description="Highest win rate runes for " + champion,
        colour='#2ECC71',
        url='https://u.gg/lol/champions/' + champion + '/build')
    embed.add_field("Runes", runes(
        link='https://u.gg/lol/champions/' + champion + '/build'))
    embed.set_thumbnail(
        "http://ddragon.leagueoflegends.com/cdn/11.7.1/img/champion/" + champion + ".png")
    embed.set_footer("Runes brought to you by Chanaram")
    await ctx.respond(embed)


@bot.command
@lightbulb.option('champion', 'champion name')
@lightbulb.command("aram", "Runes for aram")
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_aram(ctx: lightbulb.SlashContext) -> None:
    champion = ctx.options.champion.capitalize()
    link = 'https://u.gg/lol/champions/aram/' + champion + '-aram'
    embed = hikari.Embed(
        title="Chanaram Bot",
        description="Highest win rate runes for " + champion,
        colour='#3498DB',
        url='https://u.gg/lol/champions/aram/' + champion + '-aram')
    embed.add_field("Runes", runes(link))
    embed.set_thumbnail(
        "http://ddragon.leagueoflegends.com/cdn/11.7.1/img/champion/" + champion + ".png")
    embed.set_footer("Runes brought to you by Chanaram")
    await ctx.respond(embed)


bot.run()
