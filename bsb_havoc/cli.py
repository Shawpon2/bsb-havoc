"""
BSB Havoc CLI - Professional Command Line Interface
🔥 The World's Most Powerful Load Testing Tool
"""

import sys
import argparse
import asyncio
import platform
from colorama import Fore, Style, init as colorama_init
from .engine import HavocEngine
from . import __version__

colorama_init()

class BSBHavocCLI:
    """Professional CLI for BSB Havoc"""
    
    def __init__(self):
        self.banner = f"""
{Fore.RED}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ███████╗██████╗     ██╗  ██╗ █████╗ ██╗   ██╗ ██████╗  ██████╗     ║
║  ██╔══██╗██╔════╝██╔══██╗    ██║  ██║██╔══██╗██║   ██║██╔═══██╗██╔═══██╗    ║
║  ██████╔╝███████╗██████╔╝    ███████║███████║██║   ██║██║   ██║██║   ██║    ║
║  ██╔══██╗╚════██║██╔══██╗    ██╔══██║██╔══██║██║   ██║██║   ██║██║   ██║    ║
║  ██████╔╝███████║██████╔╝    ██║  ██║██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝    ║
║  ╚═════╝ ╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝     ║
║                                                                              ║
║  {Fore.CYAN}🔥 The World's Most Powerful Load Testing Tool v{__version__}{' ' * 14}{Fore.RED}║
║  {Fore.YELLOW}⚡ Professional • High-Performance • Distributed{' ' * 20}{Fore.RED}║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    
    def display_banner(self):
        """Display the professional banner"""
        print(self.banner)
        print(f"{Fore.WHITE}{'═' * 80}{Style.RESET_ALL}")
    
    def validate_url(self, url: str) -> str:
        """Validate and normalize URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Remove trailing slash for consistency
        if url.endswith('/'):
            url = url[:-1]
        
        return url
    
    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description='BSB Havoc - Professional Load Testing Tool',
            usage='bsb-havoc [OPTIONS] <target_url>',
            add_help=False
        )
        
        parser.add_argument(
            'target',
            nargs='?',
            help='Target website URL (e.g., example.com or http://example.com)'
        )
        
        parser.add_argument(
            '-c', '--concurrent',
            type=int,
            default=1000,
            help='Maximum concurrent connections (default: 1000)'
        )
        
        parser.add_argument(
            '-v', '--version',
            action='store_true',
            help='Show version information'
        )
        
        parser.add_argument(
            '-h', '--help',
            action='store_true',
            help='Show this help message'
        )
        
        return parser.parse_args()
    
    def display_help(self):
        """Display help information"""
        help_text = f"""
{Fore.CYAN}{Style.BRIGHT}BSB HAVOC - COMMAND LINE USAGE{Style.RESET_ALL}

{Fore.YELLOW}Usage:{Style.RESET_ALL}
  bsb-havoc [OPTIONS] <target_url>

{Fore.YELLOW}Options:{Style.RESET_ALL}
  -c, --concurrent NUM   Maximum concurrent connections (default: 1000)
  -v, --version          Show version information
  -h, --help             Show this help message

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  bsb-havoc example.com
  bsb-havoc https://example.com
  bsb-havoc -c 5000 http://target-site.com
  bsb-havoc --help

{Fore.YELLOW}Features:{Style.RESET_ALL}
  • {Fore.GREEN}⚡ Extreme Performance{Style.RESET_ALL} - Thousands of concurrent requests
  • {Fore.GREEN}📊 Real-time Analytics{Style.RESET_ALL} - Live statistics and monitoring
  • {Fore.GREEN}🎯 Professional Results{Style.RESET_ALL} - Comprehensive test reports
  • {Fore.GREEN}🚨 Safety Warnings{Style.RESET_ALL} - Clear warnings before destruction
  • {Fore.GREEN}🌈 Colorful Interface{Style.RESET_ALL} - Professional terminal output

{Fore.RED}⚠️  WARNING:{Style.RESET_ALL}
  This tool is designed for legitimate load testing only.
  Use responsibly and only on systems you own or have permission to test.
"""
        print(help_text)
    
    def display_version(self):
        """Display version information"""
        version_info = f"""
{Fore.CYAN}{Style.BRIGHT}BSB HAVOC v{__version__}{Style.RESET_ALL}

{Fore.YELLOW}Platform:{Style.RESET_ALL} {platform.system()} {platform.release()}
{Fore.YELLOW}Python:{Style.RESET_ALL} {platform.python_version()}
{Fore.YELLOW}Architecture:{Style.RESET_ALL} {platform.machine()}

{Fore.GREEN}⚡ The World's Most Powerful Load Testing Tool{Style.RESET_ALL}
"""
        print(version_info)
    
    async def run(self):
        """Main CLI execution"""
        args = self.parse_arguments()
        
        # Display banner
        self.display_banner()
        
        # Handle help
        if args.help:
            self.display_help()
            return 0
        
        # Handle version
        if args.version:
            self.display_version()
            return 0
        
        # Validate target URL
        if not args.target:
            print(f"{Fore.RED}❌ ERROR: Target URL is required!{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Usage:{Style.RESET_ALL} bsb-havoc <target_url>")
            print(f"{Fore.YELLOW}Example:{Style.RESET_ALL} bsb-havoc example.com")
            return 1
        
        try:
            # Validate and normalize URL
            target_url = self.validate_url(args.target)
            
            print(f"{Fore.CYAN}🎯 Target:{Style.RESET_ALL} {target_url}")
            print(f"{Fore.CYAN}⚡ Concurrent Connections:{Style.RESET_ALL} {args.concurrent:,}")
            print(f"{Fore.CYAN}🕐 Started at:{Style.RESET_ALL} {platform.node()}")
            print(f"{Fore.WHITE}{'─' * 80}{Style.RESET_ALL}")
            
            # Create and run havoc engine
            engine = HavocEngine(target_url, args.concurrent)
            await engine.run()
            
            return 0
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}👋 Session terminated by user.{Style.RESET_ALL}")
            return 0
        except Exception as e:
            print(f"\n{Fore.RED}💥 Critical Error:{Style.RESET_ALL} {str(e)}")
            return 1


def main():
    """Entry point for CLI"""
    try:
        cli = BSBHavocCLI()
        if sys.platform == 'win32':
            # Windows event loop policy
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        return asyncio.run(cli.run())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
        return 0


if __name__ == '__main__':
    sys.exit(main())
