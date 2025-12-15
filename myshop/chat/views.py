from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required
from .models  import ChatMessage

@csrf_exempt
def chatbot_api(request):
    if request.method!='POST':
        return JsonResponse({"error":"Invalid request"},status=400)
    try:
        data=json.loads(request.body)
        user_msg=data.get("message","").strip()
        if not user_msg:
            return JsonResponse({"reply": "Please type something."})
        reply = "Thanks for your message. Our assistant will help you shortly."
        ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            message=user_msg,
            response=reply
        )
        return JsonResponse({"reply": reply})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def chatbot_test_page(request):
    return render(request, "chatbot/test.html")
