from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
from django.shortcuts import render, redirect
from .interface import move_robot_safecast_linear
from . import core_main

autonomous = False
def steuerung(request):
   global autonomous
   message = ""
   if request.method == 'POST':
       if 'direction' in request.POST:
           direction = request.POST['direction']
           if not autonomous:
               move_robot_safecast_linear(direction) #TODO call from other thread?
               message = f"Bewegung: {direction}"
           else:
               message = "Autonomer Modus aktiviert. Manuelle Steuerung deaktiviert."
       if 'autonomous' in request.POST:
           autonomous = not autonomous
           core_main.autonomous_mode_enabled = autonomous
           message = "Modus geändert"
   status =  core_main.get_system_status()#todo move dict conversion into get_status / remove double keys.
    
   return render(request, 'steuerung.html',json.loads(status))

def get_status(request): 
    
    return JsonResponse(json.loads(core_main.get_system_status()), safe=False)