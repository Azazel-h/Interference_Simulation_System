from django.test import TestCase, Client
from django.urls import reverse


class TestPage(TestCase):
    def assert_updates_graph(self, data, code, content=None):
        url = reverse('fp-index') + 'graph/'
        response = self.client.post(url, data, 'application/json')
        self.assertEqual(response.status_code, code)

        if content:
            self.assertEqual(response.content, content)

    def assert_saves_preset(self, data, code, content=None):
        data['preset_operation'] = 'save_preset'
        url = reverse('fp-index') + 'preset/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, code)

        if content:
            self.assertContains(response, content)

    def assert_deletes_preset(self, preset_id, code, content=None):
        data = {
            'delete_preset': preset_id,
            'preset_operation': 'delete_preset'
        }
        url = reverse('fp-index') + 'preset/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, code)

        if content:
            self.assertContains(response, content)

    def assert_update_history(self, data, code, content=None):
        url = reverse('fp-index') + 'history/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, code)

        if content:
            self.assertContains(response, content)

    def get_data(self, **kwargs):
        data = self.basic_data.copy()
        data.update(kwargs)

        return data

    def setUp(self):
        self.basic_data = {
            'wave_length': '630',
            'wave_length_diff': '0',
            'glasses_distance': '15',
            'focal_distance': '100',
            'reflection_coefficient': '0.7',
            'refractive_index': '1',
            'picture_size': '5',
            'N': '500'
        }
        self.client = Client()

    def test_index_page(self):
        url = reverse('fp-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_interferometer_generation(self):
        request_data = self.get_data()
        self.assert_updates_graph(request_data, 200)

    def test_interferometer_generation_with_wrong_wavelength(self):
        request_data = self.get_data(wave_length=1000)
        self.assert_updates_graph(request_data, 200, None)

        request_data = self.get_data(wave_length=0)
        self.assert_updates_graph(request_data, 200, None)

    def test_interferometer_generation_with_wrong_wave_length_diff(self):
        request_data = self.get_data(wave_length_diff=-1)
        self.assert_updates_graph(request_data, 200, None)

    def test_interferometer_generation_with_wrong_glasses_distance(self):
        request_data = self.get_data(glasses_distance=-1)
        self.assert_updates_graph(request_data, 200, None)

    def test_interferometer_generation_with_wrong_focal_distance(self):
        request_data = self.get_data(focal_distance=-1)
        self.assert_updates_graph(request_data, 200, None)

    def test_interferometer_generation_with_wrong_reflectivity(self):
        request_data = self.get_data(reflection_coefficient=-1)
        self.assert_updates_graph(request_data, 200, None)

        request_data = self.get_data(reflection_coefficient=1.5)
        self.assert_updates_graph(request_data, 200, None)

    def test_interferometer_generation_with_wrong_refractive_index(self):
        request_data = self.get_data(refractive_index=-1)
        self.assert_updates_graph(request_data, 200, None)

    def test_interferometer_generation_with_wrong_picture_size(self):
        request_data = self.get_data(picture_size=-1)
        self.assert_updates_graph(request_data, 200, None)

    def test_interferometer_generation_with_wrong_n(self):
        # N less than 0
        request_data = self.get_data(N=-1)
        self.assert_updates_graph(request_data, 200, None)

        # N more than 1000
        request_data = self.get_data(N=1001)
        self.assert_updates_graph(request_data, 200, None)
