import json
import os
import unittest
from app import app


class AppEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_move_endpoint_updates_state(self):
        with self.client as c:
            # populate session with a simple board and tile_map
            with c.session_transaction() as sess:
                sess['current_state'] = [[1,2,3],[4,0,5],[6,7,8]]
                # use simple filenames
                sess['tile_map'] = { '1':'t1.png','2':'t2.png','3':'t3.png','4':'t4.png','5':'t5.png','6':'t6.png','7':'t7.png','8':'t8.png','0':None }

            # move tile 5 into blank (they are adjacent)
            resp = c.post('/move', data=json.dumps({'tile':5}), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertTrue(data.get('ok'))
            self.assertIn('state', data)
            # after move, blank should be where 5 was
            self.assertEqual(data['state'][1][2], 0)
            self.assertIn('tile_map', data)

    def test_shuffle_redirects_to_puzzle(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_state'] = [[1,2,3],[4,5,6],[7,8,0]]
            resp = c.post('/shuffle', follow_redirects=False)
            # should redirect to /puzzle
            self.assertIn(resp.status_code, (302, 303))
            self.assertTrue(resp.headers.get('Location').endswith('/puzzle'))


if __name__ == '__main__':
    unittest.main()
