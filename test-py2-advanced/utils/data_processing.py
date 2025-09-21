#!/usr/bin/env python2
"""
Data processing utilities with Python 2 patterns
"""

import pickle as pickle
import io as StringIO
import _thread
import threading
import queue
from sets import Set

class DataProcessor(object):
    """Data processor using Python 2 patterns"""
    
    def __init__(self):
        self.data_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.worker_threads = []
        
    def process_with_pickle(self, data):
        """Serialize/deserialize data using cPickle"""
        print("Processing data with cPickle...")
        
        try:
            # Serialize
            buffer = StringIO.StringIO()
            pickle.dump(data, buffer)
            serialized = buffer.getvalue()
            buffer.close()
            
            print("Serialized %d bytes" % len(serialized))
            
            # Deserialize
            buffer = StringIO.StringIO(serialized)
            restored = pickle.load(buffer)
            buffer.close()
            
            print("Deserialized successfully")
            return restored
            
        except Exception as e:
            print("Pickle error:", e)
            return None
    
    def worker_function(self, worker_id):
        """Worker thread function"""
        print("Worker %d started" % worker_id)
        
        while True:
            try:
                # Get item from queue with timeout
                item = self.data_queue.get(timeout=1.0)
                
                if item is None:  # Poison pill
                    print("Worker %d shutting down" % worker_id)
                    break
                
                # Process item
                print("Worker %d processing:" % worker_id, item)
                result = self.process_item(item)
                
                # Put result
                self.result_queue.put(result)
                self.data_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print("Worker %d error:" % worker_id, e)
    
    def process_item(self, item):
        """Process individual item"""
        import time
        time.sleep(0.1)  # Simulate work
        
        if isinstance(item, str):
            return item.upper()
        elif isinstance(item, int):
            return item * 2
        else:
            return str(item)
    
    def start_workers(self, num_workers=3):
        """Start worker threads using old threading"""
        print("Starting %d worker threads..." % num_workers)
        
        for i in range(num_workers):
            # Using old thread.start_new_thread
            try:
                thread_id = _thread.start_new_thread(self.worker_function, (i,))
                print("Started thread %d" % i)
            except Exception as e:
                print("Failed to start thread %d:" % i, e)
                
                # Fallback to threading module
                worker = threading.Thread(target=self.worker_function, args=(i,))
                worker.daemon = True
                worker.start()
                self.worker_threads.append(worker)
    
    def process_batch(self, items):
        """Process batch of items"""
        print("Processing batch of %d items" % len(items))
        
        # Add items to queue
        for item in items:
            self.data_queue.put(item)
        
        # Wait for completion
        self.data_queue.join()
        
        # Collect results
        results = []
        while not self.result_queue.empty():
            try:
                result = self.result_queue.get_nowait()
                results.append(result)
            except queue.Empty:
                break
        
        return results

def test_sets():
    """Test Python 2 sets module"""
    print("Testing sets module...")
    
    # Create sets using old sets module
    set1 = Set([1, 2, 3, 4, 5])
    set2 = Set([4, 5, 6, 7, 8])
    
    print("Set 1:", set1)
    print("Set 2:", set2)
    print("Union:", set1.union(set2))
    print("Intersection:", set1.intersection(set2))
    print("Difference:", set1.difference(set2))
    
    # Test set operations
    set1.add(10)
    print("After adding 10:", set1)
    
    set1.discard(1)
    print("After removing 1:", set1)

def test_data_types():
    """Test Python 2 data type patterns"""
    print("Testing Python 2 data types...")
    
    # Long integers
    big_num = 123456789012345678901234567890
    print("Long integer:", big_num, type(big_num))
    
    # Octal literals
    octal_num = 0o755
    print("Octal literal:", octal_num, oct(octal_num))
    
    # String vs Unicode
    byte_str = "byte string"
    unicode_str = "unicode string with émojis 🚀"
    
    print("Byte string:", repr(byte_str), type(byte_str))
    print("Unicode string:", repr(unicode_str), type(unicode_str))
    
    # Buffer type (if available)
    try:
        buf = buffer(byte_str, 2, 4)
        print("Buffer:", repr(buf), type(buf))
    except NameError:
        print("buffer type not available")

if __name__ == "__main__":
    print("Data processing utilities test")
    print("=" * 50)
    
    # Test data processor
    processor = DataProcessor()
    
    # Test pickle
    test_data = {"name": "test", "values": [1, 2, 3], "unicode": "café"}
    restored = processor.process_with_pickle(test_data)
    print("Pickle test result:", restored)
    print()
    
    # Test sets
    test_sets()
    print()
    
    # Test data types
    test_data_types()
    print()
    
    # Test threading (commented out to avoid hanging)
    # processor.start_workers(2)
    # items = ["hello", "world", 42, 3.14, u"unicode"]
    # results = processor.process_batch(items)
    # print "Batch processing results:", results