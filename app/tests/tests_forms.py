from django.test import TestCase
from forms import filterForm, dataForm


class filterFormTest(TestCase):
    def test_valid_form_with_all_fields(self):
        data = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'crime': 'THEFT',
        }
        form = filterForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['crime'], 'THEFT')

    def test_valid_form_without_end_date(self):
        data = {
            'start_date': '2023-01-01',
            'crime': 'ARSON'
        }
        form = filterForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data['end_date'])

    def test_invalid_form_missing_start_date(self):
        data = {
            'end_date': '2023-12-31',
            'crime': 'ROBBERY'
        }
        form = filterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors)

    def test_invalid_date_format(self):
        data = {
            'start_date': '01-01-2023',  # Wrong format (should be YYYY-MM-DD)
            'end_date': '2023-12-31',
            'crime': 'FRAUD'
        }
        form = filterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('start_date', form.errors)

    def test_optional_crime_field(self):
        data = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
        }
        form = filterForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['crime'], 'ALL' if 'ALL' in dict(form.fields['crime'].choices) else None)

    def test_invalid_choice_in_crime_field(self):
        data = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'crime': 'INVALID_CRIME'
        }
        form = filterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('crime', form.errors)