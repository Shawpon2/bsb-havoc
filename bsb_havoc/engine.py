"""
BSB Havoc Engine - High-Power Async Load Testing Core
⚡ Professional Load Testing Engine with Advanced Features
"""

import asyncio
import aiohttp
import time
import random
import signal
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import statistics
from colorama import Fore, Style, init as colorama_init

colorama_init()

@dataclass
class TestResult:
    """Professional test result structure"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_time: float = 0.0
    requests_per_second: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    avg_response_time: float = 0.0
    median_response_time: float = 0.0
    status_codes: Dict[int, int] = None
    
    def __post_init__(self):
        if self.status_codes is None:
            self.status_codes = {}


class HavocEngine:
    """⚡ High-Power Load Testing Engine"""
    
    def __init__(self, target_url: str, max_concurrent: int = 1000):
        """
        Initialize the Havoc Engine
        
        Args:
            target_url: Target website URL
            max_concurrent: Maximum concurrent connections
        """
        self.target_url = target_url
        self.max_concurrent = max_concurrent
        self.results = TestResult()
        self.response_times: List[float] = []
        self.is_running = False
        self.start_time = 0
        self.session: Optional[aiohttp.ClientSession] = None
        
        # User agents for realistic load
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Mozilla/5.0 (Android 11; Mobile; rv:90.0) Gecko/90.0 Firefox/90.0'
        ]
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals gracefully"""
        print(f"\n\n{Fore.YELLOW}⚠️  INTERRUPT SIGNAL RECEIVED!{Style.RESET_ALL}")
        print(f"{Fore.RED}🚫 Stopping Havoc Engine...{Style.RESET_ALL}")
        self.is_running = False
    
    async def _create_session(self):
        """Create aiohttp session with custom headers"""
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        )
    
    async def _send_request(self, request_id: int) -> Tuple[bool, float, Optional[int]]:
        """
        Send a single HTTP request
        
        Returns:
            Tuple of (success, response_time, status_code)
        """
        if not self.session:
            return False, 0.0, None
        
        start_time = time.time()
        try:
            async with self.session.get(
                self.target_url,
                ssl=False,
                allow_redirects=True,
                timeout=30
            ) as response:
                response_time = time.time() - start_time
                status = response.status
                
                # Read response body to ensure complete request
                await response.read()
                
                return True, response_time, status
                
        except aiohttp.ClientError as e:
            response_time = time.time() - start_time
            return False, response_time, None
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            return False, response_time, None
        except Exception:
            response_time = time.time() - start_time
            return False, response_time, None
    
    async def _worker(self, worker_id: int, semaphore: asyncio.Semaphore):
        """Worker coroutine for sending requests"""
        while self.is_running:
            async with semaphore:
                if not self.is_running:
                    break
                
                success, resp_time, status_code = await self._send_request(worker_id)
                
                # Update statistics
                self.results.total_requests += 1
                
                if success and resp_time > 0:
                    self.results.successful_requests += 1
                    self.response_times.append(resp_time)
                    
                    # Update response time stats
                    self.results.min_response_time = min(self.results.min_response_time, resp_time)
                    self.results.max_response_time = max(self.results.max_response_time, resp_time)
                    
                    # Update status codes
                    if status_code:
                        self.results.status_codes[status_code] = self.results.status_codes.get(status_code, 0) + 1
                else:
                    self.results.failed_requests += 1
    
    async def _monitor(self):
        """Monitor and display real-time statistics"""
        last_count = 0
        last_time = time.time()
        
        while self.is_running:
            await asyncio.sleep(1)
            
            current_time = time.time()
            elapsed = current_time - last_time
            current_count = self.results.total_requests
            
            if elapsed > 0:
                rps = (current_count - last_count) / elapsed
                
                # Calculate real-time statistics
                if self.response_times:
                    avg_time = statistics.mean(self.response_times[-100:]) if len(self.response_times) >= 100 else statistics.mean(self.response_times)
                else:
                    avg_time = 0
                
                # Display stats
                print(f"\r{Fore.CYAN}⚡ REQUESTS: {Fore.WHITE}{current_count:,} | "
                      f"{Fore.GREEN}RPS: {rps:.0f} | "
                      f"{Fore.YELLOW}AVG: {avg_time*1000:.0f}ms | "
                      f"{Fore.GREEN}SUCCESS: {self.results.successful_requests:,} | "
                      f"{Fore.RED}FAILED: {self.results.failed_requests:,}{Style.RESET_ALL}", end="")
                
                last_count = current_count
                last_time = current_time
    
    def _display_final_results(self):
        """Display comprehensive test results"""
        print(f"\n\n{'='*80}")
        print(f"{Fore.CYAN}{Style.BRIGHT}🔥 BSB HAVOC - LOAD TEST RESULTS{' ' * 40}{Style.RESET_ALL}")
        print(f"{'='*80}")
        
        if self.results.total_time > 0:
            self.results.requests_per_second = self.results.total_requests / self.results.total_time
        
        if self.response_times:
            self.results.avg_response_time = statistics.mean(self.response_times)
            self.results.median_response_time = statistics.median(self.response_times)
        
        # Summary Statistics
        print(f"{Fore.YELLOW}📊 SUMMARY STATISTICS:{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}• Target URL:{Style.RESET_ALL} {self.target_url}")
        print(f"  {Fore.WHITE}• Total Duration:{Style.RESET_ALL} {self.results.total_time:.2f} seconds")
        print(f"  {Fore.WHITE}• Total Requests:{Style.RESET_ALL} {self.results.total_requests:,}")
        print(f"  {Fore.WHITE}• Successful Requests:{Style.RESET_ALL} {self.results.successful_requests:,} ({self.results.successful_requests/self.results.total_requests*100:.1f}%)")
        print(f"  {Fore.WHITE}• Failed Requests:{Style.RESET_ALL} {self.results.failed_requests:,} ({self.results.failed_requests/self.results.total_requests*100:.1f}%)")
        print(f"  {Fore.WHITE}• Requests Per Second:{Style.RESET_ALL} {self.results.requests_per_second:.0f}")
        
        # Response Time Analysis
        if self.response_times:
            print(f"\n{Fore.YELLOW}⏱️  RESPONSE TIME ANALYSIS:{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}• Minimum:{Style.RESET_ALL} {self.results.min_response_time*1000:.0f} ms")
            print(f"  {Fore.WHITE}• Maximum:{Style.RESET_ALL} {self.results.max_response_time*1000:.0f} ms")
            print(f"  {Fore.WHITE}• Average:{Style.RESET_ALL} {self.results.avg_response_time*1000:.0f} ms")
            print(f"  {Fore.WHITE}• Median:{Style.RESET_ALL} {self.results.median_response_time*1000:.0f} ms")
            print(f"  {Fore.WHITE}• 95th Percentile:{Style.RESET_ALL} {statistics.quantiles(self.response_times, n=100)[94]*1000:.0f} ms")
        
        # Status Code Distribution
        if self.results.status_codes:
            print(f"\n{Fore.YELLOW}📈 STATUS CODE DISTRIBUTION:{Style.RESET_ALL}")
            for code, count in sorted(self.results.status_codes.items()):
                percentage = (count / self.results.total_requests) * 100
                color = Fore.GREEN if code < 300 else Fore.YELLOW if code < 400 else Fore.RED
                print(f"  {color}{code}:{Style.RESET_ALL} {count:,} ({percentage:.1f}%)")
        
        print(f"{'='*80}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}🚀 Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{'='*80}\n")
    
    async def run(self):
        """
        Run the load test
        
        Returns:
            TestResult object with comprehensive statistics
        """
        print(f"\n{Fore.RED}{Style.BRIGHT}⚠️  WARNING: This tool generates extreme load!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Press {Fore.WHITE}Ctrl+C{Fore.YELLOW} or {Fore.WHITE}Ctrl+Z{Fore.YELLOW} to stop the test immediately!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Continuing will potentially take down the target!{Style.RESET_ALL}\n")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"{Fore.RED}{'🚨' * i} Starting in {i} seconds...{'🚨' * i}{Style.RESET_ALL}", end="\r")
            await asyncio.sleep(1)
        
        print("\n" + " " * 100, end="\r")
        
        # Start the test
        self.is_running = True
        self.start_time = time.time()
        
        # Create session
        await self._create_session()
        
        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        # Create worker tasks
        workers = [
            asyncio.create_task(self._worker(i, semaphore))
            for i in range(self.max_concurrent)
        ]
        
        # Start monitoring
        monitor_task = asyncio.create_task(self._monitor())
        
        try:
            # Run until interrupted
            while self.is_running:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            print(f"\n\n{Fore.RED}🛑 Keyboard Interrupt Detected! Stopping...{Style.RESET_ALL}")
            self.is_running = False
        finally:
            # Calculate total time
            self.results.total_time = time.time() - self.start_time
            
            # Cancel all workers
            for worker in workers:
                worker.cancel()
            
            # Cancel monitor
            monitor_task.cancel()
            
            # Close session
            if self.session:
                await self.session.close()
            
            # Wait for tasks to complete
            await asyncio.gather(*workers, return_exceptions=True)
            await asyncio.gather(monitor_task, return_exceptions=True)
            
            # Display final results
            self._display_final_results()
        
        return self.results
