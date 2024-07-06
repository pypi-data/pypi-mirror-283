"""
This module contains the recognizer class, responsible for encoding the string input with specific strf-codes.

"""
import functools
import re
import string
from typing import List, Optional, Tuple

from strf_hint.strf_codes import FieldTypes, StrfCodes


class Recognizer:
    """
    Class responsible for recognizing the strf-codes and decoding the patterns.

    """

    def __init__(self, codes: Optional[StrfCodes] = StrfCodes()):
        """
        Initialization of the `Recognizer` class.
        Parameters
        ----------
        codes: Optional[`StrfCodes`], default StrfCodes()
            Instance of the codes container class.

        """
        self._matched_types: List[FieldTypes] = []  # types of the strf codes, that were matched in the single encoding.
        self._matched_mask: str = ""  # mask of the matched signs, that corresponds to the input string.
        self._codes = codes

    def _match_patterns(self, s: str) -> str:
        """
        Method responsible for recognizing predefined common patterns of strf-codes.

        Parameters
        ----------
        s: `str`
            Input text to be encoded using strf-codes.

        Returns
        -------
        str`
            Input text with recognized part replaced with the proper strf-codes.

        """
        temp_s = s
        for group in self._codes.DATE_COMMON_FORMATS + self._codes.TIME_COMMON_FORMATS:
            group_regex = self._codes.generate_format_regex(group)
            match = re.search(group_regex, temp_s.lower())
            if match:
                temp_s = temp_s[: match.span()[0]] + group + temp_s[match.span()[1] :]
                self._matched_mask = (
                    self._matched_mask[: match.span()[0]]
                    + "1" * len(group)
                    + self._matched_mask[match.span()[1] :]
                )
                self._matched_types += self._codes.get_format_types(group)

        return temp_s.replace("\\", "")

    def _recognize_single_codes(self, s: str) -> str:
        """
        Method responsible for recognizing single strf-codes from unmatched parts of input string.

        Parameters
        ----------
        s: `str`
            Input text to be encoded with the strf-codes.

        Returns
        -------
        `str`
            Input text with recognized part replaced with the proper strf-codes.

        """
        loop = True
        while loop:
            loop = False
            for unmatched, span in self._retrieve_unmatched(s):
                mask_before = self._matched_mask
                matched = self._match_single_code(
                    self._split_format_components(unmatched), span
                )
                s = s[: span[0]] + matched + s[span[1] :]
                if mask_before != self._matched_mask:
                    loop = True
                    break

        return s

    def _split_format_components(self, s: str) -> List[str]:
        """
        Methode responsible for splitting the string in the sign-typed groups (digits, letters, punctuation,
        whitespaces.

        Parameters
        ----------
        s: Input text to be split.

        Returns
        -------
        `List`[`str`]
            List of strings, as a result of splitting into sign-typed groups.

        """
        index = []
        for idx, elem in enumerate(s[1:], 1):
            if self._check_string_group(elem) != self._check_string_group(s[idx - 1]):
                index.append(idx)
        index.insert(0, 0)
        index.append(len(s))

        return [s[index[i - 1] : index[i]] for i, _ in enumerate(index[1:], 1)]

    def _match_single_code(
        self, split_str: List[str], str_span: Tuple[int, int] = None
    ) -> str:
        """
        Method recognizes the single strf-codes in elements of the list containing split input text. Then replaces
        recognized parts with specific codes.

        Parameters
        ----------
        split_str: `List`[`str`]
            List containing input text split into sign-groups.

        str_span: `Tuple` [`int`, `int`], optional
            Optional parameter, indicates currently analyzed part of entire input string.

        Returns
        -------
        `str`
            String prepared from split_str with recognized parts replaced with specific codes.

        """
        codes = []
        mask = []
        for idx, elem in enumerate(split_str):
            elem_codes = []
            if re.search(r"\W", elem) or elem.lower() in self._codes.IGNORABLE:
                codes.append(elem)
                mask.append("0" * len(elem))
                continue
            prev = split_str[idx - 1].lower() if idx != 0 else ""
            nxt = split_str[idx + 1].lower() if idx < len(split_str) - 1 else ""
            exp = prev + elem.lower() + nxt
            for code in self._codes.BASIC_CODES.keys():
                if self._codes.get_type(code) in self._matched_types:
                    continue
                match = re.search(self._codes.get_regex(code, "True"), exp)
                if not match:
                    match = re.search(self._codes.get_regex(code, "True"), elem.lower())
                if match:
                    elem_codes.append(
                        (
                            code,
                            match.span()[1] - match.span()[0],
                            self._codes.get_type(code),
                        )
                    )
            if len(set([i[1] for i in elem_codes])) != 1:
                elem_codes = sorted(elem_codes, key=lambda el: el[1], reverse=True)
            if not any(elem_codes):
                codes.append(elem)
                mask.append("0" * len(elem))
                continue
            codes.append(elem_codes[0][0])
            mask.append("1" * len(elem_codes[0][0]))

            self._matched_types.append(elem_codes[0][2])

        full_mask = "".join(mask)
        if str_span:
            self._matched_mask = (
                self._matched_mask[: str_span[0]]
                + full_mask
                + self._matched_mask[str_span[1] :]
            )

        return "".join(codes)

    def _retrieve_unmatched(self, s: str) -> List[Tuple[str, Tuple[int, int]]]:
        """
        Method responsible for retrieving unmatched parts of the input string, and returns them as a list of tuples,
        containing unmatched part of string and its span (as a tuple of integers).

        Parameters
        ----------
        s: `str`
            Input string.

        Returns
        -------
        `List`[`Tuple`[`str`, `Tuple`[`int`, `int`]]]

            List containing tuple for each unmatched part of the string. Tuples contain string, and its span in the
            input string.

        """
        return [
            (s[r.span()[0]:r.span()[1]], r.span())
            for r in re.finditer("0+", self._matched_mask)
        ]

    def encode_format(self, encoded_string: str) -> str:
        """
        Method responsible for encoding the user input string, using strf-codes.
        Parameters
        ----------
        encoded_string: `str`:
            Input text to be encoded using specific strf-codes.

        Returns
        -------
        `str`
            Input string encoded with the proper strf-codes.

        """
        self._matched_types = []  # reset types container
        # self._matched_mask indicates which signs of the input text were matched with specific strf-codes
        # 0 means unmatched sign; 1 means matched sign
        self._matched_mask = "0" * len(
            encoded_string
        )  # reset mask, set its length to the length of the input string
        encoded_string = self._match_patterns(encoded_string)
        encoded_string = self._recognize_single_codes(encoded_string)
        return encoded_string

    @staticmethod
    @functools.lru_cache
    def _check_string_group(sign: str) -> str:
        """
        Method returns name of the group of signs, that tested element bellows to. The input sign is tested against
        its membership to 4 basic groups of signs: digits, letters, punctuation signs and whitespaces.

        Parameters
        ----------
        sign: str
            Single sign to be tested.

        Returns
        -------
        `str`
            Name of the specific group, that the tested element belongs to.

        """
        if len(sign) != 1:
            raise ValueError("S must be a single sign.")

        for name, group in [
            ("digits", string.digits),
            ("letters", string.ascii_lowercase + string.ascii_uppercase),
            ("punctuation", string.punctuation),
            ("whitespace", string.whitespace),
        ]:
            if sign in group:
                return name
