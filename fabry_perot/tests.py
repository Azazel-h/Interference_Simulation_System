from django.test import TestCase, Client
from django.urls import reverse


class TestPage(TestCase):
    def assert_generates(self, data, code, content=None):
        url = reverse('index') + 'update-graph/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, code)
        if content:
            self.assertEqual(response.content, content)

    def get_data(self, **kwargs):
        data = self.basic_data.copy()
        data.update(kwargs)
        return data

    def setUp(self):
        self.basic_data = {
            "wave_length": "630",
            "glasses_distance": "15",
            "focal_distance": "100",
            "stroke_difference": "0",
            "reflectivity": "0.7",
            "refractive_index": "1",
            "picture_size": "5",
            "N": "500"
        }
        self.client = Client()

    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/fabry-perot.html')

    def test_interferometer_generation(self):
        request_data = self.get_data()

        self.assert_generates(request_data, 200)

    def test_interferometer_generation_with_wrong_wavelength(self):
        request_data = self.get_data(wave_length=1000)
        self.assert_generates(request_data, 200, b'None')

        request_data = self.get_data(wave_length=0)
        self.assert_generates(request_data, 200, b'None')

    def test_interferometer_generation_with_wrong_glasses_distance(self):
        request_data = self.get_data(glasses_distance=-1)
        self.assert_generates(request_data, 200, b'None')

    def test_interferometer_generation_with_wrong_focal_distance(self):
        request_data = self.get_data(focal_distance=-1)
        self.assert_generates(request_data, 200, b'None')

    def test_interferometer_generation_with_wrong_stroke_difference(self):
        request_data = self.get_data(stroke_difference=-1)
        self.assert_generates(request_data, 200, b'None')

    def test_interferometer_generation_with_wrong_picture_size(self):
        request_data = self.get_data(picture_size=-1)
        self.assert_generates(request_data, 200, b'None')

    def test_interferometer_generation_with_wrong_N(self):
        request_data = self.get_data(N=-1)
        self.assert_generates(request_data, 200, b'None')

        # N more than 4000
        request_data = self.get_data(N=4001)
        self.assert_generates(request_data, 200, b'None')

    def test_interferometer_generation_with_wrong_reflectivity(self):
        request_data = self.get_data(reflectivity=-1)
        self.assert_generates(request_data, 200, b'None')

        request_data = self.get_data(reflectivity=1.5)
        self.assert_generates(request_data, 200, b'None')

    def test_interferometer_generation_with_wrong_refractive_index(self):
        request_data = self.get_data(refractive_index=-1)
        self.assert_generates(request_data, 200, b'None')
