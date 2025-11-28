from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):

        if not email:
            raise ValueError("Staff must have an email address")
        if not phone:
            raise ValueError("Staff must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):

        user = self.create_user(
            email,
            password=password,
            name=name,
            phone=phone,
        )
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
