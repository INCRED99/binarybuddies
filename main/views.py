from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Footprint, Quote
import json
import random
import numpy as np
from django.utils import timezone
from .models import Streak
from datetime import timedelta
import logging
from django.shortcuts import render, redirect
import csv
import os
from django.shortcuts import render
from .models import UserScore
from django.conf import settings
from fastai.tabular.all import *

# Configure logging
logger = logging.getLogger(__name__)

# Landing page view
def landing_page(request):
    return render(request, 'landing.html')


# def pole_page(request):
#     return render(request, 'pole.html')


# Community page view
def community_page(request):
    return render(request, 'community.html')

# Home page view
# def home_page(request):
#     quotes = Quote.objects.all()
#     if quotes.exists():
#         random_quote = random.choice(quotes)
#     else:
#         random_quote = None

#     return render(request, 'home.html', {'random_quote': random_quote})

def home_page(request):
    # Load a random quote
    quotes = Quote.objects.all()
    if quotes.exists():
        random_quote = random.choice(quotes)
    else:
        random_quote = None

    # Default streak count (1 for first-time visit)
    streak = 1

    # Check if the request method is POST
    if request.method == 'POST':
        username = request.POST.get('username') or "Guest"
        try:
            user_score = UserScore.objects.get(username=username)
        except UserScore.DoesNotExist:
            user_score = UserScore(username=username)
            user_score.streak_count = 1  # Start streak from 1
            user_score.last_visit = timezone.now().date()
            user_score.save()
        else:
            today = timezone.now().date()

            # Display current streak first
            streak = user_score.streak_count

            if user_score.last_visit:
                delta = today - user_score.last_visit
                if delta.days == 1:
                    user_score.streak_count += 1  # Increment streak
                elif delta.days > 1:
                    user_score.streak_count = 1  # Reset streak if gap

            user_score.last_visit = today
            user_score.save()

    else:
        # For GET requests, default to "Guest" streak
        user_score = UserScore.objects.filter(username="Guest").first()
        streak = user_score.streak_count if user_score else 1

    return render(request, 'home.html', {
        'random_quote': random_quote,
        'streak': streak,
    })


# Stats page view
def stats_page(request):
    return render(request, 'stats.html')

# Quiz page view
def quiz_page(request):
    return render(request, 'quiz.html')

# Reset database
def reset_data(request):
    Footprint.objects.all().delete()
    return redirect('home')

# Prediction logic
@csrf_exempt
def predict(request):
    if request.method == 'POST':
        # Get form data
        electricity = float(request.POST.get('electricity', 0))
        car_km = float(request.POST.get('car_km', 0))
        meat_meals = float(request.POST.get('meat_meals', 0))
        flights = float(request.POST.get('flights', 0))

        # Calculate footprint score
        score = (electricity * 0.5) + (car_km * 0.3) + (meat_meals * 2) + (flights * 5)

        # Save to database
        footprint = Footprint.objects.create(
            electricity=electricity,
            car_km=car_km,
            meat_meals=meat_meals,
            flights=flights,
            score=score
        )

        # Get all past scores
        all_scores = Footprint.objects.values_list('score', flat=True)
        avg_score = sum(all_scores) / len(all_scores)
        previous_scores = list(all_scores)[:-1]
        previous_score = previous_scores[-1] if previous_scores else None

        # Determine recommendation
        if score < 10:
            recommendation = "Excellent! Keep it up!"
        elif score < 20:
            recommendation = "Good, but there is room for improvement."
        else:
            recommendation = "Try to reduce your footprint!"

        # Determine improvement status
        if previous_score is not None:
            if score < previous_score:
                comparison = "Good job! Your footprint has improved compared to your last calculation."
            elif score > previous_score:
                comparison = "Your footprint has increased since the last calculation."
            else:
                comparison = "Your footprint score is the same as your last calculation."
        else:
            comparison = "This is your first calculation!"

        return render(request, 'home.html', {
            'score': round(score, 2),
            'recommendation': recommendation,
            'average_score': round(avg_score, 2),
            'comparison': comparison
        })

    return render(request, 'home.html')




# Chatbot view (handle POST requests)
@csrf_exempt  # Disable CSRF protection for the chatbot endpoint (temporary for testing)
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Get the message from the request body
        user_message = data.get('message', '').lower()  # Extract and normalize the message to lowercase

        # Dictionary for chatbot responses
        responses = {
            'hello': "Hi there! How can I help you today?",
            'hi': "Hello! How can I assist you?",
                'default': "I'm sorry, I didn't quite understand that. Could you please rephrase your question?",
        }

        # Simple chatbot logic: check the message for keywords
        for key in responses:
            if key in user_message:
                reply = responses[key]
                break
        else:
            # If no keyword matches, default reply
            reply = responses['default']

        return JsonResponse({'reply': reply})  # Send the reply back to the frontend

    return JsonResponse({'reply': 'Invalid request method.'}, status=400)


