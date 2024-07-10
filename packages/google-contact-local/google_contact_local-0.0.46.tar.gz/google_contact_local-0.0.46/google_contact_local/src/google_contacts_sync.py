from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

from importer_local.importer_sync_conflict_resolution import (
    ImporterSyncConflictResolution, UpdateStatus)

from .google_contacts_push import GoogleContactsPush, SCOPES, our_get_env
from .google_contacts import DEFAULT_LOCATION_ID
from .google_contacts_constants import GoogleContactConstants


# TODO: complete to develpp this class
class GoogleContactsSync(GoogleContactsPush):
    def __init__(self):
        super().__init__()

    # TODO Please add comment why this code is commented.
    # def _insert_contact_details_to_db(self, contact_dict: dict, user_external_id: int,
    #                                   data_source_instance_id: int) -> int:
    #     # TODO: complete to develpp this method
    #     contact_dict["location_id"] = DEFAULT_LOCATION_ID
    #     try:
    #         # Get update status
    #         update_status = self.__conflict_resolution(
    #             last_modified_timestamp=contact_dict.get("last_modified_timestamp"),
    #             contact_id=contact_dict.get("contact_id"),)

    #         # insert organization
    #         organization_id = self.__sync_organization(contact_dict=contact_dict,
    #                                                    update_status=update_status)

    #         # insert link contact_location
    #         # The location is in contact_dict
    #         location_results = self.__insert_link_contact_location(
    #             # TODO Why do we need both?  contact_dict=contact_dict, contact_id=contact_id
    #             contact_dict=contact_dict) or [{}]
    #         # TODO Same comments as in contact-csv, Why location_results[0]? What if we have multiple locations? - Please add such test.
    #         # TODO Can we have one copy of this code used both by google-contact and contact-csv?
    #         contact_dict["location_id"] = location_results[0].get(
    #             "location_id")
    #         contact_dict["country_id"] = location_results[0].get("country_id")

    #         # insert link contact_group
    #         # TODO I expected to have only contact_id and group_list as parameters
    #         self.__insert_link_contact_groups(
    #             # TODO Why do we need both? contact_dict=contact_dict and contact_id=contact_id
    #             contact_dict=contact_dict)

    #         # insert link contact_persons
    #         # TODO I expected to have only contact_id and person_list as parameters
    #         contact_person_result_dict = self.__insert_link_contact_persons(
    #             contact_dict=contact_dict) or {}
    #         contact_dict["person_id"] = contact_person_result_dict.get("person_id")

    #         # insert link contact_profiles
    #         # TODO I expected to have only contact_id and profile_list as parameters
    #         # TODO contact_profiles_dict =
    #         contact_profile_info = self.__insert_contact_profiles(
    #             contact_dict=contact_dict) or {}
    #         contact_dict["profiles_ids_list"] = contact_profile_info.get("profiles_ids_list")

    #         # insert organization-profile
    #         # TODO I'm not sure I understand, contact can have multiple profiles, and contact can have multiple organizations, are we linking one organization of the contact with all his profiles?
    #         self.__insert_organization_profile(
    #             organization_id=organization_id, profiles_ids_list=contact_dict["profiles_ids_list"])

    #         # insert link contact_email_addresses
    #         # TODO I expected to have only contact_id and email_address_list as parameters
    #         self.__insert_link_contact_email_addresses(contact_dict=contact_dict)

    #         # insert link contact_notes
    #         GoogleContactsSync.__insert_link_contact_notes_and_text_blocks(contact_dict=contact_dict)

    #         # insert link contact_phones
    #         self.__insert_link_contact_phones(contact_dict=contact_dict)

    #         # inset link contact_user_externals
    #         self.__insert_link_contact_user_external(
    #             contact_dict=contact_dict)

    #         # insert link contact_internet_domains
    #         self.__insert_link_contact_domains(
    #             contact_dict=contact_dict)

    #     except Exception as exception:
    #         self.logger.exception(log_message="Error while inserting to contact connection tables",
    #                               object={"exception": exception})
    #         raise exception
    #     finally:
    #         importer_id = self.__insert_importer(
    #             # TODO As contact can have multiple locations, I think we should location_id=contact_dict.get("main_location_id")
    #             contact_id=contact_dict.get("contact_id"), location_id=contact_dict.get("location_id") or DEFAULT_LOCATION_ID,
    #             user_external_id=user_external_id,
    #             data_source_instance_id=data_source_instance_id,
    #             google_people_api_resource_name=contact_dict.get("resource_name")
    #         )
    #         self.logger.info(object={"importer_id": importer_id})

    #     return importer_id

    # # TODO: complete to develpp this method
    # def __sync_organization(self, contact_dict: dict, update_status: UpdateStatus) -> Optional[int]:

    #     if update_status == UpdateStatus.UPDATE_CIRCLEZ:
    #         if not contact_dict.get("organization"):
    #             return
    #         organization_dict = self.__create_organization_dict(
    #             organization_name=contact_dict.get("organization"))
    #         upsert_organization_result = self.organizations_local.upsert_organization(
    #             organization_dict=organization_dict)
    #         organization_id = upsert_organization_result.get("organization_id")
    #         # organization_ml_id = upsert_organization_result.get("organization_ml_id")

    #         return organization_id
    #     # elif update_status == UpdateStatus.UPDATE_DATA_SOURCE:
            
    #         # push the organization to the google contact


    # def __conflict_resolution(self, last_modified_timestamp: str, contact_id: int) -> UpdateStatus:
    #     """
    #     Conflict resolution for Google contact
    #     :return: contact_dict
    #     """

    #     if not contact_id:
    #         return UpdateStatus.DONT_UPDATE
    #     sync_conflict_resolution = ImporterSyncConflictResolution()
    #     update_status: UpdateStatus = sync_conflict_resolution.get_update_status(
    #         last_modified_timestamp=last_modified_timestamp,
    #         data_source_instance_id=GoogleContactConstants.DATA_SOURCE_TYPE_ID,
    #         entity_type_id=GoogleContactConstants.CONTACT_ENTITY_TYPE_ID,
    #         entity_id=contact_id
    #     )

    #     return update_status

    # @staticmethod
    # # TODO Let's use existing function from python-sdk, or move this function to python-sdk
    # def __get_formatted_timestamp(last_modified_timestamp_str: str) -> Optional[str]:
    #     if not last_modified_timestamp_str:
    #         return
    #     timestamp = datetime.strptime(last_modified_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    #     timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))
    #     formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    #     return formatted_timestamp
