annual_salary = float(input('Enter the starting salary: '))

# bisection search endpoints
min_savings_rate = 0
max_savings_rate = 10000

# constants
total_cost = 1000000
semi_annual_raise = 0.07
portion_down_payment = 0.25
r = 0.04
down_payment = portion_down_payment * total_cost

# accumulators
steps = 0
dp_savings_diff = down_payment  # savings is 0


def calculate_dp_savings_diff(savings_rate, salary):
    """
    Calculates the difference between the down payment and savings accumulated
    over 36 months for the given savings rate and salary.

    :param savings_rate: The savings rate to accumulate savings at.
    :type savings_rate: int
    :param salary: The annual salary to accumulate savings with.
    :type salary: int
    :returns: The difference between the down payment and accumulated savings
    :rtype: int
    """
    current_savings = 0.0
    months = 0

    while months < 36:
        return_on_investment = current_savings * r / 12
        portion_monthly_salary = savings_rate * salary / 120000
        current_savings += return_on_investment + portion_monthly_salary
        months += 1

        if (months % 6 == 0):  # Increment salary after every 6th month
            salary *= 1 + semi_annual_raise

    return down_payment - current_savings


if calculate_dp_savings_diff(max_savings_rate, annual_salary) > 0:
    print('It is not possible to pay the down payment in three years.')
    exit()

"""
Stop finding a savings rate when the savings amount is within $100 from
the down payment, or the algorithm cannot find a more precise savings rate
since the savings rate is limited to 2 decimal places.
"""
while dp_savings_diff > 100 and max_savings_rate - min_savings_rate > 1:
    mp_savings_rate = int((min_savings_rate + max_savings_rate) / 2)
    min_diff = calculate_dp_savings_diff(min_savings_rate, annual_salary)
    mp_diff = calculate_dp_savings_diff(mp_savings_rate, annual_salary)

    """
    Modify binary search endpoints, following the Intermediate Value Theorem.
    If the the interval between the midpoint and maximum savings rates includes
    the target, the difference between their accumulated savings and down
    payment will share the same sign; thus, set the minimum savings rate to the
    midpoint savings rate, and vice versa.
    """
    if (min_diff > 0) == (mp_diff > 0):
        min_savings_rate = mp_savings_rate
    else:
        max_savings_rate = mp_savings_rate

    steps += 1
    dp_savings_diff = abs(mp_diff)

print('Best savings rate: {:0.4f}'.format(mp_savings_rate / 10000))
print('Steps in the bisection search: %d' % steps)
