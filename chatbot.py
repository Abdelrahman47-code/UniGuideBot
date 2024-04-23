import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from fuzzywuzzy import fuzz

# Define intents for English
intents_en = {
    "Course Information Request": {
        "queries": [
            "Can you provide details about the Computer Science program?",
            "What courses are offered in the Business Administration department?",
            "Tell me more about the Engineering curriculum."
        ],
        "response": "The university offers a comprehensive Computer Science program focusing on algorithms, data structures, and software engineering principles. The Business Administration department provides courses in management, finance, marketing, and more. The Engineering curriculum covers various disciplines such as mechanical, electrical, and civil engineering."
    },
    "Admission-related Question": {
        "queries": [
            "What are the admission requirements for international students?",
            "How do I apply for financial aid?",
            "Can you explain the application process?"
        ],
        "response": "International students need to fulfill specific admission requirements, including English proficiency tests and visa documentation. Financial aid applications can be submitted through the university's online portal. The application process involves filling out the online form, submitting required documents, and paying the application fee."
    },
    "Academic Advising and Course Planning": {
        "queries": [
            "How can I schedule an appointment with my academic advisor?",
            "What courses should I take next semester for my major?",
            "Is there a tool to help me plan my course schedule?"
        ],
        "response": "You can schedule an appointment with your academic advisor through the university's online appointment booking system. Additionally, you can use the course planning tool available on the student portal to plan your courses for the upcoming semester."
    },
    "Tuition and Fees": {
        "queries": [
            "What is the tuition fee for international students?",
            "Are there any scholarships available to help cover tuition costs?",
            "How do I view my student account balance?"
        ],
        "response": "Tuition fees for international students vary depending on the program and course load. Scholarships and financial aid opportunities are available to help cover tuition costs for eligible students. You can view your student account balance by logging into the university's student portal."
    },
    "Student Life and Activities": {
        "queries": [
            "What extracurricular activities are available on campus?",
            "Are there any upcoming events or social gatherings for students?",
            "How can I get involved in student clubs?"
        ],
        "response": "The university offers a wide range of extracurricular activities, including clubs, sports teams, and cultural organizations. You can find information about upcoming events and social gatherings on the university's events calendar. To get involved in student clubs, you can attend club fairs or contact the club leaders directly."
    },
    "Transportation and Parking": {
        "queries": [
            "Where can I find information about campus shuttle schedules?",
            "Is there parking available for commuter students?",
            "Are there bike racks available on campus?"
        ],
        "response": "Information about campus shuttle schedules can be found on the university's transportation website. Commuter students can purchase parking permits for designated parking lots on campus. Additionally, bike racks are available at various locations on campus for cyclists."
    },
    "Graduation and Commencement": {
        "queries": [
            "How do I apply for graduation?",
            "When is the commencement ceremony scheduled?",
            "Are there any requirements for participating in graduation?"
        ],
        "response": "To apply for graduation, you need to complete the graduation application form available on the university's website. The commencement ceremony is typically scheduled at the end of each academic year. To participate in graduation, you must fulfill all degree requirements and clear any outstanding fees or holds on your student account."
    },
    "Technology and IT Support": {
        "queries": [
            "How do I access the university's Wi-Fi network?",
            "Is there technical support available for students' laptops?",
            "Where can I find information about software discounts for students?"
        ],
        "response": "You can access the university's Wi-Fi network by logging in with your student credentials. Technical support for students' laptops is available at the university's IT help desk. Information about software discounts for students can be found on the university's software portal."
    },
    "Housing and Accommodation": {
        "queries": [
            "What are the housing options available for students?",
            "How do I apply for on-campus housing?",
            "Can you provide information about off-campus accommodation?"
        ],
        "response": "The university offers various housing options for students, including on-campus dormitories and off-campus apartments. To apply for on-campus housing, you can visit the university's housing portal and complete the application form. Additionally, there are resources available to help you find off-campus accommodation near the university."
    },
    "Financial Aid Status": {
        "queries": [
            "What is the status of my financial aid application?",
            "How do I check if my scholarship application has been processed?",
            "Can you help me track my student loan status?"
        ],
        "response": "You can check the status of your financial aid application by logging into the university's financial aid portal. If you have applied for a scholarship, you will receive an email notification once your application has been processed. For student loans, you can contact the financial aid office for assistance in tracking the status of your application."
    },
    "Health and Wellness Services": {
        "queries": [
            "Where is the university health center located?",
            "How can I make an appointment with a counselor?",
            "What health services are covered by the student health insurance?"
        ],
        "response": "The university health center is located on campus, next to the student union building. You can schedule an appointment with a counselor by calling the health center or visiting their website. Student health insurance covers a wide range of services, including doctor visits, prescriptions, and mental health counseling."
    },
    "Library Services": {
        "queries": [
            "How do I borrow books from the university library?",
            "Are there any online resources available through the library?",
            "What are the library hours during exam week?"
        ],
        "response": "To borrow books from the university library, you can use your student ID card at the self-checkout machines. The library provides access to a variety of online resources, including e-books, journals, and databases. During exam week, the library extends its hours to accommodate students' study needs."
    },
    "Career Services": {
        "queries": [
            "How can I schedule a career counseling session?",
            "Are there any job fairs happening on campus?",
            "Can you help me with my resume and cover letter?"
        ],
        "response": "You can schedule a career counseling session through the university's career services website or by contacting the career center directly. Job fairs are regularly held on campus, and you can find information about upcoming events on the career services calendar. Career advisors are available to assist you with resume writing, cover letter preparation, and job search strategies."
    },
    "International Student Support": {
        "queries": [
            "What resources are available for international students?",
            "How do I apply for a student visa extension?",
            "Where can I find information about cultural adaptation workshops?"
        ],
        "response": "The university offers a range of support services for international students, including orientation programs, academic advising, and English language assistance. To apply for a student visa extension, you will need to contact the international student office for guidance and assistance. Cultural adaptation workshops are regularly organized by the international student services department to help international students adjust to life in a new country."
    },
    "Faculty and Department Contact": {
        "queries": [
            "How can I contact the Computer Science department?",
            "Who is the advisor for the Business Administration program?",
            "Can you provide me with the email address of the Dean of Students?"
        ],
        "response": "You can contact the Computer Science department by visiting their office in the science building or emailing them at csdept@university.edu. The advisor for the Business Administration program is Professor John Smith, and you can schedule an appointment with him through the department's administrative assistant. The email address of the Dean of Students is deanofstudents@university.edu."
    },
    "Research Opportunities": {
        "queries": [
            "Are there any research assistant positions available?",
            "How do I apply for undergraduate research funding?",
            "Where can I find information about ongoing research projects in my field?"
        ],
        "response": "Research assistant positions are occasionally available in various departments and research centers across campus. You can inquire about available positions by contacting faculty members or visiting the university's research office. To apply for undergraduate research funding, you will need to submit a research proposal to the undergraduate research committee. Information about ongoing research projects in your field can be found on the university's research website or through academic journals and conferences."
    },
}

