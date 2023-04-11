#!/usr/bin/env python3
"""
Example of usage/test of Cart controller implementation.
"""

import sys
from cartctl import CartCtl, Status as StatusC
from cart import Cart, CargoReq, Status, CartError
from jarvisenv import Jarvis
import unittest

def log(msg):
    "simple logging"
    print('  %s' % msg)

class TestCartRequests(unittest.TestCase):

    def test_happy(self):
        "Happy-path test"

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'helmet':
                self.assertEqual('B', c.pos)
            if cargo_req.content == 'heart':
                self.assertEqual('A', c.pos)
            #if cargo_req.content.startswith('bracelet'):
            #    self.assertEqual('C', c.pos)
            if cargo_req.content == 'braceletR':
                self.assertEqual('A', c.pos)
            if cargo_req.content == 'braceletL':
                self.assertEqual('C', c.pos)

        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 20, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 40, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        braceletR = CargoReq('D', 'A', 40, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload

        braceletL = CargoReq('D', 'C', 40, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(45, add_load, (c,heart))
        Jarvis.plan(40, add_load, (c,braceletR))
        Jarvis.plan(25, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   SUT is the Cart.
        #   Exercise means calling Cart.request in different time periods.
        #   Requests are called by add_load (via plan and its scheduler).
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', helmet.context)
        self.assertEqual('unloaded', heart.context)
        self.assertEqual('unloaded', braceletR.context)
        self.assertEqual('unloaded', braceletL.context)
        #self.assertEqual(cart_dev.pos, 'C')


    # CEG - 1. Test (without request)
    def testWithoutRequest(self):
        "testWithoutRequest"
        def on_move(c: Cart):
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))
            self.fail("Error: cart can not move anywhere.")
        
        # Setup cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)
        
        # Setup Plan
        Jarvis.reset_scheduler()
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output 
        self.assertTrue(cart_dev.empty())
        self.assertEqual(Status.Idle, cart_dev.status)
        self.assertEqual([None, None, None, None], cart_dev.slots)
        self.assertEqual('A', cart_dev.pos)

    # CEG - 2. Test (without priority)
    def testWithNormalRequest(self):
        "testWithNormalRequest"

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            self.assertEqual('A', cart_dev.pos)
            self.assertEqual('helmet', cargo_req.content)
            self.assertIn(cargo_req, cart_dev.slots)
            self.assertLess(Jarvis.time(), cargo_req.born + 60)
            self.assertTrue(cargo_req.onload)
            self.assertFalse(cargo_req.prio)
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            self.assertEqual('loaded', cargo_req.context)
            self.assertEqual('B', c.pos)
            self.assertEqual('helmet', cargo_req.content)
            self.assertNotIn(cargo_req, cart_dev.slots)
            self.assertTrue(cargo_req.onunload)
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = 'unloaded'
            
        # Setup Cart
        # 2 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(2, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 120, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertTrue(cart_dev.empty())
        self.assertEqual(Status.Idle, cart_dev.status)
        self.assertEqual('B', cart_dev.pos)

    # CEG - 3. Test (with priority)
    def testWithPriorityRequest(self):
        "testWithPriorityRequest"

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            self.assertTrue(cargo_req.prio)
            self.assertGreaterEqual(Jarvis.time(), cargo_req.born + 60)
            self.assertLess(Jarvis.time(), cargo_req.born + 120)
            self.assertIn(cargo_req, cart_dev.slots)
            self.assertTrue(cargo_req.onload)
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            #self.assertNotIn(cargo_req, c.slots)
            if cargo_req.content == 'helmet':
                self.assertEqual('B', c.pos)
                self.assertEqual('helmet', cargo_req.content)
            if cargo_req.content == 'heart':
                self.assertEqual('A', c.pos)
                self.assertEqual('heart', cargo_req.content)

            self.assertTrue(cargo_req.onunload)
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = 'unloaded'
            
        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 30, 'helmet')
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 140, 'heart')
        heart.onunload = on_unload

        braceletL = CargoReq('D', 'C', 30, 'braceletL')
        braceletL.onload = on_load

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(20, add_load, (c,heart))
        Jarvis.plan(40, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertTrue(cart_dev.empty())
        self.assertEqual(Status.Idle, cart_dev.status)
        self.assertEqual('C', cart_dev.pos)

    # CEG - 4. Test (problem with slot capacity)
    def testOnCapacity(self):
        "testOnCapacity"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            self.assertEqual(c.load_capacity, 150)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"

            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)

        # Setup Cart
        # 2 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(2, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'C', 70, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('A', 'C', 80, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        braceletR = CargoReq('C', 'B', 80, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload

        braceletL = CargoReq('C', 'B', 70, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(15, add_load, (c,heart))
        Jarvis.plan(55, add_load, (c,braceletR))
        Jarvis.plan(25, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertEqual(None, heart.context)

    # Combine tests
    def test1(self):
        "test1"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            self.fail("Error: cart shoul not load stuff.")

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            self.fail("Error: cart shoul not unload stuff.")
        
        # Setup Cart
        # 2 slots, 50 kg max payload capacity, 2=max debug
        cart_dev = Cart(2, 50, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 80, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(0, add_load, (c,helmet))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertTrue(cart_dev.empty())
        self.assertEqual(Status.Idle, cart_dev.status)
        self.assertEqual('A', cart_dev.pos)

    def test2(self):
        "test2"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            self.assertEqual(c.load_capacity, 50)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
        
        # Setup Cart
        # 3 slots, 50 kg max payload capacity, 2=max debug
        cart_dev = Cart(3, 50, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'C', 20, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('A', 'C', 30, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        braceletR = CargoReq('C', 'B', 30, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload

        braceletL = CargoReq('C', 'B', 20, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(16, add_load, (c,heart))
        Jarvis.plan(56, add_load, (c,braceletR))
        Jarvis.plan(26, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertEqual(None, heart.context)

    def test3(self):
        "test3"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            if (cargo_req.content == 'helmet'):
                self.fail("Error: cart shoul not load stuff.")
            if (cargo_req.content == 'heart'):
                self.fail("Error: cart shoul not load stuff.")
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
        
        # Setup Cart
        # 1 slot, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(1, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 700, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 1000, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(20, add_load, (c,heart))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertEqual(None, helmet.context)
        self.assertEqual(None, heart.context)

    def test4_6(self):
        "test4_6"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            self.assertTrue(cargo_req.prio)
            self.assertTrue(cargo_req.onload)
            self.assertIn(cargo_req, cart_dev.slots)
            self.assertLess(Jarvis.time(), cargo_req.born + 120)
            self.assertGreaterEqual(Jarvis.time(), cargo_req.born + 60)
        
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            #self.assertNotIn(cargo_req, c.slots)
            if cargo_req.content == 'helmet':
                self.assertEqual('helmet', cargo_req.content)
                self.assertEqual('B', c.pos)
            if cargo_req.content == 'heart':
                self.assertEqual('heart', cargo_req.content)
                self.assertEqual('A', c.pos)
            self.assertTrue(cargo_req.onunload)
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = 'unloaded'
            
        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(2, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 20, 'helmet')
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 150, 'heart')
        heart.onunload = on_unload

        braceletL = CargoReq('D', 'C', 20, 'braceletL')
        braceletL.onload = on_load

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(20, add_load, (c,helmet))
        Jarvis.plan(30, add_load, (c,heart))
        Jarvis.plan(50, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertTrue(cart_dev.empty())
        self.assertEqual('C', cart_dev.pos)
        self.assertEqual(Status.Idle, cart_dev.status)

    def test5(self):
        "test5"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            if (cargo_req.content == 'helmet'):
                self.assertEqual('A', cart_dev.pos)
                self.assertEqual('helmet', cargo_req.content)
            self.assertIn(cargo_req, cart_dev.slots)
            self.assertLess(Jarvis.time(), cargo_req.born + 60)
            self.assertTrue(cargo_req.onload)
            self.assertFalse(cargo_req.prio)
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
        
        # Setup Cart
        # 1 slot, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(3, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 70, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload


        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertTrue(cart_dev.empty())
        self.assertEqual(Status.Idle, cart_dev.status)
        self.assertEqual('B', cart_dev.pos)

    def test7(self):
        "test7"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            self.assertEqual(c.load_capacity, 500)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"

            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)

        # Setup Cart
        # 2 slots, 500 kg max payload capacity, 2=max debug
        cart_dev = Cart(2, 500, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'C', 240, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('A', 'C', 260, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        braceletR = CargoReq('C', 'B', 260, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload

        braceletL = CargoReq('C', 'B', 240, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(20, add_load, (c,heart))
        Jarvis.plan(50, add_load, (c,braceletR))
        Jarvis.plan(30, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertEqual(None, heart.context)
    
    def test8(self):
        "test8"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            self.assertEqual(c.load_capacity, 150)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"

            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)

        # Setup Cart
        # 1 slot, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(1, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'C', 60, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('A', 'C', 90, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        braceletR = CargoReq('C', 'B', 90, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload

        braceletL = CargoReq('C', 'B', 60, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(15, add_load, (c,heart))
        Jarvis.plan(55, add_load, (c,braceletR))
        Jarvis.plan(30, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertEqual(None, heart.context)

    def test9(self):
        "test9"
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            if (cargo_req.content == 'helmet'):
                self.fail("Error: cart shoul not load helmet.")
            if (cargo_req.content == 'heart'):
                self.fail("Error: cart shoul not load heart.")

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            self.fail("Error: cart shoul not unload stuff.")
        
        # Setup Cart
        # 2 slots, 50 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 50, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 80, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 80, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(0, add_load, (c,helmet))
        
        # Exercise + Verify indirect output
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        self.assertTrue(cart_dev.empty())
        self.assertEqual(Status.Idle, cart_dev.status)
        self.assertEqual('A', cart_dev.pos)

if __name__ == "__main__":
    unittest.main()
