from typing import Union
from urllib.parse import quote_plus

import aiohttp

from .platform import Platform
from .pronoun_response import PronounResponse
from .translations import english_pronouns


class Client:
    def __init__(
            self,
            user_agent: str,
            pronouns: dict[str, list[str]] = None
    ):
        """
        :param user_agent: Used as UserAgent to talk with PronounDB.
                           A descriptive User-Agent should include at least: the name of the application,
                           the version of the application (if applicable), and optionally a link to a website.
                           Ideally, all this information should be enough to clearly identify your application and
                           find a way to reach out without too much effort.
        :param pronouns: An optional parameter that allows specifying the desired language for the returned pronouns.
                         By default, English pronouns are used (see _english_pronouns).
                         You can use this argument to retrieve pronouns in other languages by providing
                         a dictionary with the corresponding pronouns for the desired language.
        """
        self.user_agent = user_agent
        self.pronouns = pronouns or english_pronouns

    def get_translated_pronoun(
            self,
            api_pronoun: str
    ) -> list[str]:
        """
        Get the translated, human-readable version of the pronoun.
        ("he" -> ["he", "him"])
        :param api_pronoun: A single pronoun that is returned by the pronoundb api
        :return: The translated, human-readable version of the given pronoun
        """
        if api_pronoun not in self.pronouns:
            raise ValueError(f'{api_pronoun} not in pronouns parameter.')

        return self.pronouns[api_pronoun]

    async def get_pronouns_by_platform_ids(
            self,
            platform: Platform,
            identifiers: Union[str, int, list[str], list[int]]
    ) -> Union[dict[str, list[str]], dict[int, list[str]]]:
        """
        Sends a request to the PronounDB API to get the pronouns of one or multiple users.
        If more than 50 identifiers are passed, the wrapper will automatically split the request into multiple requests.

        :param platform: One of the supported platforms (see the Platform enum)
        :param identifiers: Account IDs on the platform
        :return: The pronouns of the users as a list of all the pronouns the users use
        """
        if not isinstance(identifiers, list):
            identifiers = [identifiers]

        all_results: Union[dict[str, list[str]], dict[int, list[str]]] = {}
        results = await self._batch_requests(platform, identifiers)

        for identifier in identifiers:
            # If identifier doesn't exist in pronoundb, the identifier doesn't exist in the response.
            if str(identifier) not in results:
                all_results[identifier] = self.get_translated_pronoun("unspecified")
                continue

            user_data = results[str(identifier)]
            # If the identifier is registered, but the user hasn't set any pronouns yet, then "en" won't be available.
            english_set = user_data.sets["en"] if "en" in user_data.sets else ["unspecified"]

            if len(english_set) == 1:  # e.g. ["he", "him"]
                all_results[identifier] = self.get_translated_pronoun(english_set[0])
            else:  # e.g. ["he", "they", ...]
                all_results[identifier] = [self.get_translated_pronoun(single_pronoun)[0] for single_pronoun in english_set]

        return all_results

    async def get_decorations_by_platform_ids(
            self,
            platform: Platform,
            identifiers: Union[str, int, list[str], list[int]]
    ) -> Union[dict[str, Union[str, None]], dict[int, Union[str, None]]]:
        """
        Sends a request to the PronounDB API to get the decorations of one or multiple users.
        If more than 50 identifiers are passed, the wrapper will automatically split the request into multiple requests.

        :param platform: One of the supported platforms (see the Platform enum)
        :param identifiers: Account IDs on the platform
        :return: The decoration of each user
        """
        if not isinstance(identifiers, list):
            identifiers = [identifiers]

        all_results: Union[dict[str, Union[str, None]], dict[int, Union[str, None]]] = {}
        results = await self._batch_requests(platform, identifiers)

        for identifier in identifiers:
            # If identifier doesn't exist in pronoundb, the identifier doesn't exist in the response.
            if str(identifier) not in results:
                all_results[identifier] = None
                continue

            user_data = results[str(identifier)]
            all_results[identifier] = user_data.decoration

        return all_results

    async def _batch_requests(
            self,
            platform: Platform,
            identifiers: Union[list[str], list[int]]
    ) -> dict[Union[str, int], PronounResponse]:
        responses: dict[Union[str, int], PronounResponse] = {}

        # Requests to pronoundb can have max 50 identifiers.
        for i in range(0, len(identifiers), 50):
            batch: Union[list[str], list[int]] = identifiers[i:i + 50]
            data = await self._make_call(platform, batch)

            for identifier, entry in data.items():
                responses[identifier] = PronounResponse(entry)

        return responses

    async def _make_call(
            self,
            platform: Platform,
            batch: Union[list[str], list[int]]
    ):
        if len(batch) > 50:
            raise ValueError(f'Batch is too large! {len(batch)} > 50.')

        async with aiohttp.ClientSession() as session:
            session.headers["User-Agent"] = self.user_agent  # default: Python/3.10 aiohttp/3.9.5

            async with session.get("https://pronoundb.org/api/v2/lookup?platform={0}&ids={1}".format(
                    platform.value,
                    quote_plus(",".join(map(str, batch)))
            )) as response:
                data = await response.json()

                if "error" in data:
                    raise ValueError(f'{data["error"]}: {data["message"]}')

                return data
