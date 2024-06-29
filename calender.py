
activity_dates = ['1/1/2025', '2/1/2025', '3/1/2025', '4/1/2025', '5/1/2025', '6/1/2025'] 
workers = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan']
experties = ['a', 'b', 'c', 'd']

workers_experties = {
    'Alice': ['a', 'b', 'c'], 
    'Bob': ['c', 'b'], 
    'Charlie': ['a', 'd'], 
    'David': ['b', 'c'], 
    'Eve': ['a', 'b', 'c', 'd'], 
    'Frank': ['a', 'b', 'c', 'd'], 
    'Grace': ['d', 'b'], 
    'Heidi': ['d'], 
    'Ivan': ['a', 'c']
}

workers_availability = {
    'Alice': ['2/1/2025', '3/1/2025', '4/1/2025', '5/1/2025'], 
    'Bob': ['5/1/2025', '6/1/2025'], 
    'Charlie': ['1/1/2025',  '3/1/2025', '4/1/2025', '5/1/2025', '6/1/2025'], 
    'David': ['1/1/2025', '2/1/2025', '3/1/2025', '4/1/2025', '5/1/2025', '6/1/2025'], 
    'Eve': ['1/1/2025', '2/1/2025',  '5/1/2025', '6/1/2025'], 
    'Frank': [ '2/1/2025', '3/1/2025', '4/1/2025', '5/1/2025', '6/1/2025'], 
    'Grace': ['1/1/2025', '2/1/2025', '3/1/2025', '4/1/2025', '5/1/2025', '6/1/2025'], 
    'Heidi': ['1/1/2025', '5/1/2025', '6/1/2025'], 
    'Ivan': ['1/1/2025', '2/1/2025', '3/1/2025', '4/1/2025']
}
workers_max_work_days = {
    'Alice': 3, 
    'Bob': 2, 
    'Charlie': 3, 
    'David': 5, 
    'Eve': 4, 
    'Frank': 1, 
    'Grace': 4, 
    'Heidi': 1, 
    'Ivan': 2
}

mandatory_experties = {'a': 1, 'b': 2, 'c': 1, 'd': 0} # maybe should change according to the date
num_of_workers_per_day = 5

def find_workers_for_date(date):
    # mandatory_experties_copy = mandatory_experties.copy() 
    workers_for_date = []
    for date in activity_dates:
        # find available workers for this date
        available_workers = []
        for worker in workers:
            if date in workers_availability[worker]:
                available_workers.append(worker)
        # # find the workers for the activity
        # for experty in mandatory_experties_copy:
        #     if mandatory_experties_copy[experty] > 0:
        #         for worker in available_workers:
        #             if experty in workers_experties[worker]:
        #                 mandatory_experties_copy[experty] -= 1
        #                 workers_for_date.append(worker)
        #                 available_workers.remove(worker)
    return workers_for_date

def find_workers_with_special_experties():
    workers_with_special_experties = []
    for worker in workers:
        if len(workers_experties[worker]) == len(experties):
            workers_with_special_experties.append(worker)
    return workers_with_special_experties

def schedual_workers():
    for date in activity_dates:
        # sort workers by the max work days devided by the number of days they can work. pay attention to devided by zero
        workers_sorted = sorted(workers, key=lambda worker: workers_max_work_days[worker]/len(workers_availability[worker]) if len(workers_availability[worker]) > 0 else workers_max_work_days[worker])
        # workers_sorted = sorted(workers, key=lambda worker: workers_max_work_days[worker]/len(workers_availability[worker]))
        # filter the workers that can work in this date
        workers_sorted = [worker for worker in workers_sorted if date in workers_availability[worker]]
        # for each experty in mandatory_experties, book the first worker that has this experty
        experties_to_book = mandatory_experties.copy()
        num_of_workers_booked = num_of_workers_per_day
        for experty in experties_to_book:
            # todo sort the experties by the rearest experty
            workers_with_experty = [worker for worker in workers_sorted if experty in workers_experties[worker]]
            while experties_to_book[experty] > 0:
                if len(workers_with_experty) > 0:
                    worker = workers_with_experty[0]
                    workers_sorted.remove(worker)
                    workers_with_experty.remove(worker)
                    workers_max_work_days[worker] -= 1
                    # remove all the required experties on this date
                    for worker_experty in workers_experties[worker]:
                        experties_to_book[worker_experty] -= 1
                    num_of_workers_booked -= 1
                    print(worker, date)
                else: 
                    print(f'no more workers with experty {experty} on date {date}')
                    break
        # count all experties that could not be booked
        experties_not_booked = sum([experties_to_book[experty] for experty in experties_to_book if experties_to_book[experty] > 0])
        # book the rest of the workers
        # todo: take the workers with the least experties
        while num_of_workers_booked > experties_not_booked:
            for worker in workers_sorted:
                workers_sorted.remove(worker)
                workers_max_work_days[worker] -= 1
                print(worker, date)
                num_of_workers_booked -= 1

        # remove the date from the availability
        for worker in workers:
            if date in workers_availability[worker]:
                workers_availability[worker].remove(date)

if __name__ == '__main__':
    schedual_workers()


    
# option for changes!

# dates are constant
# every worker write all dates that they can
# then writes for every month how many weekends workdays, and week workdays they want.
# they do it every month/two
# better to put people that will have all experties

# אחראי פעילות, נהג, 3 אנשי צוות
# 2 רשיון משיט
# 5 poeople 

# now the surfers are signing (maybe with another person/surfer)
# 4 surfers a day/ course
# if there is a problem with the experties, we will switch the workers

# first schedule the workers that have special experties
# second schedule the workers that has less days to work
