from django.contrib import admin
from django.utils.html import format_html 
from .models import *


admin.site.site_header = 'RU Voting Admin panel'
admin.site.site_title = 'Rongo University Voting Admin panel'
admin.site.index_title = 'Welcome to Voting System Admin'



# Customize the School model display
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_formats')  # Columns to display in the list view
    search_fields = ('name',)  # Add a search bar for the 'name' field
    list_filter = ('name',)  # Add filters for the 'name' field

    # Customize the display of registration formats
    def get_formats(self, obj):
        return ", ".join(obj.get_formats())
    get_formats.short_description = 'Registration Formats'  # Column header

# Customize the Candidate model display
@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'display_image')  # Columns to display
    search_fields = ('name', 'school__name')  # Search by name or school name
    list_filter = ('school',)  # Filter by school

    # Add a preview of the image in the admin
    def display_image(self, obj):
        if obj.imageURL:  # Use the imageURL property
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit:cover;" />', obj.imageURL)
        return "No Image"

    display_image.short_description = 'Image'  # Column header for list view

# Customize the Position model display
@admin.register(SchoolPosition)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'candidates_list')  # Columns to display
    search_fields = ('name',)  # Search by name
    filter_horizontal = ('candidates',)  # Use a horizontal filter for many-to-many fields

    # Display a list of candidates for the position
    def candidates_list(self, obj):
        return ", ".join([candidate.name for candidate in obj.candidates.all()])
    candidates_list.short_description = 'Candidates'

# Customize the Voter model display
@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'candidate')  # Columns to display
    search_fields = ('user__username', 'school__name', 'candidate__name')  # Search by username, school, or candidate
    list_filter = ('school', 'candidate')  # Filter by school or candidate

# Customize the Vote model display
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'position', 'candidate', 'vote_time')  # Columns to display
    search_fields = ('voter__user__username', 'position__name', 'candidate__name')  # Search by voter, position, or candidate
    list_filter = ('position', 'candidate')  # Filter by position or candidate

    # Add a custom field to display the vote time (if you have a timestamp field)
    def vote_time(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(obj, 'timestamp') else "N/A"
    vote_time.short_description = 'Vote Time'

