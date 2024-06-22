import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import roheshbots  # Assuming roheshbots is correctly imported
from config import Config, Txt  

# Initialize Pyrogram client
app = Client("my_bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    try:
        await roheshbots.add_user(client, message)  # Assuming this function adds the user to your database
    except Exception as e:
        print(f"Error adding user: {e}")
    
    # Define initial buttons
    buttons = [
        [InlineKeyboardButton('♨️ Updates', url='https://t.me/Rohesh_Bots'),
         InlineKeyboardButton('⭕️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/Rohesh_Bots')],
        [InlineKeyboardButton('💢 About', callback_data='about'),
         InlineKeyboardButton('🥹 Help', callback_data='help')],
        [InlineKeyboardButton('📹 Watch Video', callback_data='watch_video')],  # New button for sending videos
        [InlineKeyboardButton("👨‍💻 Developer", url='https://t.me/Rohesh_Gavit')]
    ]
    
    button_markup = InlineKeyboardMarkup(buttons)
    
    try:
        if Config.START_PIC:
            await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button_markup)
        else:
            await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button_markup, disable_web_page_preview=True)
    except Exception as e:
        print(f"Error sending start message: {e}")

@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('♨️ Updates', url='https://t.me/Rohesh_Bots'),
                 InlineKeyboardButton('⭕️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/Rohesh_Bots')],
                [InlineKeyboardButton('💢 About', callback_data='about'),
                 InlineKeyboardButton('🥹 Help', callback_data='help')],
                [InlineKeyboardButton('📹 Watch Video', callback_data='watch_video')],  # New button for sending videos
                [InlineKeyboardButton("👨‍💻 Developer", url='https://t.me/Rohesh_Gavit')]
            ])
        )
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
        except Exception as e:
            print(f"Error deleting message: {e}")
    elif data == "watch_video":
        video_url = 'https://t.me/seedhe_maut/2740'  # Provided Telegram video link
        caption = "Check out this video from Seedhe Maut!"  # Optional caption for the video
        
        # Send the video
        try:
            await client.send_video(chat_id=query.message.chat.id, video=video_url, caption=caption)
        except Exception as e:
            print(f"Error sending video: {e}")

# Run the application
if __name__ == "__main__":
    app.run()
