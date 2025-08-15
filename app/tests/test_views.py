from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from models import crimeModel
from datetime import datetime
from forms import filterForm, dataForm
from unittest.mock import patch

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')  # Make sure your URL name is set
        self.create_plot_url = reverse('create_plot')  # Same here
        self.test_crime = crimeModel.objects.create(
            date='2023-06-15 12:00:00',
            latitude=49.20678,
            longitude=-122.91092,
            address="123 Test St",
            city="NEW WESTMINSTER",
            incident="THEFT"
        )


    def test_home_get_request(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIsInstance(response.context['form'], filterForm)
        self.assertIn('map', response.context)

    def test_home_post_valid_form_all_crimes(self):
        post_data = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'crime': 'ALL'
        }
        response = self.client.post(self.home_url, data=post_data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Increasing date windows" in str(m) for m in messages))
        self.assertIn('map', response.context)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_post_with_specific_crime(self):
        post_data = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'crime': 'THEFT'
        }
        response = self.client.post(self.home_url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    @patch('app.views.plot_cv_metric', return_value='<img src="mocked_plot3.png">')
    @patch('app.views.plot_crime_rate_trends', return_value='<img src="mocked_plot2.png">')
    @patch('app.views.plot_crime_rate', return_value='<img src="mocked_plot1.png">')
    @patch('app.views.process_functions', return_value=['<img src="mocked_plot1.png">', '<img src="mocked_plot2.png">'])
    @patch('app.views.set_up_model')

    def test_create_plot_with_all_graphs_mocked(
        self, mock_setup_model, mock_process, mock_plot1, mock_plot2, mock_plot3
    ):
        post_data = {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'crime': 'ALL',
            'graph_options': ['option1', 'option2']
        }

        response = self.client.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'graphs.html')

        # Check that the mocked plots were used
        self.assertTrue(response.context['chart'])
        self.assertIn('graph1', response.context)
        self.assertIn('<img src="mocked_plot1.png">', response.context['graph1'])

        self.assertIn('graph2', response.context)
        self.assertIn('<img src="mocked_plot2.png">', response.context['graph2'])

        # Confirm that the mocked functions were called
        mock_setup_model.assert_called_once()
        mock_process.assert_called_once()
        mock_plot1.assert_called_once()
        mock_plot2.assert_called_once()
        mock_plot3.assert_not_called()  # option3 not selected

        # Check message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Increasing date windows" in str(m) for m in messages))