from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Candidate, Position, Voter, Vote
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required




# Create your views here.
@login_required(login_url='login_view')
def home(request):
    return render(request, 'base/home.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'user does not exist')
            return redirect('login_view')
        elif user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
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
    if request.method == 'POST':
        # Get the voter or create one if they don't exist
        voter, created = Voter.objects.get_or_create(user=request.user)

        # Iterate through the POST data to find selected candidates for each position
        for key, value in request.POST.items():
            if key.startswith('position_'):
                position_id = key.split('_')[1]  # Extract position ID from the key
                candidate_id = value  # Selected candidate ID

                # Ensure the candidate and position exist
                position = get_object_or_404(Position, id=position_id)
                candidate = get_object_or_404(Candidate, id=candidate_id)

                # Check if the voter has already voted for this position
                if Vote.objects.filter(voter=voter, position=position).exists():
                    messages.error(request, f"You have already voted.")
                    return redirect('vote')

                # Create a new vote
                Vote.objects.create(voter=voter, position=position, candidate=candidate)

        messages.error(request, "Your votes have been submitted successfully!")
        return redirect('voted')

    # Fetch all positions and their candidates
    positions = Position.objects.prefetch_related('candidates').all()
    context = {'positions': positions}
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
    positions = Position.objects.all()
    context = {'positions': positions}
    return render(request, 'base/seats.html', context)



@login_required(login_url='login_view')
def position_details(request, position_id):
    # Fetch the position and its candidates
    position = get_object_or_404(Position, id=position_id)
    candidates = position.candidates.all()
    context = {'position': position, 'candidates': candidates}
    return render(request, 'base/position_details.html', context)



def voting_status(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        
        try:
            # Check if the user exists in the Voter model
            voter = Voter.objects.get(user__id=user_id)
            
            # Check if the user has voted for any position
            has_voted = Vote.objects.filter(voter=voter).exists()
            
            if has_voted:
                status = "Voted"
            else:
                status = "Not Voted"
        except Voter.DoesNotExist:
            # If the user does not exist, they haven't voted
            status = "Not Voted"
        
        return render(request, 'base/status.html', {'status': status, 'user_id': user_id})
    
    return render(request, 'base/status.html')




# def vote(request):
#     if request.method == 'POST':
        
#         position_id = request.POST.get('position')
#         candidate_id = request.POST.get('candidate')

#         if not position_id or not candidate_id:
#             messages.error(request, "Please select a candidate for the position.")
#             return redirect('vote')

        
#         voter = Voter.objects.filter(user=request.user).first()
#         if not voter:
#             voter = Voter.objects.create(user=request.user)

        
#         if Vote.objects.filter(voter=voter, position_id=position_id).exists():
#             messages.error(request, "You have already voted for this position.")
#             return redirect('vote')

        
#         position = get_object_or_404(Position, id=position_id)
#         candidate = get_object_or_404(Candidate, id=candidate_id)
#         Vote.objects.create(voter=voter, position=position, candidate=candidate)

#         messages.success(request, f"Vote for {position.name} submitted successfully!")
#         return redirect('voted')

    
#     positions = Position.objects.prefetch_related('candidates').all()
#     context = {'positions': positions}
#     return render(request, 'base/vote.html', context)










# def vote(request):
#     if request.method == 'POST':
#         candidate_id = request.POST.get('candidate')
#         if not candidate_id:
#             messages.error(request, "No candidate selected.")
#             return redirect('vote')

#         position = get_object_or_404(Candidate, id=candidate_id)
#         voter, created = Voter.objects.get_or_create(user=request.user)
        
        
#         if voter.candidate:
#             messages.error(request, "You have already voted.")
#             return redirect('vote')
        
        
#         voter.position = position
#         voter.save()
        
#         messages.success(request, "Vote submitted successfully!")
#         return redirect('voted')  

#     candidates = Candidate.objects.all()
#     positions = Position.objects.all()
#     context = {'candidates': candidates, 'positions':positions}
#     return render(request, 'base/vote.html', context)


# def vote(request):
#     if request.method == 'POST':
#         president_id = request.POST.get('president')
#         vice_president_id = request.POST.get('vice_president')
        
#         if president_id:
#             president = Candidate.objects.get(id=president_id)
            
#             voter = Voter.objects.get(user=request.user)
#             voter.selected_president = president
#             voter.save()
        
#         if vice_president_id:
#             vice_president = Candidate.objects.get(id=vice_president_id)
            
#             voter = Voter.objects.get(user=request.user)
#             voter.selected_vice_president = vice_president
#             voter.save()

#         if voter.candidate:
#             messages.error(request, "You have already voted.")
#             return redirect('vote')
        
#         messages.success(request, "Vote submitted successfully!")
#         return redirect('voted')  

#     candidates = Candidate.objects.all()
#     context = {'candidates': candidates}
#     return render(request, 'base/vote.html', context)