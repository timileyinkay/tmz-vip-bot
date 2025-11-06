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
VIP_GROUP_ID = os.environ.get('VIP_GROUP_ID', "-1002750986636")
VIP_GROUP_LINK = "https://t.me/TMZBRAND_VIP_OFFICIAL"
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
            "✨ *A Grand Finale!* ✨\n\n"
            "Dearest visionary,\n\n"
            "Our exclusive TMZ BRAND VIP Quiz Competition has reached its magnificent conclusion. "
            "The brilliance displayed by our esteemed participants was truly extraordinary. 🏆\n\n"
            "💫 *The Journey Continues...*\n"
            "Stay connected with TMZ BRAND for future exclusive experiences that celebrate excellence "
            "and reward brilliance. Your journey with luxury is just beginning.\n\n"
            "With utmost appreciation,\n*The TMZ BRAND Team* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        update.message.reply_text(
            "🌟 *Exclusive Access Filled* 🌟\n\n"
            "Dearest connoisseur of excellence,\n\n"
            "Our VIP sanctuary has reached its capacity of 10 distinguished participants. "
            "The response has been nothing short of extraordinary.\n\n"
            "💎 *Your Elegance is Noted*\n"
            "While our current experience is fully subscribed, your interest has been gracefully noted. "
            "We shall personally notify you when our next exclusive gathering is curated.\n\n"
            "Until then, may your days be filled with brilliance and sophistication.\n\n"
            "With refined regards,\n*TMZ BRAND* 💫",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    welcome_text = """
🎩 *WELCOME TO THE TMZ BRAND VIP QUIZ EXPERIENCE* 🎩

*Where Brilliance Meets Exclusive Luxury*

Dearest seeker of excellence,

We are profoundly delighted to welcome you to the TMZ BRAND VIP Quiz Competition—an exclusive gathering 
for those who appreciate the finer things in life and possess minds as sharp as their taste.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💎 *THE EXPERIENCE AWAITS* 💎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ *An Exclusive Affair:* Limited to 10 distinguished participants
🎯 *Interactive Excellence:* Powered by mentimeter.com
🏆 *Prestigious Recognition:* Celebrate your intellectual prowess
💫 *Sophisticated Engagement:* Where minds meet luxury

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏅 *PRESTIGIOUS ACCOLADES* 🏅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🥇 *First Honor:* ₦10,000 • The Crown of Brilliance
🥈 *Second Distinction:* ₦5,000 • The Medal of Excellence  
🥉 *Third Merit:* ₦5,000 • The Badge of Distinction

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 *Grand Finale:* {end_time}

🌟 *Why This Experience is Extraordinary:*
• An intimate gathering of only 10 brilliant minds
• State-of-the-art interactive platform
• Real-time intellectual engagement
• Prestigious recognition of your capabilities
• The TMZ BRAND seal of excellence

Darling visionary, this is more than a competition—it's a celebration of intellectual elegance. 
A moment where your brilliance takes center stage in an exclusive setting worthy of your capabilities.

*Are you ready to claim your place among the exceptional?* ✨
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    keyboard = [
        [InlineKeyboardButton("🌟 DISCOVER THE EXPERIENCE 🌟", callback_data="discover_experience")],
        [InlineKeyboardButton("💎 LEARN ABOUT THE JOURNEY 💎", callback_data="learn_journey")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def handle_discover_experience(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "✨ *A Beautiful Conclusion* ✨\n\n"
            "Dearest visionary,\n\n"
            "This exclusive experience has reached its elegant conclusion. "
            "The symphony of brilliant minds has created memories we shall cherish forever.\n\n"
            "Stay connected with TMZ BRAND for future curated experiences that celebrate "
            "the extraordinary in everyone.\n\n"
            "With gratitude and elegance,\n*The TMZ BRAND Team* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    experience_text = """
💫 *THE TMZ BRAND EXPERIENCE UNFOLDS* 💫

Dearest seeker of extraordinary moments,

