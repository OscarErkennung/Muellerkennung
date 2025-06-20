from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render, redirect
from .robot_control import get_system_status, set_autonomous_mode
from .interface import move_robot_safecast
from . import core_main

autonomous = False
def steuerung(request):
   global autonomous
   message = ""
   if request.method == 'POST':
       if 'direction' in request.POST:
           direction = request.POST['direction']
           if not autonomous:
               move_robot_safecast(direction)
               message = f"Bewegung: {direction}"
           else:
               message = "Autonomer Modus aktiviert. Manuelle Steuerung deaktiviert."
       if 'autonomous' in request.POST:
           autonomous = not autonomous
           core_main.autonomous_mode_enabled = autonomous
           message = "Modus geändert"
   status = get_system_status() #todo move dict conversion into get_status / remove double keys.
   return render(request, 'steuerung.html', {
       'trash_detected': status['trash_detected'],
       'distance': status['distance'],
       'battery_level': status['battery_level'],
       'is_autonomous': status['is_autonomous'],
       'message': status['message'],
        'total': status['total']
   })

def get_status(request): 

    return JsonResponse({})