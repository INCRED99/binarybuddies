from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Landing page view
def landing_page(request):
    return render(request, 'landing.html')

# Home page view
def home_page(request):
    return render(request, 'home.html')

def stats_page(request):
    return render(request, 'stats.html')

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
            'landing page': "You can visit our landing page for more information at [Insert Landing Page URL].",
            'home page': "You can explore our home page here: [Insert Home Page URL].",
            'hot wheels': "Hot Wheels are an exciting collection of miniature cars and toys! Let me know if you'd like to learn more.",
            'flame car': "The flame car is a special design in our Hot Wheels collection! It can be found on the right side of our website.",
            'contact': "You can contact us via the contact form on our home page or email us at contact@project.com.",
            'help': "I'm here to assist you! You can ask about our landing page, home page, Hot Wheels, or general information.",
            'thank you': "You're welcome! Feel free to ask anything else.",
            'where is the website located': "Our website is hosted online, and you can access it from anywhere in the world. Just visit [Insert Website URL].",
            'what is hot wheels': "Hot Wheels are a brand of die-cast toy cars created by Mattel. They are known for their high speed and exciting designs.",
            'can i buy hot wheels online': "Yes! You can buy Hot Wheels from various online retailers like Amazon, Walmart, or the official Hot Wheels website.",
            'how do i contact support': "To contact our support team, you can use the contact form on the website or email us directly at support@project.com.",
            'what is the project about': "This project is dedicated to showcasing the exciting world of Hot Wheels, including detailed pages, collections, and more.",
            'how to use the website': "To use our website, simply navigate through the pages to explore the different sections. If you're looking for Hot Wheels cars, check out the products page!",
            'can you help me with a problem': "I'd be happy to help! Please describe the issue you're facing, and I'll do my best to assist.",
            'default': "I'm sorry, I didn't quite understand that. Could you please rephrase your question?",
            'ok': "Do you have any other question?"
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
