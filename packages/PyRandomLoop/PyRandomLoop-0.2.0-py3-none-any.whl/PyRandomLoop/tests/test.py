import os
import unittest
from PyRandomLoop.core.rpm import RPM
from PyRandomLoop.core.utils import *


class Test(unittest.TestCase):
    def setUp(self):
        # Setup mock RPM object
        self.rpm = RPM(3, 32, 32)
        self.rpm.step(100_000, progress_bar=False)

    def test_rpm_init(self):
        try:
            m = RPM(3, 32, 32)
        except Exception as e:
            self.fail(f'RPM class init failed: {e}')

    def test_random_init(self):
        try:
            self.rpm.random_init()
        except Exception as e:
            self.fail(f'random_init failed: {e}')

    def test_build_snake(self):
        try:
            self.rpm.build_snake()
        except Exception as e:
            self.fail(f'build_snake failed: {e}')

    def test_build_donut(self):
        try:
            self.rpm.build_donut()
        except Exception as e:
            self.fail(f'build_donut failed: {e}')

    def test_uniform_init(self):
        try:
            self.rpm.uniform_init(k=2)
        except Exception as e:
            self.fail(f'uniform_init failed: {e}')

    def test_step(self):
        try:
            self.rpm.step(100_000, progress_bar=False)
        except Exception as e:
            self.fail(f'step failed: {e}')

    def test_loop_builder(self):
        try:
            l1, l2, l3 = self.rpm.loop_builder()
        except Exception as e:
            self.fail(f'loop_builder failed: {e}')

    def test_summary(self):
        try:
            s = self.rpm.summary()
        except Exception as e:
            self.fail(f'summary failed: {e}')

    def test_save_load_data(self):
        try:
            self.rpm.save_data('test.json')
        except Exception as e:
            self.fail(f'save_data failed: {e}')

        try:
            self.rpm.load_data('test.json')
        except Exception as e:
            self.fail(f'load_data failed: {e}')

        try:
            self.rpm.clear_data()
        except Exception as e:
            self.fail(f'clear_data failed: {e}')

    def test_visualization_methods(self):
        self.rpm.step(100_000, sample_rate=10_000, progress_bar=False, observables=[self.rpm.get_grid])
        loops, l1, l2 = self.rpm.loop_builder()
        try:
            plot = self.rpm.plot_loop_overlap(loops)
        except Exception as e:
            self.fail(f'plot_loop_overlap failed: {e}')

        try:
            plot = self.rpm.plot_grid()
        except Exception as e:
            self.fail(f'plot_grid failed: {e}')

        try:
            plot = self.rpm.plot_overlap()
        except Exception as e:
            self.fail(f'plot_overlap failed: {e}')

        try:
            ani = self.rpm.animate()
        except Exception as e:
            self.fail(f'animate failed: {e}')


    
        
def main():
    unittest.main()
    if os.path.exists('test.json'):
        os.remove('test.json')
    
if __name__ == '__main__':
    main()
    