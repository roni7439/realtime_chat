from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from .models import *
from django.db.models import Q

@login_required(login_url='login_page2')
def chatbox(request):
    chat_group=get_object_or_404(ChatGroup,group_name='mmcc')
    chat_massages=chat_group.chat_massages.all()
    all_user=User.objects.all()
    if request.method=='POST':
        text=request.POST.get('text_info')
        if text: 
          GroupMassage.objects.create(
            group=chat_group,
            author=request.user,
            body=text
        )      
        return redirect('chatbox1')
    return render(request,'chatbox1.html',{'chat_massages': chat_massages,'all_user':all_user})



def logout_view(request):
    logout(request)
    return redirect('login_page2')


# @login_required
# def private_chat(request, username):
#     other_user = get_object_or_404(User, username=username)
#     if request.method == "POST":
#         body = request.POST.get("text_info")
#         PrivetMassage.objects.create(
#             sender=request.user, 
#             receiver=other_user,
#             body=body
#             )
#         return redirect("private_chat", username=other_user.username)

#     messages = PrivetMassage.objects.filter(
#         Q(sender=request.user, receiver=other_user) |
#         Q(sender=other_user, receiver=request.user)
#     ).order_by("time")

#     all_user = User.objects.exclude(username=request.user.username)
#     room_name = f"private_{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}"

    
#     return render(request, "chatbox1.html", {
#         "user": request.user,
#         "other_user": other_user,
#         "messages": messages,
#         "all_user": all_user,
#         "room_name":room_name,
#     })


#updated form views is

@login_required
def private_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    # All chat messages between the two users
    messages = PrivetMassage.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by("time")

    all_user = User.objects.exclude(username=request.user.username)

    # Room name based on user IDs
    room_name = f"private_{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}"

    return render(request, "chatbox1.html", {
        "user": request.user,
        "other_user": other_user,
        "messages": messages,
        "all_user": all_user,
        "room_name": room_name,
    })