def load_questions():
    """Loads questions from a CSV file."""
    questions = []
    file_path = os.path.join(settings.BASE_DIR, 'quiz_questions.csv')
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                questions.append({
                    'question': row['question'],
                    'option1': row['option1'],
                    'option2': row['option2'],
                    'option3': row['option3'],
                    'option4': row['option4'],
                    'correct_option': row['correct_option'],
                })
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:
        print(f"Error reading questions: {e}")
    return questions

questions = load_questions()
total_questions = len(questions)

def quiz_view(request):
    
    if total_questions == 0:
        return render(request, 'quiz.html', {'error': 'No questions available.'})

    # Get current index from POST or default to 0
    current_question_index = int(request.POST.get('current_question_index', 0))
    action = request.POST.get('action', 'next')

    if request.method == 'GET':
        current_question_index = 0

    elif request.method == 'POST':
        if action == 'next':
            current_question_index = min(current_question_index + 1, total_questions - 1)
        elif action == 'prev':
            current_question_index = max(current_question_index - 1, 0)
        elif action == 'submit':
            username = request.POST.get('username', 'Anonymous')
            score = 0
            for index, question in enumerate(questions):
                selected = request.POST.get(f'question_{index}')
                correct_answer = question['correct_option']
                if selected == correct_answer:
                    score += 1

            UserScore.objects.create(username=username, score=score, total=total_questions)

            past_scores = UserScore.objects.filter(username=username)
            others_scores = UserScore.objects.exclude(username=username)

            if score == total_questions:
                recommendation = "Excellent! You're an eco-champion!"
            elif score > total_questions / 2:
                recommendation = "Good job! Keep learning to improve even more."
            else:
                recommendation = "Don't worry! Check out our resources to improve your eco-knowledge."

            return render(request, 'quiz.html', {
                'submitted': True,
                'score': score,
                'total': total_questions,
                'past_scores': past_scores,
                'others_scores': others_scores,
                'recommendation': recommendation,
            })

    # Render current question
    current_question = questions[current_question_index]
    progress = ((current_question_index ) / total_questions) * 100

    return render(request, 'quiz.html', {
        'submitted': False,
        'question_number': current_question_index +1,
        'total_questions': total_questions,
        'current_question': current_question,
        'progress': progress,
    })

def load_random_quote():
    csv_path = os.path.join(settings.BASE_DIR, 'recommendations.csv')  # adjust to your CSV name
    quotes = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            quotes = [row[0] for row in reader if row]  # Assuming single column CSV
    except FileNotFoundError:
        quotes = ["No recommendations found."]

    return random.choice(quotes) if quotes else "Stay eco-friendly!"


def home(request):
    random_quote = load_random_quote()

    streak = 1  # Default streak count

    if request.method == 'POST':
        username = request.POST.get('username') or "Guest"
        try:
            user_score = UserScore.objects.get(username=username)
        except UserScore.DoesNotExist:
            user_score = UserScore(username=username)
            user_score.streak_count = 1  # Start streak from 1
            user_score.last_visit = timezone.now().date()
            user_score.save()
        else:
            today = timezone.now().date()

            # Display current streak first
            streak = user_score.streak_count

            if user_score.last_visit:
                delta = today - user_score.last_visit
                if delta.days == 1:
                    user_score.streak_count += 1
                elif delta.days > 1:
                    user_score.streak_count = 1  # Reset streak if gap

            user_score.last_visit = today
            user_score.save()

    else:
        # Default: Look up the streak for Guest user
        user_score = UserScore.objects.filter(username="Guest").first()
        streak = user_score.streak_count if user_score else 1

    return render(request, 'home.html', {
        'random_quote': random_quote,
        'streak': streak,
    })

    return render(request, 'poll.html', {'forms': forms, 'results': results})









