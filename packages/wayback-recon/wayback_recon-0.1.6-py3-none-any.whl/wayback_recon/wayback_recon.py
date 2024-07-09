import json
import argparse
import os
import sqlite3
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import requests
import re
from urllib.parse import urlparse

def create_config_file():
    base_pattern = {
        "apis": ["/api", "/v1", "/v2", "/services", "/rest", "/graphql", "/json"],
        "leaks": ["aws", "apikey", "secret", "password", "auth", "token", "key", "access", "credential", "jwt", "kong", "kong-key"],
        "extensions": [".js", ".css", ".html", ".php", ".asp", ".aspx", ".jsp", ".json", ".xml", ".txt", ".csv"],
        "cms": ["wp-", "wordpress", "joomla", "drupal", "magento", "typo3", "shopify", "prestashop"]
    }

    with open('pattern_config.json', 'w') as f:
        f.write(json.dumps(base_pattern, indent=2))


class CategorizationStrategy:
    def __init__(self, category_name, keywords):
        self.category_name = category_name
        self.keywords = keywords

    def categorize(self, url, categories):
        if any(re.search(rf'{keyword}', url) for keyword in self.keywords):
            if self.category_name not in categories:
                categories[self.category_name] = []
            categories[self.category_name].append(url)
            return True
        return False

    def highlight_keywords(self, url):
        for keyword in self.keywords:
            if re.search(rf'{keyword}', url):
                return re.sub(rf'({keyword})', r'[red]\1[/red]', url)
        return url

class CategorizationManager:
    def __init__(self, config):
        self.strategies = [CategorizationStrategy(category, keywords) for category, keywords in config.items()]

    def categorize_urls(self, urls):
        categories = {}
        for url in urls:
            for strategy in self.strategies:
                strategy.categorize(url, categories)
        return categories

