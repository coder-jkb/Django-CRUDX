import random
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import ToDo

def get_tasks(request, new_task=None):

    id = User.objects.get(
            username=request.user.username).id
    
    task_list = list(ToDo.objects.filter(user=id))

    if new_task is not None:
        task_list.append(new_task)

    return task_list

def home(request):
    return render(request,'crudx/welcome.html')

def create(request):
    context = { 'user': User,
                'username':request.user.username,
                'tasks': []}
    context['firstname'] = User.objects.get(username = context['username']).first_name,
                
    task_list = get_tasks(request)

    context['tasks'] = task_list
    if request.method == 'POST':
        # get todo data
        title = request.POST['title']
        hrs = request.POST['hrs']
        min = request.POST['min']
        deadline = request.POST['deadline']
        color = request.POST['color']

        # Create object of ToDo table
        new_task = ToDo()
        new_task.info=title
        if hrs != '':
            new_task.duration_hrs = hrs 
        if min != '':
            new_task.duration_min = min 
        if deadline != '':    
            new_task.duedate = deadline 
            
        new_task.status = 0
        new_task.color = color
        new_task.user = request.user

        # save into database
        new_task.save()
        
        # add this data in context
        context['tasks'].append(new_task)

        messages.success(request,"Successfully inserted the task!")

        return redirect('crud')

def update(request, pk):
    if request.method == 'POST':
        # get the data
        title = request.POST['title']
        hrs = request.POST['hrs']
        min = request.POST['min']
        deadline = request.POST['deadline']


        color = request.POST['color'] 
        if 'status' in request.POST:
            status = True
        else:
            status = False

        task = ToDo.objects.get(id=pk) # create object
        task.info = title
        task.duration_hrs = hrs
        task.duration_min = min
        task.duedate = deadline
        task.status = status
        task.color = color
        # task.update(info=title, duration_hrs=hrs,  
        #             duration_min=min, duedate=deadline, 
        #             status=int(status), color=color) # run update query

        task.save() # save in DB

        messages.success(request,"Successfully updated the task!")
        return redirect('crud')
    else:
        return HttpResponse("<h1 align=\"center\" >Error 404 - Page not found.</h1>")        

def delete(request, pk):
    if request.method == 'POST':    
        todo = ToDo.objects.get(id=pk)
        todo.delete()
        messages.info(request, "Task deleted successfully")
        return redirect('crud')
    else:
        return HttpResponse("<h1 align=\"center\" >Error 404 - Page not found.</h1>")

    '''
    if request.method == 'POST':    
        # try:
        # print(request.POST.get('id-to-del', False))
        id = int(request.POST.get('id-to-del', False))
        id = int(request.POST['id-to-del'])
        row = ToDo.objects.filter(id=id)
        row.delete()
        messages.info(request, "Task deleted successfully")
        # except Exception as err:
            # DANGER = 50
            # messages.add_message(request, DANGER, err, extra_tags='danger')
        return redirect('crud')
        # return redirect("home")
    else:
        return HttpResponse("<h1 align=\"center\" >Error 404 - Page not found.</h1>")
    '''
 
def crud(request):
    data = { 'user': User,
                'username':request.user.username,
                'tasks': []
                }
    data['firstname'] = User.objects.get(username=data['username']).first_name
    
    task_list = get_tasks(request)
    data['tasks'] = task_list

    # messages.success(request,"Successfully inserted the task!") 
    return render(request,'crudx/crud.html',data)    

def signup(request):
    if request.method == 'POST':
        # get the post parameters
        fname = request.POST['fname']
        lname = request.POST['lname']

        # unique username generated is first char of fname, lname and a 3 digit random number
        while True:
            temp_uname = fname[0]+lname[0]+str(random.randint(100,999))
            exists = User.objects.filter(username=temp_uname).exists()
            if not exists:
                username = temp_uname
                break

        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # form validation
        if pass1 != pass2:
            # messages.error(request, "Confirm Password must be same as the first one.")
            '''
            --- Existing---
            Levels 	 Values
            DEBUG	    10
            INFO	    20
            SUCCESS	    25
            WARNING	    30
            ERROR	    40
            ---  new  ---
            DANGER      50
            '''
            DANGER = 50
            messages.add_message(request, DANGER, 'Confirm Password must be same as the first one.', extra_tags='danger')
            return redirect('home')

        # Put values in the DB create the user 
        newuser = User.objects.create_user(username, email, pass1)
        newuser.first_name = fname
        newuser.last_name = lname
        newuser.save()
        messages.success(request, "Signed up sucessfully!")
        return redirect('home')
    else:
        return HttpResponse("<h1 align=\"center\" >Error 404 - Page not found.</h1>")

def loginuser(request):
    if request.method == 'POST':
        email = request.POST['login_email']
        password = request.POST['login_pass']      

        exists = User.objects.filter(email=email).exists()
        # row = User.objects.get(email=email)

        # new message level (refer signup function for more details)
        DANGER = 50
        if exists:
            username = User.objects.get(email=email).username
        else:
            messages.add_message(request, DANGER, 'User doesnot exist! Please signup first', extra_tags='danger')
            return redirect('home')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"Successfully logged in!")
            context = { 'user': User,
                        'username':username,
                        'firstname': User.objects.get(username=username).first_name,
                      }

            return redirect('crud')
        else:
            messages.add_message(request, DANGER, 'Error! Invalid email id or password! Please try again', extra_tags='danger')
            return redirect('home')
    else:
        return HttpResponse("<h1 align=\"center\" >Error 404 - Page not found.</h1>")

def logoutuser(request):
    if request.method == 'POST':
        messages.warning(request,"Successfully logged out!")
        logout(request)
        return redirect('home') 

    else:
        return HttpResponse("<h1 align=\"center\" >Error 404 - Page not found.</h1>")