# NotifyPro — FAQ / الأسئلة الشائعة

## General / عام

**Q: What channels does NotifyPro support?**
A: Email, SMS, WhatsApp, Telegram, and Web Push. Each channel has a pluggable provider.

**س: ما القنوات التي يدعمها NotifyPro؟**
ج: البريد الإلكتروني، الرسائل القصيرة، واتساب، تليجرام، والإشعارات الفورية. كل قناة لها مزود قابل للتوصيل.

---

**Q: Can users opt out of notifications?**
A: Yes. Users can configure per-channel preferences, set quiet hours, and opt out entirely via the Preferences module.

**س: هل يمكن للمستخدمين إلغاء الاشتراك في الإشعارات؟**
ج: نعم. يمكن للمستخدمين ضبط تفضيلاتهم لكل قناة، وتحديد ساعات الهدوء، وإلغاء الاشتراك بالكامل.

---

**Q: How do I trigger notifications from DocType events?**
A: Use the NP Hook Rule DocType. Configure the source DocType, event (on_submit, on_update, etc.), and the template to use.

---

**Q: How are failed notifications handled?**
A: Failed notifications are logged in NP Notification Log with error details. If a fallback channel is configured via Routing Rules, the system automatically retries on the next channel.

---

**Q: Does NotifyPro support bulk notifications?**
A: Yes. Use the Campaign module to define audiences and schedule bulk sends with rate limiting.
