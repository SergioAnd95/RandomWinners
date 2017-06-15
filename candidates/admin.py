from django.contrib import admin
from .models import Candidate, GroupCandidates
# Register your models here.


class CandidateAdmin(admin.StackedInline):
    model = Candidate


@admin.register(GroupCandidates)
class GroupCandidatesAdmin(admin.ModelAdmin):
    inlines = [
        CandidateAdmin,
    ]

    readonly_fields = ('pk', 'when_created')