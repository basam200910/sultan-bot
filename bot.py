import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

TOKEN = "9084516304:AAFNc7Iyw4pfmmWbP5z3wu2lerA_XtZ_SQo"
WHATSAPP_URL = "https://wa.me/201021343490?text=السلام%20عليكم،%20بتواصل%20معاكم%20بخصوص%20خدمات%20السلطان%20ستور"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# بيانات الأجهزة المباشرة (تقدر تضيف أو تعدل أي رقم هنا مباشرة)
MAINTENANCE_DATA = {
    "101": {
        "client_name": "محمد أحمد",
        "device": "Samsung A54",
        "issue": "تغيير شاشة أصلية",
        "status": "جاهز للاستلام ✅",
        "cost": "1800 جنيه"
    },
    "102": {
        "client_name": "محمود علي",
        "device": "iPhone 11",
        "issue": "تغيير بطارية وفحص شحن",
        "status": "جاري الصيانة ⏳",
        "cost": "سيتم تحديده بعد الفحص"
    },
    "103": {
        "client_name": "خالد حسن",
        "device": "Redmi Note 12",
        "issue": "سوفت وير وفك رمز",
        "status": "تم الفحص في انتظار موافقة العميل ⚠️",
        "cost": "200 جنيه"
    }
}

# دالة لتحويل أي أرقام مكتوبة بالعربي إلى إنجليزي لضمان دقة البحث
def clean_receipt_input(text):
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    translation_table = str.maketrans(arabic_digits, english_digits)
    return text.strip().translate(translation_table)

# القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_for_receipt"] = False
    user_name = update.effective_user.first_name

    keyboard = [
        [InlineKeyboardButton("💬 تواصل مباشر عبر واتساب", url=WHATSAPP_URL)],
        [
            InlineKeyboardButton("🔍 الاستعلام عن حالة جهاز", callback_data="check_device"),
            InlineKeyboardButton("🛠️ خدمات الصيانة", callback_data="services")
        ],
        [
            InlineKeyboardButton("🌐 عروض وباقات النت", callback_data="packages"),
            InlineKeyboardButton("📍 الموقع والمواعيد", callback_data="location")
        ],
        [InlineKeyboardButton("📞 أرقام التواصل", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"أهلاً بك يا {user_name} في بوت السلطان ستور 📱✨\n\n"
        "اختر الخدمة المطلوبة أو استعلم عن جهازك مباشرة من الأزرار 👇"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(welcome_text, reply_markup=reply_markup)

# التعامل مع الأزرار
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    back_button = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]]
    back_markup = InlineKeyboardMarkup(back_button)

    if query.data == "check_device":
        context.user_data["waiting_for_receipt"] = True
        text = (
            "🔍 **الاستعلام عن حالة الصيانة**\n\n"
            "من فضلك اكتب الآن **رقم إيصال الاستلام** (مثال: `101`) في رسالة وأرسلها هنا 👇"
        )
        await query.edit_message_text(text=text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "services":
        text = (
            "🛠️ **خدمات الصيانة - السلطان ستور**\n\n"
            "• صيانة فورية لجميع أنواع الهواتف الذكية.\n"
            "• تغيير شاشات وبطاريات وقطع غيار أصلية.\n"
            "• سوفت وير كامل وحلول أعطال الشحن والمايك.\n"
            "• إيصال فحص رسمي مع كل جهاز."
        )
        await query.edit_message_text(text=text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "packages":
        text = (
            "🌐 **عروض وتجديد باقات النت**\n\n"
            "• شحن وتجديد فوري لجميع الباقات والمودم المنزلي.\n"
            "• عروض يومية وشهرية بأسعار مميزة."
        )
        await query.edit_message_text(text=text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "location":
        text = (
            "📍 **مقر المحل ومواعيد العمل**\n\n"
            "• العنوان: قنا - نقادة - الخطارة (بجوار بيت العمدة).\n"
            "• مواعيد العمل: يومياً من 10 صباحاً حتى 11 مساءً."
        )
        await query.edit_message_text(text=text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "contact":
        text = (
            "📞 **أرقام التواصل**\n\n"
            "• الخط الأول: `01021343490`\n"
            "• الخط الثاني: `01019806060`"
        )
        await query.edit_message_text(text=text, reply_markup=back_markup, parse_mode="Markdown")

    elif query.data == "main_menu":
        await start(update, context)

# التعامل مع كتابة رقم الإيصال
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_receipt"):
        raw_text = update.message.text
        receipt_number = clean_receipt_input(raw_text)

        back_button = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="main_menu")]]
        back_markup = InlineKeyboardMarkup(back_button)

        if receipt_number in MAINTENANCE_DATA:
            item = MAINTENANCE_DATA[receipt_number]
            result_text = (
                f"📋 **تقرير حالة الجهاز - إيصال رقم #{receipt_number}**\n\n"
                f"👤 **العميل:** {item['client_name']}\n"
                f"📱 **الجهاز:** {item['device']}\n"
                f"🔧 **العطل المطلوب:** {item['issue']}\n"
                f"📌 **الحالة الحالية:** {item['status']}\n"
                f"💰 **التكلفة:** {item['cost']}\n\n"
                "يسعدنا تواصلك دائماً مع السلطان ستور."
            )
            context.user_data["waiting_for_receipt"] = False
            await update.message.reply_text(result_text, reply_markup=back_markup, parse_mode="Markdown")
        else:
            await update.message.reply_text(
                f"❌ لم يتم العثور على جهاز مسجل برقم الإيصال: `{raw_text}`\n\n"
                "تأكد من كتابة الرقم بشكل صحيح (جرب كتابة 101 أو 102 أو 103 للتجربة).",
                reply_markup=back_markup,
                parse_mode="Markdown"
            )
    else:
        await update.message.reply_text(
            "مرحباً بك! للاستفادة من الخدمات، يرجى الضغط على /start واختيار ما يناسبك."
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("البوت شغال الآن بالبيانات المباشرة...")
    app.run_polling()