# Define intents for Arabic
intents_ar = {
    "طلب معلومات عن الدورات الدراسية": {
        "queries": [
            "هل يمكنك توفير تفاصيل حول برنامج علوم الكمبيوتر؟",
            "ما هي الدورات المقدمة في قسم إدارة الأعمال؟",
            "أخبرني المزيد عن منهج الهندسة."
        ],
        "response": "تقدم الجامعة برنامجًا شاملاً في علوم الكمبيوتر يركز على الخوارزميات وهياكل البيانات ومبادئ هندسة البرمجيات. يوفر قسم إدارة الأعمال دورات في الإدارة والتمويل والتسويق وغيرها. يغطي منهج الهندسة مجموعة متنوعة من التخصصات مثل الهندسة الميكانيكية والكهربائية والمدنية."
    },
    "سؤال متعلق بالقبول": {
        "queries": [
            "ما هي متطلبات القبول للطلاب الدوليين؟",
            "كيف يمكنني التقديم للحصول على المساعدة المالية؟",
            "هل يمكنك شرح عملية التقديم؟"
        ],
        "response": "يجب على الطلاب الدوليين تحقيق متطلبات القبول المحددة، بما في ذلك اختبارات اللغة الإنجليزية وتوثيق التأشيرة. يمكن تقديم طلبات المساعدة المالية من خلال بوابة الجامعة الإلكترونية. تتضمن عملية التقديم ملء النموذج عبر الإنترنت وتقديم الوثائق المطلوبة ودفع رسوم التقديم."
    },
    "الإرشاد الأكاديمي وتخطيط الدورات": {
        "queries": [
            "كيف يمكنني تحديد موعد مع مستشاري الدراسات؟",
            "ما هي الدورات التي يجب عليّ أخذها الفصل الدراسي المقبل لتخصصي؟",
            "هل هناك أداة تساعدني في تخطيط جدول الدورات؟"
        ],
        "response": "يمكنك تحديد موعد مع مستشاري الدراسات الأكاديمية من خلال نظام حجز المواعيد الإلكتروني للجامعة. بالإضافة إلى ذلك، يمكنك استخدام أداة تخطيط الدورات المتاحة على بوابة الطالب لتخطيط دوراتك للفصل الدراسي القادم."
    },
    "الرسوم الدراسية والرسوم": {
        "queries": [
            "ما هي رسوم الدراسة للطلاب الدوليين؟",
            "هل هناك منح دراسية متاحة لمساعدة في تغطية تكاليف الدراسة؟",
            "كيف يمكنني عرض رصيد حسابي الطلابي؟"
        ],
        "response": "تختلف رسوم الدراسة للطلاب الدوليين اعتمادًا على البرنامج وحمولة الدورات. تتوفر منح دراسية وفرص مساعدة مالية لمساعدة الطلاب المؤهلين في تغطية تكاليف الدراسة. يمكنك عرض رصيد حسابك الطلابي عن طريق تسجيل الدخول إلى بوابة الطالب الإلكترونية للجامعة."
    },
    "حياة الطلاب والأنشطة": {
        "queries": [
            "ما هي الأنشطة اللاصفية المتاحة على الحرم الجامعي؟",
            "هل هناك أحداث مقبلة أو تجمعات اجتماعية للطلاب؟",
            "كيف يمكنني المشاركة في نوادي الطلاب؟"
        ],
        "response": "تقدم الجامعة مجموعة واسعة من الأنشطة اللاصفية، بما في ذلك النوادي وفرق الرياضة والمنظمات الثقافية. يمكنك العثور على معلومات حول الأحداث المقبلة والتجمعات الاجتماعية على التقويم الخاص بالجامعة. للمشاركة في نوادي الطلاب، يمكنك حضور معارض النوادي أو الاتصال بقادة النوادي مباشرة."
    },
        "النقل ومواقف السيارات": {
        "queries": [
            "أين يمكنني العثور على معلومات حول جداول الحافلات على الحرم الجامعي؟",
            "هل هناك مواقف متاحة لطلاب الانتقال؟",
            "هل هناك حاملات للدراجات متاحة على الحرم الجامعي؟"
        ],
        "response": "يمكن العثور على معلومات حول جداول الحافلات على موقع الجامعة للنقل. يمكن للطلاب الانتقاليين شراء تصاريح وقوف السيارات للمواقف المخصصة في الحرم الجامعي. بالإضافة إلى ذلك، تتوفر حاملات للدراجات في مواقع متنوعة على الحرم الجامعي للدراجين."
    },
    "التخرج والحفل الختامي": {
        "queries": [
            "كيف يمكنني التقديم للتخرج؟",
            "متى يتم جدولة حفل التخرج؟",
            "هل هناك أي متطلبات للمشاركة في حفل التخرج؟"
        ],
        "response": "للتقديم للتخرج، يجب عليك ملء استمارة التقديم المتاحة على موقع الجامعة الإلكتروني. يتم جدولة حفل التخرج عادة في نهاية كل عام أكاديمي. للمشاركة في حفل التخرج، يجب عليك استيفاء جميع متطلبات الدرجة وتسوية أي رسوم معلقة أو حجوزات على حسابك الطلابي."
    },
    "التكنولوجيا ودعم تقنية المعلومات": {
        "queries": [
            "كيف يمكنني الوصول إلى شبكة الواي فاي في الجامعة؟",
            "هل هناك دعم فني متاح لأجهزة الكمبيوتر المحمولة للطلاب؟",
            "أين يمكنني العثور على معلومات حول تخفيضات البرامج الثابتة للطلاب؟"
        ],
        "response": "يمكنك الوصول إلى شبكة الواي فاي في الجامعة عن طريق تسجيل الدخول باستخدام بيانات الطالب الخاصة بك. يتوفر دعم فني لأجهزة الكمبيوتر المحمولة للطلاب في مكتب المساعدة التقنية بالجامعة. يمكن العثور على معلومات حول تخفيضات البرامج الثابتة للطلاب على بوابة البرمجيات الخاصة بالجامعة."
    },
    "الإقامة والسكن": {
        "queries": [
            "ما هي الخيارات السكنية المتاحة للطلاب؟",
            "كيف يمكنني التقديم للحصول على سكن داخل الحرم؟",
            "هل يمكنك توفير معلومات حول الإقامة خارج الحرم؟"
        ],
        "response": "تقدم الجامعة مجموعة متنوعة من الخيارات السكنية للطلاب، بما في ذلك المساكن داخل الحرم والشقق خارج الحرم. للتقديم للسكن داخل الحرم، يمكنك زيارة بوابة السكن للجامعة وملء استمارة التقديم. بالإضافة إلى ذلك، تتوفر موارد لمساعدتك في العثور على سكن خارج الحرم بالقرب من الجامعة."
    },
    "حالة المساعدات المالية": {
        "queries": [
            "ما هو حالة طلب المساعدة المالية الخاص بي؟",
            "كيف يمكنني التحقق مما إذا تم معالجة طلبي للمنحة؟",
            "هل يمكنك مساعدتي في تتبع حالة قرض الطالب الخاص بي؟"
        ],
        "response": "يمكنك التحقق من حالة طلب المساعدة المالية الخاص بك عن طريق تسجيل الدخول إلى بوابة المساعدة المالية للجامعة. إذا قدمت طلبًا للمنحة، ستتلقى إشعارًا بالبريد الإلكتروني بمجرد معالجة طلبك. بالنسبة للقروض الطلابية، يمكنك الاتصال بمكتب المساعدة المالية للحصول على مساعدة في تتبع حالة طلبك."
    },
    "خدمات الصحة والعافية": {
        "queries": [
            "أين يقع مركز الصحة الجامعية؟",
            "كيف يمكنني تحديد موعد مع مستشار؟",
            "ما هي الخدمات الصحية التي تغطيها تأمين صحة الطلاب؟"
        ],
        "response": "يقع مركز الصحة الجامعية على الحرم الجامعي، بجوار مبنى الاتحاد الطلابي. يمكنك تحديد موعد مع مستشار عن طريق الاتصال بمركز الصحة أو زيارة موقعهم على الويب. يغطي تأمين صحة الطلاب مجموعة واسعة من الخدمات، بما في ذلك زيارات الأطباء والوصفات الطبية والاستشارة الصحية النفسية."
    },
    "خدمات المكتبة": {
        "queries": [
            "كيف يمكنني استعارة الكتب من مكتبة الجامعة؟",
            "هل هناك أي موارد عبر الإنترنت متاحة من خلال المكتبة؟",
            "ما هي ساعات المكتبة خلال أسبوع الامتحانات؟"
        ],
        "response": "يمكنك استعارة الكتب من مكتبة الجامعة باستخدام بطاقة الطالب الخاصة بك في آلات الدفع الذاتي. توفر المكتبة الوصول إلى مجموعة متنوعة من الموارد عبر الإنترنت، بما في ذلك الكتب الإلكترونية والمجلات وقواعد البيانات. خلال أسبوع الامتحانات، تمتد ساعات المكتبة لتلبية احتياجات الطلاب للدراسة."
    },
    "خدمات الوظائف": {
        "queries": [
            "كيف يمكنني تحديد موعد لجلسة استشارات وظيفية؟",
            "هل هناك أي معارض وظائف تقام على الحرم الجامعي؟",
            "هل يمكنك مساعدتي في كتابة سيرتي الذاتية وخطاب الغلاف؟"
        ],
        "response": "يمكنك تحديد موعد لجلسة استشارات وظيفية من خلال موقع خدمات الوظائف للجامعة أو عن طريق الاتصال بمركز الوظائف مباشرة. تقام معارض الوظائف بانتظام على الحرم الجامعي، ويمكنك العثور على معلومات حول الفعاليات القادمة على تقويم خدمات الوظائف. يتوفر مستشارو الوظائف لمساعدتك في كتابة السيرة الذاتية وإعداد خطاب الغلاف واستراتيجيات البحث عن الوظائف."
    },
    "دعم الطلاب الدوليين": {
        "queries": [
            "ما هي الموارد المتاحة للطلاب الدوليين؟",
            "كيف يمكنني التقديم لتمديد تأشيرة الطالب؟",
            "أين يمكنني العثور على معلومات حول ورش العمل للتكيف الثقافي؟"
        ],
        "response": "تقدم الجامعة مجموعة من خدمات الدعم للطلاب الدوليين، بما في ذلك برامج التوجيه الأكاديمي والمساعدة في اللغة الإنجليزية. للتقديم لتمديد تأشيرة الطالب، ستحتاج إلى الاتصال بمكتب الطالب الدولي للحصول على الإرشاد والمساعدة. تُنظم ورش العمل للتكيف الثقافي بانتظام من قبل قسم خدمات الطلاب الدوليين لمساعدة الطلاب الدوليين على التكيف مع الحياة في بلد جديد."
    },
    "اتصال الكليات والأقسام": {
        "queries": [
            "كيف يمكنني الاتصال بقسم علوم الحاسوب؟",
            "من هو المستشار لبرنامج إدارة الأعمال؟",
            "هل يمكنك توفير عنوان البريد الإلكتروني لعميد الطلاب؟"
        ],
        "response": "يمكنك الاتصال بقسم علوم الحاسوب عن طريق زيارة مكتبهم في مبنى العلوم أو إرسال بريد إلكتروني إليهم على csdept@university.edu. المستشار لبرنامج إدارة الأعمال هو البروفيسور جون سميث، ويمكنك تحديد موعد معه من خلال مساعد الإدارة بالقسم. عنوان البريد الإلكتروني لعميد الطلاب هو deanofstudents@university.edu."
    },
    "فرص البحث": {
        "queries": [
            "هل هناك أي وظائف مساعد بحثية متاحة؟",
            "كيف يمكنني التقديم للحصول على تمويل بحث تحت الدراسة الجامعية؟",
            "أين يمكنني العثور على معلومات حول المشاريع البحثية الجارية في مجالي؟"
        ],
        "response": "تتوفر أحيانًا فرص وظائف مساعد بحثية في مختلف الأقسام ومراكز البحث عبر الحرم الجامعي. يمكنك الاستفسار عن الوظائف المتاحة عن طريق الاتصال بأعضاء هيئة التدريس أو زيارة مكتب البحث بالجامعة. للتقديم للحصول على تمويل بحث تحت الدراسة الجامعية، ستحتاج إلى تقديم مقترح بحث للجنة البحث الجامعية. يمكن العثور على معلومات حول المشاريع البحثية الجارية في مجالك على موقع الويب للبحث الجامعي للجامعة أو من خلال المجلات الأكاديمية والمؤتمرات."
    }

}

