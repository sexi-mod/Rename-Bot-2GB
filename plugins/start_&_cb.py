import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import roheshbots
from config import Config, Txt  

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    
    # Check if the user has already joined the required Telegram group
    if not await has_joined_telegram_group(client, message.chat.id):
        await message.reply_text("Please join our Telegram group to start using the bot.")
        return
    
    await roheshbots.add_user(client, message)
                
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton('Developer 🔥', url='https://t.me/+M3VR6_Ai50lhMzk0')],
        [InlineKeyboardButton('Promoter 🔥', callback_data='join_telegram')],
        [InlineKeyboardButton('Bottom Button', callback_data='bottom_button')],
    ])
    
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

async def has_joined_telegram_group(client, chat_id):
    # Implement logic to check if user is in the group
    try:
        chat_member = await client.get_chat_member(Config.TELEGRAM_GROUP_ID, chat_id)
        return True if chat_member.status in ["member", "administrator", "creator"] else False
    except Exception as e:
        print(f"Error checking group membership: {e}")
        return False

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 

    if data == "join_telegram":
        if await has_joined_telegram_group(client, query.message.chat.id):
            await query.answer()
            await query.message.reply_text('You have already joined the Telegram group.')
        else:
            await query.answer()
            await query.message.reply_text('Please join our Telegram group to continue using the bot.')

    elif data == "bottom_button":
        await query.answer()
        await query.message.reply_text('You clicked the bottom button.')

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
