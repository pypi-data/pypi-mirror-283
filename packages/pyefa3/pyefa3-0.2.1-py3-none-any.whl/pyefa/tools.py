from colorama import Fore, Back, Style


def bold(data):
    """Make a string or a list of strings bold"""
    if isinstance(data, str):
        return Style.BRIGHT + data + Style.NORMAL
    if isinstance(data, list):
        return [Style.BRIGHT + item + Style.NORMAL for item in data]
    return None


def nostyle(data):
    """Remove all styles from string"""
    a = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE, Fore.RESET,
         Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE, Back.RESET,
         Style.NORMAL, Style.BRIGHT, Style.DIM, Style.RESET_ALL]
    for b in a:
        data = data.replace(b, '')
    return data


def coords(x, y):
    return (float(x) / 1000000, float(y) / 1000000)


class Table():
    """ Table to display EFA Results """

    def __init__(self, lines):
        self.lines = lines
        self.infos = []

    def dowidth(self, string, width):
        return string + ' ' * (width - len(nostyle(string)))

    def __str__(self):
        # Spaltenbreiten
        for i in range(len(self.lines)):
            if isinstance(self.lines[i], list):
                firstline = i
                break

        colwidths = [0 for line in self.lines[firstline]]
        colwidths = [max([(0 if isinstance(line, str) else len(nostyle(line[i]))) for line in self.lines]) for i in
                     range(len(self.lines[firstline]))]
        totalwidth = (sum(colwidths) + (len(colwidths) * 2))
        for line in self.lines:
            if isinstance(type(line), str):
                totalwidth = max(totalwidth, len(nostyle(line)))

        totalwidth = min(totalwidth, 80)
        trenner = '-' * totalwidth

        string = []
        for line in self.lines:
            string.append('  '.join([self.dowidth(line[i], colwidths[i]) for i in range(len(colwidths))]) if isinstance(
                line, list) else (trenner if line == '-' else line))
        return '\n'.join(string) + '\n'
