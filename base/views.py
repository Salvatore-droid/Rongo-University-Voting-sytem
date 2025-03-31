from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Candidate, SchoolPosition, Voter, Vote, School
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models





# Create your views here.
@login_required(login_url='login_view')
def home(request):
    return render(request, 'base/home.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('school_selection')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_view')

    return render(request, 'base/login.html')



def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not email:
            messages.error(request, "email is required.")
            return redirect("register")
        
        if not username:
            messages.error(request, "registration number is required.")
            return redirect("register")


        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Student with that registration number already exists, continue to login.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        Voter.objects.create(user=user)
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login_view")

    return render(request, "base/register.html")

    
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')


@login_required(login_url='login_view')
def voted(request):
    return render(request, 'base/voted.html')




@login_required(login_url='login_view')
def vote(request):
    # Get the voter's selected school
    voter = Voter.objects.filter(user=request.user).first()
    if not voter or not voter.school:
        messages.error(request, "You must select a school before voting.")
        return redirect('school_selection')

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('position_'):
                position_id = key.split('_')[1]  
                candidate_id = value 

                
                position = get_object_or_404(SchoolPosition, id=position_id)
                candidate = get_object_or_404(Candidate, id=candidate_id)

                
                if Vote.objects.filter(voter=voter, position=position).exists():
                    messages.error(request, f"You have already voted.")
                    return redirect('vote')

                
                Vote.objects.create(voter=voter, position=position, candidate=candidate)

        messages.success(request, "Your votes have been submitted successfully!")
        return redirect('voted')

    # Fetch positions that have candidates in the voter's school
    positions = SchoolPosition.objects.filter(
        candidates__school=voter.school
    ).distinct().prefetch_related(
        models.Prefetch('candidates', queryset=Candidate.objects.filter(school=voter.school))
    )
    
    context = {
        'positions': positions,
        'voter': voter,
    }
    return render(request, 'base/vote.html', context)




@login_required(login_url='login_view')
def review(request):
    voter = Voter.objects.filter(user=request.user).first()
    votes = Vote.objects.filter(voter=voter).select_related('position', 'candidate')
    context = {'votes': votes}
    return render(request, 'base/review.html', context)

@login_required(login_url='login_view')
def positions_list(request):
    # Fetch all positions
    positions = SchoolPosition.objects.all()
    context = {'positions': positions}
    return render(request, 'base/seats.html', context)



@login_required(login_url='login_view')
def position_details(request, position_id):
    # Fetch the position and its candidates
    position = get_object_or_404(Position, id=position_id)
    candidates = position.candidates.all()
    context = {'position': position, 'candidates': candidates}
    return render(request, 'base/position_details.html', context)


@login_required(login_url='login_view')
def voting_status(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        try:
            # Check if the user exists in the User model
            user = User.objects.get(username=username)
            
            # Check if the user exists in the Voter model
            voter = Voter.objects.get(user=user)
            
            # Check if the user has voted for any position
            has_voted = Vote.objects.filter(voter=voter).exists()
            
            if has_voted:
                status = "Voted"
            else:
                status = "Not Voted"
        except User.DoesNotExist:
            # If the user does not exist, they haven't voted
            status = "Not Voted"
        except Voter.DoesNotExist:
            # If the user is not a voter, they haven't voted
            status = "Not Voted"
        
        return render(request, 'base/status.html', {'status': status, 'username': username})
    
    return render(request, 'base/status.html')




@login_required(login_url='login_view')
def spoiled_votes(request):
    # Define spoiled votes
    spoiled_votes = Vote.objects.filter(
        models.Q(candidate__isnull=True) |  # Votes with no candidate
        models.Q(position__isnull=True)     # Votes with no position
    )

    # Add logic to detect multiple votes by the same voter for the same position
    # (Optional, depending on your requirements)

    context = {
        'spoiled_votes': spoiled_votes,
    }
    return render(request, 'base/spoiled_votes.html', context)


@login_required(login_url='login_view')
def school_selection(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to access this page.")
        return redirect('login')

    username = request.user.username

    if request.method == 'POST':
        selected_school_id = request.POST.get('school')
        selected_school = get_object_or_404(School, id=selected_school_id)

        # Check if the username matches any of the school's registration formats
        if any(username.startswith(prefix) for prefix in selected_school.get_formats()):
            # Save the selected school in the Voter model
            voter, created = Voter.objects.get_or_create(user=request.user)
            voter.school = selected_school
            voter.save()

            messages.success(request, f"You have successfully selected the {selected_school.name}.")
            return redirect('home')
        else:
            messages.error(request, "You are not registered in the selected school. Please choose a different school.")
            return redirect('school_selection')

    schools = School.objects.all()
    return render(request, 'base/school.html', {'schools': schools})








