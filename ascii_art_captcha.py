from art import text2art
from typing import NoReturn, List, Dict
from string import ascii_uppercase, ascii_letters, digits, printable
from random import choices, choice, randint


class Captcha:
    def __init__(self, ascii_art: str, solution: str, *, max_fails: int = 0):
        self._ascii_art = ascii_art
        self._fails = 0
        self._max_fails = max_fails
        self._solution = solution
        self._solved = False

    @property
    def failed(self) -> bool:
        return 0 < self._max_fails <= self._fails

    @property
    def solved(self) -> bool:
        return self._solved

    def check(self, user_input: str, /) -> bool:
        if self.failed:
            return False

        if user_input.lower() == self._solution.lower() or self._solved:
            self._solved = True
            return True

        self._fails += 1
        return False

    def print(self) -> NoReturn:
        print(self)
        print()

    def check_user_input(self, prompt: str = "ENTER CODE > ") -> bool:
        try:
            user_input: str = input(prompt)
            return self.check(user_input)
        except KeyboardInterrupt:
            print()
            return self.check("")

    def execute(self) -> bool:
        self.print()

        while not self.failed and not self._solved:
            if self._max_fails > 0:
                print(self._max_fails - self._fails, "attempts left...")

            result: bool = self.check_user_input()

            if result:
                print("SOLVED!")
                return True
            elif self.failed:
                print(self._solution)
                print("FAILED!")
                return False

            print("WRONG!")

    def __repr__(self) -> str:
        return self._ascii_art

    def __str__(self) -> str:
        return self._ascii_art

    @staticmethod
    def generate(*, length: int = 5, max_fails: int = 3) -> "Captcha":
        base: List[str] = [""]
        solution: str = "".join(choices(ascii_uppercase, k=length))

        current_length: int = 0

        noise_characters: List[str] = list(printable + digits + ascii_letters)
        font_list: List[str] = ["1943", "5lineoblique", "alpha", "alphabet", "arrows", "banner", "banner4",
                                "big", "colossal", "doom", "dotmatrix", "epic",
                                "modular", "nancyj", "oldbanner", "os2", "pawp", "rounded", "slant",
                                "small", "smslant", "speed", "standard", "starwars", "univers", "varsit"]

        for character in solution:
            font: str = choice(font_list)
            ascii_art: str = text2art(character, font=font)

            character_distribution: Dict[str, int] = {character: ascii_art.count(character) for character in
                                                      set(ascii_art.replace("\r", "").replace("\n", "").replace(" ",
                                                                                                                ""))}
            most_common_character: str = max(character_distribution, key=character_distribution.get)

            special_characters: List[str] = ["-", "+", "!", "|", ":"]

            replace_character: str = choice(special_characters)
            if most_common_character.isdigit():
                replace_character = choice(digits)
            elif most_common_character.isalpha():
                replace_character = choice(ascii_letters)

            ascii_art = ascii_art.replace(most_common_character, replace_character)

            lines: List[str] = ascii_art.split("\r\n")

            max_length: int = max(map(len, lines))

            for index, line in enumerate(lines):
                if index >= len(base):
                    base.append(current_length * " ")

                base[index] += line

            random_offset: int = randint(0, 5)

            for index in range(len(base)):
                base[index] = base[index].ljust(current_length + max_length + random_offset)

            current_length = max(map(len, base))

        while len(base[0].strip()) == 0:
            del base[0]

        while len(base[-1].strip()) == 0:
            del base[-1]

        for noise_character in choices(noise_characters, k=randint(15, 30)):
            base_index: int = randint(0, len(base) - 1)
            line: str = base[base_index]
            line_index: int = randint(0, len(line) - 1)

            base[base_index] = line[:line_index] + noise_character + line[line_index + 1:]

        ascii_art: str = "\r\n".join(base)

        return Captcha(ascii_art=ascii_art, solution=solution, max_fails=max_fails)


if __name__ == "__main__":
    captcha: Captcha = Captcha.generate()
    captcha.execute()
