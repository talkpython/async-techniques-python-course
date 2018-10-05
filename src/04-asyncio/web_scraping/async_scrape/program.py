import aiohttp
import bs4
from colorama import Fore
import asyncio


class Scraper:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.get_title_range())

    async def get_html(self, episode_number: int) -> str:
        print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

        url = f'https://talkpython.fm/{episode_number}'
        # resp = requests.get(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()

                return await resp.text()

    def get_title(self, html: str, episode_number: int) -> str:
        print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        header = soup.select_one('h1')
        if not header:
            return "MISSING"

        return header.text.strip()

    async def get_title_range(self):
        # Please keep this range pretty small to not DDoS my site. ;)

        tasks = []
        for n in range(150, 160):
            tasks.append((n, self.loop.create_task(self.get_html(n))))

        for n, t in tasks:
            html = await t
            title = self.get_title(html, n)
            print(Fore.WHITE + f"Title found: {title}", flush=True)


if __name__ == '__main__':
    Scraper()

