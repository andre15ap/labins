
from django.contrib.auth.backends import ModelBackend as BaseModelBackend

# from django.contrib.auth import get_user_model
from .models import User
# from django.contrib.auth.models import User


class ModelBackend(BaseModelBackend):

	def authenticate(self, request, username=None, password=None):
		# print('------------------ enrou ')
		if not username is None:
			print('--------------nao é none')

			# userModel = get_user_model
			try:
				user = User.objects.get(username=username)
				if user.check_password(password):
					return user
			except User.DoesNotExist:
				# print('======== entrou no except')
				pass
		