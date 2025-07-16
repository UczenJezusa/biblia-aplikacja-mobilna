description = (
    "description=Polska Biblia Gdańska 1879\n"
    "short.title=PBG\n"
    "lang=pol\n"
    "publish.date=2025\n"
    "publisher=\n"
    "version.major=1\n"
    "version.minor=0.1\n"
    "source=<a href=\"https://github.com/piotrskurzynski/biblia\">https://github.com/piotrskurzynski/biblia</a>\n"
    "about=Polska Biblia Gdańska 1879 (1632, rewizja 1879). "
    "\"Biblija Święta to jest wszystko Pismo Święte starego i nowego Testamentu. "
    "Z hebrajskiego i greckiego języka na polski pilnie i wiernie przetłómaczona.\""
)

def main():
    print(len(''.join(description.split())))

if __name__ == "__main__":
    main()