#  'landing page': "You can visit our landing page for more information at [Insert Landing Page URL].",
#            'home page': "You can explore our home page here: [Insert Home Page URL].",
#                 'hot wheels': "Hot Wheels are an exciting collection of miniature cars and toys! Let me know if you'd like to learn more.",
#                 'flame car': "The flame car is a special design in our Hot Wheels collection! It can be found on the right side of our website.",
#                 'contact': "You can contact us via the contact form on our home page or email us at contact@project.com.",
#                 'help': "I'm here to assist you! You can ask about our landing page, home page, Hot Wheels, or general information.",
#                 'thank you': "You're welcome! Feel free to ask anything else.",
#                 'where is the website located': "Our website is hosted online, and you can access it from anywhere in the world. Just visit [Insert Website URL].",
#                 'what is hot wheels': "Hot Wheels are a brand of die-cast toy cars created by Mattel. They are known for their high speed and exciting designs.",
#                 'can i buy hot wheels online': "Yes! You can buy Hot Wheels from various online retailers like Amazon, Walmart, or the official Hot Wheels website.",
#                 'how do i contact support': "To contact our support team, you can use the contact form on the website or email us directly at support@project.com.",
#                 'what is the project about': "This project is dedicated to showcasing the exciting world of Hot Wheels, including detailed pages, collections, and more.",
#                 'how to use the website': "To use our website, simply navigate through the pages to explore the different sections. If you're looking for Hot Wheels cars, check out the products page!",
#                 'can you help me with a problem': "I'd be happy to help! Please describe the issue you're facing, and I'll do my best to assist.",
#                 'ok': "Do you have any other question?",
#                 'what is eco shift': "ECO SHIFT is a platform dedicated to helping you calculate your carbon footprint and providing personalized suggestions to reduce your environmental impact. We offer tools, community support, and educational resources to help you live more sustainably.",
#                 'how to calculate carbon footprint': "To calculate your carbon footprint on our website, go to the Dashboard section and click on 'Carbon Calculator'. You'll need to answer questions about your energy usage, transportation habits, diet, and consumption patterns. Our tool will then generate a detailed report of your carbon footprint with suggestions for improvement.",
#                 'what is a carbon footprint': "A carbon footprint is the total amount of greenhouse gases (including carbon dioxide and methane) that are generated by our actions. This includes activities like driving, electricity usage, food consumption, and product purchases. Our calculator helps you measure and understand your personal impact.",
#                 'how can i reduce my carbon footprint': "There are many ways to reduce your carbon footprint! Some effective strategies include: using public transportation or carpooling, reducing meat consumption, minimizing food waste, using energy-efficient appliances, and reducing overall consumption. Check out our 'Challenges' section for guided activities to lower your impact.",
#                 'what is the streak feature': "The Streak feature helps you build sustainable habits by tracking consecutive days of eco-friendly actions. Each day you complete an eco-challenge or log a green activity, your streak increases. Maintaining longer streaks earns you achievements and rewards on our platform!",
#                 'tell me about eco facts': "Our 'Eco Facts' section provides daily interesting and educational information about environmental issues and sustainability. Each fact is researched and verified by our team to help you learn something new about our planet every day.",
#                 'how do quizzes work': "Our quizzes and polls are interactive ways to test your knowledge about environmental topics and participate in community discussions. New quizzes are posted weekly in the Quiz/Polls section. Completing quizzes earns you points that contribute to your profile achievements.",
#                 'what challenges are available': "We offer various eco-challenges ranging from beginner to advanced levels. These include 'Meatless Monday', 'Zero-Waste Week', 'Local Shopping Month', and 'Energy Saving Challenge'. Visit the Challenges section to see all available options and join one that interests you!",
#                 'who are your partners': "We collaborate with leading environmental organizations and government agencies including Green Earth Alliance, Environmental Protection Department, Sustainable Future Initiative, Clean Ocean Foundation, Department of Conservation, and Renewable Energy Cooperative. Visit our Partners page to learn more about each organization.",
#                 'how can i contribute': "You can contribute to our mission by donating to our partner environmental organizations, volunteering for local initiatives, or participating in our community challenges. Visit the 'Contribute' section for detailed information on how to get involved.",
#                 'community features': "Our Community section allows you to connect with like-minded individuals, share your sustainability journey, participate in discussions, and join group challenges. You can also share tips and celebrate achievements with community members.",
#                 'login issues': "If you're experiencing login issues, try resetting your password through the 'Forgot Password' link on the login page. If problems persist, please contact our support team at support@ecoshift.com with details about the issue you're facing.",
#                 'transportation carbon impact': "Transportation typically accounts for a significant portion of personal carbon footprints. Cars, planes, and other fossil fuel-powered vehicles release CO2 directly into the atmosphere. Our calculator can help you understand your transportation impact and suggest alternatives like public transit, carpooling, biking, or electric vehicles.",
#                 'food carbon footprint': "Food production contributes to carbon emissions through farming, processing, transportation, and waste. Animal products generally have higher carbon footprints than plant-based foods. Our calculator analyzes your diet and suggests lower-impact food choices.",
#                 'energy saving tips': "To reduce your energy usage: switch to LED bulbs, unplug electronics when not in use, use a programmable thermostat, wash clothes in cold water, air-dry clothes when possible, and consider renewable energy options. Visit our Dashboard for personalized energy-saving recommendations.",
#                 'what are carbon offsets': "Carbon offsets are investments in environmental projects that reduce greenhouse gas emissions to compensate for emissions you can't avoid. These might include renewable energy, forest conservation, or methane capture projects. Our 'Contribute' section provides information on reputable offset programs.",
#                 'eco-friendly products': "Looking for sustainable products? Check out our recommended eco-friendly alternatives for everyday items in the Resources section. We feature products with minimal packaging, renewable materials, and ethical production practices.",
#                 'plant-based diet': "A plant-based diet significantly reduces your carbon footprint. Our calculator can show you the impact of different dietary choices, and our Resources section offers plant-based recipes and meal plans to help you transition.",
#                 'recycling information': "Proper recycling reduces waste and conserves resources. Visit our Resources section for detailed guides on what can be recycled in your area, how to prepare items for recycling, and creative ways to reuse materials before recycling.",
#                 'water conservation': "Water conservation reduces energy use and protects freshwater ecosystems. Our Dashboard provides personalized water-saving tips based on your household profile, and our Challenges section includes water conservation challenges.",