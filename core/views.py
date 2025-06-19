from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .robot_control import get_status, set_autonomous_mode
from .interface import move_robot_safecast
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
           set_autonomous_mode(autonomous)
           message = "Modus geändert"
   status = get_status()
   return render(request, 'steuerung.html', {
       'trash_detected': status['trash_detected'],
       'distance': status['distance'],
       'battery_level': status['battery_level'],
       'is_autonomous': autonomous,
       'message': message
   })