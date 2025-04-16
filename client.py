from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections
from flask_cors import CORS
from ast import literal_eval 
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dhananjaydogne:DD@cluster0.q565lol.mongodb.net/?retryWrites=true&w=majority"

# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#DB
mongo = PyMongo(app)
# Define patterns and responses for the chatbot (your existing patterns)
patterns = [
    (r'hi|hello|hey', ['Hello! I am a SmileTalk made by Techgeeks']),

    #depression
    (r'(.*) (depressed|anxious|lonely|loneliness|stressed|sad|irritate| anxiety)',
        ['I’m sorry to hear that. Its okay to feel that way sometimes. How can I support you?']),
    (r'(.*) (solution of depression|depression treatment|solution of anxiousness|anxiety treatment|solution of loneliness|loneliness treatment|treatment for stress|stress treatment| sadness |irritation)',
        ['Therapy or counseling Build a support network Stay active and engage in social activities Self-care and stress management Challenge negative thoughts Limit social media use Medication (if prescribed by a healthcare professional) Set personal goals']),
    (r'(.*) (solution of depression|depression treatment|solution of anxiousness|anxiety treatment|solution of loneliness|loneliness treatment|treatment for stress|stress treatment| sadness |irritation)(.*)',
        ['Therapy or counseling Build a support network Stay active and engage in social activities Self-care and stress management Challenge negative thoughts Limit social media use Medication (if prescribed by a healthcare professional) Set personal goals']),
    (r'(solution of depression|depression treatment|solution of anxiousness|anxiety treatment|solution of loneliness|loneliness treatment|treatment for stress|stress treatment| sadness |irritation)(.*)',
        ['Therapy or counseling Build a support network Stay active and engage in social activities Self-care and stress management Challenge negative thoughts Limit social media use Medication (if prescribed by a healthcare professional) Set personal goals']),
    (r'(solution of depression|depression treatment|solution of anxiousness|anxiety treatment|solution of loneliness|loneliness treatment|treatment for stress|stress treatment| sadness |irritation)',
        ['Therapy or counseling Build a support network Stay active and engage in social activities Self-care and stress management Challenge negative thoughts Limit social media use Medication (if prescribed by a healthcare professional) Set personal goals']),



    (r'(.*) (need someone to talk to|mental health professional|nearby mental care center)',
        ['I am here to listen and offer support. What is been bothering you?']),
    (r'(.*) help with (.*)',
        ['I can provide information and suggestions. What do you need help with?']),
    # (r'(.*) (symptom of mental health|sign of mental health)', ['It is estimated that mental illness affects 1 in 5 adults in America, and that 1 in 24 adults have a serious mental illness. Mental illness does not discriminate; it can affect anyone, regardless of gender, age, income, social status, ethnicity, religion, sexual orientation, or background. Although mental illness can affect anyone, certain conditions may be more common in different populations. For instance, eating disorders tend to occur more often in females, while disorders such as attention deficit/hyperactivity disorder is more prevalent in children. Additionally, all ages are susceptible, but the young and the old are especially vulnerable. Mental illnesses usually strike individuals in the prime of their lives, with 75 percent of mental health conditions developing by the age of 24. This makes identification and treatment of mental disorders particularly difficult, because the normal personality and behavioral changes of adolescence may mask symptoms of a mental health condition. Parents and caretakers should be aware of this fact, and take notice of changes in their childâ€™s mood, personality, personal habits, and social withdrawal. When these occur in children under 18, they are referred to as serious emotional disturbances (SEDs).']),
    (r'(.*) (symptom of mental health|sign of mental health)', ['Common mental health signs and symptoms include changes in mood, behavior, and thoughts, along with physical and emotional symptoms. These indicators can vary depending on the specific mental health condition and its severity, making professional evaluation and support essential for diagnosis and treatment.']),
    (r'(.*) (mental health|mental illeness)', ['Mental health is feeling good and coping well with life, while mental illness is when you are struggling with your thoughts and emotions']),
    (r'(.*) (mental illness recover|recover)', ['Yes, many individuals with mental illnesses can recover, manage their conditions effectively, and lead fulfilling lives with the right treatment, support, and coping strategies. Recovery is possible and varies from person to person.']),
    (r'(.*) (help)', ['I will be very happy to help you']),
    (r'(.*) (dissociative indentity disorder)', ['Dissociative Identity Disorder (DID) is a rare mental health condition characterized by the presence of multiple distinct identities or personality states within one individual, often arising from a history of severe trauma. Treatment typically involves therapy to integrate these identities and address underlying trauma. ']),
    (r'(.*) (treatement for dissociative indentity disorder)', ['The primary treatment for DID involves psychotherapy, utilizing approaches such as Dialectical Behavior Therapy (DBT), Cognitive-Behavioral Therapy (CBT), or Eye Movement Desensitization and Reprocessing (EMDR) to address the unique challenges presented by different identity states. This treatment also emphasizes stabilization, helping individuals manage their symptoms, emotional regulation, and safety. Trauma-informed care is central to this process, recognizing and addressing past traumatic experiences. Additionally, support from loved ones and a respectful approach to the individuals autonomy are key. The ultimate goal is to work towards integration, merging the identity states into a more unified sense of self, although this is done in a manner that respects the individuals choices and progress. Its important to note that DID treatment is often a long-term endeavor, and ongoing support is crucial to successful management of the disorder.']),
    (r'(.*) (difference between mental health and mental illness)', ['Mental health relates to overall emotional well-being and the ability to cope with lifes challenges, while mental illness specifically refers to diagnosed conditions that disrupt a person mental and emotional functioning, often requiring treatment and support. Mental health encompasses a broad spectrum, while mental illness is a specific subset of mental health concerns.']),
    # sucidal thoughts.
    (r'(.*) (sucide)', ['Sucide is not a right way to solve any problem so please do not follow it']),
    (r'(.*) (income assistance|fee|pay)', ['There are so many goverment schemes for treatment and government treatement center you can visit which are affordabel']),
    # (r'(.*) ()', ['I will be very happy to help you']),

    #some more!
    (r'(.*) (help)', ['I will be very happy to help you']),
    (r'(say something|say you something| problem| private|share| listen| say)', ['yes sure, I am listening']),
    (r'(.*) (say something| problem| private|share| listen| say)(.*)', ['yes sure, I am listening']),
    (r'(.*) (say something| problem| private|share| listen| say)', ['yes sure, I am listening']),
    (r'(say something| problem| private|share| listen| say)(.*)', ['yes sure, I am listening']),

    (r'(i love you|marry me|will you be my girlfriend|will you be my boyfriend)', ['I appreciate your sentiment, but I am just a computer program, so I dont have feelings. However, Im here to assist you and provide information and support to the best of my abilities. If you have any questions or need assistance with anything, please feel free to ask.']),




    (r'(.*) (medication)', ['Medication in mental health is essential for managing symptoms, restoring brain chemical balance, and improving the quality of life for individuals with various mental health conditions when used as part of a comprehensive treatment plan.']),
    (r'(.*) (physical health)', ['To care for your physical health, eat well, stay active, get enough rest, and avoid harmful habits like smoking and excessive drinking. Regular check-ups and staying safe can help keep you healthy.']),
    (r'(.*) (counsellor|psychaiatrist|psychologist)', ['I am currently working on that I will update the information soon']),

     # CBT/DBT
    (r'(.*) (negative thoughts)(.*)', ['CBT (Cognitive Behavioral Therapy) focuses on changing negative thought patterns and behaviors, while DBT (Dialectical Behavior Therapy) specializes in managing intense emotions and improving relationships, often used for borderline personality disorder. but you can deal it, Challenge Negative Thoughts: Learn to identify and challenge irrational or negative thoughts. Your therapist will help you develop techniques to reframe your thinking.Develop Coping Strategies: Work with your therapist to develop effective coping strategies for managing stress, anxiety, and other challenging emotions. Be Patient: CBT is not a quick fix; it takes time and effort. Be patient with yourself and the process. Stay Committed: Attend your therapy sessions regularly and commit to the treatment plan. Consistency is key to seeing progress. Monitor Progress: Keep track of your progress and any changes in your thoughts and behaviors. Share this information with your therapist to make adjustments to your treatment plan as needed.']),
    (r'(.*) (negative thoughts)', ['CBT (Cognitive Behavioral Therapy) focuses on changing negative thought patterns and behaviors, while DBT (Dialectical Behavior Therapy) specializes in managing intense emotions and improving relationships, often used for borderline personality disorder. but you can deal it, Challenge Negative Thoughts: Learn to identify and challenge irrational or negative thoughts. Your therapist will help you develop techniques to reframe your thinking.Develop Coping Strategies: Work with your therapist to develop effective coping strategies for managing stress, anxiety, and other challenging emotions. Be Patient: CBT is not a quick fix; it takes time and effort. Be patient with yourself and the process. Stay Committed: Attend your therapy sessions regularly and commit to the treatment plan. Consistency is key to seeing progress. Monitor Progress: Keep track of your progress and any changes in your thoughts and behaviors. Share this information with your therapist to make adjustments to your treatment plan as needed.']),
    (r'(negative thoughts) (.*)', ['CBT (Cognitive Behavioral Therapy) focuses on changing negative thought patterns and behaviors, while DBT (Dialectical Behavior Therapy) specializes in managing intense emotions and improving relationships, often used for borderline personality disorder. but you can deal it, Challenge Negative Thoughts: Learn to identify and challenge irrational or negative thoughts. Your therapist will help you develop techniques to reframe your thinking.Develop Coping Strategies: Work with your therapist to develop effective coping strategies for managing stress, anxiety, and other challenging emotions. Be Patient: CBT is not a quick fix; it takes time and effort. Be patient with yourself and the process. Stay Committed: Attend your therapy sessions regularly and commit to the treatment plan. Consistency is key to seeing progress. Monitor Progress: Keep track of your progress and any changes in your thoughts and behaviors. Share this information with your therapist to make adjustments to your treatment plan as needed.']),
    (r'(negative thoughts)', ['CBT (Cognitive Behavioral Therapy) focuses on changing negative thought patterns and behaviors, while DBT (Dialectical Behavior Therapy) specializes in managing intense emotions and improving relationships, often used for borderline personality disorder. but you can deal it, Challenge Negative Thoughts: Learn to identify and challenge irrational or negative thoughts. Your therapist will help you develop techniques to reframe your thinking.Develop Coping Strategies: Work with your therapist to develop effective coping strategies for managing stress, anxiety, and other challenging emotions. Be Patient: CBT is not a quick fix; it takes time and effort. Be patient with yourself and the process. Stay Committed: Attend your therapy sessions regularly and commit to the treatment plan. Consistency is key to seeing progress. Monitor Progress: Keep track of your progress and any changes in your thoughts and behaviors. Share this information with your therapist to make adjustments to your treatment plan as needed.']),


    (r'(.*) (CBT|DBT)', ['CBT (Cognitive Behavioral Therapy) focuses on changing negative thought patterns and behaviors, while DBT (Dialectical Behavior Therapy) specializes in managing intense emotions and improving relationships, often used for borderline personality disorder.']),

    # addict

    (r' (leave my addiction|leave addiction |leave alcohol|quit alcohol|leave drinking|quit drinking| leave drugs|quit drugs|quit smoking|leave smoking)', ['Acknowledge the problem. Seek professional help, such as therapy or counseling. Join a support group. Remove triggers and temptations. Develop a support system. Set clear, achievable goals for quitting. Replace addiction with healthy habits and activities. Stay committed to your recovery plan. Practice self-compassion and patience. Consider inpatient or outpatient treatment if necessary. Reach out to loved ones for support. Stay accountable through regular check-ins with a counselor or sponsor. Remember, quitting addiction is a journey, and relapses can happen. Dont get discouraged; seek help and keep working toward recovery.']),
    (r'(.*) (leave my addiction|leave addiction |leave alcohol|quit alcohol|leave drinking|quit drinking| leave drugs|quit drugs|quit smoking|leave smoking)(.*)', ['Acknowledge the problem. Seek professional help, such as therapy or counseling. Join a support group. Remove triggers and temptations. Develop a support system. Set clear, achievable goals for quitting. Replace addiction with healthy habits and activities. Stay committed to your recovery plan. Practice self-compassion and patience. Consider inpatient or outpatient treatment if necessary. Reach out to loved ones for support. Stay accountable through regular check-ins with a counselor or sponsor. Remember, quitting addiction is a journey, and relapses can happen. Dont get discouraged; seek help and keep working toward recovery.']),
    (r'(.*) (leave my addiction|leave addiction |leave alcohol|quit alcohol|leave drinking|quit drinking| leave drugs|quit drugs|quit smoking|leave smoking)', ['Acknowledge the problem. Seek professional help, such as therapy or counseling. Join a support group. Remove triggers and temptations. Develop a support system. Set clear, achievable goals for quitting. Replace addiction with healthy habits and activities. Stay committed to your recovery plan. Practice self-compassion and patience. Consider inpatient or outpatient treatment if necessary. Reach out to loved ones for support. Stay accountable through regular check-ins with a counselor or sponsor. Remember, quitting addiction is a journey, and relapses can happen. Dont get discouraged; seek help and keep working toward recovery.']),
    (r'(leave my addiction|leave addiction |leave alcohol|quit alcohol|leave drinking|quit drinking| leave drugs|quit drugs|quit smoking|leave smoking)(.*)', ['Acknowledge the problem. Seek professional help, such as therapy or counseling. Join a support group. Remove triggers and temptations. Develop a support system. Set clear, achievable goals for quitting. Replace addiction with healthy habits and activities. Stay committed to your recovery plan. Practice self-compassion and patience. Consider inpatient or outpatient treatment if necessary. Reach out to loved ones for support. Stay accountable through regular check-ins with a counselor or sponsor. Remember, quitting addiction is a journey, and relapses can happen. Dont get discouraged; seek help and keep working toward recovery.']),

    (r'(.*) (addiction)', ['Sometimes addiction is harmful so please take care']),
    (r'(.*) (alcohol|drinking|durg|durgs|smoking)', ['this will harmful for your body and will affect your body system so please overcome pro']),
    (r'(.*) (ADHD)', ['ADHD stands for Attention-Deficit/Hyperactivity Disorder. It is a neurodevelopmental disorder that affects both children and adults.']),
    (r'(.*) (Prodrome)', ['A prodrome is an early or initial set of signs and symptoms that precede the full onset of a medical condition or disease. In the context of mental health, it can refer to the early warning signs or symptoms that precede a more acute phase of a mental health disorder. ']),
    (r'(.*) (trust|trust anyone)',['Trust is an expensive emotion not everyone can earn it.']),


    (r'(.*)(treatment of insomia|insomia treatment|treatment of sleep|sleep treatment|treatment of not rest| treatment for restlessness) (.*)',['Treatment for insomnia can vary depending on its underlying causes and severity. It important to consult a healthcare professional for a proper evaluation and personalized treatment plan. Here are some common approaches to treating insomnia 1. Lifestyle and Behavioral Changes:- Sleep hygiene: Maintain a regular sleep schedule, create a comfortable sleep environment, and avoid stimulating activities before bedtime.- Cognitive-behavioral therapy for insomnia (CBT-I): This therapeutic approach helps address the thoughts and behaviors that contribute to insomnia.2. Medications:- Over-the-counter (OTC) sleep aids: These may help with occasional insomnia, but should not be used regularly.- Prescription medications: Your doctor may prescribe sleep medications for short-term use. These include benzodiazepines, non-benzodiazepine sedative-hypnotics, and melatonin receptor agonists.3. Addressing Underlying Conditions- If insomnia is a symptom of an underlying medical or psychiatric condition (e.g., depression, anxiety, sleep apnea), treating the primary condition can help alleviate insomnia.4. Relaxation Techniques:- Relaxation exercises, such as progressive muscle relaxation and deep breathing, can help reduce anxiety and promote better sleep.5. Cognitive and Behavioral Therapies:- CBT-I, as mentioned earlier, can be highly effective for chronic insomnia. It involves identifying and changing thought patterns and behaviors that contribute to sleep problems.6. Mindfulness and Meditation:- Mindfulness meditation and other relaxation techniques can help calm the mind and promote better sleep.7. Light Therapy- Light therapy can be used to regulate your circadian rhythm and improve sleep-wake patterns, especially for conditions like seasonal affective disorder.8. Herbal Supplements:- Some people find relief from insomnia with herbal remedies like valerian root, chamomile, or melatonin. Consult a healthcare provider before using any supplements.9. Avoid Stimulants:- Avoid caffeine, nicotine, and alcohol close to bedtime, as they can interfere with sleep.10. Physical Activity:- Regular exercise can improve sleep quality, but avoid vigorous exercise close to bedtime. It essential to work with a healthcare provider to determine the most appropriate treatment for your specific insomnia symptoms. They can help you identify the underlying causes and tailor a treatment plan to your needs. Also, remember that establishing good sleep habits and maintaining a healthy lifestyle are crucial for managing insomnia in the long term. ']),
    (r'(.*)(treatment of insomia|insomia treatment|treatment of sleep|sleep treatment|treatment of not rest| treatment for restlessness)',['Treatment for insomnia can vary depending on its underlying causes and severity. It important to consult a healthcare professional for a proper evaluation and personalized treatment plan. Here are some common approaches to treating insomnia 1. Lifestyle and Behavioral Changes:- Sleep hygiene: Maintain a regular sleep schedule, create a comfortable sleep environment, and avoid stimulating activities before bedtime.- Cognitive-behavioral therapy for insomnia (CBT-I): This therapeutic approach helps address the thoughts and behaviors that contribute to insomnia.2. Medications:- Over-the-counter (OTC) sleep aids: These may help with occasional insomnia, but should not be used regularly.- Prescription medications: Your doctor may prescribe sleep medications for short-term use. These include benzodiazepines, non-benzodiazepine sedative-hypnotics, and melatonin receptor agonists.3. Addressing Underlying Conditions- If insomnia is a symptom of an underlying medical or psychiatric condition (e.g., depression, anxiety, sleep apnea), treating the primary condition can help alleviate insomnia.4. Relaxation Techniques:- Relaxation exercises, such as progressive muscle relaxation and deep breathing, can help reduce anxiety and promote better sleep.5. Cognitive and Behavioral Therapies:- CBT-I, as mentioned earlier, can be highly effective for chronic insomnia. It involves identifying and changing thought patterns and behaviors that contribute to sleep problems.6. Mindfulness and Meditation:- Mindfulness meditation and other relaxation techniques can help calm the mind and promote better sleep.7. Light Therapy- Light therapy can be used to regulate your circadian rhythm and improve sleep-wake patterns, especially for conditions like seasonal affective disorder.8. Herbal Supplements:- Some people find relief from insomnia with herbal remedies like valerian root, chamomile, or melatonin. Consult a healthcare provider before using any supplements.9. Avoid Stimulants:- Avoid caffeine, nicotine, and alcohol close to bedtime, as they can interfere with sleep.10. Physical Activity:- Regular exercise can improve sleep quality, but avoid vigorous exercise close to bedtime. It essential to work with a healthcare provider to determine the most appropriate treatment for your specific insomnia symptoms. They can help you identify the underlying causes and tailor a treatment plan to your needs. Also, remember that establishing good sleep habits and maintaining a healthy lifestyle are crucial for managing insomnia in the long term. ']),

    (r'(treatment of insomia|insomia treatment|treatment of sleep|sleep treatment|treatment of not rest| treatment for restlessness) (.*)',['Treatment for insomnia can vary depending on its underlying causes and severity. It important to consult a healthcare professional for a proper evaluation and personalized treatment plan. Here are some common approaches to treating insomnia 1. Lifestyle and Behavioral Changes:- Sleep hygiene: Maintain a regular sleep schedule, create a comfortable sleep environment, and avoid stimulating activities before bedtime.- Cognitive-behavioral therapy for insomnia (CBT-I): This therapeutic approach helps address the thoughts and behaviors that contribute to insomnia.2. Medications:- Over-the-counter (OTC) sleep aids: These may help with occasional insomnia, but should not be used regularly.- Prescription medications: Your doctor may prescribe sleep medications for short-term use. These include benzodiazepines, non-benzodiazepine sedative-hypnotics, and melatonin receptor agonists.3. Addressing Underlying Conditions- If insomnia is a symptom of an underlying medical or psychiatric condition (e.g., depression, anxiety, sleep apnea), treating the primary condition can help alleviate insomnia.4. Relaxation Techniques:- Relaxation exercises, such as progressive muscle relaxation and deep breathing, can help reduce anxiety and promote better sleep.5. Cognitive and Behavioral Therapies:- CBT-I, as mentioned earlier, can be highly effective for chronic insomnia. It involves identifying and changing thought patterns and behaviors that contribute to sleep problems.6. Mindfulness and Meditation:- Mindfulness meditation and other relaxation techniques can help calm the mind and promote better sleep.7. Light Therapy- Light therapy can be used to regulate your circadian rhythm and improve sleep-wake patterns, especially for conditions like seasonal affective disorder.8. Herbal Supplements:- Some people find relief from insomnia with herbal remedies like valerian root, chamomile, or melatonin. Consult a healthcare provider before using any supplements.9. Avoid Stimulants:- Avoid caffeine, nicotine, and alcohol close to bedtime, as they can interfere with sleep.10. Physical Activity:- Regular exercise can improve sleep quality, but avoid vigorous exercise close to bedtime. It essential to work with a healthcare provider to determine the most appropriate treatment for your specific insomnia symptoms. They can help you identify the underlying causes and tailor a treatment plan to your needs. Also, remember that establishing good sleep habits and maintaining a healthy lifestyle are crucial for managing insomnia in the long term. ']),
    (r'(.*) (insomia|sleep|not rest)',['Insomnia is a common sleep disorder characterized by difficulty falling asleep, staying asleep, or experiencing poor-quality sleep, despite having the opportunity for sufficient sleep. ']),

    #lets add some more

    (r'(.*) (relations| relationship| friends| family| bond| vibes)(.*)', ['Remember that no relationship is perfect, and its normal to face challenges. The key is to work together with them to overcome those challenges and grow . Communication, respect, and understanding are your best tools for building a strong, healthy relation be that any.']),
    (r'(.*) (relations| relationship| friends| family| bond| vibes)', ['Remember that no relationship is perfect, and its normal to face challenges. The key is to work together with them to overcome those challenges and grow . Communication, respect, and understanding are your best tools for building a strong, healthy relation be that any.']),
    (r'(relations| relationship| friends| family| bond| vibes)(.*)', ['Remember that no relationship is perfect, and its normal to face challenges. The key is to work together with them to overcome those challenges and grow . Communication, respect, and understanding are your best tools for building a strong, healthy relation be that any.']),
    (r'(relations| relationship| friends| family| bond| vibes)', ['Remember that no relationship is perfect, and its normal to face challenges. The key is to work together with them to overcome those challenges and grow . Communication, respect, and understanding are your best tools for building a strong, healthy relation be that any.']),


    (r'(.*) (grief |loss| pain |finance | sadness| tension)(.*)', ['listen its perfectly okay to have a human such problem, you can tell me the exact problem ']),
    (r'(.*) (grief |loss| pain |finance | sadness| tension)', ['listen its perfectly okay to have a human such problem, you can tell me the exact problem ']),
    (r'(grief |loss| pain |finance | sadness| tension)(.*)', ['listen its perfectly okay to have a human such problem, you can tell me the exact problem ']),
    (r'(grief |loss| pain |finance | sadness| tension)', ['listen its perfectly okay to have a human such problem, you can tell me the exact problem ']),





    (r'(how are you)', ['as fine as your beautiful inner self']),
    #(r'(.*) (treatment of insomia|insommia treatment|sleep treatment|treatment of sleep  |not rest treatment| treatment of not rest)',['Establish a Consistent Sleep Schedule: Setting a consistent sleep routine is fundamental. Try going to bed and waking up at the same time every day, even on weekends. This routine helps regulate your body internal clock, making it easier to fall asleep and wake up naturally.Create a Relaxing Bedtime Routine: Prior to bedtime, engage in calming activities that signal your body to wind down. Reading a book, taking a warm bath, or practicing relaxation exercises can help prepare your mind and body for sleep. Steer clear of stimulating activities such as watching TV or using electronic devices, as these can disrupt the transition into sleep.Optimize Your Sleep Environment: Design your bedroom to be a sleep-friendly environment. Keep the room dark, quiet, and at a comfortable temperature. Investing in a comfortable mattress and pillows can significantly impact your sleep quality.Mindfulness and Stress Reduction: Incorporate relaxation techniques into your evening routine. Methods such as meditation, deep breathing exercises, or mindfulness practices can reduce stress and anxiety, making it easier to relax before bedtime.Regular Exercise: Engaging in regular physical activity during the day can promote better sleep. However, avoid exercising too close to bedtime, as it can have a stimulating effect that may interfere with falling asleep.Limit Stimulants and Screen Time: Cut back on stimulants like caffeine and nicotine close to bedtime, as they can hinder your ability to sleep. Additionally, reduce screen time an hour before bed as the blue light emitted by screens can disrupt the production of the sleep-inducing hormone melatonin.Consult a Healthcare Professional: If insomnia persists and significantly impacts your daily life, seek advice from a healthcare professional or sleep specialist. They can identify underlying causes and suggest suitable treatments, which might include therapy, medication, or cognitive-behavioral techniques aimed at improving sleep quality.Evaluate Your Diet: Assess your diet to avoid heavy meals and excessive liquids close to bedtime. Certain foods and drinks, like herbal teas or foods rich in tryptophan, may aid in promoting sleep.Remember, the effectiveness of these strategies may vary for each individual. Its crucial to find a personalized approach that works best for you. Seeking professional advice and making healthy lifestyle adjustments can greatly assist in managing insomnia. ']),
    (r'(.*)',['Sorry i can not understand please describe in proper way'])

    
]

# Create the chatbot
chatbot = Chat(patterns, reflections)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define a route to handle user input and get responses
@app.route('/get_response', methods=['POST'])
def get_response():
    
    user_input = request.data
    user_input=literal_eval(user_input.decode('utf-8'))
    
    response = chatbot.respond(user_input['user_input'])
    return jsonify({'response': response})

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

    # Check if the user exists in the MongoDB collection
#     user = mongo.db.users.find_one({'username': username, 'password': password})

#     if user:
#         return jsonify({'message': 'Login successful'})
#     else:
#         return jsonify({'message': 'Login failed'})
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the user already exists in the MongoDB collection
    existing_user = mongo.db.users.find_one({'username': username})

    if existing_user:
        return jsonify({'message': 'User already exists'})

    # If the user doesn't exist, create a new user in the MongoDB collection
    user_id = mongo.db.budget.budget.insert_one({'username': username, 'password': password})

    if user_id:
        return jsonify({'message': 'Signup successful'})
    else:
        return jsonify({'message': 'Signup failed'})
    

if __name__ == '__main__':
    app.run(debug=True)
