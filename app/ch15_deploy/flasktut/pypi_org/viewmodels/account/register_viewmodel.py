from pypi_org.services import user_service
from pypi_org.viewmodels.shared.viewmodelbase import ViewModelBase


class RegisterViewModel(ViewModelBase):
    def __init__(self):
        super().__init__()
        self.name: str = self.request_dict.name
        self.email: str = self.request_dict.email.lower().strip()
        self.password: str = self.request_dict.password.strip()
        self.age: str = self.request_dict.age.strip()

    def validate(self):

        # Basic face-value validation
        if not self.name or not self.name.strip():
            self.error = 'You must specify a name'
        elif not self.email or not self.email.strip():
            self.error = 'Email required'
        elif not self.password:
            self.error = 'You must set a password'
        elif len(self.password) < 5:
            self.error = 'Your password must be at least 5 characters long'
        # Deeper validation wrt database
        elif user_service.find_user_by_email(self.email):
            self.error = 'A user with that email already exists.'
