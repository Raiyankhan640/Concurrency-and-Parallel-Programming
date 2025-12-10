"""
Producer-Consumer Problem Simulation: Bakery Model
This module simulates a bakery where producers (bakers) create items and 
consumers (customers) consume them using a thread-safe queue.
Demonstrates proper synchronization to prevent buffer overflow/underflow.
"""

import threading
import time
import queue
import random

class BakerySimulation:
    """
    A bakery simulation with bakers (producers) and customers (consumers)
    sharing a limited basket using a thread-safe queue.
    """
    def __init__(self, max_basket_size=5, total_items=12):
        """
        Initialize the bakery simulation.
        
        Args:
            max_basket_size (int): Maximum capacity of the shared basket.
            total_items (int): Total number of items to produce before stopping.
        """
        self.basket = queue.Queue(maxsize=max_basket_size)
        self.total_items = total_items
        self.items_produced = 0
        self.items_consumed = 0
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        
    def baker(self, name):
        """
        Baker thread function - produces bread items.
        
        Args:
            name (str): Name of the baker thread.
        """
        while not self.stop_event.is_set():
            with self.lock:
                if self.items_produced >= self.total_items:
                    self.stop_event.set()
                    break
                
                bread_id = self.items_produced
                self.items_produced += 1
            
            # Simulate bread preparation time
            prep_time = random.uniform(0.3, 0.8)
            time.sleep(prep_time)
            
            bread_item = f"Bread-{bread_id} by {name}"
            
            # Add to basket - blocks if basket is full
            try:
                self.basket.put(bread_item, timeout=2)
                basket_size = self.basket.qsize()
                print(f"[{name}] baked {bread_item} | Basket: {basket_size}/{self.basket.maxsize}")
            except queue.Full:
                print(f"[{name}] WARNING: Basket full! Waiting for space...")
                continue
        
        print(f"[{name}] Finished work. Total baked: {bread_id + 1}")
    
    def customer(self, name):
        """
        Customer thread function - consumes bread items.
        
        Args:
            name (str): Name of the customer thread.
        """
        while not self.stop_event.is_set() or not self.basket.empty():
            try:
                # Get bread from basket - blocks if basket is empty
                bread_item = self.basket.get(timeout=2)
                
                # Simulate eating time
                eat_time = random.uniform(0.5, 1.5)
                time.sleep(eat_time)
                
                with self.lock:
                    self.items_consumed += 1
                
                basket_size = self.basket.qsize()
                print(f"  -> [{name}] ate {bread_item} | Basket: {basket_size}/{self.basket.maxsize}")
                
                # Mark task as done for queue.join()
                self.basket.task_done()
                
            except queue.Empty:
                if self.stop_event.is_set():
                    break
                print(f"  -> [{name}] Basket empty, waiting for fresh bread...")
        
        print(f"  -> [{name}] Finished eating.")
    
    def run(self):
        """
        Run the complete bakery simulation.
        """
        print("=" * 50)
        print("BAKERY SIMULATION - Producer-Consumer Pattern")
        print("=" * 50)
        print(f"Configuration: {self.total_items} total items, Basket size: {self.basket.maxsize}")
        print("-" * 50)
        
        # Create thread lists
        bakers = [
            threading.Thread(target=self.baker, args=("Baker-1",)),
            threading.Thread(target=self.baker, args=("Baker-2",))
        ]
        
        customers = [
            threading.Thread(target=self.customer, args=("Customer-1",)),
            threading.Thread(target=self.customer, args=("Customer-2",))
        ]
        
        # Record start time
        start_time = time.time()
        
        # Start all threads
        print("\nStarting bakery operations...")
        for thread in bakers + customers:
            thread.start()
        
        # Wait for all bakers to finish
        for baker_thread in bakers:
            baker_thread.join()
        
        # Signal customers that production has stopped
        self.stop_event.set()
        
        # Wait for customers to finish consuming remaining items
        for customer_thread in customers:
            customer_thread.join()
        
        # Wait for basket to be completely empty
        self.basket.join()
        
        # Calculate statistics
        duration = time.time() - start_time
        
        print("\n" + "=" * 50)
        print("SIMULATION COMPLETE - SUMMARY")
        print("=" * 50)
        print(f"Total items produced: {self.items_produced}")
        print(f"Total items consumed: {self.items_consumed}")
        print(f"Items remaining in basket: {self.basket.qsize()}")
        print(f"Total simulation time: {duration:.2f} seconds")
        print("=" * 50)

if __name__ == "__main__":
    """
    Main execution block for the Producer-Consumer simulation.
    Demonstrates how a thread-safe queue prevents race conditions
    and handles full/empty conditions gracefully.
    """
    # Run simulation
    bakery = BakerySimulation(max_basket_size=5, total_items=12)
    bakery.run()