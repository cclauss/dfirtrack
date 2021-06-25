import csv
import hashlib
import os
from datetime import datetime
from logging import debug
from dfirtrack_main.logger.default_logger import info_logger, debug_logger
from dfirtrack_main.async_messages import message_user
from dfirtrack_main.models import Case, Entry, System
from django.contrib.messages import constants
from django.core.exceptions import ValidationError
from django.utils.timezone import get_current_timezone


def csv_entry_import_async(system_id, file_name, field_mapping, request_user, case_id=None):
    """ async entry csv import """

    row_count = 0
    fail_count = 0
    dup_count = 0
    
    system = System.objects.get(system_id=system_id)
    case = Case.objects.get(case_id=case_id) if case_id else None
    try:
        with open(file_name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(spamreader)
            for row in spamreader: 
                try:
                    row_count += 1
                    entry = Entry()
                    entry.system = system
                    entry.entry_created_by_user_id = request_user
                    entry.entry_modified_by_user_id = request_user                
                    m = hashlib.sha1()
                    entry.entry_time = row[field_mapping['entry_time']]
                    entry.entry_api_time = datetime.now(tz=get_current_timezone())
                    m.update(entry.entry_time.encode())                
                    entry.entry_type = row[field_mapping['entry_type']]
                    m.update(entry.entry_type .encode())
                    entry.entry_content = row[field_mapping['entry_content']]
                    m.update(entry.entry_content.encode())                       
                    entry.entry_sha1 = m.hexdigest()                    
                    entry.case = case
                    if not Entry.objects.filter(entry_sha1=m.hexdigest()).exists():
                        entry.full_clean()
                        entry.save()
                    else:
                        dup_count += 1
                        continue
                except ValidationError as e:
                    debug_logger(
                        str(request_user),
                        f' ENTRY_CSV_IMPORT'
                        f' ERROR: {e}'
                    )
                    fail_count += 1
                    continue

        os.remove(file_name)

    except FileNotFoundError:
        info_logger(
            str(request_user),
            f' ENTRY_CSV_IMPORT'
            f' ERROR: File not found'
        )
        message_user(
            request_user,
            f"Could not import the csv file. Maybe the upload wasn't successfull or the file was deleted.",
            constants.ERROR
        )
        return

    if fail_count == 0 and dup_count != 0:
        message_user(
            request_user,
            f'Imported {row_count-dup_count} entries for system "{system.system_name}". Removed {dup_count} duplicates.',
            constants.SUCCESS
        )
    elif fail_count == 0:
        message_user(
            request_user,
            f'Imported {row_count} entries for system "{system.system_name}".',
            constants.SUCCESS
        )
    else: 
        message_user(
            request_user,
            f'Could not import {fail_count} of {row_count} entries for system "{system.system_name}".',
            constants.WARNING
        )

    # call logger
    info_logger(
        str(request_user),
        f' ENTRY_CSV_IMPORT'
        f' created:{row_count}'
        f' failed:{fail_count}'
        f' duplicates:{dup_count}'
    )