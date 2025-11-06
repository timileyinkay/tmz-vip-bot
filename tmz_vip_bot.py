import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.parsemode import ParseMode
from datetime import datetime, timedelta
from flask import Flask

# Bot Configuration - Use environment variables for deployment
BOT_TOKEN = os.environ.get('BOT_TOKEN', "7703532839:AAG5yNnTAye8zmV58MnWLnuorBg8gaFpbB0")
ADMIN_USER_ID = int(os.environ.get('ADMIN_USER_ID', "6011041717"))
VIP_GROUP_ID = os.environ.get('VIP_GROUP_ID', "-1002750986636")  # Add your group ID here
VIP_GROUP_LINK = "https://t.me/TMZBRAND_VIP_OFFICIAL"  # VIP group link
PORT = int(os.environ.get('PORT', 8080))

# Store user data and registration count
user_data = {}
registered_users = set()
MAX_REGISTRATIONS = 10

# Store users who have already been messaged in groups to prevent spam
messaged_in_groups = set()

# Set competition end date and time
COMPETITION_END_TIME = datetime(2024, 12, 25, 22, 0, 0)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def is_competition_active():
    """Check if competition is still active based on end time"""
    return datetime.now() < COMPETITION_END_TIME

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    # Check if this is a group message and we've already replied
    if update.message.chat.type in ['group', 'supergroup']:
        if user.id in messaged_in_groups:
            return  # Don't reply again in groups
        messaged_in_groups.add(user.id)
    
    if not is_competition_active():
        update.message.reply_text(
            "🎯 *Competition Complete!* 🎯\n\n"
            "✨ *Thank you for your interest!* ✨\n\n"
            "This VIP Quiz Competition has now concluded. Our amazing participants have been amazing! 🏆\n\n"
            "🌟 *Stay tuned for our next exciting competition!* 🌟\n"
            "We'll be back with more fun and bigger prizes! 💫",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        update.message.reply_text(
            "🚫 *Registration Full!* 🚫\n\n"
            "😮 Wow! All 10 VIP spots have been filled! \n\n"
            "💔 We're sorry you missed this one, but don't worry!\n\n"
            "⭐ *Follow us for future competitions* ⭐\n"
            "We'll be hosting more exciting quizzes soon! 🎉",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    welcome_text = """
🎊 *WELCOME TO TMZ BRAND VIP FUN QUIZ COMPETITION!* 🎊

🔥 *THIS IS FOR THE BRAVE AND BRILLIANT!* 🔥
*Only if you're ready to showcase your smarts and win big!* 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💼 *COMPETITION DETAILS:*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 *Entry Fee:* ₦2,000
🏦 *Bank:* OPAY 
👤 *Account Name:* OLUWATOBILOBA KEHINDE
🔢 *Account Number:* 8079304530

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 *AMAZING PRIZES AWAITING YOU!* 🏆
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 *First Place:* ₦10,000 💰
🥈 *Second Place:* ₦5,000 💵  
🥉 *Third Place:* ₦5,000 💸

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 *Competition Ends:* {end_time}

🎯 *QUICK FACTS:*
• 🎮 We use *mentimeter.com* for super fun interactive sessions!
• 👥 Only *10 VIP participants* will be selected
• ⏰ First to complete registration gets priority!
• 🎁 Everyone gets a chance to shine!

💫 *Ready to join the excitement?* 
*This could be your moment to shine!* ✨
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    keyboard = [[InlineKeyboardButton("💰 I'VE PAID - SUBMIT PROOF 🎯", callback_data="paid_confirmation")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def handle_paid_confirmation(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "⏰ *Competition Closed!* ⏰\n\n"
            "This amazing quiz has ended. But don't worry! 🌈\n\n"
            "🌟 *More exciting competitions coming soon!* 🌟\n"
            "Stay connected with us for future opportunities! 🎉",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    payment_instructions = """
✅ *PAYMENT INSTRUCTIONS* ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💳 *BANK DETAILS FOR PAYMENT:*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏦 *Bank:* OPAY 
👤 *Account Name:* OLUWATOBILOBA KEHINDE
🔢 *Account Number:* 8079304530
💵 *Amount:* ₦2,000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 *Competition Ends:* {end_time}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 *FOLLOW THESE SIMPLE STEPS:*
1️⃣ Make payment to the account above
2️⃣ Take a clear screenshot 📸
3️⃣ Make sure all details are visible
4️⃣ Upload the screenshot here

💡 *PRO TIPS FOR FAST APPROVAL:*
• Ensure screenshot is clear and bright ✨
• Show transaction details clearly
• No edits or modifications please

🚀 *WHAT HAPPENS NEXT?*
• We'll verify your payment quickly ⚡
• You'll get VIP group access instantly 🎉
• Ready to compete and win! 🏆

🎮 *ABOUT OUR QUIZ PLATFORM:*
• We use *mentimeter.com* - super fun and interactive! 🎯
• No downloads needed - works on any device 📱💻
• Real-time leaderboard and excitement! 🎊

🌟 *We're excited to have you join us!* 🌟
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    query.edit_message_text(payment_instructions, parse_mode=ParseMode.MARKDOWN)

def handle_payment_proof(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    if not is_competition_active():
        update.message.reply_text(
            "⏰ *Competition Complete!* ⏰\n\n"
            "This exciting quiz has ended. Thank you for your interest! 🙏\n\n"
            "🌈 *Stay tuned for our next amazing competition!* 🌈\n"
            "We promise it will be worth the wait! 💫",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        update.message.reply_text(
            "😮 *All Spots Filled!* 😮\n\n"
            "Wow! All 10 VIP spots have been taken! 🚀\n\n"
            "💔 We're sorry you missed out this time.\n\n"
            "⭐ *But don't worry!* ⭐\n"
            "Follow us for future exciting opportunities! 🎊\n\n"
            "🌟 Your enthusiasm is appreciated! 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if user.id in registered_users:
        update.message.reply_text(
            "🎉 *Welcome Back!* 🎉\n\n"
            "You're already part of our VIP Quiz family! 🏆\n\n"
            f"💫 Join our VIP group here: {VIP_GROUP_LINK}\n"
            "Get ready to showcase your brilliance! ✨",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if user.id in user_data and user_data[user.id].get('submitted', False):
        update.message.reply_text(
            "⏳ *Almost There!* ⏳\n\n"
            "Your payment proof is being reviewed by our team! 👀\n\n"
            "💫 We're working quickly to get you verified!\n"
            "You'll hear from us very soon! ⚡",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    user_data[user.id] = {
        'username': user.username or user.first_name,
        'first_name': user.first_name,
        'submitted': True,
        'approved': False
    }
    
    keyboard = [
        [InlineKeyboardButton("✅ APPROVE & WELCOME 🎉", callback_data=f"approve_{user.id}"),
         InlineKeyboardButton("❌ NEEDS REVIEW 🔄", callback_data=f"reject_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption = f"💰 *NEW PAYMENT PROOF RECEIVED!* 💰\n\n👤 From: @{user.username or user.first_name}\n📛 Name: {user.first_name}\n🎯 Slots Used: {len(registered_users)}/{MAX_REGISTRATIONS}\n\n⚡ *Ready for review!* ⚡"
    
    try:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            context.bot.send_photo(ADMIN_USER_ID, photo=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        elif update.message.document:
            file_id = update.message.document.file_id
            context.bot.send_document(ADMIN_USER_ID, document=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        
        update.message.reply_text(
            "🎉 *PAYMENT PROOF RECEIVED!* 🎉\n\n"
            "✅ *Great! We've got your payment proof!*\n\n"
            "⏰ *What's happening now?*\n"
            "• Our team is reviewing your submission 👀\n"
            "• Verification usually takes 5-10 minutes ⚡\n"
            "• You'll get VIP access once approved! 🎊\n\n"
            "💫 *Competition ends on* {end_time}\n\n"
            "🌟 *Get ready to showcase your skills!* 🌟".format(
                end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        update.message.reply_text(
            "😅 *Oops! Something went wrong!* 😅\n\n"
            "❌ We encountered a small issue processing your proof.\n\n"
            "💡 *Please try again or contact* @Tmzbrandceo *for assistance.*\n\n"
            "🌟 We're here to help you join the fun! 🌟",
            parse_mode=ParseMode.MARKDOWN
        )

def handle_admin_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "⏰ *Competition Ended* ⏰\n\n"
            "This competition has concluded. No more approvals can be processed.\n\n"
            "🌟 *Thank you for your admin support!* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    data = query.data
    action, user_id_str = data.split('_')
    user_id = int(user_id_str)
    
    if len(registered_users) >= MAX_REGISTRATIONS and action == 'approve':
        query.edit_message_text(
            "🚫 *Maximum Capacity Reached!* 🚫\n\n"
            "All 10 VIP spots have been filled! 🎯\n\n"
            "🌟 *Competition is now full and ready to begin!* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if action == 'approve':
        registered_users.add(user_id)
        user_data[user_id]['approved'] = True
        
        try:
            context.bot.send_message(
                chat_id=user_id,
                text="🎊 *CONGRATULATIONS! WELCOME TO THE VIP QUIZ!* 🎊\n\n"
                     "🌟 *You're IN!* 🌟\n\n"
                     "✅ *Your payment has been verified successfully!*\n\n"
                     "🎯 *WHAT TO DO NEXT:*\n"
                     "• 📱 *Go to Telegram Search* 🔍\n"
                     "• 🔗 *Search and join:* `TMZBRAND_VIP_OFFICIAL`\n"
                     "• 💫 *Or click this link:* {vip_link}\n\n"
                     "🏆 *VIP Group Access:* {vip_link}\n\n"
                     "⏰ *Competition ends on* {end_time}\n\n"
                     "🚀 *Let the games begin! We're excited to have you!* 🚀\n\n"
                     "🌈 *Best of luck! May the best mind win!* 🌈".format(
                         vip_link=VIP_GROUP_LINK,
                         end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')
                     ),
                parse_mode=ParseMode.MARKDOWN
            )
            
            if VIP_GROUP_ID:
                try:
                    context.bot.send_message(
                        chat_id=VIP_GROUP_ID,
                        text=f"🎉 *NEW VIP MEMBER ALERT!* 🎉\n\n"
                             f"🌟 Please welcome @{user_data[user_id]['username']} to our VIP Quiz Competition! 🌟\n\n"
                             f"💫 Let's give them a warm welcome and get ready for some amazing quiz action! 🎯"
                    )
                except Exception:
                    pass
                    
        except Exception:
            pass
        
        query.edit_message_text(
            f"✅ *SUCCESSFULLY APPROVED!* ✅\n\n"
            f"👤 *User:* @{user_data[user_id]['username']}\n"
            f"🎯 *VIP Spot Confirmed!* 🎯\n\n"
            f"📊 *Registration Status:* {len(registered_users)}/{MAX_REGISTRATIONS}\n"
            f"⏰ *Competition Ends:* {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}\n\n"
            f"🌟 *Another amazing participant joined!* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        
    elif action == 'reject':
        try:
            context.bot.send_message(
                chat_id=user_id,
                text="🔍 *PAYMENT VERIFICATION NEEDED* 🔍\n\n"
                     "❌ *We couldn't verify your payment just yet.*\n\n"
                     "💡 *This could be because:*\n"
                     "• Payment details weren't clear in the screenshot 📸\n"
                     "• Wrong amount was transferred 💰\n"
                     "• Bank details were incorrect 🏦\n\n"
                     "🔄 *No worries! You can try again:*\n"
                     "1. Double-check the bank details\n"
                     "2. Take a clearer screenshot\n"
                     "3. Upload it again\n\n"
                     "🌟 *We want you to join us!* 🌟\n"
                     "Let's get this sorted so you can participate! 🎯",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            pass
        
        if user_id in user_data:
            user_data[user_id]['submitted'] = False
        
        query.edit_message_text(
            "🔄 *PAYMENT NEEDS REVIEW* 🔄\n\n"
            "❌ The user has been notified to provide clearer payment proof.\n\n"
            "💫 They can try again with better documentation!",
            parse_mode=ParseMode.MARKDOWN
        )

def show_stats(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id != ADMIN_USER_ID:
        return
    
    time_remaining = COMPETITION_END_TIME - datetime.now()
    hours_remaining = int(time_remaining.total_seconds() // 3600)
    minutes_remaining = int((time_remaining.total_seconds() % 3600) // 60)
    
    participants_list = "\n".join([f"🎯 @{user_data[uid]['username']}" for uid in registered_users if uid in user_data]) or "🌟 No participants yet"
    
    stats_text = (
        f"📊 *VIP QUIZ DASHBOARD* 📊\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 *Registered Participants:* {len(registered_users)}/{MAX_REGISTRATIONS}\n"
        f"⏰ *Competition Ends:* {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}\n"
        f"🕒 *Time Remaining:* {hours_remaining}h {minutes_remaining}m\n"
        f"🎯 *Status:* {'🚀 ACTIVE' if is_competition_active() else '✅ COMPLETED'}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🌟 *AMAZING PARTICIPANTS:* 🌟\n{participants_list}\n\n"
        f"💫 *Let the quiz begin!* 💫"
    )
    
    update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

def end_competition(update: Update, context: CallbackContext) -> None:
    """Manually end competition and clear all data (Admin only)"""
    user = update.effective_user
    if user.id != ADMIN_USER_ID:
        return
    
    global COMPETITION_END_TIME
    COMPETITION_END_TIME = datetime.now() - timedelta(minutes=1)
    
    registered_users.clear()
    user_data.clear()
    messaged_in_groups.clear()
    
    update.message.reply_text(
        "🎊 *COMPETITION CONCLUDED!* 🎊\n\n"
        "✅ *All participant data has been cleared successfully!*\n\n"
        "🌟 *The stage is set for our next amazing competition!* 🌟\n\n"
        "💫 *Ready to welcome new champions!* 💫",
        parse_mode=ParseMode.MARKDOWN
    )

def set_end_time(update: Update, context: CallbackContext) -> None:
    """Set new competition end time (Admin only)"""
    user = update.effective_user
    if user.id != ADMIN_USER_ID:
        return
    
    if context.args:
        try:
            date_str = " ".join(context.args)
            new_end_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            global COMPETITION_END_TIME
            COMPETITION_END_TIME = new_end_time
            
            update.message.reply_text(
                f"⏰ *COMPETITION SCHEDULE UPDATED!* ⏰\n\n"
                f"✅ *New end time set successfully!*\n\n"
                f"📅 *Competition now ends:* {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}\n\n"
                f"🌟 *Let the excitement continue!* 🌟",
                parse_mode=ParseMode.MARKDOWN
            )
        except ValueError:
            update.message.reply_text(
                "❌ *Oops! Format Issue* ❌\n\n"
                "💡 *Please use:* /settime YYYY-MM-DD HH:MM\n\n"
                "🎯 *Example:* /settime 2024-12-25 22:00\n\n"
                "🌟 *Let's get this right!* 🌟",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        update.message.reply_text(
            "❌ *Missing Time Details* ❌\n\n"
            "💡 *Please provide the end time:* /settime YYYY-MM-DD HH:MM\n\n"
            "🎯 *Example:* /settime 2024-12-25 22:00\n\n"
            "🌟 *We need this to schedule properly!* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )

def set_group_id(update: Update, context: CallbackContext) -> None:
    global VIP_GROUP_ID
    if update.message.chat.type in ['group', 'supergroup']:
        VIP_GROUP_ID = update.message.chat.id
        if update.effective_user.id == ADMIN_USER_ID:
            update.message.reply_text(
                f"🎉 *VIP GROUP CONFIGURED!* 🎉\n\n"
                f"✅ *Group ID set to:* {VIP_GROUP_ID}\n\n"
                f"🌟 *Ready to welcome amazing participants!* 🌟",
                parse_mode=ParseMode.MARKDOWN
            )

def check_competition_end(context: CallbackContext):
    """Background task to check if competition has ended"""
    if not is_competition_active() and registered_users:
        registered_users.clear()
        user_data.clear()
        messaged_in_groups.clear()
        logging.info("Competition ended - all data cleared automatically")

def main() -> None:
    # Add web server for Render
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "🤖 TMZ VIP Bot is running!"

    # Start web server in background
    import threading
    def run_flask():
        app.run(host='0.0.0.0', port=PORT)
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Initialize bot
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stats", show_stats))
    dp.add_handler(CommandHandler("end", end_competition))
    dp.add_handler(CommandHandler("settime", set_end_time))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, handle_payment_proof))
    dp.add_handler(MessageHandler(Filters.chat_type.groups, set_group_id))
    dp.add_handler(CallbackQueryHandler(handle_paid_confirmation, pattern="^paid_confirmation$"))
    dp.add_handler(CallbackQueryHandler(handle_admin_action, pattern="^(approve|reject)_"))

    j = updater.job_queue
    j.run_repeating(check_competition_end, interval=60, first=10)

    print("🎊 TMZ VIP BOT IS LIVE! 🎊")
    print(f"⏰ Competition ends: {COMPETITION_END_TIME}")
    print(f"🔗 VIP Group: {VIP_GROUP_LINK}")
    print("🌟 Ready to welcome amazing participants! 🌟")
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
