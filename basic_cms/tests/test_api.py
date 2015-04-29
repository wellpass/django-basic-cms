"""Django page CMS functionnal tests suite module."""
from basic_cms.models import Page
from basic_cms.tests.testcase import TestCase

import json
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse


class CMSPagesApiTests(TestCase):

    fixtures = ['api.json']

    def setUp(self):
        self.original_data = Page.objects.from_path('terms', 'eng')
        self.original_json_data = json.dumps(self.original_data.dump_json_data())
        self.original_html_data = render_to_string(self.original_data.template,
                                                   {"current_page": self.original_data})

    def tests_basic_cms_api_access(self):
        data = {
            'format': 'json'
        }
        response = self.client.get(reverse('basic_cms_api', args=['alamakota']), data)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('basic_cms_api', args=['terms']), data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(self.original_json_data, response.content)

        response = self.client.get(reverse('basic_cms_api', args=['terms']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please read these Terms of Use', response.content)

        response = self.client.get(reverse('basic_cms_api', args=['coaches']), {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title']['eng'], 'coaches')
        self.assertEqual(len(response.data['children']), 3)
        self.assertEqual(response.data['children'][0]['title']['eng'], 'Judith Singer')
        self.assertEqual(response.data['children'][1]['title']['eng'], 'Melissa Litwak')
        self.assertEqual(response.data['children'][2]['title']['eng'], 'Joanna Schaffler')

    def test_urls(self):
        from nutrimom.accounts.api import links_append_domain

        body = """
            <a href="http://google.com">google.com</a>
            <a href="foo">foo</a>
            <a href="#a">#a</a>
            <a href="/#a">/#a</a>
            <img src="http://x.com/x.jpg"/>
            <img src="a.jpg"/>
        """
        return_body = """
            <a href="http://google.com">google.com</a>
            <a href="http://a.com/foo">foo</a>
            <a href="#a">#a</a>
            <a href="/#a">/#a</a>
            <img src="http://x.com/x.jpg"/>
            <img src="http://a.com/a.jpg"/>
        """
        self.assertIn(return_body.strip(), links_append_domain(body, 'http://a.com'))