# Define exit keywords
exit_keywords = ["exit", "quit", "close", "end"]

# Initialize stemmer
stemmer = PorterStemmer()

# Function to preprocess text
def preprocess_text(text):
    # Tokenize text
    tokens = word_tokenize(text)
    # Stem tokens
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

# Function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    # Preprocess texts
    tokens1 = preprocess_text(text1)
    tokens2 = preprocess_text(text2)
    # Calculate Jaccard similarity
    similarity = len(set(tokens1).intersection(tokens2)) / len(set(tokens1).union(tokens2))
    return similarity

# Function to match user input to intents based on language
def match_intent(user_input, lang='en'):
    if lang == 'en':
        intents = intents_en
    elif lang == 'ar':
        intents = intents_ar
    else:
        return None  # Unsupported language
    
    max_similarity = 0
    matched_intent = None
    for intent, data in intents.items():
        for query in data["queries"]:
            similarity = calculate_similarity(user_input, query)
            if similarity > max_similarity:
                max_similarity = similarity
                matched_intent = intent
    return matched_intent if max_similarity > 0.5 else None

# Function to check if user wants to exit
def check_exit(user_input):
    return any(keyword in user_input.lower() for keyword in exit_keywords)

# Function to generate responses based on language and matched intent
def generate_response(intent, lang='en'):
    if lang == 'en':
        intents = intents_en
    elif lang == 'ar':
        intents = intents_ar
    else:
        return "Sorry, I can't understand your language."
    
    return intents[intent]["response"] if intent in intents else "Sorry, I'm not sure how to respond to that."
