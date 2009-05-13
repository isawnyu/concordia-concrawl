from datetime import datetime
import logging
import time

import multiprocessing
from multiprocessing import Process, current_process
from multiprocessing.managers import BaseManager

from zc.dict import Dict, OrderedDict


class Crawler(Process):
    
    """Implements a crawling loop.
    
    Reference:
    Crawling the Web: Gautam Pant, Padmini Srinivasan, and Filippo 
    Menczer
    
    http://dollar.biz.uiowa.edu/~fil/Papers/crawling.pdf
    http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.14.1830
    """
    
    def __init__(self, horizon, current, history):
        super(Crawler, self).__init__()
        self.horizon = horizon
        self.current = current
        self.history = history
    
    def wait(self):
        time.sleep(3.0)
    
    def run(self):
        logger = multiprocessing.get_logger()
        horizon = self.horizon
        current = self.current
        history = self.history
        
        # Main loop
        while 1:
            timestamp = datetime.now()
            try:
                hitem = horizon.popitem()
            except KeyError:
                hitem = None
            
            # Horizon could be empty at any time
            if hitem is None:
                # If there's nothing to wait for, break out of loop.
                # Otherwise, wait.
                if len(current.keys()) == 0:
                    logger.debug("[%s] Nothing to wait for, returning: %s",
                             str(timestamp),  str(current_process())
                             )
                    break
                else:
                    logger.debug("[%s] Waiting for new horizon items: %s",
                             str(timestamp),  str(current_process())
                             )
                    self.wait()
                    continue
            
            # We do have an item from the crawl horizon
            key, val = hitem
            logger.debug("[%s] Horizon popped: %s, %s, %s",
                         str(timestamp),  str(current_process()), key, val
                         )
            
            # Fetch and parse document if it hasn't already been done
            if key not in history.keys():
                current[key] = val
                logger.log(51, "[%s] Process %s working on %s",
                           str(timestamp), str(current_process()), key
                           )
                self.wait() # simulate parsing
                history[key] = current.pop(key)
            
            # end of loop inner
        
        # end


class SharedData(BaseManager):
    pass

dict_methods = ['update', 'keys', 'items', 'pop', 'popitem', '__setitem__', '__getitem__', '__len__']

SharedData.register('Horizon', OrderedDict, exposed=dict_methods)
SharedData.register('History', OrderedDict, exposed=dict_methods)
SharedData.register('Current', Dict, exposed=dict_methods)


if __name__ == '__main__':
    
    multiprocessing.log_to_stderr(logging.ERROR)
    
    d = SharedData()
    d.start()
    horizon = d.Horizon()
    seeds = [
        ('http://atlantides.org/where-demo.html', 1.0),
        ('http://pleiades.stoa.org', 1.0)
        ]
    horizon.update(seeds)
    history = d.History()
    current = d.Current()
    
    crawls = []
    for i in range(4):
        p = Crawler(horizon, current, history)
        crawls.append(p)
        p.start()
    
    for p in crawls:
        p.join()
    
    print "Horizon: ", list(horizon.items())
    print "History: ", list(history.items())
    