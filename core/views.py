from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
from django.shortcuts import render, redirect
from .interface import move_robot_safecast_linear
from . import core_main

def steuerung(request):
   message = ""
   if request.method == 'POST':
       if 'direction' in request.POST:
           direction = request.POST['direction']
           if not core_main.our_status.get_is_autonomous():
               move_robot_safecast_linear(direction) #TODO call from other thread?
               core_main.our_status.set_message(f"Bewegung: {direction}")
           else:
               core_main.our_status.set_message("Autonomer Modus aktiviert. Manuelle Steuerung deaktiviert.")
       if 'autonomous' in request.POST:
           core_main.our_status.set_is_autonomous(not core_main.our_status.get_is_autonomous())
           core_main.our_status.set_message("Modus geändert")
   status = core_main.get_system_status()  #todo move dict conversion into get_status / remove double keys.
    
   return render(request, 'steuerung.html',json.loads(status.to_json()))

def get_status(request):
    status = core_main.get_system_status()
    return JsonResponse(json.loads(status.to_json()), safe=False)