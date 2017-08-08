from django.contrib import admin
from assessproject import models
# Register your models here.

class DataAdmin(admin.ModelAdmin):
    list_display=('pk','Assessmenttype','level','Requirement','datatype')

admin.site.register(models.Data_table,DataAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display=('username','nickname','generatetime',)

admin.site.register(models.User_table,UserAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display=('projectname','generatetime',)
admin.site.register(models.Project_table,ProjectAdmin)

class AssessmentAdmin(admin.ModelAdmin):
    list_display=('username','project')
admin.site.register(models.Assessment_table,AssessmentAdmin)

class AssessmentAdmin(admin.ModelAdmin):
    list_display=('username',)
admin.site.register(models.File_table,AssessmentAdmin)

