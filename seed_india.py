import mysql.connector
import random
from db import get_db_connection

def seed_india_questions():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database.")
        return
    
    cursor = conn.cursor()
    all_q = []
    
    # -------------------------------
    # ✅ BASE QUESTIONS (Existing 100+)
    # -------------------------------
    base_questions = [
        {"en": "What is the national animal of India?", "hi": "भारत का राष्ट्रीय पशु क्या है?", "mr": "भारताचा राष्ट्रीय प्राणी कोणता आहे?", "options": [{"en": "Tiger", "hi": "बाघ", "mr": "वाघ"}, {"en": "Lion", "hi": "शेर", "mr": "सिंह"}, {"en": "Peacock", "hi": "मोर", "mr": "मोर"}, {"en": "Elephant", "hi": "हाथी", "mr": "हत्ती"}], "correct": "Tiger"},
        {"en": "Which river is known as the 'Ganga of the South'?", "hi": "किस नदी को 'दक्षिण की गंगा' कहा जाता है?", "mr": "कोणत्या नदीला 'दक्षिणेची गंगा' म्हणतात?", "options": [{"en": "Godavari", "hi": "गोदावरी", "mr": "गोदावरी"}, {"en": "Cauvery", "hi": "कावेरी", "mr": "कावेरी"}, {"en": "Krishna", "hi": "कृष्णा", "mr": "कृष्णा"}, {"en": "Narmada", "hi": "नर्मदा", "mr": "नर्मदा"}], "correct": "Godavari"},
        {"en": "Who is known as the 'Iron Man of India'?", "hi": "किसे 'भारत के लौह पुरुष' के रूप में जाना जाता है?", "mr": "कोणाला 'भारताचे लोहपुरुष' म्हणून ओळखले जाते?", "options": [{"en": "Sardar Vallabhbhai Patel", "hi": "सरदार वल्लभभाई पटेल", "mr": "सरदार वल्लभभाई पटेल"}, {"en": "Mahatma Gandhi", "hi": "महत्मा गांधी", "mr": "महात्मा गांधी"}, {"en": "Subhas Chandra Bose", "hi": "सुभाष चंद्र बोस", "mr": "सुभाषचंद्र बोस"}, {"en": "Bhagat Singh", "hi": "भगत सिंह", "mr": "भगतसिंग"}], "correct": "Sardar Vallabhbhai Patel"},
        {"en": "Which city is known as the 'Pink City' of India?", "hi": "भारत के 'गुलाबी शहर' के रूप में किस शहर को जाना जाता है?", "mr": "भारतातील 'गुलाबी शहर' म्हणून कोणते शहर ओळखले जाते?", "options": [{"en": "Jaipur", "hi": "जयपुर", "mr": "जयपूर"}, {"en": "Jodhpur", "hi": "जोधपुर", "mr": "जोधपूर"}, {"en": "Udaipur", "hi": "उदयपुर", "mr": "उदयपूर"}, {"en": "Bikaner", "hi": "बीकानेर", "mr": "बिकानेर"}], "correct": "Jaipur"},
        {"en": "What is the capital of India?", "hi": "भारत की राजधानी क्या है?", "mr": "भारताची राजधानी कोणती?", "options": [{"en": "New Delhi", "hi": "नई दिल्ली", "mr": "नवी दिल्ली"}, {"en": "Mumbai", "hi": "मुंबई", "mr": "मुंबई"}, {"en": "Kolkata", "hi": "कोलकाता", "mr": "कोलकाता"}, {"en": "Chennai", "hi": "चेन्नई", "mr": "चेन्नई"}], "correct": "New Delhi"},
        {"en": "Which is the national bird of India?", "hi": "भारत का राष्ट्रीय पक्षी क्या है?", "mr": "भारताचा राष्ट्रीय पक्षी कोणता?", "options": [{"en": "Peacock", "hi": "मोर", "mr": "मोर"}, {"en": "Parrot", "hi": "तोता", "mr": "पोपट"}, {"en": "Eagle", "hi": "चील", "mr": "गरुड"}, {"en": "Sparrow", "hi": "गौरैया", "mr": "चिमणी"}], "correct": "Peacock"},
        {"en": "Who wrote the National Anthem of India?", "hi": "भारतीय राष्ट्रगान किसने लिखा था?", "mr": "भारतीय राष्ट्रगीत कोणी लिहिले?", "options": [{"en": "Rabindranath Tagore", "hi": "रवींद्रनाथ टैगोर", "mr": "रवींद्रनाथ टागोर"}, {"en": "Bankim Chandra Chatterjee", "hi": "बंकिम चंद्र चटर्जी", "mr": "बंकिमचंद्र चॅटर्जी"}, {"en": "Sarojini Naidu", "hi": "सरोजिनी नायडू", "mr": "सरोजिनी नायडू"}, {"en": "Gulzar", "hi": "गुलज़ार", "mr": "गुलझार"}], "correct": "Rabindranath Tagore"},
        {"en": "In which year did India get independence?", "hi": "भारत को किस वर्ष स्वतंत्रता मिली?", "mr": "भारताला कोणत्या वर्षी स्वातंत्र्य मिळाले?", "options": [{"en": "1947", "hi": "1947", "mr": "1947"}, {"en": "1942", "hi": "1942", "mr": "1942"}, {"en": "1950", "hi": "1950", "mr": "1950"}, {"en": "1930", "hi": "1930", "mr": "1930"}], "correct": "1947"},
        {"en": "National fruit of India?", "hi": "भारत का राष्ट्रीय फल क्या है?", "mr": "भारताचे राष्ट्रीय फळ कोणते?", "options": [{"en": "Mango", "hi": "आम", "mr": "आंबा"}, {"en": "Apple", "hi": "सेब", "mr": "सफरचंद"}, {"en": "Banana", "hi": "केला", "mr": "केळे"}, {"en": "Orange", "hi": "संतरा", "mr": "संत्रा"}], "correct": "Mango"},
        {"en": "National flower of India?", "hi": "भारत का राष्ट्रीय फूल क्या है?", "mr": "भारताचे राष्ट्रीय फूल कोणते?", "options": [{"en": "Lotus", "hi": "कमल", "mr": "कमळ"}, {"en": "Rose", "hi": "गुलाब", "mr": "गुलाब"}, {"en": "Marigold", "hi": "गेंदा", "mr": "झेंडू"}, {"en": "Jasmine", "hi": "चमेली", "mr": "जाई"}], "correct": "Lotus"},
        {"en": "Who is known as the 'Father of the Nation' in India?", "hi": "भारत में 'राष्ट्रपिता' के रूप में किसे जाना जाता है?", "mr": "भारतात 'राष्ट्रपिता' म्हणून कोणाला ओळखले जाते?", "options": [{"en": "Mahatma Gandhi", "hi": "महात्मा गांधी", "mr": "महात्मा गांधी"}, {"en": "Nehru", "hi": "नेहरू", "mr": "नेहरूंनी"}, {"en": "Bose", "hi": "बोस", "mr": "बोस"}, {"en": "Patel", "hi": "पटेल", "mr": "पटेल"}], "correct": "Mahatma Gandhi"},
        {"en": "Which is the longest river in India?", "hi": "भारत की सबसे लंबी नदी कौन सी है?", "mr": "भारतातील सर्वात लांब नदी कोणती?", "options": [{"en": "Ganga", "hi": "गंगा", "mr": "गंगा"}, {"en": "Yamuna", "hi": "यमुना", "mr": "यमुना"}, {"en": "Brahmaputra", "hi": "ब्रह्मपुत्र", "mr": "ब्रह्मपुत्रा"}, {"en": "Godavari", "hi": "गोदावरी", "mr": "गोदावरी"}], "correct": "Ganga"},
        {"en": "Financial capital of India?", "hi": "भारत की वित्तीय राजधानी क्या है?", "mr": "भारताची आर्थिक राजधानी कोणती?", "options": [{"en": "Mumbai", "hi": "मुंबई", "mr": "मुंबई"}, {"en": "Delhi", "hi": "दिल्ली", "mr": "दिल्ली"}, {"en": "Bengaluru", "hi": "बेंगलुरु", "mr": "बेंगळुरू"}, {"en": "Kolkata", "hi": "कोलकाता", "mr": "कोलकाता"}], "correct": "Mumbai"},
        {"en": "Largest state of India by area?", "hi": "क्षेत्रफल के हिसाब से भारत का सबसे बड़ा राज्य कौन सा है?", "mr": "क्षेत्रफळाच्या दृष्टीने भारतातील सर्वात मोठे राज्य कोणते?", "options": [{"en": "Rajasthan", "hi": "राजस्थान", "mr": "राजस्थान"}, {"en": "MP", "hi": "मध्य प्रदेश", "mr": "मध्य प्रदेश"}, {"en": "Maharashtra", "hi": "महाराष्ट्र", "mr": "महाराष्ट्र"}, {"en": "UP", "hi": "उत्तर प्रदेश", "mr": "उत्तर प्रदेश"}], "correct": "Rajasthan"},
        {"en": "Smallest state of India?", "hi": "भारत का सबसे छोटा राज्य कौन सा है?", "mr": "भारतातील सर्वात लहान राज्य कोणते?", "options": [{"en": "Goa", "hi": "गोवा", "mr": "गोवा"}, {"en": "Sikkim", "hi": "सिक्किम", "mr": "सिक्कीम"}, {"en": "Tripura", "hi": "त्रिपुरा", "mr": "त्रिपुरा"}, {"en": "Mizoram", "hi": "मिजोरम", "mr": "मिझोरम"}], "correct": "Goa"},
        {"en": "Silicon Valley of India?", "hi": "भारत की सिलिकॉन वैली किसे कहते हैं?", "mr": "भारताची सिलिकॉन व्हॅली कोणाला म्हणतात?", "options": [{"en": "Bengaluru", "hi": "बेंगलुरु", "mr": "बेंगळुरू"}, {"en": "Hyderabad", "hi": "हैदराबाद", "mr": "हैदराबाद"}, {"en": "Pune", "hi": "पुणे", "mr": "पुणे"}, {"en": "Chennai", "hi": "चेन्नई", "mr": "चेन्नई"}], "correct": "Bengaluru"},
        {"en": "Who was the first woman PM of India?", "hi": "भारत की पहली महिला प्रधानमंत्री कौन थीं?", "mr": "भारताच्या पहिल्या महिला पंतप्रधान कोण होत्या?", "options": [{"en": "Indira Gandhi", "hi": "इन्दिरा गाँधी", "mr": "इंदिरा गांधी"}, {"en": "Pratibha Patil", "hi": "प्रतिभा पाटिल", "mr": "प्रतिभा पाटील"}, {"en": "Sarojini Naidu", "hi": "सरोजिनी नायडू", "mr": "सरोजिनी नायडू"}, {"en": "Sushma Swaraj", "hi": "सुषमा स्वराज", "mr": "सुषमा स्वराज"}], "correct": "Indira Gandhi"},
        {"en": "National song of India?", "hi": "भारत का राष्ट्रीय गीत क्या है?", "mr": "भारताचे राष्ट्रीय गीत कोणते आहे?", "options": [{"en": "Vande Mataram", "hi": "वन्दे मातरम्", "mr": "व वंदे मातरम"}, {"en": "Jana Gana Mana", "hi": "जन गण मन", "mr": "जन गण मन"}, {"en": "Saare Jahan Se Achha", "hi": "सारे जहाँ से अच्छा", "mr": "सारे जहाँ से अच्छा"}, {"en": "Ae Mere Watan Ke Logo", "hi": "ऐ मेरे वतन के लोगों", "mr": "ऐ मेरे वतन के लोगों"}], "correct": "Vande Mataram"},
        {"en": "Hawa Mahal is in which city?", "hi": "हवा महल किस शहर में है?", "mr": "हवा महल कोणत्या शहरात आहे?", "options": [{"en": "Jaipur", "hi": "जयपुर", "mr": "जयपूर"}, {"en": "Jodhpur", "hi": "जोधपुर", "mr": "जोधपूर"}, {"en": "Udaipur", "hi": "उदयपुर", "mr": "उदयपूर"}, {"en": "Bikaner", "hi": "बीकानेर", "mr": "बिकानेर"}], "correct": "Jaipur"},
        {"en": "Who built the Taj Mahal?", "hi": "ताजमहल किसने बनवाया था?", "mr": "ताजमहल कोणी बांधला?", "options": [{"en": "Shah Jahan", "hi": "शाहजहाँ", "mr": "शहाजहान"}, {"en": "Akbar", "hi": "अकबर", "mr": "अकबर"}, {"en": "Humayun", "hi": "हुमायूँ", "mr": "हुमायून"}, {"en": "Aurangzeb", "hi": "औरंगजेब", "mr": "औरंगजेब"}], "correct": "Shah Jahan"},
        {"en": "India's first satellite name?", "hi": "भारत के पहले उपग्रह का नाम क्या है?", "mr": "भारताच्या पहिल्या उपग्रहाचे नाव काय?", "options": [{"en": "Aryabhata", "hi": "आर्यभट्ट", "mr": "आर्यभट्ट"}, {"en": "Rohini", "hi": "रोहिणी", "mr": "रोहिणी"}, {"en": "Bhaskara", "hi": "भास्कर", "mr": "भास्कर"}, {"en": "Apple", "hi": "एप्पल", "mr": "ऍपल"}], "correct": "Aryabhata"},
        {"en": "National tree of India?", "hi": "भारत का राष्ट्रीय वृक्ष क्या है?", "mr": "भारताचा राष्ट्रीय वृक्ष कोणता?", "options": [{"en": "Banyan", "hi": "बरगद", "mr": "वड"}, {"en": "Peepal", "hi": "पीपल", "mr": "पिंपळ"}, {"en": "Neem", "hi": "नीम", "mr": "कडुलिंब"}, {"en": "Mango", "hi": "आम", "mr": "आंबा"}], "correct": "Banyan"},
        {"en": "Capital of Telangana?", "hi": "तेलंगाना की राजधानी क्या है?", "mr": "तेलंगणाची राजधानी कोणती?", "options": [{"en": "Hyderabad", "hi": "हैदराबाद", "mr": "हैदराबाद"}, {"en": "Warangal", "hi": "वारंगल", "mr": "वरंगल"}, {"en": "Nizamabad", "hi": "निज़ामाबाद", "mr": "निझामाबाद"}, {"en": "Karimnagar", "hi": "करीमनगर", "mr": "करीमनगर"}], "correct": "Hyderabad"},
        {"en": "Golden Temple location?", "hi": "स्वर्ण मंदिर कहाँ है?", "mr": "सुवर्ण मंदिर कोठे आहे?", "options": [{"en": "Amritsar", "hi": "अमृतसर", "mr": "अमृतसर"}, {"en": "Ludhiana", "hi": "लुधियाना", "mr": "लुधियाना"}, {"en": "Jalandhar", "hi": "जालंधर", "mr": "जालंधर"}, {"en": "Patiala", "hi": "पतियाळा", "mr": "पतियाळा"}], "correct": "Amritsar"},
        {"en": "Zero was invented by?", "hi": "शून्य का आविष्कार किसने किया?", "mr": "शून्याचा शोध कोणी लावला?", "options": [{"en": "Aryabhata", "hi": "आर्यभट्ट", "mr": "आर्यभट्ट"}, {"en": "Brahmagupta", "hi": "ब्रह्मगुप्त", "mr": "ब्रह्मगुप्त"}, {"en": "Varahamihira", "hi": "वराहमिहिर", "mr": "वराहमिहिर"}, {"en": "Sushruta", "hi": "सुश्रुत", "mr": "सुश्रुत"}], "correct": "Aryabhata"},
        {"en": "Largest democracy in the world?", "hi": "दुनिया का सबसे बड़ा लोकतंत्र कौन सा है?", "mr": "जगातील सर्वात मोठी लोकशाही कोणती?", "options": [{"en": "India", "hi": "भारत", "mr": "भारत"}, {"en": "USA", "hi": "यूएसए", "mr": "यूएसए"}, {"en": "UK", "hi": "यूके", "mr": "यूके"}, {"en": "France", "hi": "फ्रांस", "mr": "फ्रान्स"}], "correct": "India"},
        {"en": "White Revolution is for?", "hi": "श्वेत क्रांति किसके लिए है?", "mr": "धवल क्रांती कशासाठी आहे?", "options": [{"en": "Milk", "hi": "दूध", "mr": "दूध"}, {"en": "Fish", "hi": "मछली", "mr": "मासे"}, {"en": "Eggs", "hi": "अंडे", "mr": "अंडी"}, {"en": "Wheat", "hi": "गेहूँ", "mr": "गहू"}], "correct": "Milk"},
        {"en": "Green Revolution is for?", "hi": "हरित क्रांति किसके लिए है?", "mr": "हरित क्रांती कशासाठी आहे?", "options": [{"en": "Agriculture", "hi": "कृषि", "mr": "शेती"}, {"en": "Milk", "hi": "दूध", "mr": "दूध"}, {"en": "Oilseeds", "hi": "तिलहन", "mr": "तेलबिया"}, {"en": "Water", "hi": "पानी", "mr": "पाणी"}], "correct": "Agriculture"},
        {"en": "Blue Revolution is related to?", "hi": "नीली क्रांति किससे संबंधित है?", "mr": "नील क्रांती कशाशी संबंधित आहे?", "options": [{"en": "Fish", "hi": "मछली", "mr": "मासे"}, {"en": "Sky", "hi": "आकाश", "mr": "आकाश"}, {"en": "Indigo", "hi": "नील", "mr": "नीळ"}, {"en": "Milk", "hi": "दूध", "mr": "दूध"}], "correct": "Fish"},
        {"en": "Diamond City of India?", "hi": "भारत का 'हीरों का शहर' कौन सा है?", "mr": "भारताची 'हिऱ्यांची नगरी' कोणती?", "options": [{"en": "Surat", "hi": "सूरत", "mr": "सुरत"}, {"en": "Panna", "hi": "पन्ना", "mr": "पन्ना"}, {"en": "Mumbai", "hi": "मुंबई", "mr": "मुंबई"}, {"en": "Jaipur", "hi": "जयपुर", "mr": "जयपूर"}], "correct": "Surat"},
        {"en": "Leather City of the World?", "hi": "दुनिया का 'चमड़ा शहर' किसे कहते हैं?", "mr": "जगातील 'कातडयाचे शहर' कोणाला म्हणतात?", "options": [{"en": "Kanpur", "hi": "कानपुर", "mr": "कानपूर"}, {"en": "Agra", "hi": "आगरा", "mr": "आग्रा"}, {"en": "Lucknow", "hi": "लखनऊ", "mr": "लखनऊ"}, {"en": "Meerut", "hi": "मेरठ", "mr": "मेरठ"}], "correct": "Kanpur"},
        {"en": "Manchester of India?", "hi": "भारत का मैनचेस्टर किसे कहते हैं?", "mr": "भारताचे मँचेस्टर कोणाला म्हणतात?", "options": [{"en": "Ahmedabad", "hi": "अहमदाबाद", "mr": "अहमदाबाद"}, {"en": "Kanpur", "hi": "कानपुर", "mr": "कानपूर"}, {"en": "Mumbai", "hi": "मुंबई", "mr": "मुंबई"}, {"en": "Coimbatore", "hi": "कोयंबटूर", "mr": "कोइंबतूर"}], "correct": "Ahmedabad"},
        {"en": "Abode of Clouds?", "hi": "'बादलों का निवास' किसे कहते हैं?", "mr": "'ढगांचे निवासस्थान' कोणाला म्हणतात?", "options": [{"en": "Meghalaya", "hi": "मेघालय", "mr": "मेघालय"}, {"en": "Mizoram", "hi": "मिजोरम", "mr": "मिझोरम"}, {"en": "Sikkim", "hi": "सिक्किम", "mr": "सिक्कीम"}, {"en": "Kerala", "hi": "केरल", "mr": "केरळ"}], "correct": "Meghalaya"},
        {"en": "Rice Bowl of India?", "hi": "भारत का 'चावल का कटोरा' कौन सा है?", "mr": "भारतातील 'भाताचे कोठार' कोणते?", "options": [{"en": "Andhra Pradesh", "hi": "आंध्र प्रदेश", "mr": "आंध्र प्रदेश"}, {"en": "Punjab", "hi": "पंजाब", "mr": "पंजाब"}, {"en": "Chhattisgarh", "hi": "छत्तीसगढ़", "mr": "छत्तीसगड"}, {"en": "UP", "hi": "यूपी", "mr": "यूपी"}], "correct": "Andhra Pradesh"},
        {"en": "Saffron State of India?", "hi": "भारत का 'केसर राज्य' कौन सा है?", "mr": "भारतातील 'केशर राज्य' कोणते?", "options": [{"en": "J&K", "hi": "जम्मू और कश्मीर", "mr": "जम्मू आणि काश्मीर"}, {"en": "Himachal", "hi": "हिमाचल", "mr": "हिमाचल"}, {"en": "Uttarakhand", "hi": "उत्तराखंड", "mr": "उत्तराखंड"}, {"en": "Sikkim", "hi": "सिक्किम", "mr": "सिक्कीम"}], "correct": "J&K"},
        {"en": "National Heritage Animal?", "hi": "भारत का राष्ट्रीय विरासत पशु कौन सा है?", "mr": "भारताचा राष्ट्रीय वारसा प्राणी कोणता?", "options": [{"en": "Elephant", "hi": "हाथी", "mr": "हत्ती"}, {"en": "Tiger", "hi": "बाघ", "mr": "वाघ"}, {"en": "Lion", "hi": "शेर", "mr": "सिंह"}, {"en": "Rhino", "hi": "गैंडा", "mr": "गेंडा"}], "correct": "Elephant"},
        {"en": "Which state has the best literacy rate?", "hi": "किस राज्य में साक्षरता दर सबसे अधिक है?", "mr": "कोणत्या राज्यात साक्षरतेचे प्रमाण सर्वाधिक आहे?", "options": [{"en": "Kerala", "hi": "केरल", "mr": "केरळ"}, {"en": "Mizoram", "hi": "मिजोरम", "mr": "मिझोरम"}, {"en": "Goa", "hi": "गोवा", "mr": "गोवा"}, {"en": "Maharastra", "hi": "महाराष्ट्र", "mr": "महाराष्ट्र"}], "correct": "Kerala"},
        {"en": "Victoria Memorial is in?", "hi": "विक्टोरिया मेमोरियल कहाँ है?", "mr": "व्हिक्टोरिया मेमोरियल कोठे आहे?", "options": [{"en": "Kolkata", "hi": "कोलकाता", "mr": "कोलकाता"}, {"en": "Chennai", "hi": "चेन्नई", "mr": "चेन्नई"}, {"en": "Mumbai", "hi": "मुंबई", "mr": "मुंबई"}, {"en": "Delhi", "hi": "दिल्ली", "mr": "दिल्ली"}], "correct": "Kolkata"},
        {"en": "Gateway of India is in?", "hi": "गेटवे ऑफ इंडिया कहाँ है?", "mr": "गेटवे ऑफ इंडिया कोठे आहे?", "options": [{"en": "Mumbai", "hi": "मुंबई", "mr": "मुंबई"}, {"en": "Delhi", "hi": "दिल्ली", "mr": "दिल्ली"}, {"en": "Kolkata", "hi": "कोलकाता", "mr": "कोलकाता"}, {"en": "Chennai", "hi": "चेन्नई", "mr": "चेन्नई"}], "correct": "Mumbai"},
        {"en": "Who is the 'Flying Sikh'?", "hi": "'फ्लाइंग सिख' किसे कहा जाता है?", "mr": "'फ्लाइंग सिख' कोणाला म्हणतात?", "options": [{"en": "Milkha Singh", "hi": "मिलखा सिंह", "mr": "मिलखा सिंग"}, {"en": "Harbhajan", "hi": "हरभजन", "mr": "हरभजन"}, {"en": "Yuvi", "hi": "युवी", "mr": "युवी"}, {"en": "Dhoni", "hi": "धोनी", "mr": "धोनी"}], "correct": "Milkha Singh"},
        {"en": "Bhangra is dance of?", "hi": "भांगड़ा कहाँ का नृत्य है?", "mr": "भांगडा कोठला नृत्य प्रकार आहे?", "options": [{"en": "Punjab", "hi": "पंजाब", "mr": "पंजाब"}, {"en": "Haryana", "hi": "हरियाणा", "mr": "हरियाणा"}, {"en": "Rajasthan", "hi": "राजस्थान", "mr": "राजस्थान"}, {"en": "UP", "hi": "यूपी", "mr": "यूपी"}], "correct": "Punjab"},
        {"en": "Garba is dance of?", "hi": "गरबा कहाँ का नृत्य है?", "mr": "गरबा कोठला नृत्य प्रकार आहे?", "options": [{"en": "Gujarat", "hi": "गुजरात", "mr": "गुजरात"}, {"en": "Rajasthan", "hi": "राजस्थान", "mr": "राजस्थान"}, {"en": "Maharashtra", "hi": "महाराष्ट्र", "mr": "महाराष्ट्र"}, {"en": "Punjab", "hi": "पंजाब", "mr": "पंजाब"}], "correct": "Gujarat"},
        {"en": "Bihu is festival of?", "hi": "बिहू कहाँ का त्यौहार है?", "mr": "बिहू कोठला सण आहे?", "options": [{"en": "Assam", "hi": "असम", "mr": "आसाम"}, {"en": "Sikkim", "hi": "सिक्किम", "mr": "सिक्कीम"}, {"en": "Manipur", "hi": "मणिपुर", "mr": "मणिपूर"}, {"en": "Meghalaya", "hi": "मेघालय", "mr": "मेघालय"}], "correct": "Assam"},
        {"en": "Cricket originated in?", "hi": "क्रिकेट की शुरुआत कहाँ से हुई?", "mr": "क्रिकेटची सुरुवात कोठून झाली?", "options": [{"en": "England", "hi": "इंग्लैंड", "mr": "इंग्लंड"}, {"en": "India", "hi": "भारत", "mr": "भारत"}, {"en": "Australia", "hi": "ऑस्ट्रेलिया", "mr": "ऑस्ट्रेलिया"}, {"en": "West Indies", "hi": "वेस्टइंडीज", "mr": "वेस्ट इंडीज"}], "correct": "England"},
        {"en": "Sun Temple is in?", "hi": "सूर्य मंदिर कहाँ है?", "mr": "सूर्य मंदिर कोठे आहे?", "options": [{"en": "Konark", "hi": "कोणारक", "mr": "कोणार्क"}, {"en": "Madurai", "hi": "मदुरै", "mr": "मदुराई"}, {"en": "Tanjore", "hi": "तंजौर", "mr": "तंजावर"}, {"en": "Khajuraho", "hi": "खजुराहो", "mr": "खजुराहो"}], "correct": "Konark"},
        {"en": "Chess originated in?", "hi": "शतरंज (Chess) की शुरुआत कहाँ से हुई?", "mr": "बुद्धिबळाची (Chess) सुरुवात कोठून झाली?", "options": [{"en": "India", "hi": "भारत", "mr": "भारत"}, {"en": "Persia", "hi": "फारस", "mr": "पर्शिया"}, {"en": "China", "hi": "चीन", "mr": "चीन"}, {"en": "Europe", "hi": "यूरोप", "mr": "युरोप"}], "correct": "India"},
        {"en": "Largest salt water lake in India?", "hi": "भारत की सबसे बड़ी खारे पानी की झील?", "mr": "भारतातील सर्वात मोठे खाऱ्या पाण्याचे सरोवर कोणते?", "options": [{"en": "Chilika", "hi": "चिलिका", "mr": "चिलिका"}, {"en": "Wular", "hi": "वुलर", "mr": "वुलर"}, {"en": "Dal", "hi": "डल", "mr": "डल"}, {"en": "Pulicat", "hi": "पुलिकट", "mr": "पुलिकट"}], "correct": "Chilika"},
        {"en": "Zero inventor?", "hi": "शून्य का आविष्कार किसने किया?", "mr": "शून्याचा शोध कोणी लावला?", "options": [{"en": "Aryabhata", "hi": "आर्यभट्ट", "mr": "आर्यभट्ट"}, {"en": "Chanakya", "hi": "चाणक्य", "mr": "चाणक्य"}, {"en": "Varahamihira", "hi": "वराहमिहिर", "mr": "वराहमिहिर"}, {"en": "Newton", "hi": "न्यूटन", "mr": "न्यूटन"}], "correct": "Aryabhata"},
        {"en": "National Anthem writer?", "hi": "राष्ट्रगान किसने लिखा?", "mr": "राष्ट्रगीत कोणी लिहिले?", "options": [{"en": "Rabindranath Tagore", "hi": "रवींद्रनाथ टैगोर", "mr": "रवींद्रनाथ टागोर"}, {"en": "Bankim Chandra", "hi": "बंकिम चंद्र", "mr": "बंकिमचंद्र"}, {"en": "Sarojini Naidu", "hi": "सरोजिनी नायडू", "mr": "सरोजिनी नायडू"}, {"en": "Premchand", "hi": "प्रेमचंद", "mr": "प्रेमचंद"}], "correct": "Rabindranath Tagore"},
        {"en": "National Song writer?", "hi": "राष्ट्रीय गीत किसने लिखा?", "mr": "राष्ट्रीय गीत कोणी लिहिले?", "options": [{"en": "Bankim Chandra Chatterjee", "hi": "बंकिम चंद्र चटर्जी", "mr": "बंकिमचंद्र चॅटर्जी"}, {"en": "Tagore", "hi": "टैगोर", "mr": "टागोर"}, {"en": "Gulzar", "hi": "गुलज़ार", "mr": "गुलझार"}, {"en": "Prasoon Joshi", "hi": "प्रसून जोशी", "mr": "प्रसून जोशी"}], "correct": "Bankim Chandra Chatterjee"},
    ]
    all_q.extend(base_questions)
    
    # -------------------------------
    # ✅ GK QUESTIONS (Programmatic)
    # -------------------------------
    capitals = [
        ("Maharashtra", "Mumbai", "मुंबई", "मुंबई"), ("Gujarat", "Gandhinagar", "गांधीनगर", "गांधीनगर"),
        ("Karnataka", "Bengaluru", "बेंगलुरु", "बेंगळुरू"), ("Tamil Nadu", "Chennai", "चेन्नई", "चेन्नई"),
        ("Goa", "Panaji", "पणजी", "पणजी"), ("Punjab", "Chandigarh", "चंडीगढ़", "चंदीगड"),
        ("West Bengal", "Kolkata", "कोलकाता", "कोलकाता"), ("Rajasthan", "Jaipur", "जयपुर", "जयपूर"),
        ("Assam", "Dispur", "दिसपुर", "दिसपूर"), ("Bihar", "Patna", "पटना", "पाटणा"),
        ("Haryana", "Chandigarh", "चंडीगढ़", "चंदीगड"), ("Kerala", "Thiruvananthapuram", "तिरुवनंतपुरम", "तिरुवनंतपुरम"),
        ("Odisha", "Bhubaneswar", "भुवनेश्वर", "भुवनेश्वर"), ("UP", "Lucknow", "लखनऊ", "लखनऊ"),
        ("MP", "Bhopal", "भोपाल", "भोपाळ"), ("Telangana", "Hyderabad", "हैदराबाद", "हैदराबाद"),
        ("Andhra Pradesh", "Amaravati", "अमरावती", "अमरावती"), ("Sikkim", "Gangtok", "गंगटोक", "गंगटोक"),
        ("Manipur", "Imphal", "इम्फाल", "इम्फाळ"), ("Tripura", "Agartala", "अगरतला", "आगरतळा")
    ]
    
    for state, cap, cap_hi, cap_mr in capitals:
        # Pick 3 wrong capitals from other states
        wrong_caps = random.sample([c for c in capitals if c[1] != cap], 3)
        
        options = [{"en": cap, "hi": cap_hi, "mr": cap_mr}]
        for w in wrong_caps:
            options.append({"en": w[1], "hi": w[2], "mr": w[3]})
            
        random.shuffle(options)
        
        all_q.append({
            "en": f"What is the capital of {state}?",
            "hi": f"{state} की राजधानी क्या है?",
            "mr": f"{state} ची राजधानी कोणती?",
            "options": options,
            "correct": cap
        })

    general_knowledge = [
        # (q_en, q_hi, q_mr, ans_en, ans_hi, ans_mr, [distractor1_en_hi_mr...])
        ("How many colors in Indian Flag?", "भारतीय ध्वज में कितने रंग हैं?", "भारतीय ध्वजात किती रंग आहेत?", "3", "3", "३", [("4", "4", "४"), ("2", "2", "२"), ("5", "5", "५")]),
        ("First Man on Moon?", "चाँद पर पहला आदमी कौन था?", "चंद्रावर जाणारा पहिला माणूस कोण?", "Neil Armstrong", "नील आर्मस्ट्रांग", "नील आर्मस्ट्राँग", [("Buzz Aldrin", "बज़ एल्ड्रिन", "बझ एल्ड्रिन"), ("Yuri Gagarin", "यूरी गागरिन", "युरी गागरिन"), ("Rakesh Sharma", "राकेश शर्मा", "राकेश शर्मा")]),
        ("Which planet is Red?", "कौन सा ग्रह लाल है?", "कोणता ग्रह लाल आहे?", "Mars", "मंगल", "मंगळ", [("Venus", "शुक्र", "शुक्र"), ("Saturn", "शनि", "शनि"), ("Jupiter", "बृहस्पति", "गुरु")]),
        ("Who is Prime Minister of India?", "भारत के प्रधानमंत्री कौन हैं?", "भारताचे पंतप्रधान कोण आहेत?", "Narendra Modi", "नरेन्द्र मोदी", "नरेन्द्र मोदी", [("Rahul Gandhi", "राहुल गांधी", "राहुल गांधी"), ("Amit Shah", "अमित शाह", "अमित शाह"), ("Manmohan Singh", "मनमोहन सिंह", "मनमोहन सिंग")]),
        ("National Sport (de-facto)?", "राष्ट्रीय खेल कौन सा है?", "राष्ट्रीय खेळ कोणता?", "Hockey", "हॉकी", "हॉकी", [("Cricket", "क्रिकेट", "क्रिकेट"), ("Football", "फुटबॉल", "फुटबॉल"), ("Kabaddi", "कबड्डी", "कबड्डी")]),
        ("How many legs does a spider have?", "मकड़ी की कितनी टांगें होती हैं?", "कोळयाला किती पाय असतात?", "8", "8", "८", [("6", "6", "६"), ("4", "4", "४"), ("10", "10", "१०")]),
        ("Sun rises in the?", "सूरज कहाँ से निकलता है?", "सूर्य कोठून उगवतो?", "East", "पूर्व", "पूर्व", [("West", "पश्चिम", "पश्चिम"), ("North", "उत्तर", "उत्तर"), ("South", "दक्षिण", "दक्षिण")]),
        ("Water boils at (Celsius)?", "पानी कितने डिग्री पर उबलता है?", "पाणी किती अंशावर उकळते?", "100", "100", "१००", [("0", "0", "०"), ("50", "50", "५०"), ("200", "200", "२००")]),
        ("Largest animal on Earth?", "पृथ्वी पर सबसे बड़ा जानवर?", "पृथ्वीवरील सर्वात मोठा प्राणी?", "Blue Whale", "ब्लू व्हेल", "ब्लू व्हेल", [("Elephant", "हाथी", "हत्ती"), ("Giraffe", "जिराफ", "जिराफ"), ("Shark", "शार्क", "शार्क")]),
        ("Tallest animal?", "सबसे ऊँचा जानवर?", "सर्वात उंच प्राणी?", "Giraffe", "जिराफ", "जिराफ", [("Elephant", "हाथी", "हत्ती"), ("Ostrich", "शुतुरमुर्ग", "शहामृग"), ("Camel", "ऊंट", "उंट")]),
        ("Capital of USA?", "USA की राजधानी?", "USA ची राजधानी?", "Washington D.C.", "वाशिंगटन डी.सी.", "वॉशिंग्टन डी.सी.", [("New York", "न्यूयॉर्क", "न्यूयॉर्क"), ("Chicago", "शिकागो", "शिकागो"), ("Los Angeles", "लॉस एंजिल्स", "लॉस एंजेलिस")]),
        ("How many continents?", "कितने महाद्वीप हैं?", "किती खंड आहेत?", "7", "7", "७", [("5", "5", "५"), ("6", "6", "६"), ("8", "8", "८")]),
        ("Largest Ocean?", "सबसे बड़ा महासागर?", "सर्वात मोठा महासागर?", "Pacific", "प्रशांत", "पॅसिफिक", [("Atlantic", "अटलांटिक", "अटलांटिक"), ("Indian", "हिंद", "हिंदी"), ("Arctic", "आर्कटिक", "आर्कटिक")]),
        ("Mount Everest is in?", "माउंट एवरेस्ट कहाँ है?", "माउंट एवरेस्ट कोठे आहे?", "Nepal", "नेपाल", "नेपाळ", [("India", "भारत", "भारत"), ("China", "चीन", "चीन"), ("Bhutan", "भूटान", "भूतान")]),
        ("Which gas we breathe in?", "हम कौन सी गैस लेते हैं?", "आपण कोणता वायू घेतो?", "Oxygen", "ऑक्सीजन", "ऑक्सिजन", [("Nitrogen", "नाइट्रोजन", "नायट्रोजन"), ("CO2", "सीओ2", "कर्बवायू"), ("Hydrogen", "हाइड्रोजन", "हायड्रोजन")]),
        ("Largest planet?", "सबसे बड़ा ग्रह?", "सर्वात मोठा ग्रह?", "Jupiter", "बृहस्पति", "गुरु", [("Saturn", "शनि", "शनि"), ("Mars", "मंगल", "मंगळ"), ("Earth", "पृथ्वी", "पृथ्वी")]),
        ("Moon is a?", "चंद्रमा क्या है?", "चंद्र काय आहे?", "Satellite", "उपग्रह", "उपग्रह", [("Planet", "ग्रह", "ग्रह"), ("Star", "तारा", "तारा"), ("Comet", "धूमकेतु", "धूमकेतू")]),
        ("Sun is a?", "सूरज क्या है?", "सूर्य काय आहे?", "Star", "तारा", "तारा", [("Planet", "ग्रह", "ग्रह"), ("Moon", "चंद्रमा", "चंद्र"), ("Galaxy", "आकाशगंगा", "आकाशगंगा")]),
        ("Heart is on which side?", "दिल किस तरफ होता है?", "हृदय कोणत्या बाजूला असते?", "Left", "बाएं", "डाव्या", [("Right", "दाएं", "उजव्या"), ("Center", "बीच में", "मध्यभागी"), ("Bottom", "नीचे", "खाली")])
    ]
    
    for en_q, hi_q, mr_q, cor, cor_hi, cor_mr, distractors in general_knowledge:
        options = [{"en": cor, "hi": cor_hi, "mr": cor_mr}]
        for d_en, d_hi, d_mr in distractors:
            options.append({"en": d_en, "hi": d_hi, "mr": d_mr})
        random.shuffle(options)
        
        all_q.append({
            "en": en_q, "hi": hi_q, "mr": mr_q,
            "options": options,
            "correct": cor
        })
        
    # -------------------------------
    # ✅ RANDOM GK (300+)
    # -------------------------------
    countries = [
        ("India", "भारत", "भारत"), ("USA", "अमेरिका", "अमेरिका"), ("China", "चीन", "चीन"),
        ("Japan", "जापान", "जपान"), ("Germany", "जर्मनी", "जर्मनी"), ("France", "फ्रांस", "फ्रान्स"),
        ("Russia", "रूस", "रशिया"), ("UK", "यूके", "यूके"), ("Australia", "ऑस्ट्रेलिया", "ऑस्ट्रेलिया"),
        ("Canada", "कनाडा", "कॅनडा"), ("Brazil", "ब्राजील", "ब्राझील"), ("Italy", "इटली", "इटली"),
        ("Spain", "स्पेन", "स्पेन"), ("Mexico", "मेक्सिको", "मेक्सिको"), ("Egypt", "मिस्र", "इजिप्त"),
        ("South Africa", "दक्षिण अफ्रीका", "दक्षिण आफ्रिका"), ("Argentina", "अर्जेंटीना", "अर्जेंटिना"),
        ("Turkey", "तुर्की", "तुर्की"), ("South Korea", "दक्षिण कोरिया", "दक्षिण कोरिया"),
        ("Thailand", "थाईलैंड", "थायलंड"), ("Vietnam", "वियतनाम", "व्हिएतनाम"),
        ("Indonesia", "इंडोनेशिया", "इंडोनेशिया"), ("Singapore", "सिंगापुर", "सिंगापूर"),
        ("United Arab Emirates", "संयुक्त अरब अमीरात", "संयुक्त अरब अमिराती"),
        ("Saudi Arabia", "सऊदी अरब", "सौदी अरेबिया"), ("Israel", "इज़राइल", "इस्रायल"),
        ("Switzerland", "स्विट्जरलैंड", "स्वित्झर्लंड"), ("Netherlands", "नीदरलैंड", "नेदरलँड"),
        ("Sweden", "स्वीडन", "स्वीडन"), ("Norway", "नार्वे", "नॉर्वे"),
        ("New Zealand", "न्यूजीलैंड", "न्यूझीलंड"), ("Greece", "ग्रीस", "ग्रीस"),
        ("Portugal", "पुर्तगाल", "पोर्तुगाल"), ("Belgium", "बेल्जियम", "बेल्जियम"),
        ("Austria", "ऑस्ट्रिया", "ऑस्ट्रिया"), ("Denmark", "डेनमार्क", "डेन्मार्क"),
        ("Finland", "फिनलैंड", "फिनलँड"), ("Poland", "पोलैंड", "पोलंड"),
        ("Ireland", "आयरलैंड", "आयर्लंड"), ("New Zealand", "न्यूजीलैंड", "न्यूझीलंड")
    ]
    
    country_capitals = [
        ("New Delhi", "नई दिल्ली", "नवी दिल्ली"), ("Washington", "वाशिंगटन", "वॉशिंग्टन"),
        ("Beijing", "बीजिंग", "बीजिंग"), ("Tokyo", "टोक्यो", "टोकियो"), ("Berlin", "बर्लिन", "बर्लिन"),
        ("Paris", "पेरिस", "पॅरिस"), ("Moscow", "मास्को", "मॉस्को"), ("London", "लंदन", "लंडन"),
        ("Canberra", "कैनबरा", "कॅनबेरा"), ("Ottawa", "ओटावा", "ओटावा"), ("Brasilia", "ब्रासीलिया", "ब्राझीलिया"),
        ("Rome", "रोम", "रोम"), ("Madrid", "मैड्रिड", "माद्रिद"), ("Mexico City", "मेक्सिको सिटी", "मेक्सिको सिटी"),
        ("Cairo", "काहिरा", "कैरो"), ("Pretoria", "प्रिटोरिया", "प्रिटोरिया"), ("Buenos Aires", "ब्यूनस आयर्स", "ब्यूनस आयर्स"),
        ("Ankara", "अंकारा", "अंकारा"), ("Seoul", "सियोल", "सोल"), ("Bangkok", "बैंकॉक", "बँकॉक"),
        ("Hanoi", "हनोई", "हनोई"), ("Jakarta", "जकार्ता", "जकार्ता"), ("Singapore", "सिंगापुर", "सिंगापूर"),
        ("Abu Dhabi", "अबू धाबी", "अबू धाबी"), ("Riyadh", "रियाद", "रियाध"), ("Jerusalem", "यरूशलेम", "जेरुसलेम"),
        ("Bern", "बर्न", "बर्न"), ("Amsterdam", "एम्स्टर्डम", "ॲमस्टरडॅम"), ("Stockholm", "स्टॉकहोम", "स्टॉकहोम"),
        ("Oslo", "ओस्लो", "ओस्लो"), ("Wellington", "वेलिंगटन", "वेलिंग्टन"), ("Athens", "एथेंस", "अथेन्स"),
        ("Lisbon", "लिस्बन", "लिस्बन"), ("Brussels", "ब्रसेल्स", "ब्रसेल्स"), ("Vienna", "वियना", "व्हिएन्ना"),
        ("Copenhagen", "कोपेनहेगन", "कोपनहेगन"), ("Helsinki", "हेलसिंकी", "हेलसिंकी"),
        ("Warsaw", "वारसॉ", "वॉर्सा"), ("Dublin", "डबलिन", "डब्लिन"), ("Wellington", "वेलिंगटन", "वेलिंग्टन")
    ]
    
    for i in range(len(countries)):
        c = countries[i]
        correct_cap = country_capitals[i]
        
        # Pick 3 wrong options
        wrong_options = random.sample([cap for idx, cap in enumerate(country_capitals) if idx != i], 3)
        
        options = [{"en": correct_cap[0], "hi": correct_cap[1], "mr": correct_cap[2]}]
        for w in wrong_options:
            options.append({"en": w[0], "hi": w[1], "mr": w[2]})
            
        random.shuffle(options)
        
        all_q.append({
            "en": f"What is the capital of {c[0]}?",
            "hi": f"{c[1]} की राजधानी क्या है?",
            "mr": f"{c[2]} ची राजधानी कोणती?",
            "options": options,
            "correct": correct_cap[0]
        })

    # -------------------------------
    # ✅ MATH QUESTIONS (850+)
    # -------------------------------
    # Addition
    for i in range(300):
        a, b = random.randint(1, 200), random.randint(1, 200)
        ans = a + b
        options = [
            {"en": str(ans), "hi": str(ans), "mr": str(ans)},
            {"en": str(ans + random.randint(1, 10)), "hi": str(ans + random.randint(1, 10)), "mr": str(ans + random.randint(1, 10))},
            {"en": str(ans - random.randint(1, 5)), "hi": str(ans - random.randint(1, 5)), "mr": str(ans - random.randint(1, 5))},
            {"en": str(ans + 15), "hi": str(ans + 15), "mr": str(ans + 15)}
        ]
        random.shuffle(options)
        all_q.append({
            "en": f"What is {a} + {b}?",
            "hi": f"{a} + {b} कितना होता है?",
            "mr": f"{a} + {b} किती होतात?",
            "options": options, "correct": str(ans)
        })

    # Subtraction
    for i in range(250):
        a, b = random.randint(1, 200), random.randint(1, 200)
        if a < b: a, b = b, a
        ans = a - b
        options = [
            {"en": str(ans), "hi": str(ans), "mr": str(ans)},
            {"en": str(ans + random.randint(1, 5)), "hi": str(ans + random.randint(1, 5)), "mr": str(ans + random.randint(1, 5))},
            {"en": str(ans - random.randint(1, 5)), "hi": str(ans - random.randint(1, 5)), "mr": str(ans - random.randint(1, 5))},
            {"en": str(ans + 12), "hi": str(ans + 12), "mr": str(ans + 12)}
        ]
        random.shuffle(options)
        all_q.append({
            "en": f"What is {a} - {b}?",
            "hi": f"{a} - {b} कितना होता है?",
            "mr": f"{a} - {b} किती होतात?",
            "options": options, "correct": str(ans)
        })

    # Multiplication
    for i in range(300):
        a, b = random.randint(2, 25), random.randint(2, 25)
        ans = a * b
        options = [
            {"en": str(ans), "hi": str(ans), "mr": str(ans)},
            {"en": str(ans + random.randint(1, 10)), "hi": str(ans + random.randint(1, 10)), "mr": str(ans + random.randint(1, 10))},
            {"en": str(ans - random.randint(1, 10)), "hi": str(ans - random.randint(1, 10)), "mr": str(ans - random.randint(1, 10))},
            {"en": str(ans + a), "hi": str(ans + a), "mr": str(ans + a)}
        ]
        random.shuffle(options)
        all_q.append({
            "en": f"What is {a} * {b}?",
            "hi": f"{a} * {b} कितना होता है?",
            "mr": f"{a} * {b} किती होतात?",
            "options": options, "correct": str(ans)
        })

    # Division (ensure perfectly divisible)
    for i in range(150):
        divisor = random.randint(2, 20)
        ans = random.randint(2, 50)
        dividend = divisor * ans
        options = [
            {"en": str(ans), "hi": str(ans), "mr": str(ans)},
            {"en": str(ans + random.randint(1, 5)), "hi": str(ans + random.randint(1, 5)), "mr": str(ans + random.randint(1, 5))},
            {"en": str(ans - random.randint(1, 3)), "hi": str(ans - random.randint(1, 3)), "mr": str(ans - random.randint(1, 3))},
            {"en": str(ans + 10), "hi": str(ans + 10), "mr": str(ans + 10)}
        ]
        random.shuffle(options)
        all_q.append({
            "en": f"What is {dividend} ÷ {divisor}?",
            "hi": f"{dividend} ÷ {divisor} कितना होता है?",
            "mr": f"{dividend} ÷ {divisor} किती होतात?",
            "options": options, "correct": str(ans)
        })

    # -------------------------------
    # ✅ CATEGORIZED SCIENCE QUESTIONS (120+)
    # -------------------------------
    science_categories = {
        "Planets": [
            ("Which planet is closest to the Sun?", "सूर्य के सबसे निकट कौन सा ग्रह है?", "सूर्याच्या सर्वात जवळचा ग्रह कोणता?", "Mercury", "बुध", "बुध"),
            ("Planet known as Red Planet?", "किस ग्रह को लाल ग्रह कहा जाता है?", "कोणत्या ग्रहाला लाल ग्रह म्हणतात?", "Mars", "मंगल", "मंगळ"),
            ("Largest planet in our Solar System?", "हमारे सौर मंडल का सबसे बड़ा ग्रह?", "आपल्या सूर्यमालेतील सर्वात मोठा ग्रह?", "Jupiter", "बृहस्पति", "गुरु"),
            ("Which planet has prominent rings?", "किस ग्रह के प्रमुख छल्ले हैं?", "कोणत्या ग्रहाला प्रमुख कड्या आहेत?", "Saturn", "शनि", "शनि"),
            ("Which planet is known as Earth's twin?", "किस ग्रह को पृथ्वी की जुड़वां बहन कहा जाता है?", "कोणत्या ग्रहाला पृथ्वीची जुळी बहीण म्हणतात?", "Venus", "शुक्र", "शुक्र"),
            ("Which planet is the hottest in our solar system?", "हमारे सौर मंडल का सबसे गर्म ग्रह कौन सा है?", "आपल्या सूर्यमालेतील सर्वात उष्ण ग्रह कोणता?", "Venus", "शुक्र", "शुक्र")
        ],
        "Units": [
            ("Unit of force?", "बल का मात्रक क्या है?", "बलाचे एकक काय आहे?", "Newton", "न्यूटन", "न्यूटन"),
            ("Unit of electrical current?", "विद्युत धारा का मात्रक क्या है?", "विजेच्या प्रवाहाचे एकक काय आहे?", "Ampere", "एम्पीयर", "अँपिअर"),
            ("Unit of power?", "शक्ति का मात्रक क्या है?", "शक्तीचे एकक काय आहे?", "Watt", "वाट", "वॉट"),
            ("Unit of frequency?", "आवृत्ति का मात्रक क्या है?", "वारंवारतेचे एकक काय आहे?", "Hertz", "हर्ट्ज़", "हर्ट्झ"),
            ("Unit of energy?", "ऊर्जा का मात्रक क्या है?", "उर्जेचे एकक काय आहे?", "Joule", "जूल", "जूल"),
            ("Unit of electrical resistance?", "विद्युत प्रतिरोध का मात्रक क्या है?", "विद्युत रोधाचे एकक काय आहे?", "Ohm", "ओम", "ओहम")
        ],
        "Biology": [
            ("Powerhouse of the cell?", "कोशिका का पावरहाउस किसे कहते हैं?", "पेशींचे ऊर्जाकेंद्र कोणाला म्हणतात?", "Mitochondria", "माइटोकॉन्ड्रिया", "मायटोकॉन्ड्रिया"),
            ("Study of plants?", "पौधों के अध्ययन को क्या कहते हैं?", "वनस्पतींच्या अभ्यासाला काय म्हणतात?", "Botany", "वनस्पति विज्ञान", "वनस्पतिशास्त्र"),
            ("Study of animals?", "जानवरों के अध्ययन को क्या कहते हैं?", "प्राण्यांच्या अभ्यासाला काय म्हणतात?", "Zoology", "जंतु विज्ञान", "प्राणीशास्त्र"),
            ("Vitamin from Sun?", "सूर्य से कौन सा विटामिन मिलता है?", "सूर्यापासून कोणते जीवनसत्व मिळते?", "Vitamin D", "विटामिन डी", "जीवनसत्व डी"),
            ("Green pigment in plants?", "पौधों में हरा वर्णक?", "वनस्पतींमधील हिरवे रंगद्रव्य कोणते?", "Chlorophyll", "क्लोरोफिल", "हरितद्रव्य"),
            ("Which blood cells carry oxygen?", "कौन सी रक्त कोशिकाएं ऑक्सीजन ले जाती हैं?", "कोणत्या रक्तपेशी ऑक्सिजन वाहून नेतात?", "Red Blood Cells", "लाल रक्त कोशिकाएं", "तांबड्या रक्तपेशी")
        ],
        "Chemistry": [
            ("What is the chemical symbol for water?", "पानी का रासायनिक सूत्र क्या है?", "पाण्याचे रासायनिक सूत्र काय आहे?", "H2O", "H2O", "H2O"),
            ("Gas used in balloons?", "गुब्बारों में कौन सी गैस भरी जाती है?", "फुग्यांमध्ये कोणता वायू भरला जातो?", "Helium", "हीलियम", "हिलिअम"),
            ("Symbol of Gold?", "सोने का प्रतीक क्या है?", "सोन्याची संज्ञा काय आहे?", "Au", "Au", "Au"),
            ("What gas do humans breathe in?", "मनुष्य कौन सी गैस लेते हैं?", "माणूस कोणता वायू श्वासावाटे घेतो?", "Oxygen", "ऑक्सीजन", "ऑक्सिजन"),
            ("Chemical symbol for Iron?", "लोहे का रासायनिक प्रतीक क्या है?", "लोखंडाची रासायनिक संज्ञा काय आहे?", "Fe", "Fe", "Fe"),
            ("Which gas is responsible for global warming?", "ग्लोबल वार्मिंग के लिए कौन सी गैस जिम्मेदार है?", "ग्लोबल वॉर्मिंगला कोणता वायू जबाबदार आहे?", "Carbon Dioxide", "कार्बन डाइऑक्साइड", "कार्बन डायऑक्साइड")
        ]
    }

    # Generate facts by sampling randomly from same category
    for cat, facts in science_categories.items():
        for i in range(30):
            fact = random.choice(facts)
            other_facts = [f for f in facts if f[0] != fact[0]]
            wrong_facts = random.sample(other_facts, min(3, len(other_facts)))
            
            options = [{"en": fact[3], "hi": fact[4], "mr": fact[5]}]
            for wf in wrong_facts:
                options.append({"en": wf[3], "hi": wf[4], "mr": wf[5]})
            
            while len(options) < 4:
                filler = random.choice(other_facts)
                options.append({"en": filler[3], "hi": filler[4], "mr": filler[5]})
                
            random.shuffle(options)
            all_q.append({
                "en": f"{fact[0]}",
                "hi": f"{fact[1]}",
                "mr": f"{fact[2]}",
                "options": options,
                "correct": fact[3]
            })

    seen_questions = set()
    unique_all_q = []
    
    for q in all_q:
        if q['en'] not in seen_questions:
            unique_all_q.append(q)
            seen_questions.add(q['en'])
            
    print(f"Total unique questions to seed: {len(unique_all_q)}")

    try:
        # Clear existing
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE user_answers")
        cursor.execute("TRUNCATE TABLE options")
        cursor.execute("TRUNCATE TABLE questions")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        correct_count = 0
        for q in unique_all_q:
            cursor.execute("INSERT INTO questions (question, question_hi, question_mr) VALUES (%s, %s, %s)", (q['en'], q['hi'], q['mr']))
            q_id = cursor.lastrowid
            
            q_correct_val = str(q['correct']).strip()
            for opt in q['options']:
                opt_en_val = str(opt['en']).strip()
                is_correct = 1 if opt_en_val == q_correct_val else 0
                if is_correct: correct_count += 1
                
                cursor.execute("""
                    INSERT INTO options (question_id, option_text, option_text_hi, option_text_mr, is_correct) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (q_id, opt['en'], opt['hi'], opt['mr'], is_correct))
        
        conn.commit()
        print(f"✅ Successfully seeded {len(unique_all_q)} questions. Total correct flags set: {correct_count}")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_india_questions()
