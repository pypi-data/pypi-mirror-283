from datetime import datetime

from database_mysql_local.generic_mapping import GenericMapping
from language_remote.lang_code import LangCode
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.MetaLogger import MetaLogger
from user_context_remote.user_context import UserContext

# TODO: move to constants.py
EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_ID = 174
EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_NAME = 'email address local'
DEVELOPER_EMAIL = "idan.a@circ.zone"
EMAIL_ADDRESS_SCHEMA_NAME = "email_address"
EMAIL_ADDRESS_ID_COLLUMN_NAME = "email_address_id"
EMAIL_ADDRESS_ML_TABLE_NAME = "email_address_ml_table"
CONTACT_EMAIL_ADDRESS_TABLE_NAME = "contact_email_address_table"
# TODO? use https://github.com/circles-zone/contact-email-address-local-python-package/blob/dev/contact-email-address-local/contact_email_address_local/src/contact_email_addresses_local.py
# TODO Later, we should consider to move this to contact-email_address_str-address-python-package repo
CONTACT_EMAIL_ADDRESS_SCHEMA_NAME = "contact_email_address"
EMAIL_ADDRESS_ENTITY_NAME1 = "contact"
EMAIL_ADDRESS_ENTITY_NAME2 = "email_address"
EMAIL_ADDRESS_COLUMN_NAME = "email_address"

object1 = {
    'component_id': EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': EMAIL_ADDRESS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': "idan.a@circ.zone"
}


# TODO def process_email( email_address_str: str) -> dict:
#          extract organization_name
#          extract top_level_domain (TLD)
#          SELECT profile_id, is_webmain FROM `internet_domain`.`internet_domain_table` WHERE
#          if result set is empty INSERT INTO `internet_domain`.`internet_domain_table`

