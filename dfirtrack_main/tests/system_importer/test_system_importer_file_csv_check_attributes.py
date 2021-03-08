from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv import system_cron
from dfirtrack_main.models import Analysisstatus, Ip, System, Systemstatus
from dfirtrack_main.tests.system_importer.config_functions import change_csv_import_filename
from mock import patch
import os
import urllib.parse


class SystemImporterFileCsvCheckAttributesViewTestCase(TestCase):
    """ system importer file CSV view tests """

    @classmethod
    def setUpTestData(cls):
        """ one-time setup """

        """ create objects """

        # create users
        test_user = User.objects.create_user(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        User.objects.create_user(username='message_user', password='POPKkir2A2biti52AYJG')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        """ set config with fixed values """

        # build local path with test files
        csv_import_path = os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/')

        # set fixed config values
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_headline = False
        system_importer_file_csv_config_model.csv_import_path = csv_import_path
        system_importer_file_csv_config_model.csv_import_username = test_user
        system_importer_file_csv_config_model.csv_default_systemstatus = systemstatus_1
        system_importer_file_csv_config_model.csv_default_analysisstatus = analysisstatus_1
        system_importer_file_csv_config_model.csv_default_tagfree_systemstatus = systemstatus_1
        system_importer_file_csv_config_model.csv_default_tagfree_analysisstatus = analysisstatus_1
        system_importer_file_csv_config_model.csv_tag_lock_systemstatus = 'LOCK_SYSTEMSTATUS'
        system_importer_file_csv_config_model.csv_tag_lock_analysisstatus = 'LOCK_ANALYSISSTATUS'
        system_importer_file_csv_config_model.csv_field_delimiter = 'field_comma'
        system_importer_file_csv_config_model.csv_text_quote = 'text_double_quotation_marks'
        system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_semicolon'
        system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'

        # save config
        system_importer_file_csv_config_model.save()

#    @classmethod
#    def setUp(cls):
#        """ setup in advance of every test """
#
#        """ clean non-mandatory values which may set by other tests """
#
#        # get config
#        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
#
#        # (re)set config values
#        system_importer_file_csv_config_model.csv_column_system = 1
#        system_importer_file_csv_config_model.csv_skip_existing_system = False
#        system_importer_file_csv_config_model.csv_remove_systemstatus = False
#        system_importer_file_csv_config_model.csv_remove_analysisstatus = False
#        system_importer_file_csv_config_model.csv_choice_tagfree_systemstatus = False
#        system_importer_file_csv_config_model.csv_choice_tagfree_analysisstatus = False
#        system_importer_file_csv_config_model.csv_choice_ip = False
#        system_importer_file_csv_config_model.csv_column_ip = None
#        system_importer_file_csv_config_model.csv_remove_ip = False
#        system_importer_file_csv_config_model.csv_choice_dnsname = False
#        system_importer_file_csv_config_model.csv_column_dnsname = None
#        system_importer_file_csv_config_model.csv_default_dnsname = None
#        system_importer_file_csv_config_model.csv_remove_dnsname = False
#        system_importer_file_csv_config_model.csv_choice_domain = False
#        system_importer_file_csv_config_model.csv_column_domain = None
#        system_importer_file_csv_config_model.csv_default_domain = None
#        system_importer_file_csv_config_model.csv_remove_domain = False
#        system_importer_file_csv_config_model.csv_choice_location = False
#        system_importer_file_csv_config_model.csv_column_location = None
#        system_importer_file_csv_config_model.csv_default_location = None
#        system_importer_file_csv_config_model.csv_remove_location = False
#        system_importer_file_csv_config_model.csv_choice_os = False
#        system_importer_file_csv_config_model.csv_column_os = None
#        system_importer_file_csv_config_model.csv_default_os = None
#        system_importer_file_csv_config_model.csv_remove_os = False
#        system_importer_file_csv_config_model.csv_choice_reason = False
#        system_importer_file_csv_config_model.csv_column_reason = None
#        system_importer_file_csv_config_model.csv_default_reason = None
#        system_importer_file_csv_config_model.csv_remove_reason = False
#        system_importer_file_csv_config_model.csv_choice_recommendation = False
#        system_importer_file_csv_config_model.csv_column_recommendation = None
#        system_importer_file_csv_config_model.csv_default_recommendation = None
#        system_importer_file_csv_config_model.csv_remove_recommendation = False
#        system_importer_file_csv_config_model.csv_choice_serviceprovider = False
#        system_importer_file_csv_config_model.csv_column_serviceprovider = None
#        system_importer_file_csv_config_model.csv_default_serviceprovider = None
#        system_importer_file_csv_config_model.csv_remove_serviceprovider = False
#        system_importer_file_csv_config_model.csv_choice_systemtype = False
#        system_importer_file_csv_config_model.csv_column_systemtype = None
#        system_importer_file_csv_config_model.csv_default_systemtype = None
#        system_importer_file_csv_config_model.csv_remove_systemtype = False
#        system_importer_file_csv_config_model.csv_choice_case = False
#        system_importer_file_csv_config_model.csv_column_case = None
#        system_importer_file_csv_config_model.csv_default_case.clear()
#        system_importer_file_csv_config_model.csv_remove_case = False
#        system_importer_file_csv_config_model.csv_choice_company = False
#        system_importer_file_csv_config_model.csv_column_company = None
#        system_importer_file_csv_config_model.csv_default_company.clear()
#        system_importer_file_csv_config_model.csv_remove_company = False
#        system_importer_file_csv_config_model.csv_choice_tag = False
#        system_importer_file_csv_config_model.csv_column_tag = None
#        system_importer_file_csv_config_model.csv_default_tag.clear()
#        system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
#        system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
#        system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
#
#        # save config
#        system_importer_file_csv_config_model.save()

    """ faulty system (system_name) """

    def test_system_importer_file_csv_check_attributes_cron_faulty_system(self):
        """ test importer view """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 2
        system_importer_file_csv_config_model.save()
        # set file system attributes
        csv_import_filename = 'system_importer_file_csv_testfile_31_faulty_system.csv'
        # change config
        change_csv_import_filename(csv_import_filename)

        # mock timezone.now()
        t_1 = datetime(2021, 3, 8, 18, 5, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_1):

            # execute cron job / scheduled task
            system_cron()

        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_attributes')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 3 | multiple: 0 [2021-03-08 18:05:00 - 2021-03-08 18:05:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 3 | multiple: 0 [2021-03-08 18:05:00 - 2021-03-08 18:05:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self.assertTrue(System.objects.filter(system_name='system_csv_31_001').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_31_003').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_31_006').exists())
        self.assertEqual(System.objects.get(system_name='system_csv_31_001').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_003').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_006').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_001').systemstatus, systemstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_003').systemstatus, systemstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_006').systemstatus, systemstatus_1)

    def test_system_importer_file_csv_check_attributes_instant_faulty_system(self):
        """ test importer view """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 2
        system_importer_file_csv_config_model.save()
        # set file system attributes
        csv_import_filename = 'system_importer_file_csv_testfile_31_faulty_system.csv'
        # change config
        change_csv_import_filename(csv_import_filename)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - messages / meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Value for system in row 2 was too long. System not created.')
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(messages[1].message, 'Value for system in row 4 was an empty string. System not created.')
        self.assertEqual(messages[1].level_tag, 'warning')
        self.assertEqual(messages[2].message, 'Index for system in row 5 was out of range. System not created.')
        self.assertEqual(messages[2].level_tag, 'warning')
        self.assertEqual(messages[3].message, '3 systems were created.')
        self.assertEqual(messages[3].level_tag, 'success')
        self.assertEqual(messages[4].message, '3 systems were skipped.')
        self.assertEqual(messages[4].level_tag, 'success')
        # compare - systems / attributes
        self.assertTrue(System.objects.filter(system_name='system_csv_31_001').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_31_003').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_31_006').exists())
        self.assertEqual(System.objects.get(system_name='system_csv_31_001').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_003').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_006').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_001').systemstatus, systemstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_003').systemstatus, systemstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_006').systemstatus, systemstatus_1)

    def test_system_importer_file_csv_check_attributes_upload_post_faulty_system(self):
        """ test importer view """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 2
        system_importer_file_csv_config_model.save()
        # set file system attributes
        csv_import_filename = 'system_importer_file_csv_testfile_31_faulty_system.csv'
        # change config
        change_csv_import_filename(csv_import_filename)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_31_faulty_system.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # get objects
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        systemstatus_1 = Systemstatus.objects.get(systemstatus_name='systemstatus_1')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - messages / meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Value for system in row 2 was too long. System not created.')
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(messages[1].message, 'Value for system in row 4 was an empty string. System not created.')
        self.assertEqual(messages[1].level_tag, 'warning')
        self.assertEqual(messages[2].message, 'Index for system in row 5 was out of range. System not created.')
        self.assertEqual(messages[2].level_tag, 'warning')
        self.assertEqual(messages[3].message, '3 systems were created.')
        self.assertEqual(messages[3].level_tag, 'success')
        self.assertEqual(messages[4].message, '3 systems were skipped.')
        self.assertEqual(messages[4].level_tag, 'success')
        # compare - systems / attributes
        self.assertTrue(System.objects.filter(system_name='system_csv_31_001').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_31_003').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_31_006').exists())
        self.assertEqual(System.objects.get(system_name='system_csv_31_001').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_003').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_006').analysisstatus, analysisstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_001').systemstatus, systemstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_003').systemstatus, systemstatus_1)
        self.assertEqual(System.objects.get(system_name='system_csv_31_006').systemstatus, systemstatus_1)
        # close file
        systemcsv.close()

    """ faulty ip (ip_ip) """

    def test_system_importer_file_csv_check_attributes_cron_faulty_ip(self):
        """ test importer view """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_choice_ip = True
        system_importer_file_csv_config_model.csv_column_ip = 2
        system_importer_file_csv_config_model.save()
        # set file system attributes
        csv_import_filename = 'system_importer_file_csv_testfile_32_faulty_ip.csv'
        # change config
        change_csv_import_filename(csv_import_filename)

        # mock timezone.now()
        t_2 = datetime(2021, 3, 8, 18, 10, tzinfo=timezone.utc)
        with patch.object(timezone, 'now', return_value=t_2):

            # execute cron job / scheduled task
            system_cron()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 1
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_check_attributes')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:10:00 - 2021-03-08 18:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # switch user context
        self.client.logout()
        self.client.login(username='message_user', password='POPKkir2A2biti52AYJG')
        # get response
        response = self.client.get('/system/')
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - user 2
        self.assertEqual(str(response.context['user']), 'message_user')
        self.assertEqual(messages[0].message, 'System CSV importer: created: 3 | updated: 0 | skipped: 0 | multiple: 0 [2021-03-08 18:10:00 - 2021-03-08 18:10:00]')
        self.assertEqual(messages[0].level_tag, 'success')
        # compare - systems / attributes
        self.assertTrue(System.objects.filter(system_name='system_csv_32_001').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_32_002').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_32_003').exists())
        self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.1').exists())
        self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.2').exists())
        # get object (for better readability)
        self.assertTrue(System.objects.filter(system_name='system_csv_32_001').exists())
        # compare - systems / attributes
        self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.1').exists())
        self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.2').exists())

    def test_system_importer_file_csv_check_attributes_instant_faulty_ip(self):
        """ test importer view """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_choice_ip = True
        system_importer_file_csv_config_model.csv_column_ip = 2
        system_importer_file_csv_config_model.save()
        # set file system attributes
        csv_import_filename = 'system_importer_file_csv_testfile_32_faulty_ip.csv'
        # change config
        change_csv_import_filename(csv_import_filename)

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/importer/file/csv/instant/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - messages / meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Value for ip address in row 2 was not a valid IP address.')
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(messages[1].message, 'Index for IP in row 3 was out of range.')
        self.assertEqual(messages[1].level_tag, 'warning')
        self.assertEqual(messages[2].message, '3 systems were created.')
        self.assertEqual(messages[2].level_tag, 'success')
        # compare - systems / attributes
        self.assertTrue(System.objects.filter(system_name='system_csv_32_001').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_32_002').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_32_003').exists())
        self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.1').exists())
        self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.2').exists())
        # get object (for better readability)
        self.assertTrue(System.objects.filter(system_name='system_csv_32_001').exists())
        # compare - systems / attributes
        self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.1').exists())
        self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.2').exists())

    def test_system_importer_file_csv_check_attributes_upload_post_faulty_ip(self):
        """ test importer view """

        # change config
        system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
        system_importer_file_csv_config_model.csv_column_system = 1
        system_importer_file_csv_config_model.csv_choice_ip = True
        system_importer_file_csv_config_model.csv_column_ip = 2
        system_importer_file_csv_config_model.save()

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_check_attributes', password='vlQnN2tg9HVGyyyIvezt')
        # open upload file
        systemcsv = open(os.path.join(BASE_DIR, 'dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_32_faulty_ip.csv'), 'r')
        # create post data
        data_dict = {
            'systemcsv': systemcsv,
        }
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.post('/system/importer/file/csv/upload/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare - messages / meta
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)
        self.assertEqual(messages[0].message, 'Value for ip address in row 2 was not a valid IP address.')
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(messages[1].message, 'Index for IP in row 3 was out of range.')
        self.assertEqual(messages[1].level_tag, 'warning')
        self.assertEqual(messages[2].message, '3 systems were created.')
        self.assertEqual(messages[2].level_tag, 'success')
        # compare - systems / attributes
        self.assertTrue(System.objects.filter(system_name='system_csv_32_001').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_32_002').exists())
        self.assertTrue(System.objects.filter(system_name='system_csv_32_003').exists())
        self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.1').exists())
        self.assertTrue(Ip.objects.filter(ip_ip='127.32.1.2').exists())
        # get object (for better readability)
        self.assertTrue(System.objects.filter(system_name='system_csv_32_001').exists())
        # compare - systems / attributes
        self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.1').exists())
        self.assertTrue(System.objects.get(system_name='system_csv_32_001').ip.filter(ip_ip='127.32.1.2').exists())
        # close file
        systemcsv.close()
