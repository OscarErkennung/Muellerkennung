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
               message = f"Bewegung: {direction}"
           else:
               message = "Autonomer Modus aktiviert. Manuelle Steuerung deaktiviert."
       if 'autonomous' in request.POST:
           autonomous = not autonomous
           message = "Modus geändert"
           core_main.our_status.set_is_autonomous(True if autonomous=="on" else False)

   status =  core_main.get_system_status()#todo move dict conversion into get_status / remove double keys.
    
   return render(request, 'steuerung.html',json.loads(status.to_json()))

def get_status(request):
    status = core_main.get_system_status()
    return JsonResponse(json.loads(status.to_json()), safe=False)