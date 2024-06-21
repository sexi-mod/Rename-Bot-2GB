import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import roheshbots
from config import Config, Txt  

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await roheshbots.add_user(client, message)
                
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton('Developer 🔥', url='https://t.me/+M3VR6_Ai50lhMzk0')],
        [InlineKeyboardButton('JOIN ALL FIRST', callback_data='join_telegram')],
    ])
    
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 

    if data == "join_telegram":
        await query.answer()
        await query.message.reply_text('❌JOIN ALL TELEGRAM FIRST')

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚡ 4GB Rename Bot", url="https://t.me/Rohesh_Bots")],
                [InlineKeyboardButton("🔒 Close", callback_data="close"),
                 InlineKeyboardButton("◀️ Back", callback_data="start")]
            ])            
        )

    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤖 More Bots", url="https://t.me/Rohesh_Bots")],
                [InlineKeyboardButton("🔒 Close", callback_data="close"),
                 InlineKeyboardButton("◀️ Back", callback_data="start")]
            ])            
        )

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

@Client.on_message(filters.private & filters.command(["donate", "d"]))
async def donate(client, message):
    text = Txt.DONATE_TXT
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔰 Admin", url="https://t.me/Rohesh_Gavit"), 
         InlineKeyboardButton("✖️ Close", callback_data="close")]
    ])
    await message.reply_text(text=text, reply_markup=keyboard)