Allow us to unveil the sophisticated journey that awaits you in our exclusive VIP Quiz Competition.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎭 *THE CURATED JOURNEY* 🎭
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ *Elegant Engagement:* Our platform transforms competition into an art form
🌟 *Intimate Setting:* Only 10 distinguished participants for personalized attention
🎯 *Cutting-Edge Technology:* Powered by mentimeter.com for seamless interaction
💎 *Luxurious Pace:* Thoughtfully timed to appreciate every moment
🏆 *Prestigious Recognition:* Your brilliance celebrated with sophistication

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤵 *YOUR HOSTS* 🤵
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Our TMZ BRAND curators are dedicated to creating an atmosphere of intellectual luxury, 
where every participant feels valued, celebrated, and inspired.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 *Grand Finale:* {end_time}

Darling visionary, this is not merely a competition—it's a gathering of minds, 
a celebration of intellect, and an opportunity to connect with fellow exceptional individuals 
in an atmosphere of refined elegance.

*Ready to explore how to secure your exclusive place?* 🌟
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    keyboard = [
        [InlineKeyboardButton("💼 SECURE MY PLACE 💼", callback_data="secure_place")],
        [InlineKeyboardButton("🌟 THE JOURNEY CONTINUES 🌟", callback_data="learn_journey")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(experience_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def handle_learn_journey(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "🎭 *A Performance to Remember* 🎭\n\n"
            "Dearest patron of excellence,\n\n"
            "Our grand performance has reached its final curtain call. "
            "The stage was graced by extraordinary talent and brilliant minds.\n\n"
            "TMZ BRAND continues to curate exceptional experiences for those "
            "who appreciate the art of intellectual engagement.\n\n"
            "With artistic appreciation,\n*The TMZ BRAND Ensemble* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    journey_text = """
🎭 *THE ART OF INTELLECTUAL ELEGANCE* 🎭

Dearest appreciator of fine experiences,

At TMZ BRAND, we believe that intellectual engagement should be as luxurious 
as the finest things in life. Our VIP Quiz Competition is crafted as a symphony 
of minds, where every moment is designed to celebrate your brilliance.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ *THE EXPERIENCE CURATION* ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 *Exclusive Access:* Limited to 10 participants for intimate engagement
🎯 *Technological Sophistication:* mentimeter.com ensures flawless interaction
🌟 *Elegant Atmosphere:* Where every mind feels celebrated and valued
🏆 *Prestigious Recognition:* Awards that honor true intellectual achievement
🤵 *Personalized Attention:* Our hosts ensure your comfort and enjoyment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 *Grand Finale:* {end_time}

This is more than a competition—it's a gathering of extraordinary individuals 
in a setting worthy of their capabilities. A moment where intellectual prowess 
meets sophisticated engagement.

Darling visionary, your place at this exclusive gathering awaits. 
The question is not if you're worthy, but if you're ready to claim the experience 
you truly deserve.

*Shall we discuss securing your distinguished place?* 💫
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    keyboard = [
        [InlineKeyboardButton("💎 SECURE MY DISTINGUISHED PLACE 💎", callback_data="secure_place")],
        [InlineKeyboardButton("🌟 DISCOVER THE EXPERIENCE 🌟", callback_data="discover_experience")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(journey_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

def handle_secure_place(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "💫 *An Experience Concluded* 💫\n\n"
            "Dearest visionary,\n\n"
            "This exclusive gathering has reached its beautiful conclusion. "
            "The connections made and brilliance displayed will be remembered fondly.\n\n"
            "TMZ BRAND looks forward to welcoming you to future curated experiences "
            "that celebrate intellectual excellence in luxurious settings.\n\n"
            "With elegant anticipation,\n*The TMZ BRAND Team* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        query.edit_message_text(
            "🌟 *Exclusive Capacity Reached* 🌟\n\n"
            "Dearest seeker of excellence,\n\n"
            "Our intimate gathering of 10 distinguished participants has reached capacity. "
            "The response has been overwhelmingly elegant.\n\n"
            "Your interest in TMZ BRAND experiences has been gracefully noted in our records. "
            "We shall personally contact you when our next exclusive event is being curated.\n\n"
            "Until our paths cross again in celebration of brilliance,\n\n"
            "With refined regards,\n*TMZ BRAND* 💎",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    payment_text = """
💎 *SECURING YOUR DISTINGUISHED PLACE* 💎

Dearest future participant,

We are delighted that you've chosen to join our exclusive gathering of brilliant minds. 
Securing your place is a simple, elegant process that reflects the TMZ BRAND experience.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏦 *CONTRIBUTION DETAILS* 🏦
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This contribution ensures our ability to create an extraordinary experience 
worthy of participants of your caliber.

💵 *Amount:* ₦2,000
🏛️ *Bank:* OPAY 
👤 *Account Name:* OLUWATOBILOBA KEHINDE
🔢 *Account Number:* 8079304530

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 *Grand Finale:* {end_time}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 *THE ELEGANT PROCESS:*
1️⃣ Complete your contribution using the details above
2️⃣ Capture a clear image of your transaction confirmation
3️⃣ Gracefully submit your confirmation here

💫 *FOR EXPEDITED PROCESSING:*
• Ensure all transaction details are clearly visible
• Natural lighting works wonders for clarity
• No digital alterations, please

🚀 *UPON CONFIRMATION:*
• Immediate access to our exclusive VIP gathering
• Personal welcome from our TMZ BRAND hosts
• All competition details and elegant preparations

Darling visionary, we are genuinely excited to welcome you into our exclusive circle 
of brilliant minds. Your journey toward prestigious recognition begins now.

*Ready to complete your reservation?* ✨
""".format(end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p'))
    
    query.edit_message_text(payment_text, parse_mode=ParseMode.MARKDOWN)

def handle_payment_proof(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    
    if not is_competition_active():
        update.message.reply_text(
            "✨ *A Beautiful Conclusion* ✨\n\n"
            "Dearest visionary,\n\n"
            "Our exclusive gathering has reached its elegant conclusion. "
            "The symphony of brilliant minds has created memories we shall cherish.\n\n"
            "Thank you for your interest in TMZ BRAND experiences. "
            "We look forward to welcoming you to future curated events that celebrate excellence.\n\n"
            "With gratitude and sophistication,\n*The TMZ BRAND Team* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if len(registered_users) >= MAX_REGISTRATIONS:
        update.message.reply_text(
            "💎 *Exclusive Capacity Achieved* 💎\n\n"
            "Dearest seeker of excellence,\n\n"
            "Our intimate gathering of 10 distinguished participants has reached its elegant capacity. "
            "The response has been nothing short of extraordinary.\n\n"
            "Your enthusiasm for intellectual luxury has been gracefully noted. "
            "We shall personally inform you when our next exclusive experience is being curated.\n\n"
            "Until then, may your days be filled with brilliance and sophisticated engagements.\n\n"
            "With refined appreciation,\n*TMZ BRAND* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if user.id in registered_users:
        update.message.reply_text(
            "🌟 *Welcome Back, Distinguished Participant!* 🌟\n\n"
            "Dearest valued member,\n\n"
            "You are already part of our exclusive TMZ BRAND VIP gathering! "
            "Your place among our brilliant participants is secured and celebrated.\n\n"
            f"💫 *Access our exclusive circle here:* {VIP_GROUP_LINK}\n\n"
            "Prepare to engage in an experience worthy of your capabilities. "
            "The stage is set for intellectual elegance and prestigious recognition.\n\n"
            "With anticipation and elegance,\n*TMZ BRAND* 💎",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if user.id in user_data and user_data[user.id].get('submitted', False):
        update.message.reply_text(
            "⏳ *Your Submission is Being Curated* ⏳\n\n"
            "Dearest future participant,\n\n"
            "Your reservation details are currently undergoing our elegant review process. "
            "We are ensuring every detail meets the TMZ BRAND standard of excellence.\n\n"
            "This sophisticated process typically requires 5-10 minutes of careful attention. "
            "You will receive personal notification the moment your exclusive access is granted.\n\n"
            "Thank you for your patience and understanding of our commitment to quality.\n\n"
            "With elegant anticipation,\n*TMZ BRAND* 🌟",
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
        [InlineKeyboardButton("🎩 APPROVE & WELCOME ELEGANTLY 💫", callback_data=f"approve_{user.id}")],
        [InlineKeyboardButton("🔍 REQUEST REFINED CLARIFICATION 🎭", callback_data=f"reject_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption = f"💎 *NEW RESERVATION REQUEST* 💎\n\n👤 *From:* @{user.username or user.first_name}\n🎩 *Name:* {user.first_name}\n💫 *Current Gathering:* {len(registered_users)}/{MAX_REGISTRATIONS}\n\n🌟 *Ready for Sophisticated Review* 🌟"
    
    try:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            context.bot.send_photo(ADMIN_USER_ID, photo=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        elif update.message.document:
            file_id = update.message.document.file_id
            context.bot.send_document(ADMIN_USER_ID, document=file_id, caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
        
        update.message.reply_text(
            "🎭 *RESERVATION CONFIRMATION RECEIVED* 🎭\n\n"
            "Dearest future participant,\n\n"
            "✨ *Elegant Submission Acknowledged!*\n\n"
            "Your reservation details have been gracefully received and are now "
            "undergoing our sophisticated review process.\n\n"
            "⏰ *Our Curated Timeline:*\n"
            "• Our team is personally reviewing your submission with careful attention\n"
            "• This elegant process typically requires 5-10 minutes\n"
            "• You will receive immediate notification upon approval\n"
            "• Exclusive VIP access will be granted seamlessly\n\n"
            "💫 *Grand Finale:* {end_time}\n\n"
            "We are genuinely excited about the prospect of welcoming you into "
            "our exclusive circle of brilliant minds. Your intellectual elegance "
            "will be a wonderful addition to our gathering.\n\n"
            "With sophisticated anticipation,\n*TMZ BRAND* 🌟".format(
                end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        update.message.reply_text(
            "🎭 *A Moment of Refinement Needed* 🎭\n\n"
            "Dearest visionary,\n\n"
            "We encountered a temporary elegance interruption while processing your submission.\n\n"
            "💡 *For personalized assistance, please contact* @Tmzbrandceo\n\n"
            "Our team is dedicated to ensuring your journey with TMZ BRAND begins smoothly "
            "and continues with the sophistication you deserve.\n\n"
            "With commitment to excellence,\n*TMZ BRAND* 💎",
            parse_mode=ParseMode.MARKDOWN
        )

def handle_admin_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if not is_competition_active():
        query.edit_message_text(
            "✨ *Experience Concluded* ✨\n\n"
            "Dearest curator,\n\n"
            "This exclusive gathering has reached its beautiful conclusion. "
            "No further reservations can be processed at this time.\n\n"
            "Thank you for your elegant stewardship of this TMZ BRAND experience.\n\n"
            "With appreciation,\n*TMZ BRAND* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    data = query.data
    action, user_id_str = data.split('_')
    user_id = int(user_id_str)
    
    if len(registered_users) >= MAX_REGISTRATIONS and action == 'approve':
        query.edit_message_text(
            "💎 *Exclusive Capacity Achieved* 💎\n\n"
            "Dearest curator,\n\n"
            "Our intimate gathering of 10 distinguished participants has reached "
            "its elegant capacity. The experience is now perfectly curated.\n\n"
            "The stage is set for an extraordinary display of intellectual elegance "
            "among our exclusive circle of brilliant minds.\n\n"
            "With sophisticated satisfaction,\n*TMZ BRAND* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    if action == 'approve':
        registered_users.add(user_id)
        user_data[user_id]['approved'] = True
        
        try:
            context.bot.send_message(
                chat_id=user_id,
                text="🎩 *WELCOME TO THE TMZ BRAND INNER CIRCLE* 🎩\n\n"
                     "Dearest distinguished participant,\n\n"
                     "🌟 *The Gates to Excellence Have Opened!* 🌟\n\n"
                     "✨ *Your Reservation is Confirmed!*\n\n"
                     "We are profoundly delighted to welcome you into our exclusive "
                     "gathering of brilliant minds. Your place among the exceptional "
                     "is now officially secured.\n\n"
                     "💫 *YOUR ELEGANT NEXT STEPS:*\n"
                     "• 📱 *Proceed to Telegram Search* 🔍\n"
                     "• 🎭 *Search for our exclusive salon:* `TMZBRAND_VIP_OFFICIAL`\n"
                     "• 💎 *Or grace us with your presence via:* {vip_link}\n\n"
                     "🏆 *Your Exclusive Access:* {vip_link}\n\n"
                     "📅 *Grand Finale:* {end_time}\n\n"
                     "Prepare to engage in an experience worthy of your capabilities. "
                     "Our TMZ BRAND hosts await your arrival with anticipation.\n\n"
                     "May your journey with us be filled with intellectual elegance, "
                     "sophisticated engagement, and the prestigious recognition you deserve.\n\n"
                     "With the utmost elegance and anticipation,\n*The TMZ BRAND Team* 💫".format(
                         vip_link=VIP_GROUP_LINK,
                         end_time=COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')
                     ),
                parse_mode=ParseMode.MARKDOWN
            )
            
            if VIP_GROUP_ID:
                try:
                    context.bot.send_message(
                        chat_id=VIP_GROUP_ID,
                        text=f"🎭 *NEW DISTINGUISHED ARRIVAL* 🎭\n\n"
                             f"💫 Esteemed members, please welcome @{user_data[user_id]['username']} "
                             f"to our exclusive TMZ BRAND gathering! 🌟\n\n"
                             f"Another brilliant mind graces our elegant circle. "
                             f"Let us prepare for an extraordinary experience together! 🎩"
                    )
                except Exception:
                    pass
                    
        except Exception:
            pass
        
        query.edit_message_text(
            f"💎 *ELEGANTLY APPROVED* 💎\n\n"
            f"🎩 *Distinguished Participant:* @{user_data[user_id]['username']}\n"
            f"🌟 *Exclusive Place Confirmed!* 🌟\n\n"
            f"📊 *Current Gathering:* {len(registered_users)}/{MAX_REGISTRATIONS}\n"
            f"📅 *Grand Finale:* {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}\n\n"
            f"Our exclusive circle grows more brilliant with each distinguished addition. "
            f"The stage is set for an extraordinary experience.\n\n"
            f"With sophisticated satisfaction,\n*TMZ BRAND* 💫",
            parse_mode=ParseMode.MARKDOWN
        )
        
    elif action == 'reject':
        try:
            context.bot.send_message(
                chat_id=user_id,
                text="🎭 *REFINEMENT REQUESTED* 🎭\n\n"
                     "Dearest future participant,\n\n"
                     "We require a moment of elegant clarification regarding your reservation details.\n\n"
                     "💫 *Possible Areas for Refinement:*\n"
                     "• Transaction details require clearer visibility\n"
                     "• Contribution amount needs verification\n"
                     "• Banking information alignment\n\n"
                     "🔄 *Our Elegant Solution:*\n"
                     "1. Review the banking details with careful attention\n"
                     "2. Capture a more refined image of your confirmation\n"
                     "3. Gracefully resubmit for our consideration\n\n"
                     "We are genuinely excited about welcoming you to our exclusive gathering "
                     "and want to ensure every detail reflects the TMZ BRAND standard of excellence.\n\n"
                     "With elegant anticipation,\n*TMZ BRAND* 🌟",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception:
            pass
        
        if user_id in user_data:
            user_data[user_id]['submitted'] = False
        
        query.edit_message_text(
            "🔍 *ELEGANT CLARIFICATION REQUESTED* 🔍\n\n"
            "The distinguished participant has been gracefully notified to provide "
            "more refined reservation details.\n\n"
            "Their journey toward exclusive access continues with our guidance "
            "and their commitment to excellence.\n\n"
            "With sophisticated patience,\n*TMZ BRAND* 💎",
            parse_mode=ParseMode.MARKDOWN
        )

def show_stats(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if user.id != ADMIN_USER_ID:
        return
    
    time_remaining = COMPETITION_END_TIME - datetime.now()
    hours_remaining = int(time_remaining.total_seconds() // 3600)
    minutes_remaining = int((time_remaining.total_seconds() % 3600) // 60)
    
    participants_list = "\n".join([f"🎩 @{user_data[uid]['username']}" for uid in registered_users if uid in user_data]) or "💫 No distinguished participants yet"
    
    stats_text = (
        f"💎 *TMZ BRAND VIP DASHBOARD* 💎\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎭 *Distinguished Participants:* {len(registered_users)}/{MAX_REGISTRATIONS}\n"
        f"📅 *Grand Finale:* {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}\n"
        f"⏰ *Elegant Countdown:* {hours_remaining}h {minutes_remaining}m\n"
        f"🌟 *Experience Status:* {'🎩 CURATED & ACTIVE' if is_competition_active() else '✨ BEAUTIFULLY CONCLUDED'}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💫 *OUR DISTINGUISHED GATHERING:* 💫\n{participants_list}\n\n"
        f"The stage is set for intellectual elegance and sophisticated engagement. "
        f"Each participant adds to the brilliance of our exclusive circle.\n\n"
        f"With curated excellence,\n*TMZ BRAND* 🌟"
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
        "✨ *EXPERIENCE BEAUTIFULLY CONCLUDED* ✨\n\n"
        "💎 *All elegant data has been gracefully archived!*\n\n"
        "The stage is now cleared for our next exclusive TMZ BRAND experience. "
        "The memories of brilliant minds and sophisticated engagement will inspire "
        "our future curated gatherings.\n\n"
        "With gratitude and anticipation for future excellence,\n*TMZ BRAND* 🌟",
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
                f"📅 *EXPERIENCE RESCHEDULED WITH ELEGANCE* 📅\n\n"
                f"💫 *New Grand Finale successfully curated!*\n\n"
                f"🎭 *The experience now concludes:* {COMPETITION_END_TIME.strftime('%B %d, %Y at %I:%M %p')}\n\n"
                f"Our distinguished participants will appreciate the extended opportunity "
                f"for intellectual engagement and sophisticated celebration.\n\n"
                f"With curated timing,\n*TMZ BRAND* 🌟",
                parse_mode=ParseMode.MARKDOWN
            )
        except ValueError:
            update.message.reply_text(
                "🎭 *Elegant Format Required* 🎭\n\n"
                "💎 *Please use:* /settime YYYY-MM-DD HH:MM\n\n"
                "✨ *Example:* /settime 2024-12-25 22:00\n\n"
                "Our sophisticated scheduling requires this specific elegant format "
                "to ensure perfect timing for our exclusive gathering.\n\n"
                "With appreciation for precision,\n*TMZ BRAND* 💫",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        update.message.reply_text(
            "💎 *Timing Details Required* 💎\n\n"
            "🎭 *Please provide the elegant conclusion time:* /settime YYYY-MM-DD HH:MM\n\n"
            "✨ *Example:* /settime 2024-12-25 22:00\n\n"
            "The sophistication of our experience depends on perfectly curated timing.\n\n"
            "With anticipation for precision,\n*TMZ BRAND* 🌟",
            parse_mode=ParseMode.MARKDOWN
        )

def set_group_id(update: Update, context: CallbackContext) -> None:
    global VIP_GROUP_ID
    if update.message.chat.type in ['group', 'supergroup']:
        VIP_GROUP_ID = update.message.chat.id
        # Silent configuration - no message sent to the group
        # Only log it for admin reference
        if update.effective_user.id == ADMIN_USER_ID:
            # Send confirmation privately to admin instead of in group
            context.bot.send_message(
                chat_id=ADMIN_USER_ID,
                text=f"💎 *VIP GATHERING SPACE CONFIGURED* 💎\n\n"
                     f"🎭 *Elegant Space ID:* {VIP_GROUP_ID}\n\n"
                     f"Our exclusive circle now has its perfectly curated venue. "
                     f"Ready to welcome distinguished participants with sophistication and grace.\n\n"
                     f"With elegant preparation,\n*TMZ BRAND* 🌟",
                parse_mode=ParseMode.MARKDOWN
            )

def check_competition_end(context: CallbackContext):
    """Background task to check if competition has ended"""
    if not is_competition_active() and registered_users:
        registered_users.clear()
        user_data.clear()
        messaged_in_groups.clear()
        logging.info("Experience concluded - all elegant data archived automatically")

def main() -> None:
    # Add web server for Render
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "🤖 TMZ BRAND VIP Experience Bot is elegantly running!"

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
    dp.add_handler(CallbackQueryHandler(handle_discover_experience, pattern="^discover_experience$"))
    dp.add_handler(CallbackQueryHandler(handle_learn_journey, pattern="^learn_journey$"))
    dp.add_handler(CallbackQueryHandler(handle_secure_place, pattern="^secure_place$"))
    dp.add_handler(CallbackQueryHandler(handle_admin_action, pattern="^(approve|reject)_"))

    j = updater.job_queue
    j.run_repeating(check_competition_end, interval=60, first=10)

    print("💎 TMZ BRAND VIP EXPERIENCE BOT IS ELEGANTLY LIVE! 💎")
    print(f"🎭 Grand Finale: {COMPETITION_END_TIME}")
    print(f"🌟 Exclusive Gathering: {VIP_GROUP_LINK}")
    print("💫 Ready to curate extraordinary experiences for distinguished minds! 🌟")
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
