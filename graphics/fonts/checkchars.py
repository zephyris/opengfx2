#https://pastebin.com/DZi5xsE2
#https://discordapp.com/channels/142724111502802944/337701432230805505/1187014122810920981
import glob
for c in sorted(set(''.join(open(f).read() for f in glob.glob('lang/*')))):
    print(hex(ord(c)), c)