class EmailAddressesLocal(GenericMapping, metaclass=MetaLogger, object=object1):
    # TODO Where shall we link email-address_id to person, contact, profile ...?
    # Can we create generic function for that in GenericCRUD and use it multiple times
    # in https://github.com/circles-zone/email-address-local-python-package
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name=EMAIL_ADDRESS_SCHEMA_NAME,
                         default_entity_name1=EMAIL_ADDRESS_ENTITY_NAME1,
                         default_entity_name2=EMAIL_ADDRESS_ENTITY_NAME2,
                         is_test_data=is_test_data)
        self.user_context = UserContext()

    def insert(self, *,  # noqa
               email_address_str: str, lang_code: LangCode, name: str, data_dict: dict = None) -> int or None:
        email_address_dict = data_dict or {}
        email_address_dict[EMAIL_ADDRESS_COLUMN_NAME] = email_address_str
        email_address_id = super().insert(data_dict=email_address_dict)
        email_address_ml_dict = {
            "email_address_id": email_address_id,
            "lang_code": lang_code.value,
            "title": name
        }
        super().insert(table_name=EMAIL_ADDRESS_ML_TABLE_NAME, data_dict=email_address_ml_dict)

        return email_address_id

    def update_email_address(self, email_address_id: int, new_email_address_str: str) -> None:
        email_address_dict = {EMAIL_ADDRESS_COLUMN_NAME: new_email_address_str}
        self.update_by_column_and_value(column_value=email_address_id, data_dict=email_address_dict)

    def delete(self, email_address_id: int) -> None:
        self.delete_by_column_and_value(column_value=email_address_id)

    def get_email_address_by_email_address_id(self, email_address_id: int) -> str:
        assert isinstance(email_address_id, int)
        email_address_str = self.select_one_value_by_column_and_value(
            select_clause_value=EMAIL_ADDRESS_COLUMN_NAME, column_value=email_address_id)

        return email_address_str

    def get_email_address_id_by_email_address_str(self, email_address_str: str) -> int:
        assert isinstance(email_address_str, str)
        email_address_id = self.select_one_value_by_column_and_value(
            select_clause_value=EMAIL_ADDRESS_ID_COLLUMN_NAME,
            column_name=EMAIL_ADDRESS_COLUMN_NAME, column_value=email_address_str)
        return email_address_id

    def verify_email_address_str(self, email_address_str: str) -> None:
        """verify_email_address executed by SmartLink/Action"""
        # TODO Think about creating parent both to verifiy_email_address and verify_phone
        assert isinstance(email_address_str, str)
        self.update_by_column_and_value(column_name=EMAIL_ADDRESS_COLUMN_NAME,
                                        column_value=email_address_str, data_dict={"is_verified": True})

    # TODO def process_email(email_address_str: str) -> dict:
    #          extract organization_name
    #          extract top_level_domain (TLD)
    #          SELECT profile_id, is_webmain FROM `internet_domain`.`internet_domain_table` WHERE
    #          if result set is empty INSERT INTO `internet_domain`.`internet_domain_table`
    # todo answer is in url-remote Domain.py currenlty 1/15/24 6am workflow not working

    def process_email(self, contact_id: int, email_address_str: str) -> int or dict:  # TODO: let's return single type
        """
        Process the given email address for a contact.

        Parameters:
        - contact_id (int): The ID of the contact.
        - email_address_str (str): The email address to be processed.

        Returns:
        - int: If the email address is already in the system and mapped to the contact,
        the method returns the contact_email_id.
        If the email address is not in the system, it returns a dictionary with
        process information, including email_address_id, contact_email_id,
        email_address_str, and contact_id.
        """

        email_address_id = self.get_email_address_id_by_email_address_str(
            email_address_str=email_address_str)
        if email_address_id:  # email_address_str is in the system
            self.logger.info("email address is in the system", object={
                "email_address_str": email_address_str})
            contact_email_address_mapping_result = self.select_multi_mapping_tuple_by_id(
                schema_name=CONTACT_EMAIL_ADDRESS_SCHEMA_NAME,
                entity_name1=EMAIL_ADDRESS_ENTITY_NAME1, entity_name2=EMAIL_ADDRESS_ENTITY_NAME2,
                entity_id1=contact_id, entity_id2=email_address_id)
            if contact_email_address_mapping_result:  # email is mapped to contact
                self.logger.info("email address is already mapped to contact", object={
                    "email_address_str": email_address_str})
                email_address_dict = {
                    'contact_id': contact_id,
                    'email_address_id': email_address_id
                }
                self.update_by_column_and_value(
                    schema_name=CONTACT_EMAIL_ADDRESS_SCHEMA_NAME,
                    table_name=CONTACT_EMAIL_ADDRESS_TABLE_NAME,
                    column_value=email_address_str, data_dict=email_address_dict)

                return contact_email_address_mapping_result[0][0]
            else:  # email is not mapped to contact
                self.logger.info("email address is not mapped to contact", object={
                    "email_address_str": email_address_str})
                contact_email_id = self.insert_mapping(
                    schema_name=CONTACT_EMAIL_ADDRESS_SCHEMA_NAME,
                    entity_name1=EMAIL_ADDRESS_ENTITY_NAME1, entity_name2=EMAIL_ADDRESS_ENTITY_NAME2,
                    entity_id1=contact_id, entity_id2=email_address_id)

                return contact_email_id
        else:  # email is not in the system
            self.logger.info("email address is not in the system")
            effective_profile_preferred_lang_code = self.user_context.get_effective_profile_preferred_lang_code()
            # TODO: self.user_context.get_full_name() is not implemented yet
            name = self.user_context.get_real_first_name() + " " + self.user_context.get_real_last_name()
            email_address_id = self.insert(
                email_address_str=email_address_str, lang_code=LangCode(effective_profile_preferred_lang_code),
                name=name)
            contact_email_id = self.insert_mapping(schema_name=CONTACT_EMAIL_ADDRESS_SCHEMA_NAME,
                                                   entity_name1=EMAIL_ADDRESS_ENTITY_NAME1,
                                                   entity_name2=EMAIL_ADDRESS_ENTITY_NAME2,
                                                   entity_id1=contact_id, entity_id2=email_address_id)
            process_information = {
                "email_address_id": email_address_id,
                "contact_email_id": contact_email_id,
                "email_address": email_address_str,
                "contact_id": contact_id,
            }

            return process_information

    def get_domain_id_from_email(self, email_address_str: str) -> int:
        email_address_domain = email_address_str.split("@", 1)[-1]
        internet_domain_id = self.select_one_value_by_column_and_value(
            select_clause_value="internet_domain_id",
            schema_name="internet_domain",
            view_table_name="internet_domain_view",
            column_name="domain",
            column_value=email_address_domain)

        return internet_domain_id

    def get_username_from_email(self, email_address_str: str) -> str:
        username_str = email_address_str.split("@", 1)[0]
        # TODO: why we update? Should we select instead of the split above?
        # self.update_by_column_and_value(schema_name="email_address",
        #                                 table_name="email_address_table",
        #                                 column_name="email_address",
        #                                 column_value=email_address_str,
        #                                 data_dict={"username": username_str}
        #                                 )
        return username_str

    @staticmethod
    def get_test_email_address() -> str:
        """Generates a generic email_address_str address.
        For example: email2023-12-24 23:29:43.269076@test.com"""
        """Generates a generic email address.
        For example: email20231224232943@test.com"""
        test_email_address = "email" + str(datetime.now()) + "@test.com"
        return test_email_address

    def get_test_email_address_id(self) -> int:
        return super().get_test_entity_id(entity_name="email_address",
                                          insert_function=self.insert,
                                          insert_kwargs={"email_address_str": self.get_test_email_address(),
                                                         "lang_code": LangCode.ENGLISH,
                                                         "name": "test"})