class WaybackRecon:
    def __init__(self, target=None, config_file='pattern_config.json', output_file=None):
        self.target = target
        self.console = Console()
        self.config = self._load_config(config_file)
        self.categorization_manager = CategorizationManager(self.config)
        self.domain_base = self._get_domain_base()
        self.output_folder = self._set_output_folder()
        self.output_file = self._set_output_file(output_file)
        self.db_file = os.path.join(self.output_folder, f'{self.domain_base}.sqlite')

    def _get_domain_base(self):
        parsed_url = urlparse(self.target)
        domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
        domain_base = domain.split('.')[0]
        return domain_base

    def _set_output_folder(self):
        folder_name = self.domain_base
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def _set_output_file(self, output_file):
        if output_file and not output_file.endswith('.json'):
            output_file += '.json'
        elif not output_file:
            output_file = os.path.join(self.output_folder, f'{self.domain_base}_wayback_recon.json')
        return output_file

    def _load_config(self, config_file):
        with open(config_file, 'r') as f:
            return json.load(f)

    def _fetch_urls(self):
        url = f'http://web.archive.org/cdx/search/cdx?url=*.{self.target}/*&output=json&fl=original&collapse=urlkey'
        response = requests.get(url)
        results = response.json()
        return [result[0] for result in results[1:]]

    def _log_categories(self, categories, selected_categories=None):
        if selected_categories:
            selected_categories = set(selected_categories)
            invalid_categories = selected_categories - set(categories.keys())
            if invalid_categories:
                self.console.print(f"[red]Invalid categories: {', '.join(invalid_categories)}[/red]")
                self.show_options_panel()
                return
        else:
            selected_categories = categories.keys()

        for category in selected_categories:
            if category in categories and categories[category]:
                highlighted_urls = [self.categorization_manager.strategies[0].highlight_keywords(url) for url in categories[category]]
                panel = Panel(
                    "\n".join(highlighted_urls),
                    title=f"[yellow]Found {len(categories[category])} {category.capitalize()} URLs[/yellow]",
                    border_style="light_sky_blue1",
                    box=box.ROUNDED,
                    expand=False
                )
                self.console.print(panel)

    def _save_to_json(self, data):
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=4)

    def _save_to_sqlite(self, data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                category TEXT,
                url TEXT
            )
        ''')
        cursor.execute('DELETE FROM urls')
        for category, urls in data.items():
            for url in urls:
                cursor.execute('INSERT INTO urls (category, url) VALUES (?, ?)', (category, url))
        conn.commit()
        conn.close()

    def run(self):
        self._print_log("[*] Fetching URLs...")
        urls = self._fetch_urls()
        self._print_log("[*] Categorizing URLs...")
        categorized_urls = self.categorization_manager.categorize_urls(urls)
        self._log_categories(categorized_urls)
        self._print_log("[*] Saving to JSON...")
        self._save_to_json(categorized_urls)
        self._print_log("[*] Saving to SQLite...")
        self._save_to_sqlite(categorized_urls)
        self._print_log("[+] Process Completed.")

    def _print_log(self, message):
        panel = Panel(f"[green]{message}[/green]", border_style="light_sky_blue1", box=box.ROUNDED)
        self.console.print(panel)

    def search(self, categories):
        if not os.path.exists(self.db_file):
            self._print_log("[red][-] Output file not found. Please run the tool first to generate the output file.[/red]")
            return

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for category in categories:
            cursor.execute('SELECT url FROM urls WHERE category = ?', (category,))
            urls = cursor.fetchall()
            if urls:
                highlighted_urls = [url[0] for url in urls]
                panel = Panel(
                    "\n".join(highlighted_urls),
                    title=f"[yellow]Found {len(highlighted_urls)} {category.capitalize()} URLs[/yellow]",
                    border_style="light_sky_blue1",
                    box=box.ROUNDED,
                    expand=False
                )
                self.console.print(panel)
        conn.close()

    def show_options_panel(self):
        options = "\n".join([f"[bold magenta]{key}[/bold magenta]" for key in self.config.keys()])
        panel = Panel(options, title="[bold yellow]Available Categories[/bold yellow]", border_style="light_sky_blue1", box=box.ROUNDED)
        self.console.print(panel)

def print_banner():
    banner_text = Text("""
    
    ██╗    ██╗ █████╗ ██╗   ██╗██████╗  █████╗  ██████╗██╗  ██╗    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
    ██║    ██║██╔══██╗╚██╗ ██╔╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
    ██║ █╗ ██║███████║ ╚████╔╝ ██████╔╝███████║██║     █████╔╝     ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
    ██║███╗██║██╔══██║  ╚██╔╝  ██╔══██╗██╔══██║██║     ██╔═██╗     ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
    ╚███╔███╔╝██║  ██║   ██║   ██████╔╝██║  ██║╚██████╗██║  ██╗    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
     ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
                                qayback-recon 0.1.5 powered by Renato Pinheiro
    """, justify="center", style="bold cyan")
    console = Console()
    console.print(banner_text)

def main():
    if not os.path.exists('pattern_config.json'): create_config_file()
    print_banner()
    
    parser = argparse.ArgumentParser(description="Fetch and categorize URLs from Wayback Machine")
    parser.add_argument('-t', '--target', type=str, help='Target domain to fetch URLs for', required=True)
    parser.add_argument('-p', '--pattern-file', type=str, default='pattern_config.json', help='Path to the pattern config JSON file')
    parser.add_argument('-o', '--output-file', type=str, help='Output file name for the JSON results')
    parser.add_argument('-s', '--search', nargs='*', help='Search and display specific categories (e.g., apis, leaks, extensions, cms)')
    args = parser.parse_args()

    recon = WaybackRecon(args.target, args.pattern_file, args.output_file)

    if args.search is not None:
        if args.search:
            invalid_categories = set(args.search) - set(recon.config.keys())
            if invalid_categories:
                recon.console.print(f"[red]Invalid categories: {', '.join(invalid_categories)}[/red]")
                recon.show_options_panel()
            else:
                recon.search(args.search)
        else:
            recon.show_options_panel()
    elif args.target:
        recon.run()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
