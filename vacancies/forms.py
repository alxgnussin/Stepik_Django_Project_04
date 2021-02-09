from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

from django.contrib.auth.password_validation import validate_password

from django.forms import Form, CharField, ValidationError, PasswordInput, ImageField, IntegerField, Textarea


class RegisterForm(Form):
    username = CharField(min_length=3, max_length=20, label='Логин')
    first_name = CharField(max_length=20, label='Имя')
    last_name = CharField(max_length=20, label='Фамилия')
    password = CharField(widget=PasswordInput, label='Пароль')
    confirm = CharField(widget=PasswordInput, label='Проверка')

    def clean_confirm(self):
        p1 = self.cleaned_data['password']
        p2 = self.cleaned_data['confirm']

        if p1 != p2:
            raise ValidationError('Пароли должны совпадать.', code='password_mismatch')

        validate_password(p1)

        return p2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class='float-right'))
        # включаем стили
        self.helper.form_class = "container form-horizontal mt-5"
        self.helper.label_class = "col-sm-3 col-form-label"
        self.helper.field_class = "col-lg-9"


class LoginForm(Form):
    username = CharField(min_length=3, max_length=20, label='Логин')
    password = CharField(widget=PasswordInput)


class CompanyForm(Form):
    title = CharField(max_length=20, label='Название компании')
    location = CharField(max_length=20, label='География')
    logo = ImageField(label='Загрузить новый логотип', required=False)
    description = CharField(widget=Textarea(attrs={'rows': 4}), label='Информация о компании')
    employee_count = IntegerField(label='Количество человек в компании')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить', css_class='float-right'))

        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('logo', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('employee_count', css_class='form-group col-md-6 mb-0'),
                Column('location', css_class='form-group col-md-6 mb-0'),
            ),
            'description'
        )


class ApplicationForm(Form):
    written_username = CharField(max_length=20, label='Вас зовут')
    written_phone = CharField(max_length=20, label='Ваш телефон')
    written_cover_letter = CharField(widget=Textarea(attrs={'rows': 4}), label='Сопроводительное письмо')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Записаться на собеседование', css_class='float-right'))

        self.helper.layout = Layout(
            'written_username',
            'written_phone',
            'written_cover_letter'
        )
