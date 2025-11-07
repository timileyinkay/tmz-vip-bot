import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.parsemode import ParseMode
from datetime import datetime, timedelta
from flask import Flask

# Bot Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN', "7703532839:AAG5yNnTAye8zmV58MnWLnuorBg8gaFpbB0")
ADMIN_USER_ID = int(os.environ.get('ADMIN_USER_ID', "6011041717"))
VIP_GROUP_ID = os.environ.get('VIP_GROUP_ID', "-1002750986636")
VIP_GROUP_LINK = "https://t.me/TMZBRAND_VIP_OFFICIAL"
PORT = int(os.environ.get('PORT', 8080))

# Store user data
user_data = {}
registered_users = set()
MAX_REGISTRATIONS = 10
messaged_in_groups = set()

# Competition end time
COMPETITION_END_TIME = datetime(2024, 12, 25, 22, 0, 0)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def is_competition_active():
    return datetime.now() < COMPETITION_END_TIME

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    # Prevent multiple replies in groups
    if update.message.chat.type in ['group', 'supergroup']:
        if user.id in messaged_in_groups:
            return
        messaged_in_groups.add(user.id)
    
    if not is_competition_active():
        update.message.reply_text(
            "🏆 *Competition Ended*\n\n"
            "Thank you for your interest! This TMZ BRAND VIP Quiz has concluded.\n\n"
            "Stay tuned for our next exciting competition!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        update.message.reply_text(
            "🚫 *Registration Full*\n\n"
            "All 10 VIP spots have been filled!\n\n"
            "Follow us for future competitions and opportunities.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    welcome_text = """
🎯 *TMZ BRAND VIP QUIZ COMPETITION*

*Exclusive Experience for 10 Participants*

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 **AMAZING PRIZES:**
• 1st Place: ₦10,000
• 2nd Place: ₦5,000  
• 3rd Place: ₦5,000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 **Competition Ends:** {end_time}

🌟 **What Makes This Special:**
• Only 10 VIP participants
• Interactive platform (mentimeter.com)
• Real-time leaderboard
• Exclusive experience

Ready to join this exclusive competition?
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    keyboard = [
        [InlineKeyboardButton("🌟 Learn More", callback_data="learn_more")],
        [InlineKeyboardButton("💼 How to Join", callback_data="how_to_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def handle_learn_more(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "🏆 *Competition Complete*\n\n"
            "This event has ended. Thank you for your interest!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    learn_text = """
📋 **COMPETITION DETAILS**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **What to Expect:**
• Exclusive quiz for 10 participants only
• Interactive questions via mentimeter.com
• Real-time scoring and leaderboard
• Professional hosting by TMZ BRAND

⏰ **Event Flow:**
1. Registration and verification
2. Join VIP group for instructions
3. Participate in live quiz session
4. Winners announced immediately

🏆 **Why Join:**
• Chance to win great cash prizes
• Exclusive VIP experience
• Professional environment
• Quick and smooth process

📅 **Ends:** {end_time}

Ready to secure your spot?
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    keyboard = [
        [InlineKeyboardButton("💳 Payment Details", callback_data="payment_details")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(learn_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def handle_how_to_join(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "🏆 *Event Completed*\n\n"
            "This competition has ended. Watch out for our next event!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    join_text = """
📝 **HOW TO JOIN**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **Simple 3-Step Process:**

1. **Make Payment**
   • Amount: ₦2,000
   • Bank: OPAY
   • Account: OLUWATOBILOBA KEHINDE
   • Number: 8079304530

2. **Take Screenshot**
   • Clear transaction proof
   • All details visible

3. **Submit Here**
   • Upload your screenshot
   • Wait for verification
   • Get VIP access

⏰ **Verification:**
• Usually 5-10 minutes
• Approved users get VIP group link
• Quick and professional process

📅 **Ends:** {end_time}

Proceed to payment details?
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    keyboard = [
        [InlineKeyboardButton("💳 View Payment Info", callback_data="payment_details")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(join_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def handle_payment_details(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "⏰ *Registration Closed*\n\n"
            "This competition is no longer accepting participants.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        query.edit_message_text(
            "🚫 *All Spots Filled*\n\n"
            "All 10 VIP positions have been taken.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    payment_text = """
💳 **PAYMENT INFORMATION**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏦 **Bank Details:**
• **Bank:** OPAY
• **Name:** OLUWATOBILOBA KEHINDE
• **Number:** 8079304530
• **Amount:** ₦2,000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📸 **After Payment:**
1. Take clear screenshot
2. Make sure details are visible
3. Upload it here

✅ **What Happens Next:**
• We verify your payment (5-10 mins)
• You get VIP group access
• Ready to compete!

🔗 **VIP Group:** {vip_link}

📅 **Competition Ends:** {end_time}

Upload your payment screenshot now!
""".format(
        vip_link=VIP_GROUP_LINK,
        end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')
    )
    
    query.edit_message_text(payment_text, parse_mode=ParseMode.MARKDOWN)

def handle_back_to_start(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    start(update, context)

def handle_payment_proof(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    if not is_competition_active():
        update.message.reply_text(
            "🏆 *Competition Ended*\n\n"
            "This event has concluded. Thank you for your interest!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        update.message.reply_text(
            "🚫 *All Spots Taken*\n\n"
            "All 10 positions are filled. Follow us for future events!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if user.id in registered_users:
        update.message.reply_text(
            "✅ *Already Registered*\n\n"
            "You're already in the VIP competition!\n\n"
            f"Join group: {VIP_GROUP_LINK}",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if user.id in user_data and user_data[user.id].get('submitted', False):
        update.message.reply_text(
            "⏳ *Under Review*\n\n"
            "Your payment is being verified. Please wait 5-10 minutes.",
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
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption = f"💰 *New Payment*\nFrom: @{user.username or user.first_name}\nName: {user.first_name}\nSpots: {len(registered_users)}/{MAX_REGISTRATIONS}"
    
    try:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            context.bot.send_photo(ADMIN_USER_ID, photo=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        elif update.message.document:
            file_id = update.message.document.file_id
            context.bot.send_document(ADMIN_USER_ID, document=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        
        update.message.reply_text(
            "✅ *Payment Received*\n\n"
            "We've got your payment proof!\n\n"
            "• Under review (5-10 mins)\n"
            "• You'll get VIP access when approved\n"
            "• Check back soon!\n\n"
            f"Ends: {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}",
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        update.message.reply_text(
            "❌ *Error*\n\n"
            "Please try again or contact @Tmzbrandceo for help.",
            parse_mode=ParseMode.MARKDOWN
        )

def handle_admin_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text("Competition ended - no more approvals.")
        return
    
    data = query.data
    
    # Extract user_id from callback data (approve_123456 or reject_123456)
    if data.startswith('approve_'):
        user_id = int(data.split('_')[1])
        action = 'approve'
    elif data.startswith('reject_'):
        user_id = int(data.split('_')[1])
        action = 'reject'
    else:
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS and action == 'approve':
        query.edit_message_text("All 10 spots are filled!")
        return
    
    if action == 'approve':
        # Add user to registered users
        registered_users.add(user_id)
        
        # Update user data
        if user_id in user_data:
            user_data[user_id]['approved'] = True
            user_data[user_id]['submitted'] = True
        
        try:
            # Send approval message to user
            context.bot.send_message(
                chat_id=user_id,
                text="🎉 *APPROVED!*\n\n"
                     "Welcome to TMZ BRAND VIP Quiz!\n\n"
                     "✅ Payment verified successfully\n"
                     "🎯 You now have VIP access\n\n"
                     "📱 *Next Steps:*\n"
                     "1. Go to Telegram Search\n"
                     "2. Search: TMZBRAND_VIP_OFFICIAL\n"
                     "3. Join the group\n\n"
                     f"🔗 Or click: {VIP_GROUP_LINK}\n\n"
                     "Good luck in the competition! 🏆",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Notify VIP group
            if VIP_GROUP_ID:
                try:
                    username = user_data[user_id].get('username', 'New User')
                    context.bot.send_message(
                        chat_id=VIP_GROUP_ID,
                        text=f"🎉 New VIP member: @{username}! Welcome to the competition! 🏆"
                    )
                except Exception as e:
                    print(f"Error sending to group: {e}")
                    
        except Exception as e:
            print(f"Error sending approval message: {e}")
        
        # Update admin message
        username = user_data[user_id].get('username', 'User') if user_id in user_data else 'User'
        query.edit_message_text(
            f"✅ *Approved Successfully!*\n\n"
            f"User: @{username}\n"
            f"Spots filled: {len(registered_users)}/{MAX_REGISTRATIONS}\n\n"
            f"User has been notified and added to VIP list.",
            parse_mode=ParseMode.MARKDOWN
        )
        
    elif action == 'reject':
        try:
            context.bot.send_message(
                chat_id=user_id,
                text="❌ *Payment Issue*\n\n"
                     "We need clearer payment proof.\n\n"
                     "Please check:\n"
                     "• Amount is ₦2,000\n"
                     "• Screenshot is clear\n"
                     "• Details are visible\n\n"
                     "Upload again with better image.",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Error sending rejection message: {e}")
        
        # Reset user submission status
        if user_id in user_data:
            user_data[user_id]['submitted'] = False
        
        query.edit_message_text(
            "❌ *User Rejected*\n\n"
            "User has been asked to provide better payment proof.",
            parse_mode=ParseMode.MARKDOWN
        )

def show_stats(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id != ADMIN_USER_ID:
        return
    
    time_remaining = COMPETITION_END_TIME - datetime.now()
    hours_remaining = int(time_remaining.total_seconds() // 3600)
    minutes_remaining = int((time_remaining.total_seconds() % 3600) // 60)
    
    participants_list = "\n".join([f"• @{user_data[uid]['username']}" for uid in registered_users if uid in user_data]) or "No participants yet"
    
    stats_text = (
        f"📊 *TMZ VIP DASHBOARD*\n\n"
        f"Participants: {len(registered_users)}/{MAX_REGISTRATIONS}\n"
        f"Ends: {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}\n"
        f"Time Left: {hours_remaining}h {minutes_remaining}m\n"
        f"Status: {'Active' if is_competition_active() else 'Ended'}\n\n"
        f"VIP Members:\n{participants_list}"
    )
    
    update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

def end_competition(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id != ADMIN_USER_ID:
        return
    
    global COMPETITION_END_TIME
    COMPETITION_END_TIME = datetime.now() - timedelta(minutes=1)
    
    registered_users.clear()
    user_data.clear()
    messaged_in_groups.clear()
    
    update.message.reply_text("Competition ended and data cleared.")

def set_end_time(update: Update, context: CallbackContext) -> None:
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
                f"New end time: {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}",
                parse_mode=ParseMode.MARKDOWN
            )
        except ValueError:
            update.message.reply_text("Use: /settime YYYY-MM-DD HH:MM")
    else:
        update.message.reply_text("Use: /settime YYYY-MM-DD HH:MM")

def set_group_id(update: Update, context: CallbackContext) -> None:
    global VIP_GROUP_ID
    if update.message.chat.type in ['group', 'supergroup']:
        VIP_GROUP_ID = update.message.chat.id
        # Silent configuration - no group message
        if update.effective_user.id == ADMIN_USER_ID:
            context.bot.send_message(
                chat_id=ADMIN_USER_ID,
                text=f"Group ID set: {VIP_GROUP_ID}",
                parse_mode=ParseMode.MARKDOWN
            )

def check_competition_end(context: CallbackContext):
    if not is_competition_active() and registered_users:
        registered_users.clear()
        user_data.clear()
        messaged_in_groups.clear()
        logging.info("Competition ended - data cleared")

def main() -> None:
    # Web server for deployment
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "TMZ VIP Bot is running!"

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
    dp.add_handler(CallbackQueryHandler(handle_learn_more, pattern="^learn_more$"))
    dp.add_handler(CallbackQueryHandler(handle_how_to_join, pattern="^how_to_join$"))
    dp.add_handler(CallbackQueryHandler(handle_payment_details, pattern="^payment_details$"))
    dp.add_handler(CallbackQueryHandler(handle_back_to_start, pattern="^back_to_start$"))
    
    # FIXED: Use a single handler for both approve and reject with proper pattern
    dp.add_handler(CallbackQueryHandler(handle_admin_approval, pattern="^(approve|reject)_"))

    j = updater.job_queue
    j.run_repeating(check_competition_end, interval=60, first=10)

    print("TMZ VIP BOT IS LIVE!")
    print(f"Competition ends: {COMPETITION_END_TIME}")
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
