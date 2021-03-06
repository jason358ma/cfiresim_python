from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from market_data.models import DataPoint
from calculator.simulation import Cycle, Segment, run_simulation, Input
from calculator.forms import CalculatorForm
from django.db import connection, reset_queries
from django.test.utils import override_settings


@override_settings(DEBUG=True)
class SimulatorTestCase(TestCase):
    def setUp(self):
        reset_queries()
        self.start_time = datetime.now()
        self.form = CalculatorForm(data={
            'retirement_year': "2017",
            'retirement_end_year': "2046",
            'data_method': 'historical_all',
            'portfolio_value': '1000000',
            'equities': '75',
            'bonds': '25',
            'gold': '0',
            'cash': '0',
            'fees': '0.18',
            'growth_of_cash': '0.25',
            'spending_plan': 'inflation_adjusted',
            'initial_yearly_spending': '40000',
            'ss_annual_value': '0',
            'ss_start_year': '2032',
            'ss_end_year': '2100',
            'ss_spouse_annual_value': '0',
            'ss_spouse_start_year': '2032',
            'ss_spouse_end_year': '2100'
        })
        self.results = run_simulation(self.form) if self.form.is_valid() else None
        self.queries = connection.queries

    # def test_default_form(self):
    #     self.assertTrue(self.form.is_valid())
    #
    # def test_end_inflation_default(self):
    #     cumulative_inflation = round(self.results.sim[-1].cumulative_inflation, 8)
    #     baseline = round(0.63358892, 8)
    #     self.assertEqual(cumulative_inflation, baseline)
    #
    # def test_end_spending_default(self):
    #     spending = round(self.results.sim[-1].spending, 2)
    #     baseline = round(25343.56, 2)
    #     self.assertEqual(spending, baseline)
    #
    # def test_end_inflation_adjusted_spending_default(self):
    #     spending = round(self.results.sim[-1].inflation_adjusted_spending, 2)
    #     baseline = 40000
    #     self.assertEqual(spending, baseline)
    #
    # def test_end_portfolio_default(self):
    #     portfolio = round(self.results.sim[-1].portfolio['end'], 2)
    #     baseline = 3289028.87
    #     self.assertEqual(portfolio, baseline)

    def test_equities_and_bonds_calculations(self):
        equities_growth = round(self.results.sim[0].equities['growth'], 2)
        bonds_growth = round(self.results.sim[0].bonds['growth'], 2)
        baseline_equities_growth = 68108.11
        baseline_bonds_growth = 12096.46
        self.assertEqual(equities_growth, baseline_equities_growth)
        self.assertEqual(bonds_growth, baseline_bonds_growth)

    def tearDown(self):
        self.end_time = datetime.now()
        rd = relativedelta(self.end_time, self.start_time)
        print "Queries:", len(connection.queries)
        print "Unit tests took {} minutes and {} seconds".format(rd.minutes, rd.seconds)



