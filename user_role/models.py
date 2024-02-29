from django.db import models
from user.models import User
from role.models import Role
# Create your models here.
class UserRole(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'user_roles'
        verbose_name_plural = 'user_roles'
        db_table = "user_roles"