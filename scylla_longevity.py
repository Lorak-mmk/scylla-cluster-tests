#!/usr/bin/env python

from avocado import main

from sdcm.tester import ClusterTester
from sdcm.nemesis import StopStartMonkey
from sdcm.nemesis import DecommissionMonkey


class LongevityTest(ClusterTester):

    """
    Test a Scylla cluster stability over a time period.

    :avocado: enable
    """

    def test_20_minutes(self):
        """
        Run a very short test, as a config/code sanity check.
        """
        self.db_cluster.add_nemesis(StopStartMonkey)
        self.db_cluster.start_nemesis(interval=5)
        self.run_stress(duration=20)

    def test_12_hours(self):
        self.db_cluster.add_nemesis(StopStartMonkey)
        self.db_cluster.start_nemesis(interval=30)
        self.run_stress(duration=60 * 12)

    def test_1_day(self):
        self.db_cluster.add_nemesis(StopStartMonkey)
        self.db_cluster.start_nemesis(interval=30)
        self.run_stress(duration=60 * 24)

    def test_1_week(self):
        self.db_cluster.add_nemesis(StopStartMonkey)
        self.db_cluster.start_nemesis(interval=30)
        self.run_stress(duration=60 * 24 * 7)

if __name__ == '__main__':
    main()
