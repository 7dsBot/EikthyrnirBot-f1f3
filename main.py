import sys
from DeerBot import DeerBot

if __name__ == "__main__":
    bot = DeerBot()
    bot.run(*sys.argv[1:])
