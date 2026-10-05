from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.test import override_settings


class ContactFormTests(TestCase):
    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CONTACT_EMAIL='baronecodificando@gmail.com',
    )
    def test_valid_contact_message_is_emailed(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'Ana',
            'email': 'ana@example.com',
            'subject': 'Consulta de proyecto',
            'message': 'Quisiera conversar sobre una aplicación web.',
        })

        self.assertRedirects(response, f"{reverse('core:index')}#contacto", fetch_redirect_response=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['baronecodificando@gmail.com'])
        self.assertEqual(mail.outbox[0].reply_to, ['ana@example.com'])
        self.assertIn('Mensaje de Ana <ana@example.com>', mail.outbox[0].body)

    def test_invalid_contact_message_is_not_emailed(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'Ana',
            'email': 'correo-invalido',
            'subject': 'Consulta',
            'message': 'Hola',
        })

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context['contact_form'].errors['email'])
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_subject_cannot_contain_newlines(self):
        response = self.client.post(reverse('core:contact'), {
            'name': 'Ana',
            'email': 'ana@example.com',
            'subject': 'Consulta\nBcc: atacante@example.com',
            'message': 'Hola',
        })

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'El asunto debe ocupar una sola línea.', status_code=400)
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_page_includes_form(self):
        response = self.client.get(reverse('core:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'baronecodificando@gmail.com')
        self.assertContains(response, 'Enviar mensaje')

    def test_learning_area_is_promoted_outside_the_navigation(self):
        response = self.client.get(reverse('core:index'))

        self.assertContains(response, 'Explorar espacio de cursos')
        self.assertContains(response, '/admin/login/?next=/cursos/')
        navigation = response.content.decode().split('</nav>', 1)[0]
        self.assertNotIn('Cursos</a>', navigation)
        self.assertIn('href="#aprendizaje"', navigation)
        self.assertContains(response, 'Aprende conmigo.')

    def test_projects_section_has_prominent_heading(self):
        response = self.client.get(reverse('core:index'))

        self.assertContains(response, 'Proyectos que convierten ideas en soluciones.')
        self.assertContains(response, 'href="#proyectos"')

    def test_home_navigation_scrolls_to_page_top_without_reloading(self):
        response = self.client.get(reverse('core:index'))
        navigation = response.content.decode().split('</nav>', 1)[0]

        self.assertIn('id="inicio"', response.content.decode())
        self.assertEqual(navigation.count('href="#inicio"'), 2)
