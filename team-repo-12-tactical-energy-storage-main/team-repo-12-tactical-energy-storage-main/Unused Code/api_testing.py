import requests
import json

# api_token = None

base_url = "https://vrmapi.victronenergy.com/v2/"


class APIUser:
    def __init__(self, api_token):
        self.self = self
        self.__api_token = api_token
        self.headers = {}
        self.response = None
        self.response_status_code = None
        self.request_data = None
        self.__bearer_token = None

    def dump_response(self):
        return self.response, self.response_status_code

    def handle_response(self):
        if self.response_status_code == 200:
            data = self.response.json()
            return data
        else:
            print(f"Couldn't get data for the request: {self.response_status_code} - {self.response.text}")
            return None

    def login_demo(self):
        url = base_url + "auth/loginAsDemo"
        self.headers['Content-Type'] = "application/json"
        self.response = requests.get(
            url=url,
            headers={"Content-Type": "application/json"}
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()
        print(self.request_data)

    def login(self, email, password):
        url = base_url + "auth/login"
        get_data = {
            "username": email,
            "password": password
        }
        self.response = requests.post(
            url=url,
            headers={"Content-Type": "application/json"},
            data=get_data
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()
        print(self.request_data)

    def logout_token(self):
        url = base_url + "auth/logout"
        if self.__bearer_token is not None:
            logout_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            logout_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.get(
            url=url,
            headers=logout_headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def add_new_site(self, idUser):
        url = f"https://vrmapi.victronenergy.com/v2/users/{idUser}/addsite"

        payload = {"installation_identifier": "string"}
        headers = {
            "Content-Type": "application/json",
            "x-authorization": f"Token {self.__api_token}"
        }

        self.response = requests.post(
            url=url,
            json=payload,
            headers=headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def all_installations_for_user(self, idUser, extended):
        url = base_url + f"users/{idUser}/installations"
        querystring = {"extended": f"{extended}"}
        if self.__bearer_token is not None:
            install_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            install_headers = {"Content-Type": "application/json", "X-Authorization": f"Token {self.__api_token}"}
        self.response = requests.get(
            url=url,
            headers=install_headers,
            params=querystring
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def create_access_token_for_user(self, idUser):
        url = base_url + f"users/{idUser}/accesstokens/create"
        if self.__bearer_token is not None:
            create_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            create_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.post(
            url=url,
            headers=create_headers,
            data={
                "name": "MyNewToken"
            }
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def list_all_access_token_for_user(self, idUser):
        url = base_url + f"users/{idUser}/accesstokens/list"
        if self.__bearer_token is not None:
            list_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            list_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.get(
            url=url,
            headers=list_headers
        )
        self.response_status_code = self.response.status_code
        self.response = self.handle_response()

    def remove_access_token_for_user(self, idUser, idAccessToken):
        url = base_url + f"users/{idUser}/accesstokens/{idAccessToken}/revoke"
        if self.__bearer_token is not None:
            removal_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            removal_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.get(
            url=url,
            headers=removal_headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def site_id(self, idUser):
        url = base_url + f"users/{idUser}/get-site-id"
        if self.__bearer_token is not None:
            site_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            site_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.post(
            url=url,
            headers=site_headers,
            data={
                "installation_identifier": "string"  # Instillation Identifier
            }
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def basic_user_info(self):
        url = base_url + "users/me"
        if self.__bearer_token is not None:
            info_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            info_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.get(
            url=url,
            headers=info_headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()
        print(self.request_data)

    def get_alarms(self, idSite):
        url = base_url + f"installations/{idSite}/alarms"
        if self.__bearer_token is not None:
            get_alarms_headers = {"Content-Type": "application/json",
                                  "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            get_alarms_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.get(
            url=url,
            headers=get_alarms_headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def add_alarms(self, idSite):
        url = base_url + f"installations/{idSite}/alarms"
        if self.__bearer_token is not None:
            add_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            add_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.pos(
            url=url,
            headers=add_headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def delete_alarm(self, idSite):
        url = base_url + f"installations/{idSite}/alarms"
        if self.__bearer_token is not None:
            add_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            add_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.delete(
            url=url,
            headers=add_headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def edit_alarm(self, idSite, alarmEmbeded, notifyAfterSeconds, highAlarm, highAlarmHysteresis, idDataAttr,
                   instance, lowAlarm, lowAlarmHysteresis):
        url = base_url + f"installations/{idSite}/alarms"
        if self.__bearer_token is not None:
            add_headers = {"Content-Type": "application/json", "x-authorization": f"Bearer {self.__bearer_token}"}
        elif self.__api_token is not None:
            add_headers = {"Content-Type": "application/json", "x-authorization": f"Token {self.__api_token}"}
        self.response = requests.put(
            url=url,
            headers=add_headers,
            data={
                "AlarmEnabled": alarmEmbeded,
                "NotifyAfterSeconds": notifyAfterSeconds,
                "highAlarm": highAlarm,
                "highAlarmHysteresis": highAlarmHysteresis,
                "idDataAttribute": idDataAttr,
                "instance": instance,
                "lowAlarm": lowAlarm,
                "lowAlarmHysteresis": lowAlarmHysteresis
            }
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    # TODO: Everything past <clear alarm> to include <clear alarm>

    def clear_alarm(self, idSite, alarmId):
        url = base_url + f"installations/{idSite}/clear-alarm"
        headers = {
            "Content-Type": "application/json",
            "x-authorization": f"Token {self.__api_token}"
        }
        data = {
            "alarmId": f"{alarmId}"
        }
        self.response = requests.post(
            url=url,
            headers=headers,
            data=data
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def connected_devices_for_given_installation(self, idSite):
        url = base_url + f"installations/{idSite}/system-overview"
        headers = {
            "Content-Type": "application/json",
            "x-authorization": f"Token {self.__api_token}"
        }
        self.response = requests.get(
            url=url,
            headers=headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def diagnostic_data_for_installatio(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/diagnostics"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def dynamic_ESS_config_get(self, idSite):
        url = base_url + f"installations/{idSite}/dynamic-ess-settings"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        self.response = requests.get(
            url=url,
            headers=headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def dynamic_ESS_config_post(self, idSite, payload):
        url = base_url + f"installations/{idSite}/dynamic-ess-settings"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        self.response = requests.post(
            url=url,
            headers=headers,
            json=payload
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def gps_tracks_for_installation(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/gps-download"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def get_installation_tags(self, idSite):
        url = base_url + f"installations/{idSite}/tags"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        self.response = requests.get(
            url=url,
            headers=headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def download_installation_data(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/data-download"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def installation_stats(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/stats"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def overall_installation_stats(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/overallstats"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def update_settings_for_installation(self, idSite, payload):
        url = base_url + f"installations/{idSite}/settings"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        self.response = requests.post(
            url=url,
            headers=headers,
            json=payload
        )

        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def invite_user_to_installation(self, idSite, payload):
        url = base_url + f"installations/{idSite}/data-download"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        self.response = requests.post(
            url=url,
            headers=headers,
            params=payload
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    # -------------------------------------------------------------------

    def graph_series_for_installation_and_attributes(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/widgets/Graph"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def gps_data_for_installation(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/widgets/GPS"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def hours_AC_for_installation(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/widgets/HoursOfAc"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    # -------------------------------------------------------------------

    def generator_state_graph_data(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/widgets/GeneratorState"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    def input_state_graph_data(self, idSite, querystring=None):
        url = base_url + f"installations/{idSite}/widgets/InputState"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        if querystring is not None:
            self.response = requests.get(
                url=url,
                headers=headers,
                params=querystring
            )
        else:
            self.response = requests.get(
                url=url,
                headers=headers
            )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()

    # -------------------------------------------------------------------

    def list_all_sites(self):
        url = base_url + f"installations"
        headers = {
            "X-Authorizations": f"{self.__api_token}",
            "Content-Type": "application/json"
        }
        self.response = requests.get(
            url=url,
            headers=headers
        )
        self.response_status_code = self.response.status_code
        self.request_data = self.handle_response()


test = APIUser("7a16dd84630fda1a275fc555e491038567ba98b4a54a88bc355e161d89084382")
# test.basic_user_info()
# print(test.response)
test.add_new_site(530569)
print(test.response)
test.all_installations_for_user(530569, 1)
# print(test.response)
# test.site_id(530569)
# print(test.dump_response())
# test.list_all_sites()
# test.all_installations_for_user()
print(test.response)
