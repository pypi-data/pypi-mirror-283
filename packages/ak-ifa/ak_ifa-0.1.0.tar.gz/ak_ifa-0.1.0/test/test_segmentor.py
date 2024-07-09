from unittest import TestCase


from ifa.segmentor import *

class TestSegmentor(TestCase):

    def test_segmentor(self):
        rs = np.random.RandomState(42)
        x = rs.uniform(0, 1, 100).reshape(-1,1)
        segmentor = NtileSegmentor(5)
        self.assertTrue(segmentor.state is None)
        s = segmentor.segment(x, 0)
        self.assertEqual(s.shape, (x.size, 2))
        self.assertTrue(set(np.unique(s[:, 1]).tolist()) == {1., 2., 3., 4., 5.})
        self.assertTrue(np.abs(segmentor.state - np.array([0.00552212, 0.15601382, 0.32867095, 0.57373215, 0.77282238, 0.98688694])).mean() < 1e-8)

        segmentor = NtileSegmentor(10)
        self.assertTrue(segmentor.state is None)
        s = segmentor.segment(x, 0)
        self.assertEqual(s.shape, (x.size, 2))
        self.assertTrue(set(np.unique(s[:, 1]).tolist()) == {1., 2., 3., 4., 5., 6., 7., 8., 9., 10.})
        self.assertTrue(np.abs(segmentor.state - 
                               np.array([0.00552212, 0.07450004, 0.15601382, 0.26757832, 0.32867095, 0.46414245,
                                         0.57373215, 0.69102032, 0.77282238, 0.8879742,  0.98688694])).mean() < 1e-8)

        x[:10] = np.nan
        segmentor = NtileSegmentor(3)
        self.assertTrue(segmentor.state is None)
        s = segmentor.segment(x, 0)
        self.assertEqual(s.shape, (x.size, 2))
        self.assertEqual(len(np.unique(s[:, 1])), 4)
        self.assertTrue(np.all(np.isnan(s[s[:,1] == -1][:,0])))
        self.assertTrue(np.abs(segmentor.state - np.array([0.00552212, 0.29183948, 0.61566797, 0.98688694])).mean() < 
        1e-8)

        x = np.array(['a', 'b', 'c', 'c', np.nan, None]).reshape(-1,1)
        segmentor = CategoricalSegmentor()
        self.assertTrue(segmentor.state is None)
        s = segmentor.segment(x, 0)
        self.assertTrue(s.shape == (6,2))
        self.assertListEqual(s[:,0].tolist(), x.reshape(-1).tolist())
        self.assertEqual(np.unique(s[:,1]).size, 4)
        self.assertDictEqual({'a': 2, 'b': 3, 'c': 1}, segmentor.state)

        # segmentor with top_k = 2
        segmentor = CategoricalSegmentor(2)
        self.assertTrue(segmentor.state is None)
        s = segmentor.segment(x, 0)
        self.assertTrue(s.shape == (6,2))
        self.assertEqual(np.unique(s[:,1]).size, 4)
        self.assertTrue('_other_' in s[:,0].tolist())
        self.assertDictEqual({'a': 2, 'c': 1}, segmentor.state)

        # segmentor with top_k = 1
        segmentor = CategoricalSegmentor(1)
        s = segmentor.segment(x, 0)
        self.assertTrue(s.shape == (6,2))
        self.assertEqual(np.unique(s[:,1]).size, 3)
        self.assertTrue('_other_' in s[:,0].tolist())

        # segmentor with top_k = 1, and other name
        segmentor = CategoricalSegmentor(1, 'xxx')
        s = segmentor.segment(x, 0)
        self.assertTrue(s.shape == (6,2))
        self.assertEqual(np.unique(s[:,1]).size, 3)
        self.assertTrue('xxx' in s[:,0].tolist())