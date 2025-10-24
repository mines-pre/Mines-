from flask import Flask, request, jsonify
import os
import requests
import json
import random
import time

app = Flask(__name__)

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')
VERCEL_URL = os.environ.get('VERCEL_URL')
AFFILIATE_LINK = os.environ.get('AFFILIATE_LINK', 'https://lkpq.cc/73f2')

# Storage
users_data = {}
postback_events = []

# All Mines Signals
MINES_SIGNALS = [
    {"traps": 1, "accuracy": 97, "grid": ["🔒🔒🔒🔒💰", "🔒🔒🔒💰🔒", "💰🔒🔒🔒🔒", "🔒💰🔒🔒🔒", "🔒🔒🔒🔒💰"]},
    {"traps": 1, "accuracy": 90, "grid": ["🔒🔒🔒🔒🔒", "💰🔒💰🔒🔒", "🔒💰🔒🔒🔒", "🔒💰🔒💰🔒", "🔒🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 96, "grid": ["🔒🔒🔒🔒🔒", "🔒🔒🔒💰🔒", "🔒💰🔒🔒💰", "💰🔒🔒🔒💰", "🔒🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 95, "grid": ["💰🔒🔒🔒🔒", "💰🔒🔒🔒🔒", "🔒🔒🔒🔒🔒", "💰🔒🔒🔒🔒", "💰🔒🔒💰🔒"]},
    {"traps": 1, "accuracy": 96, "grid": ["🔒🔒💰🔒🔒", "🔒💰🔒💰🔒", "💰🔒🔒🔒🔒", "🔒🔒💰🔒🔒", "🔒🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 91, "grid": ["🔒💰🔒🔒🔒", "🔒💰🔒🔒🔒", "🔒💰🔒💰🔒", "💰🔒🔒🔒🔒", "🔒🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 94, "grid": ["🔒💰💰🔒🔒", "🔒🔒🔒🔒🔒", "🔒🔒🔒🔒💰", "🔒🔒🔒🔒🔒", "💰🔒💰🔒🔒"]},
    {"traps": 1, "accuracy": 92, "grid": ["🔒🔒🔒💰🔒", "💰💰🔒🔒💰", "🔒🔒🔒🔒🔒", "🔒🔒🔒💰🔒", "🔒🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 90, "grid": ["💰🔒🔒💰🔒", "💰🔒💰🔒🔒", "🔒🔒🔒🔒🔒", "🔒💰🔒🔒🔒", "🔒🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 92, "grid": ["🔒🔒🔒💰🔒", "🔒🔒🔒🔒🔒", "🔒🔒🔒🔒🔒", "🔒🔒💰🔒🔒", "💰🔒💰💰🔒"]},
    {"traps": 1, "accuracy": 93, "grid": ["💰🔒🔒🔒🔒", "🔒🔒💰🔒🔒", "💰🔒🔒🔒🔒", "🔒🔒💰🔒🔒", "💰🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 97, "grid": ["💰🔒🔒🔒🔒", "🔒💰🔒🔒🔒", "🔒🔒🔒🔒🔒", "💰💰🔒🔒💰", "🔒🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 90, "grid": ["💰🔒🔒💰🔒", "🔒🔒🔒🔒🔒", "🔒🔒🔒🔒🔒", "💰🔒💰🔒🔒", "💰🔒🔒🔒🔒"]},
    {"traps": 1, "accuracy": 96, "grid": ["🔒🔒🔒🔒🔒", "🔒💰🔒🔒🔒", "🔒🔒🔒🔒🔒", "🔒🔒💰🔒🔒", "💰🔒💰💰🔒"]},
    {"traps": 1, "accuracy": 94, "grid": ["🔒🔒💰🔒🔒", "🔒🔒💰🔒🔒", "💰🔒🔒🔒🔒", "🔒💰🔒🔒🔒", "🔒💰🔒🔒🔒"]}
]

# Complete Language Messages with ALL 5 Languages
MESSAGES = {
    'en': {
        'welcome': '✅ <b>You selected English!</b>',
        'step1': '🌐 <b>Step 1 - Register</b>',
        'account_must_be_new': '‼️ <b>THE ACCOUNT MUST BE NEW</b>',
        'step1_instructions': '1️⃣ If after clicking the "REGISTER" button you get to the old account, you need to log out of it and click the button again.\n\n2️⃣ Specify a promocode during registration: <b>OGGY</b>\n\n3️⃣ Make a Minimum deposit atleast <b>500₹ or 5$</b> in any currency',
        'after_success': '✅ After Successfully REGISTRATION, click the "CHECK REGISTRATION" button',
        'enter_player_id': '🎯 <b>Please enter your 1Win Player ID to verify:</b>',
        'how_to_find_id': '📝 <b>How to find Player ID:</b>\n1. Login to 1Win account\n2. Go to Profile Settings\n3. Copy Player ID number\n4. Paste it here',
        'enter_id_now': '🔢 <b>Enter your Player ID now:</b>',
        'congratulations': '🎉 <b>Congratulations!</b>',
        'not_registered': '❌ <b>Sorry, You are Not Registered!</b>',
        'not_registered_msg': 'Please click the REGISTER button first and complete your registration using our link.\n\nAfter successful registration, come back and enter your Player ID.',
        'registered_no_deposit': '🎉 <b>Great, you have successfully completed registration!</b>',
        'sync_success': '✅ Your account is synchronized with the bot',
        'deposit_required': '💴 To gain access to signals, deposit your account (make a deposit) with at least <b>500₹ or $5</b> in any currency',
        'after_deposit': '🕹️ After successfully replenishing your account, click on the CHECK DEPOSIT button and gain access',
        'limit_reached': "⚠️ <b>You've Reached Your Limit!</b>",
        'deposit_again': 'Please deposit again atleast <b>400₹ or 4$</b> in any currency for continue prediction',
        'get_signal': '🕹️ Get a signal',
        'next_signal': '🔄 Next Signal',
        'back': '🔙 Back',
        'deposit_again_btn': '💰 Deposit Again',
        'register_now': '📲 Register Now',
        'check_deposit': '🔍 Check Deposit',
        'register_btn': '📲 Register',
        'check_registration_btn': '🔍 Check Registration',
        'motivational': "💎 You're missing your chance to win big! /start to get Prediction now 🚀",
        'signal_title': '💣 <b>Mines - Signals</b> 💣',
        'select_traps': '💣 <b>Select:</b> {} traps',
        'accuracy': '💡 <b>Accuracy:</b> {}%',
        'open_cells': '👉 <b>Open the cells</b> 👇',
        'get_new_signal': '❇️ <b>Get a new signal</b> 👇',
        'automatic_check': '🔄 Automatic Check',
        'manual_entry': '🔢 Manual Entry',
        'check_again': '🔄 Check Again',
        'auto_verify_failed': '❌ Automatic verification failed. Please enter Player ID manually.',
        'verification_options': '🎯 <b>Verify Your Registration</b>',
        'choose_method': 'Choose verification method:',
        'auto_check_desc': '🔄 <b>Automatic Check</b>\n• Instant verification\n• No Player ID needed\n• Works if you used our link',
        'manual_entry_desc': '🔢 <b>Manual Entry</b>\n• Enter Player ID manually\n• 100% accurate\n• Works in all cases',
        'checking_status': '🔍 <b>Checking your registration status...</b>',
        'no_registration_found': '❌ <b>No registration found yet!</b>',
        'wait_and_retry': 'Please wait 2-3 minutes after registration and click Check Again button.\nOr enter your Player ID manually for instant verification.',
        'registration_confirmed': '🎉 <b>Registration Confirmed!</b>',
        'deposit_received': '💰 <b>Deposit Received!</b>',
        'check_status': '🔄 Check Status'
    },
    'hi': {
        'welcome': '✅ <b>आपने हिंदी चुनी!</b>',
        'step1': '🌐 <b>चरण 1 - पंजीकरण</b>',
        'account_must_be_new': '‼️ <b>खाता नया होना चाहिए</b>',
        'step1_instructions': '1️⃣ यदि "पंजीकरण" बटन पर क्लिक करने के बाद आपको पुराना खाता मिलता है, तो आपको उससे लॉग आउट करना होगा और बटन को फिर से क्लिक करना होगा।\n\n2️⃣ पंजीकरण के दौरान प्रोमोकोड निर्दिष्ट करें: <b>OGGY</b>\n\n3️⃣ न्यूनतम जमा करें कम से कम <b>500₹ या 5$</b> किसी भी मुद्रा में',
        'after_success': '✅ सफल पंजीकरण के बाद, "पंजीकरण जांचें" बटन पर क्लिक करें',
        'enter_player_id': '🎯 <b>कृपया सत्यापन के लिए अपना 1Win Player ID दर्ज करें:</b>',
        'how_to_find_id': '📝 <b>Player ID कैसे ढूंढें:</b>\n1. 1Win खाते में लॉगिन करें\n2. प्रोफाइल सेटिंग्स पर जाएं\n3. Player ID नंबर कॉपी करें\n4. यहां पेस्ट करें',
        'enter_id_now': '🔢 <b>अपना Player ID अभी दर्ज करें:</b>',
        'congratulations': '🎉 <b>बधाई हो!</b>',
        'not_registered': '❌ <b>क्षमा करें, आप पंजीकृत नहीं हैं!</b>',
        'not_registered_msg': 'कृपया पहले REGISTER बटन पर क्लिक करें और हमारे लिंक का उपयोग करके अपना पंजीकरण पूरा करें।\n\nसफल पंजीकरण के बाद, वापस आएं और अपना Player ID दर्ज करें।',
        'registered_no_deposit': '🎉 <b>बढ़िया, आपने सफलतापूर्वक पंजीकरण पूरा कर लिया है!</b>',
        'sync_success': '✅ आपका खाता बॉट के साथ सिंक्रनाइज़ हो गया है',
        'deposit_required': '💴 सिग्नल तक पहुंच प्राप्त करने के लिए, अपने खाते में कम से कम <b>500₹ या $5</b> किसी भी मुद्रा में जमा करें',
        'after_deposit': '🕹️ अपना खाता सफलतापूर्वक भरने के बाद, CHECK DEPOSIT बटन पर क्लिक करें और पहुंच प्राप्त करें',
        'limit_reached': "⚠️ <b>आप अपनी सीमा तक पहुँच गए हैं!</b>",
        'deposit_again': 'कृपया भविष्यवाणी जारी रखने के लिए फिर से कम से कम <b>400₹ या 4$</b> किसी भी मुद्रा में जमा करें',
        'get_signal': '🕹️ सिग्नल प्राप्त करें',
        'next_signal': '🔄 अगला सिग्नल',
        'back': '🔙 वापस',
        'deposit_again_btn': '💰 फिर से जमा करें',
        'register_now': '📲 अभी पंजीकरण करें',
        'check_deposit': '🔍 जमा जांचें',
        'register_btn': '📲 पंजीकरण',
        'check_registration_btn': '🔍 पंजीकरण जांचें',
        'motivational': "💎 आप बड़ी जीत का मौका खो रहे हैं! भविष्यवाणी प्राप्त करने के लिए /start दबाएं 🚀",
        'signal_title': '💣 <b>Mines - सिग्नल</b> 💣',
        'select_traps': '💣 <b>चुनें:</b> {} जाल',
        'accuracy': '💡 <b>सटीकता:</b> {}%',
        'open_cells': '👉 <b>कोशिकाएं खोलें</b> 👇',
        'get_new_signal': '❇️ <b>नया सिग्नल प्राप्त करें</b> 👇',
        'automatic_check': '🔄 स्वचालित जांच',
        'manual_entry': '🔢 मैनुअल प्रविष्टि',
        'check_again': '🔄 फिर से जांचें',
        'auto_verify_failed': '❌ स्वचालित सत्यापन विफल। कृपया मैन्युअल रूप से Player ID दर्ज करें।',
        'verification_options': '🎯 <b>अपना पंजीकरण सत्यापित करें</b>',
        'choose_method': 'सत्यापन विधि चुनें:',
        'auto_check_desc': '🔄 <b>स्वचालित जांच</b>\n• तत्काल सत्यापन\n• Player ID की आवश्यकता नहीं\n• काम करता है यदि आपने हमारा लिंक इस्तेमाल किया',
        'manual_entry_desc': '🔢 <b>मैनुअल प्रविष्टि</b>\n• मैन्युअल रूप से Player ID दर्ज करें\n• 100% सटीक\n• सभी मामलों में काम करता है',
        'checking_status': '🔍 <b>आपकी पंजीकरण स्थिति की जाँच की जा रही है...</b>',
        'no_registration_found': '❌ <b>अभी तक कोई पंजीकरण नहीं मिला!</b>',
        'wait_and_retry': 'कृपया पंजीकरण के 2-3 मिनट बाद प्रतीक्षा करें और फिर से जांचें बटन क्लिक करें।\nया त्वरित सत्यापन के लिए अपना Player ID मैन्युअल रूप से दर्ज करें।',
        'registration_confirmed': '🎉 <b>पंजीकरण पुष्टि हुई!</b>',
        'deposit_received': '💰 <b>जमा प्राप्त हुआ!</b>',
        'check_status': '🔄 स्थिति जांचें'
    },
    'bn': {
        'welcome': '✅ <b>আপনি বাংলা নির্বাচন করেছেন!</b>',
        'step1': '🌐 <b>ধাপ 1 - নিবন্ধন</b>',
        'account_must_be_new': '‼️ <b>অ্যাকাউন্টটি নতুন হতে হবে</b>',
        'step1_instructions': '১️⃣ "নিবন্ধন" বাটনে ক্লিক করার পরে যদি আপনি পুরানো অ্যাকাউন্টে প্রবেশ করেন, তাহলে আপনাকে এটি থেকে লগ আউট করতে হবে এবং বাটনটি আবার ক্লিক করতে হবে।\n\n২️⃣ নিবন্ধনের সময় প্রমোকোড নির্দিষ্ট করুন: <b>OGGY</b>\n\n৩️⃣ ন্যূনতম জমা করুন কমপক্ষে <b>500₹ বা 5$</b> যেকোনো মুদ্রায়',
        'after_success': '✅ সফল নিবন্ধনের পরে, "নিবন্ধন পরীক্ষা করুন" বাটনে ক্লিক করুন',
        'enter_player_id': '🎯 <b>যাচাই করার জন্য আপনার 1Win Player ID লিখুন:</b>',
        'how_to_find_id': '📝 <b>Player ID কিভাবে খুঁজে পাবেন:</b>\n1. 1Win অ্যাকাউন্টে লগইন করুন\n2. প্রোফাইল সেটিংসে যান\n3. Player ID নম্বর কপি করুন\n4. এখানে পেস্ট করুন',
        'enter_id_now': '🔢 <b>এখনই আপনার Player ID লিখুন:</b>',
        'congratulations': '🎉 <b>অভিনন্দন!</b>',
        'not_registered': '❌ <b>দুঃখিত, আপনি নিবন্ধিত নন!</b>',
        'not_registered_msg': 'অনুগ্রহ করে প্রথমে REGISTER বাটনে ক্লিক করুন এবং আমাদের লিঙ্ক ব্যবহার করে আপনার নিবন্ধন সম্পূর্ণ করুন।\n\nসফল নিবন্ধনের পরে, ফিরে আসুন এবং আপনার Player ID লিখুন।',
        'registered_no_deposit': '🎉 <b>দারুন, আপনি সফলভাবে নিবন্ধন সম্পূর্ণ করেছেন!</b>',
        'sync_success': '✅ আপনার অ্যাকাউন্ট বটের সাথে সিঙ্ক্রোনাইজ হয়েছে',
        'deposit_required': '💴 সিগন্যাল অ্যাক্সেস পেতে, আপনার অ্যাকাউন্টে কমপক্ষে <b>500₹ বা $5</b> যেকোনো মুদ্রায় জমা করুন',
        'after_deposit': '🕹️ আপনার অ্যাকাউন্ট সফলভাবে রিচার্জ করার পরে, CHECK DEPOSIT বাটনে ক্লিক করুন এবং অ্যাক্সেস পান',
        'limit_reached': "⚠️ <b>আপনি আপনার সীমায় পৌঁছে গেছেন!</b>",
        'deposit_again': 'অনুগ্রহ করে ভবিষ্যদ্বাণী চালিয়ে যেতে আবার কমপক্ষে <b>400₹ বা 4$</b> যেকোনো মুদ্রায় জমা করুন',
        'get_signal': '🕹️ সিগন্যাল পান',
        'next_signal': '🔄 পরবর্তী সিগন্যাল',
        'back': '🔙 ফিরে যান',
        'deposit_again_btn': '💰 আবার জমা করুন',
        'register_now': '📲 এখনই নিবন্ধন করুন',
        'check_deposit': '🔍 জমা পরীক্ষা করুন',
        'register_btn': '📲 নিবন্ধন',
        'check_registration_btn': '🔍 নিবন্ধন পরীক্ষা',
        'motivational': "💎 আপনি বড় জয়ের সুযোগ হারাচ্ছেন! ভবিষ্যদ্বাণী পেতে /start টিপুন 🚀",
        'signal_title': '💣 <b>Mines - সিগন্যাল</b> 💣',
        'select_traps': '💣 <b>নির্বাচন করুন:</b> {} ফাঁদ',
        'accuracy': '💡 <b>সঠিকতা:</b> {}%',
        'open_cells': '👉 <b>সেল খুলুন</b> 👇',
        'get_new_signal': '❇️ <b>নতুন সিগন্যাল পান</b> 👇',
        'automatic_check': '🔄 স্বয়ংক্রিয় চেক',
        'manual_entry': '🔢 ম্যানুয়াল এন্ট্রি',
        'check_again': '🔄 আবার চেক করুন',
        'auto_verify_failed': '❌ স্বয়ংক্রিয় যাচাই ব্যর্থ হয়েছে। দয়া করে ম্যানুয়ালি Player ID লিখুন।',
        'verification_options': '🎯 <b>আপনার নিবন্ধন যাচাই করুন</b>',
        'choose_method': 'যাচাই পদ্ধতি নির্বাচন করুন:',
        'auto_check_desc': '🔄 <b>স্বয়ংক্রিয় চেক</b>\n• তাৎক্ষণিক যাচাই\n• Player ID প্রয়োজন নেই\n• কাজ করে যদি আপনি আমাদের লিঙ্ক ব্যবহার করেন',
        'manual_entry_desc': '🔢 <b>ম্যানুয়াল এন্ট্রি</b>\n• ম্যানুয়ালি Player ID লিখুন\n• 100% সঠিক\n• সব ক্ষেত্রে কাজ করে',
        'checking_status': '🔍 <b>আপনার নিবন্ধন স্ট্যাটাস চেক করা হচ্ছে...</b>',
        'no_registration_found': '❌ <b>এখনও কোন নিবন্ধন পাওয়া যায়নি!</b>',
        'wait_and_retry': 'নিবন্ধনের ২-৩ মিনিট পরে অপেক্ষা করুন এবং আবার চেক করুন বাটন ক্লিক করুন।\nঅথবা তাত্ক্ষণিক যাচাইয়ের জন্য আপনার Player ID ম্যানুয়ালি লিখুন।',
        'registration_confirmed': '🎉 <b>নিবন্ধন নিশ্চিত হয়েছে!</b>',
        'deposit_received': '💰 <b>জমা প্রাপ্ত!</b>',
        'check_status': '🔄 স্ট্যাটাস চেক করুন'
    },
    'ur': {
        'welcome': '✅ <b>آپ نے اردو منتخب کی!</b>',
        'step1': '🌐 <b>مرحلہ 1 - رجسٹریشن</b>',
        'account_must_be_new': '‼️ <b>اکاؤنٹ نیا ہونا چاہیے</b>',
        'step1_instructions': '1️⃣ اگر "رجسٹر" بٹن پر کلک کرنے کے بعد آپ کو پرانا اکاؤنٹ ملتا ہے، تو آپ کو اس سے لاگ آؤٹ ہونا پڑے گا اور بٹن کو دوبارہ کلک کرنا پڑے گا۔\n\n2️⃣ رجسٹریشن کے دوران پروموکوڈ بتائیں: <b>OGGY</b>\n\n3️⃣ کم از کم ڈپازٹ کریں <b>500₹ یا 5$</b> کسی بھی کرنسی میں',
        'after_success': '✅ کامیاب رجسٹریشن کے بعد، "چیک رجسٹریشن" بٹن پر کلک کریں',
        'enter_player_id': '🎯 <b>براہ کرم تصدیق کے لیے اپنا 1Win Player ID درج کریں:</b>',
        'how_to_find_id': '📝 <b>Player ID کیسے ڈھونڈیں:</b>\n1. 1Win اکاؤنٹ میں لاگ ان کریں\n2. پروفائل سیٹنگز پر جائیں\n3. Player ID نمبر کاپی کریں\n4. یہاں پیسٹ کریں',
        'enter_id_now': '🔢 <b>ابھی اپنا Player ID درج کریں:</b>',
        'congratulations': '🎉 <b>مبارک ہو!</b>',
        'not_registered': '❌ <b>معذرت، آپ رجسٹرڈ نہیں ہیں!</b>',
        'not_registered_msg': 'براہ کرم پہلے REGISTER بٹن پر کلک کریں اور ہمارے لنک کا استعمال کرتے ہوئے اپنی رجسٹریشن مکمل کریں۔\n\nکامیاب رجسٹریشن کے بعد، واپس آئیں اور اپنا Player ID درج کریں۔',
        'registered_no_deposit': '🎉 <b>بہت اچھے، آپ نے کامیابی کے ساتھ رجسٹریشن مکمل کر لی ہے!</b>',
        'sync_success': '✅ آپ کا اکاؤنٹ بوٹ کے ساتھ sync ہو گیا ہے',
        'deposit_required': '💴 سگنلز تک رسائی حاصل کرنے کے لیے، اپنے اکاؤنٹ میں کم از کم <b>500₹ یا $5</b> کسی بھی کرنسی میں ڈپازٹ کریں',
        'after_deposit': '🕹️ اپنا اکاؤنٹ کامیابی سے ریچارج کرنے کے بعد، CHECK DEPOSIT بٹن پر کلک کریں اور رسائی حاصل کریں',
        'limit_reached': "⚠️ <b>آپ اپنی حد تک پہنچ گئے ہیں!</b>",
        'deposit_again': 'براہ کرم پیشن گوئی جاری رکھنے کے لیے پھر سے کم از کم <b>400₹ یا 4$</b> کسی بھی کرنسی میں ڈپازٹ کریں',
        'get_signal': '🕹️ سگنل حاصل کریں',
        'next_signal': '🔄 اگلا سگنل',
        'back': '🔙 واپس',
        'deposit_again_btn': '💰 دوبارہ ڈپازٹ کریں',
        'register_now': '📲 ابھی رجسٹر کریں',
        'check_deposit': '🔍 ڈپازٹ چیک کریں',
        'register_btn': '📲 رجسٹر',
        'check_registration_btn': '🔍 رجسٹریشن چیک کریں',
        'motivational': "💎 آپ بڑی جیت کا موقع کھو رہے ہیں! پیشن گوئی حاصل کرنے کے لیے /start دبائیں 🚀",
        'signal_title': '💣 <b>Mines - سگنل</b> 💣',
        'select_traps': '💣 <b>منتخب کریں:</b> {} جال',
        'accuracy': '💡 <b>درستگی:</b> {}%',
        'open_cells': '👉 <b>خانے کھولیں</b> 👇',
        'get_new_signal': '❇️ <b>نیا سگنل حاصل کریں</b> 👇',
        'automatic_check': '🔄 خودکار چیک',
        'manual_entry': '🔢 دستی اندراج',
        'check_again': '🔄 دوبارہ چیک کریں',
        'auto_verify_failed': '❌ خودکار تصدیق ناکام ہوئی۔ براہ کرم دستی طور پر Player ID درج کریں۔',
        'verification_options': '🎯 <b>اپنی رجسٹریشن کی تصدیق کریں</b>',
        'choose_method': 'تصدیق کا طریقہ منتخب کریں:',
        'auto_check_desc': '🔄 <b>خودکار چیک</b>\n• فوری تصدیق\n• Player ID کی ضرورت نہیں\n• کام کرتا ہے اگر آپ نے ہمارا لنک استعمال کیا',
        'manual_entry_desc': '🔢 <b>دستی اندراج</b>\n• دستی طور پر Player ID درج کریں\n• 100% درست\n• تمام معاملات میں کام کرتا ہے',
        'checking_status': '🔍 <b>آپ کی رجسٹریشن کی حیثیت چیک کی جا رہی ہے...</b>',
        'no_registration_found': '❌ <b>ابھی تک کوئی رجسٹریشن نہیں ملی!</b>',
        'wait_and_retry': 'براہ کرم رجسٹریشن کے 2-3 منٹ بعد انتظار کریں اور دوبارہ چیک کریں بٹن پر کلک کریں۔\nیا فوری تصدیق کے لیے اپنا Player ID دستی طور پر درج کریں۔',
        'registration_confirmed': '🎉 <b>رجسٹریشن کی تصدیق ہو گئی!</b>',
        'deposit_received': '💰 <b>ڈپازٹ موصول!</b>',
        'check_status': '🔄 حیثیت چیک کریں'
    },
    'ne': {
        'welcome': '✅ <b>तपाईंले नेपाली चयन गर्नुभयो!</b>',
        'step1': '🌐 <b>चरण 1 - दर्ता</b>',
        'account_must_be_new': '‼️ <b>खाता नयाँ हुनुपर्छ</b>',
        'step1_instructions': '१️⃣ यदि "दर्ता" बटन क्लिक गरेपछि तपाईंले पुरानो खाता प्राप्त गर्नुभयो भने, तपाईंले यसबाट लग आउट गर्नुपर्छ र बटन फेरि क्लिक गर्नुपर्छ।\n\n२️⃣ दर्ताको समयमा प्रोमोकोड निर्दिष्ट गर्नुहोस्: <b>OGGY</b>\n\n३️⃣ न्यूनतम जम्मा गर्नुहोस् कम्तिमा <b>500₹ वा 5$</b> कुनै पनि मुद्रामा',
        'after_success': '✅ सफल दर्ता पछि, "दर्ता जाँच गर्नुहोस्" बटन क्लिक गर्नुहोस्',
        'enter_player_id': '🎯 <b>कृपया सत्यापनको लागि आफ्नो 1Win Player ID प्रविष्ट गर्नुहोस्:</b>',
        'how_to_find_id': '📝 <b>Player ID कसरी खोज्ने:</b>\n1. 1Win खातामा लगइन गर्नुहोस्\n2. प्रोफाइल सेटिङहरूमा जानुहोस्\n3. Player ID नम्बर कपी गर्नुहोस्\n4. यहाँ पेस्ट गर्नुहोस्',
        'enter_id_now': '🔢 <b>अब आफ्नो Player ID प्रविष्ट गर्नुहोस्:</b>',
        'congratulations': '🎉 <b>बधाई छ!</b>',
        'not_registered': '❌ <b>माफ गर्नुहोस्, तपाईं दर्ता गरिएको छैन!</b>',
        'not_registered_msg': 'कृपया पहिले REGISTER बटन क्लिक गर्नुहोस् र हाम्रो लिङ्क प्रयोग गरेर आफ्नो दर्ता पूरा गर्नुहोस्।\n\nसफल दर्ता पछि, फिर्ता आउनुहोस् र आफ्नो Player ID प्रविष्ट गर्नुहोस्।',
        'registered_no_deposit': '🎉 <b>राम्रो, तपाईंले सफलतापूर्वक दर्ता पूरा गर्नुभयो!</b>',
        'sync_success': '✅ तपाईंको खाता बोटसँग सिङ्क्रोनाइज भएको छ',
        'deposit_required': '💴 सिग्नलहरू पहुँच प्राप्त गर्न, आफ्नो खातामा कम्तिमा <b>500₹ वा $5</b> कुनै पनि मुद्रामा जम्मा गर्नुहोस्',
        'after_deposit': '🕹️ आफ्नो खाता सफलतापूर्वक रिचार्ज गरेपछि, CHECK DEPOSIT बटन क्लिक गर्नुहोस् र पहुँच प्राप्त गर्नुहोस्',
        'limit_reached': "⚠️ <b>तपाईं आफ्नो सीमामा पुग्नुभयो!</b>",
        'deposit_again': 'कृपया भविष्यवाणी जारी राख्न फेरि कम्तिमा <b>400₹ वा 4$</b> कुनै पनि मुद्रामा जम्मा गर्नुहोस्',
        'get_signal': '🕹️ सिग्नल प्राप्त गर्नुहोस्',
        'next_signal': '🔄 अर्को सिग्नल',
        'back': '🔙 फिर्ता',
        'deposit_again_btn': '💰 फेरि जम्मा गर्नुहोस्',
        'register_now': '📲 अहिले दर्ता गर्नुहोस्',
        'check_deposit': '🔍 जम्मा जाँच गर्नुहोस्',
        'register_btn': '📲 दर्ता',
        'check_registration_btn': '🔍 दर्ता जाँच',
        'motivational': "💎 तपाईं ठूलो जित्ने मौका गुमाउँदै हुनुहुन्छ! भविष्यवाणी प्राप्त गर्न /start थिच्नुहोस् 🚀",
        'signal_title': '💣 <b>Mines - सिग्नल</b> 💣',
        'select_traps': '💣 <b>छान्नुहोस्:</b> {} जाल',
        'accuracy': '💡 <b>सटिकता:</b> {}%',
        'open_cells': '👉 <b>कोठाहरू खोल्नुहोस्</b> 👇',
        'get_new_signal': '❇️ <b>नयाँ सिग्नल प्राप्त गर्नुहोस्</b> 👇',
        'automatic_check': '🔄 स्वचालित जाँच',
        'manual_entry': '🔢 म्यानुअल प्रविष्टि',
        'check_again': '🔄 फेरि जाँच गर्नुहोस्',
        'auto_verify_failed': '❌ स्वचालित प्रमाणीकरण असफल भयो। कृपया म्यानुअल रूपमा Player ID प्रविष्ट गर्नुहोस्।',
        'verification_options': '🎯 <b>आफ्नो दर्ता प्रमाणित गर्नुहोस्</b>',
        'choose_method': 'प्रमाणीकरण विधि चयन गर्नुहोस्:',
        'auto_check_desc': '🔄 <b>स्वचालित जाँच</b>\n• तत्काल प्रमाणीकरण\n• Player ID आवश्यक छैन\n• काम गर्दछ यदि तपाईंले हाम्रो लिङ्क प्रयोग गर्नुभयो भने',
        'manual_entry_desc': '🔢 <b>म्यानुअल प्रविष्टि</b>\n• म्यानुअल रूपमा Player ID प्रविष्ट गर्नुहोस्\n• 100% सही\n• सबै अवस्थामा काम गर्दछ',
        'checking_status': '🔍 <b>तपाईंको दर्ता स्थिति जाँच गरिँदैछ...</b>',
        'no_registration_found': '❌ <b>अहिले सम्म कुनै दर्ता भेटिएन!</b>',
        'wait_and_retry': 'कृपया दर्ता पछि २-३ मिनेट प्रतीक्षा गर्नुहोस् र फेरि जाँच गर्नुहोस् बटन क्लिक गर्नुहोस्।\nवा तत्काल प्रमाणीकरणको लागि आफ्नो Player ID म्यानुअल रूपमा प्रविष्ट गर्नुहोस्।',
        'registration_confirmed': '🎉 <b>दर्ता पुष्टि भयो!</b>',
        'deposit_received': '💰 <b>जम्मा प्राप्त भयो!</b>',
        'check_status': '🔄 स्थिति जाँच गर्नुहोस्'
    }
}

def get_message(lang, key):
    return MESSAGES.get(lang, MESSAGES['en']).get(key, '')

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def edit_message(chat_id, message_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error editing message: {e}")
        return None

def answer_callback(callback_id, text=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    payload = {'callback_query_id': callback_id}
    if text:
        payload['text'] = text
    
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error answering callback: {e}")

def get_user(user_id):
    return users_data.get(str(user_id), {
        'user_id': user_id,
        'language': 'en',
        'player_id': None,
        'predictions_used': 0,
        'total_deposit': 0,
        'registered': False
    })

def update_user(user_id, **kwargs):
    user_id = str(user_id)
    if user_id not in users_data:
        users_data[user_id] = {'user_id': user_id}
    
    for key, value in kwargs.items():
        users_data[user_id][key] = value

def check_user_registration_automatically(chat_id):
    """
    Automatically check if user is registered through our affiliate link
    without requiring player ID
    """
    try:
        user = get_user(chat_id)
        language = user.get('language', 'en')
        
        # Get user's last activity to find potential player ID
        user_events = [event for event in postback_events if event.get('user_id')]
        
        if not user_events:
            # No postbacks received yet
            keyboard = {
                'inline_keyboard': [
                    [{'text': get_message(language, 'register_now'), 'url': AFFILIATE_LINK}],
                    [{'text': get_message(language, 'check_again'), 'callback_data': 'auto_check_registration'}],
                    [{'text': get_message(language, 'manual_entry'), 'callback_data': 'manual_player_id'}]
                ]
            }
            send_message(chat_id, 
                f"{get_message(language, 'checking_status')}\n\n"
                f"{get_message(language, 'no_registration_found')}\n\n"
                f"{get_message(language, 'wait_and_retry')}",
                keyboard
            )
            return
        
        # Find latest registration event for this user (by various identifiers)
        latest_registration = None
        for event in user_events:
            if event.get('event_type') in ['registration', 'Registration', 'register']:
                latest_registration = event
                break
        
        if latest_registration:
            user_id = latest_registration.get('user_id')
            # Auto-update user with player ID
            update_user(chat_id, player_id=user_id, registered=True)
            
            # Check if user has deposited
            user_deposits = [e for e in user_events if e.get('user_id') == user_id and e.get('amount', 0) > 0]
            total_deposit = sum(deposit.get('amount', 0) for deposit in user_deposits)
            
            if total_deposit >= 5:
                # User has deposited enough
                keyboard = {
                    'inline_keyboard': [
                        [{'text': get_message(language, 'get_signal'), 'callback_data': 'get_signal'}]
                    ]
                }
                send_message(chat_id, 
                    f"🎉 <b>Automatic Verification Successful!</b>\n\n"
                    f"✅ <b>Player ID:</b> {user_id}\n"
                    f"💰 <b>Total Deposit:</b> ${total_deposit}\n\n"
                    f"{get_message(language, 'congratulations')}",
                    keyboard
                )
            else:
                # Registered but no deposit
                keyboard = {
                    'inline_keyboard': [
                        [{'text': '💰 Deposit', 'url': AFFILIATE_LINK}],
                        [{'text': get_message(language, 'check_deposit'), 'callback_data': 'auto_check_deposit'}]
                    ]
                }
                send_message(chat_id,
                    f"🎉 <b>Registration Verified Automatically!</b>\n\n"
                    f"✅ <b>Player ID:</b> {user_id}\n"
                    f"🔄 <b>Status:</b> Registered - Deposit Required\n\n"
                    f"{get_message(language, 'deposit_required')}",
                    keyboard
                )
        else:
            # No registration found
            keyboard = {
                'inline_keyboard': [
                    [{'text': get_message(language, 'register_now'), 'url': AFFILIATE_LINK}],
                    [{'text': get_message(language, 'check_again'), 'callback_data': 'auto_check_registration'}],
                    [{'text': get_message(language, 'manual_entry'), 'callback_data': 'manual_player_id'}]
                ]
            }
            send_message(chat_id, 
                f"🔍 <b>Automatic Check Complete</b>\n\n"
                f"{get_message(language, 'no_registration_found')}\n\n"
                f"Possible reasons:\n"
                f"• You didn't use our affiliate link\n"
                f"• Registration is still processing\n"
                f"• Used different browser/device\n\n"
                f"Try:\n"
                f"1. Wait 2-3 minutes and click 'Check Again'\n"
                f"2. Enter Player ID manually\n"
                f"3. Re-register using our link",
                keyboard
            )
            
    except Exception as e:
        print(f"Auto verification error: {e}")
        send_message(chat_id, f"❌ {get_message(language, 'auto_verify_failed')}")

def check_1win_user_status(player_id):
    """
    Check user status from 1Win postback system
    """
    try:
        # Check if we have stored postback events for this player
        user_events = [event for event in postback_events if str(event.get('user_id')) == str(player_id)]
        
        print(f"🔍 Checking user {player_id}, found {len(user_events)} events")
        
        if not user_events:
            return "not_registered"
        
        # Check for registration event
        has_registration = any(
            event.get('event_type') in ['registration', 'Registration', 'REGISTRATION', 'register', 'reg'] 
            for event in user_events
        )
        
        # Calculate total deposits
        total_deposit = sum(
            float(event.get('amount', 0)) 
            for event in user_events 
            if event.get('event_type') in ['first_deposit', 'deposit', 'recurring_deposit', 'Deposit', 'FIRST_DEPOSIT', 'first_deposit', 'recurring']
        )
        
        print(f"📊 User {player_id} - Registered: {has_registration}, Total Deposit: ${total_deposit}")
        
        if not has_registration:
            return "not_registered"
        elif total_deposit < 5:  # $5 minimum deposit
            return "registered_no_deposit"
        else:
            return "verified"
            
    except Exception as e:
        print(f"❌ Error checking 1Win user status: {e}")
        return "not_registered"

def show_language_selection(chat_id):
    keyboard = {
        'inline_keyboard': [
            [{'text': '🇺🇸 English', 'callback_data': 'lang_en'}],
            [{'text': '🇮🇳 हिंदी', 'callback_data': 'lang_hi'}],
            [{'text': '🇧🇩 বাংলা', 'callback_data': 'lang_bn'}],
            [{'text': '🇵🇰 اردو', 'callback_data': 'lang_ur'}],
            [{'text': '🇳🇵 नेपाली', 'callback_data': 'lang_ne'}]
        ]
    }
    
    send_message(chat_id, "<b>Select your preferred Language:</b>", keyboard)

def handle_language_selection(chat_id, message_id, language):
    user = get_user(chat_id)
    update_user(chat_id, language=language)
    
    # Show registration section
    keyboard = {
        'inline_keyboard': [
            [{'text': get_message(language, 'register_btn'), 'url': AFFILIATE_LINK}],
            [{'text': get_message(language, 'check_registration_btn'), 'callback_data': 'check_registration'}]
        ]
    }
    
    message_text = (
        f"{get_message(language, 'welcome')}\n\n"
        f"{get_message(language, 'step1')}\n\n"
        f"{get_message(language, 'account_must_be_new')}\n\n"
        f"{get_message(language, 'step1_instructions')}\n\n"
        f"{get_message(language, 'after_success')}"
    )
    
    edit_message(chat_id, message_id, message_text, keyboard)

def handle_check_registration(chat_id, message_id):
    user = get_user(chat_id)
    language = user.get('language', 'en')
    
    # Show options for verification
    keyboard = {
        'inline_keyboard': [
            [{'text': get_message(language, 'automatic_check'), 'callback_data': 'auto_check_registration'}],
            [{'text': get_message(language, 'manual_entry'), 'callback_data': 'manual_player_id'}],
            [{'text': get_message(language, 'register_btn'), 'url': AFFILIATE_LINK}]
        ]
    }
    
    message_text = (
        f"{get_message(language, 'verification_options')}\n\n"
        f"{get_message(language, 'choose_method')}\n\n"
        f"{get_message(language, 'auto_check_desc')}\n\n"
        f"{get_message(language, 'manual_entry_desc')}"
    )
    
    edit_message(chat_id, message_id, message_text, keyboard)

def handle_auto_check_registration(chat_id, message_id):
    """Handle automatic registration check"""
    check_user_registration_automatically(chat_id)

def handle_manual_player_id(chat_id, message_id):
    """Switch to manual player ID entry"""
    user = get_user(chat_id)
    language = user.get('language', 'en')
    
    message_text = (
        f"{get_message(language, 'enter_player_id')}\n\n"
        f"{get_message(language, 'how_to_find_id')}\n\n"
        f"{get_message(language, 'enter_id_now')}"
    )
    
    # Set user as waiting for player ID
    update_user(chat_id, waiting_for_player_id=True)
    
    edit_message(chat_id, message_id, message_text)

def handle_player_id(chat_id, player_id):
    user = get_user(chat_id)
    language = user.get('language', 'en')
    
    # Remove waiting flag
    update_user(chat_id, waiting_for_player_id=False)
    
    # Check user status from 1Win postback system
    user_status = check_1win_user_status(player_id)
    
    if user_status == "not_registered":
        keyboard = {
            'inline_keyboard': [
                [{'text': get_message(language, 'register_now'), 'url': AFFILIATE_LINK}]
            ]
        }
        send_message(chat_id, 
            f"{get_message(language, 'not_registered')}\n\n{get_message(language, 'not_registered_msg')}", 
            keyboard
        )
        
    elif user_status == "registered_no_deposit":
        keyboard = {
            'inline_keyboard': [
                [{'text': '💰 Deposit', 'url': AFFILIATE_LINK}],
                [{'text': get_message(language, 'check_deposit'), 'callback_data': 'check_deposit'}]
            ]
        }
        send_message(chat_id,
            f"{get_message(language, 'registered_no_deposit')}\n\n"
            f"{get_message(language, 'sync_success')}\n\n"
            f"{get_message(language, 'deposit_required')}\n\n"
            f"{get_message(language, 'after_deposit')}",
            keyboard
        )
        
    elif user_status == "verified":
        update_user(chat_id, player_id=player_id, registered=True)
        
        keyboard = {
            'inline_keyboard': [
                [{'text': get_message(language, 'get_signal'), 'callback_data': 'get_signal'}]
            ]
        }
        send_message(chat_id, get_message(language, 'congratulations'), keyboard)

def handle_get_signal(chat_id, message_id):
    user = get_user(chat_id)
    language = user.get('language', 'en')
    
    predictions_used = user.get('predictions_used', 0)
    
    if predictions_used >= 15:
        handle_limit_reached(chat_id, message_id, language)
        return
    
    signal = random.choice(MINES_SIGNALS)
    update_user(chat_id, predictions_used=predictions_used + 1)
    
    signal_text = (
        f"{get_message(language, 'signal_title')}\n"
        f"➖➖➖➖➖➖➖\n"
        f"{get_message(language, 'select_traps').format(signal['traps'])}\n"
        f"{get_message(language, 'accuracy').format(signal['accuracy'])}\n"
        f"➖➖➖➖➖➖➖\n"
        f"{get_message(language, 'open_cells')}\n\n"
    )
    
    for row in signal['grid']:
        signal_text += f"{row}\n"
    
    signal_text += f"\n➖➖➖➖➖➖➖\n"
    signal_text += f"{get_message(language, 'get_new_signal')}"
    
    keyboard = {
        'inline_keyboard': [
            [
                {'text': get_message(language, 'next_signal'), 'callback_data': 'next_signal'},
                {'text': get_message(language, 'back'), 'callback_data': 'back_to_start'}
            ]
        ]
    }
    
    edit_message(chat_id, message_id, signal_text, keyboard)

def handle_next_signal(chat_id, message_id):
    user = get_user(chat_id)
    language = user.get('language', 'en')
    
    predictions_used = user.get('predictions_used', 0)
    
    if predictions_used >= 15:
        handle_limit_reached(chat_id, message_id, language)
        return
    
    signal = random.choice(MINES_SIGNALS)
    update_user(chat_id, predictions_used=predictions_used + 1)
    
    signal_text = (
        f"{get_message(language, 'signal_title')}\n"
        f"➖➖➖➖➖➖➖\n"
        f"{get_message(language, 'select_traps').format(signal['traps'])}\n"
        f"{get_message(language, 'accuracy').format(signal['accuracy'])}\n"
        f"➖➖➖➖➖➖➖\n"
        f"{get_message(language, 'open_cells')}\n\n"
    )
    
    for row in signal['grid']:
        signal_text += f"{row}\n"
    
    signal_text += f"\n➖➖➖➖➖➖➖\n"
    signal_text += f"{get_message(language, 'get_new_signal')}"
    
    keyboard = {
        'inline_keyboard': [
            [
                {'text': get_message(language, 'next_signal'), 'callback_data': 'next_signal'},
                {'text': get_message(language, 'back'), 'callback_data': 'back_to_start'}
            ]
        ]
    }
    
    # Send new message instead of editing
    send_message(chat_id, signal_text, keyboard)

def handle_limit_reached(chat_id, message_id, language):
    keyboard = {
        'inline_keyboard': [
            [{'text': get_message(language, 'deposit_again_btn'), 'url': AFFILIATE_LINK}]
        ]
    }
    
    edit_message(chat_id, message_id, 
        f"{get_message(language, 'limit_reached')}\n\n{get_message(language, 'deposit_again')}", 
        keyboard
    )

def handle_back_to_start(chat_id, message_id):
    user = get_user(chat_id)
    language = user.get('language', 'en')
    
    keyboard = {
        'inline_keyboard': [
            [{'text': get_message(language, 'register_btn'), 'url': AFFILIATE_LINK}],
            [{'text': get_message(language, 'check_registration_btn'), 'callback_data': 'check_registration'}]
        ]
    }
    
    message_text = (
        f"{get_message(language, 'welcome')}\n\n"
        f"{get_message(language, 'step1')}\n\n"
        f"{get_message(language, 'account_must_be_new')}\n\n"
        f"{get_message(language, 'step1_instructions')}\n\n"
        f"{get_message(language, 'after_success')}"
    )
    
    edit_message(chat_id, message_id, message_text, keyboard)

# Flask Routes
@app.route('/')
def home():
    return "🤖 Mines Predictor Bot - All Features Working!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        if 'message' in data:
            message = data['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            if text == '/start':
                show_language_selection(chat_id)
            else:
                user = get_user(chat_id)
                if user.get('waiting_for_player_id'):
                    handle_player_id(chat_id, text)
        
        elif 'callback_query' in data:
            callback = data['callback_query']
            chat_id = callback['message']['chat']['id']
            message_id = callback['message']['message_id']
            callback_data = callback['data']
            callback_id = callback['id']
            
            answer_callback(callback_id)
            
            if callback_data.startswith('lang_'):
                language = callback_data.split('_')[1]
                handle_language_selection(chat_id, message_id, language)
            elif callback_data == 'check_registration':
                handle_check_registration(chat_id, message_id)
            elif callback_data == 'auto_check_registration':
                handle_auto_check_registration(chat_id, message_id)
            elif callback_data == 'manual_player_id':
                handle_manual_player_id(chat_id, message_id)
            elif callback_data == 'get_signal':
                handle_get_signal(chat_id, message_id)
            elif callback_data == 'next_signal':
                handle_next_signal(chat_id, message_id)
            elif callback_data == 'back_to_start':
                handle_back_to_start(chat_id, message_id)
            elif callback_data == 'check_deposit':
                handle_check_registration(chat_id, message_id)
            elif callback_data == 'auto_check_deposit':
                handle_auto_check_registration(chat_id, message_id)
        
        return 'OK'
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return 'OK'

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    if BOT_TOKEN:
        try:
            webhook_url = f"{VERCEL_URL}/webhook"
            response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}")
            return f"✅ Webhook set: {response.json()}"
        except Exception as e:
            return f"❌ Webhook error: {e}"
    return "❌ BOT_TOKEN not set"

# 1WIN POSTBACK ENDPOINT - With ALL Parameters
@app.route('/1win-postback', methods=['GET'])
def handle_1win_postback():
    """
    1Win Postback Endpoint with ALL parameters
    """
    try:
        # Get ALL parameters from 1Win
        event_id = request.args.get('event_id', '')
        date = request.args.get('date', '')
        hash_id = request.args.get('hash_id', '')
        hash_name = request.args.get('hash_name', '')
        source_id = request.args.get('source_id', '')
        source_name = request.args.get('source_name', '')
        amount = request.args.get('amount', 0, type=float)
        transaction_id = request.args.get('transaction_id', '')
        country = request.args.get('country', '')
        user_id = request.args.get('user_id', '')
        sub1 = request.args.get('sub1', '')
        
        # Determine event type based on parameters
        event_type = 'unknown'
        if amount > 0:
            if 'first' in hash_name.lower() or 'first' in source_name.lower():
                event_type = 'first_deposit'
            else:
                event_type = 'deposit'
        else:
            if 'register' in hash_name.lower() or 'registration' in source_name.lower():
                event_type = 'registration'
            elif 'recurring' in hash_name.lower():
                event_type = 'recurring_deposit'
        
        print(f"🎯 1Win Postback Received:")
        print(f"   Event Type: {event_type}")
        print(f"   User ID: {user_id}")
        print(f"   Amount: ${amount}")
        print(f"   Hash ID: {hash_id}")
        print(f"   Source: {source_name}")
        
        # Store the postback event
        postback_events.append({
            'event_type': event_type,
            'user_id': user_id,
            'amount': amount,
            'event_id': event_id,
            'date': date,
            'hash_id': hash_id,
            'hash_name': hash_name,
            'source_id': source_id,
            'source_name': source_name,
            'transaction_id': transaction_id,
            'country': country,
            'sub1': sub1,
            'timestamp': time.time()
        })
        
        # Admin notification
        if ADMIN_CHAT_ID:
            admin_message = (
                f"🔄 1Win Postback - {event_type.upper()}\n"
                f"User ID: {user_id}\n"
                f"Amount: ${amount}\n"
                f"Source: {source_name}\n"
                f"Time: {time.ctime()}"
            )
            send_message(ADMIN_CHAT_ID, admin_message)
        
        # Return success response to 1Win
        return jsonify({
            "status": "success",
            "message": "Postback received successfully",
            "event_type": event_type,
            "user_id": user_id,
            "amount": amount
        }), 200
        
    except Exception as e:
        print(f"❌ 1Win Postback error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/debug')
def debug():
    return jsonify({
        "users_count": len(users_data),
        "postbacks_count": len(postback_events),
        "webhook_url": f"{VERCEL_URL}/webhook",
        "postback_events": postback_events[-5:]  # Last 5 events
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
