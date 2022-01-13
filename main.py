import discord
import whostherebot
import os
from dotenv import load_dotenv

def main():
    load_dotenv()

    myBot = whostherebot.WhosThereBot(os.getenv('TOKEN'))
    myBot.runMainLoop()


if __name__ == "__main__":
    main()

