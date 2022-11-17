from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse , JsonResponse

# Create your views here.

def home(request):
    return render(request, "home.html")

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)

    return render(request, "room.html", {
        'username':username,
        'room': room,
        'room_details': room_details,
    })

def checkview(request):
    # checking the room entererd nby the user and creating a new room if needed source = home.html
    room = request.POST["room_name"]
    username = request.POST["username"]

    if Room.objects.filter(name=room).exists():
        # redirecting the user if the room exists
        return redirect("/"+room+"/?username="+username)
    
    # creating a new room if it doesnt
    new_room = Room.objects.create(name=room)
    new_room.save()
    return redirect("/"+room+"/?username="+username)

def send(request):
    # getting the message detalis from the form in room . html page
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    # creating a new message obj and saving it'

    new_message = Message.objects.create(value=message, user=username, room = room_id)
    new_message.save()

    return HttpResponse("Message sent successfully")

def getMessages(request, room):

    # displaying the messages in real time to the user in room.html
    # getting details from room html
    room_details = Room.objects.get(name=room)

    # getting message content related to that room usong room details/id

    messages = Message.objects.filter(room=room_details.id)

    return JsonResponse({"messages":list(messages.values())})


