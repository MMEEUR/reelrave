from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProflieAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'comments_count')
    ordering = ('user',)
    search_fields = ('user',)
    
    def comments_count(self, obj):
        return obj.user_comments.count()
    comments_count.short_description = 'Comments'