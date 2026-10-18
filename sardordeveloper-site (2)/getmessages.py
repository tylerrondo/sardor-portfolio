async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Xabarni qabul qiladi va adminga yuboradi."""
    message = update.message.text.strip()
    user = update.effective_user
    
    if len(message) < 5:
        await update.message.reply_text("❌ Xabar juda qisqa. Batafsil yozing:")
        return MESSAGE
    
    if len(message) > 2000:
        await update.message.reply_text("❌ Xabar juda uzun (maks 2000 belgi). Qisqartiring:")
        return MESSAGE
    
    name = context.user_data.get("name", "Noma'lum")
    phone = context.user_data.get("phone", "Noma'lum")
    
    # Username ni tayyorlash
    username_text = f"@{user.username}" if user.username else "yo'q"
    
    # Adminga yuboriladigan xabar
    admin_text = (
        f"🆕 *YANGI XABAR!*\n\n"
        f"👤 *Ism:* {name}\n"
        f"📱 *Aloqa:* {phone}\n"
        f"🆔 *Telegram ID:* `{user.id}`\n"
        f"🔗 *Username:* {username_text}\n\n"
        f"💬 *Xabar:*\n{message}\n\n"
        f"🕐 *Vaqt:* {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    
    try:
        # Adminga yuborish
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode="Markdown"
        )
        
        # Foydalanuvchiga tasdiqlash
        await update.message.reply_text(
            "✅ *Xabaringiz muvaffaqiyatli yuborildi!*\n\n"
            f"👤 Ism: {name}\n"
            f"📱 Aloqa: {phone}\n\n"
            "Sardor tez orada siz bilan bog'lanadi. Rahmat! 🙏\n\n"
            "Yana xabar qoldirish uchun /contact bosing.",
            parse_mode="Markdown"
        )
        
        logger.info(f"Yangi xabar: {name} ({user.id})")
        
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        await update.message.reply_text(
            "❌ Xatolik yuz berdi. Keyinroq qayta urinib ko'ring."
        )
    
    # Ma'lumotlarni tozalash
    context.user_data.clear()
    return ConversationHandler.END