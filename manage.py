#!/usr/bin/env python3
from datetime import date
import argparse
import sys
import os
import settings
import logging
from telegram import Bot, Update, InputMediaDocument
import time
from Database import Database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser("Manage your uni notes")
    parser.add_argument("strings", metavar="string", type=str, nargs="*", help="name of the file where you took your notes")
    parser.add_argument("-c", "--convert", action="store_true", help="Convert the selected .md files to .pdf")
    parser.add_argument("-a", "--all", action="store_true", help="Convert all the .md files in the subdirs of the working directory into .pdf")
    args = parser.parse_args()
    print(args)
    try:
        if args.strings and not args.convert:
            for name in args.strings:
                with open(f"{name}/{name}.md", "a+") as file:
                    file.write("<h3><p style=\"text-align: right\">" + date.today().strftime("%d/%m/%Y")+ "</p></h3>\n\n")
        if args.convert and (args.all or not args.strings):
            os.system("./script.sh")
        elif args.convert and args.strings:
            basedir = os.getcwd()
            basedir = basedir if basedir[-1] == '/' else basedir + '/'
            for name in args.strings:
                os.system(f"pandoc -o {basedir}{name}/{name}.pdf {basedir}{name}/{name}.md")
    except IndexError:
        print("No argument supplied", file=sys.stderr)
    except FileNotFoundError:
        print(f"{name}/{name}.md", file=sys.stderr)
    delete_messages()
    upload()

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def delete_messages():
    bot = Bot(settings.TOKEN)
    db = Database()
    entries = db.load_entries()
    print("######################## ENTRIES")
    print(entries)
    print("########################")

    for tuple in entries:
        try:
            bot.delete_message(settings.CHAT_ID, tuple[0])
        except:
            pass
# ---------------- The actual meat --------------------

def upload():
    """Start the bot."""
    bot = Bot(settings.TOKEN)
    db = Database()
    updated_docs_id = None
    for name, full_name in settings.NAMES.items():
        filename = f"{name}/{name}.pdf"
        try:
            with open(filename, "rb") as file:
                print(f"Uploading {filename}")
                updated_docs_id = bot.send_document(settings.CHAT_ID, file, filename=f"{filename.split('/')[1]}",
                    caption=f"{full_name} | Upload date: {time.ctime(os.path.getmtime(settings.BASEDIR + filename))}").message_id
                db.update(updated_docs_id, name)
        except Exception as e:
            print(e)

if __name__ == '__main__':
	main()
