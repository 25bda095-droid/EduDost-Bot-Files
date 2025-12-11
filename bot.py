import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Bot token from BotFather
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Career paths database
STREAM_INFO = {
    'science': {
        'subjects': ['Physics', 'Chemistry', 'Mathematics', 'Biology', 'Computer Science'],
        'careers': ['Engineering', 'Medicine (MBBS)', 'Research Scientist', 'Data Scientist', 'Pharmacist', 'Biotechnology'],
        'exams': ['JEE Main/Advanced', 'NEET', 'BITSAT', 'State Engineering Exams', 'AIIMS']
    },
    'commerce': {
        'subjects': ['Accountancy', 'Business Studies', 'Economics', 'Mathematics', 'Informatics Practices'],
        'careers': ['Chartered Accountant (CA)', 'Company Secretary (CS)', 'Banking', 'Stock Market Analyst', 'Entrepreneur'],
        'exams': ['CA Foundation', 'CS Foundation', 'CMA', 'BBA Entrance', 'B.Com Entrance']
    },
    'arts': {
        'subjects': ['History', 'Political Science', 'Psychology', 'Sociology', 'English Literature'],
        'careers': ['Civil Services (IAS/IPS)', 'Journalism', 'Teaching', 'Social Work', 'Law', 'Content Writing'],
        'exams': ['CLAT (Law)', 'UPSC (Civil Services)', 'Mass Communication Entrance', 'BA Entrance']
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with main menu"""
    keyboard = [
        [InlineKeyboardButton("📚 Explore Streams", callback_data='streams')],
        [InlineKeyboardButton("💼 Career Guidance", callback_data='careers')],
        [InlineKeyboardButton("📝 Entrance Exams", callback_data='exams')],
        [InlineKeyboardButton("🎓 Scholarship Info", callback_data='scholarships')],
        [InlineKeyboardButton("🤖 Ask AI Career Advisor", callback_data='ai_chat')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🎓 *Welcome to Career Guidance Bot!*\n\n"
        "Congratulations on completing your 10th grade! 🎉\n\n"
        "I'm here to help you make informed decisions about:\n"
        "✅ Choosing the right stream (Science/Commerce/Arts)\n"
        "✅ Career opportunities in each field\n"
        "✅ Entrance exams and preparation tips\n"
        "✅ Scholarships and financial aid\n"
        "✅ Personalized career advice using AI\n\n"
        "Select an option below to get started!"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'streams':
        await show_streams(query)
    elif query.data == 'careers':
        await show_career_options(query)
    elif query.data == 'exams':
        await show_exam_info(query)
    elif query.data == 'scholarships':
        await show_scholarship_info(query)
    elif query.data == 'ai_chat':
        await start_ai_chat(query)
    elif query.data.startswith('stream_'):
        await show_stream_details(query)
    elif query.data == 'back_main':
        await back_to_main(query)

async def show_streams(query):
    """Show available streams"""
    keyboard = [
        [InlineKeyboardButton("🔬 Science Stream", callback_data='stream_science')],
        [InlineKeyboardButton("💰 Commerce Stream", callback_data='stream_commerce')],
        [InlineKeyboardButton("🎨 Arts/Humanities Stream", callback_data='stream_arts')],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "📚 *CHOOSE YOUR STREAM*\n\n"
        "After 10th grade, you can choose from three main streams:\n\n"
        "🔬 *Science* - For those interested in technology, medicine, research\n"
        "💰 *Commerce* - For business, finance, and accounting enthusiasts\n"
        "🎨 *Arts/Humanities* - For creative, social science, and liberal arts\n\n"
        "Click on any stream to learn more!"
    )
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_stream_details(query):
    """Show detailed information about a specific stream"""
    stream = query.data.replace('stream_', '')
    info = STREAM_INFO.get(stream, {})
    
    text = f"🎯 *{stream.upper()} STREAM*\n\n"
    
    text += "📖 *Main Subjects:*\n"
    for subject in info.get('subjects', []):
        text += f"• {subject}\n"
    
    text += f"\n💼 *Career Opportunities:*\n"
    for career in info.get('careers', []):
        text += f"• {career}\n"
    
    text += f"\n📝 *Important Entrance Exams:*\n"
    for exam in info.get('exams', []):
        text += f"• {exam}\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Streams", callback_data='streams')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_career_options(query):
    """Show popular career options"""
    text = (
        "💼 *POPULAR CAREER PATHS AFTER 10TH*\n\n"
        "🏥 *Medical Field:*\n"
        "• Doctor (MBBS, BDS)\n"
        "• Nursing\n"
        "• Pharmacy\n"
        "• Physiotherapy\n\n"
        "💻 *Technology & Engineering:*\n"
        "• Software Engineer\n"
        "• Mechanical Engineer\n"
        "• Civil Engineer\n"
        "• Data Scientist\n\n"
        "💰 *Business & Finance:*\n"
        "• Chartered Accountant\n"
        "• Banking Professional\n"
        "• Entrepreneur\n"
        "• Financial Analyst\n\n"
        "⚖️ *Law & Civil Services:*\n"
        "• Lawyer (5-year LLB)\n"
        "• IAS/IPS Officer\n"
        "• Judge\n\n"
        "🎨 *Creative Fields:*\n"
        "• Graphic Designer\n"
        "• Fashion Designer\n"
        "• Content Creator\n"
        "• Journalist\n\n"
        "💡 *Tip:* Choose based on your interests, not just trends!"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_exam_info(query):
    """Show entrance exam information"""
    text = (
        "📝 *IMPORTANT ENTRANCE EXAMS*\n\n"
        "🔬 *For Engineering:*\n"
        "• JEE Main (National level)\n"
        "• JEE Advanced (for IITs)\n"
        "• State Engineering Exams\n"
        "• BITSAT, VITEEE, etc.\n\n"
        "🏥 *For Medical:*\n"
        "• NEET UG (for MBBS/BDS)\n"
        "• AIIMS (separate exam discontinued)\n"
        "• JIPMER\n\n"
        "⚖️ *For Law:*\n"
        "• CLAT (National Law Universities)\n"
        "• AILET (NLU Delhi)\n\n"
        "💰 *For Commerce:*\n"
        "• CA Foundation\n"
        "• CS Foundation\n"
        "• CMA Foundation\n\n"
        "🎓 *General:*\n"
        "• CUET (Central Universities)\n"
        "• State University Entrance Exams\n\n"
        "💡 *Tip:* Start preparing early and practice regularly!"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def show_scholarship_info(query):
    """Show scholarship information"""
    text = (
        "🎓 *SCHOLARSHIP OPPORTUNITIES*\n\n"
        "💰 *Government Scholarships:*\n"
        "• National Means cum Merit Scholarship (NMMS)\n"
        "• Post Matric Scholarship (SC/ST/OBC)\n"
        "• Pre-Matric Scholarship\n"
        "• Prime Minister's Scholarship Scheme\n\n"
        "🏢 *Private Scholarships:*\n"
        "• Sitaram Jindal Foundation\n"
        "• Inspire Scholarship\n"
        "• KVPY (Kishore Vaigyanik Protsahan Yojana)\n"
        "• Buddy4Study Platform\n\n"
        "🌍 *State-Level Scholarships:*\n"
        "Check your state education portal\n\n"
        "📌 *How to Apply:*\n"
        "1. Visit National Scholarship Portal (scholarships.gov.in)\n"
        "2. Register with required documents\n"
        "3. Fill application form\n"
        "4. Submit before deadline\n\n"
        "💡 *Documents Needed:*\n"
        "• 10th Marksheet\n"
        "• Aadhar Card\n"
        "• Bank Details\n"
        "• Income Certificate (if applicable)"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def start_ai_chat(query):
    """Initiate AI chat mode"""
    text = (
        "🤖 *AI CAREER ADVISOR*\n\n"
        "Ask me anything about your career!\n\n"
        "Examples:\n"
        "• What should I choose if I'm good at math?\n"
        "• I'm interested in computers, what are my options?\n"
        "• What's the scope of commerce stream?\n"
        "• How to prepare for JEE?\n\n"
        "Just type your question below! 👇"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context = query._bot
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_ai_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle AI-powered career questions"""
    user_message = update.message.text
    
    # Send typing action
    await update.message.chat.send_action(action="typing")
    
    try:
        # Create context-aware prompt
        prompt = f"""You are a career guidance counselor for Indian students who have completed 10th grade. 
        
Student's question: {user_message}

Provide helpful, accurate, and encouraging advice about:
- Stream selection (Science/Commerce/Arts)
- Career opportunities in India
- Entrance exams and preparation
- Subject choices
- Skill development

Keep your response concise (max 500 words), practical, and motivating. Use bullet points where appropriate."""

        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Add quick action buttons
        keyboard = [
            [InlineKeyboardButton("📚 Explore Streams", callback_data='streams')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='back_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(ai_response, reply_markup=reply_markup, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"AI Error: {e}")
        await update.message.reply_text(
            "Sorry, I couldn't process your question. Please try again or use the menu options.",
            parse_mode='Markdown'
        )

async def back_to_main(query):
    """Return to main menu"""
    keyboard = [
        [InlineKeyboardButton("📚 Explore Streams", callback_data='streams')],
        [InlineKeyboardButton("💼 Career Guidance", callback_data='careers')],
        [InlineKeyboardButton("📝 Entrance Exams", callback_data='exams')],
        [InlineKeyboardButton("🎓 Scholarship Info", callback_data='scholarships')],
        [InlineKeyboardButton("🤖 Ask AI Career Advisor", callback_data='ai_chat')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "🎓 *Career Guidance Bot - Main Menu*\n\n"
        "What would you like to know about your future?\n"
        "Select an option below:"
    )
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = (
        "ℹ️ *HOW TO USE THIS BOT*\n\n"
        "1️⃣ Use /start to see the main menu\n"
        "2️⃣ Click on buttons to explore different options\n"
        "3️⃣ Ask the AI advisor any career-related questions\n"
        "4️⃣ Use /help anytime to see this message\n\n"
        "💡 *Quick Tips:*\n"
        "• Take your time exploring all options\n"
        "• Research about different careers\n"
        "• Talk to professionals in fields you're interested in\n"
        "• Don't rush your decision\n"
        "• Choose based on interest, not peer pressure\n\n"
        "Good luck with your future! 🚀"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ai_query))
    
    # Start the bot
    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
