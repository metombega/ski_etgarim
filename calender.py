
activity_dates = ['1/1/2025', '2/1/2025', '3/1/2025', '4/1/2025', '5/1/2025', '6/1/2025'] 
workers = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan']
experties = ['a', 'b', 'c', 'd']

workers_experties = {
    'Alice': ['a', 'b', 'c'], 
    'Bob': ['c', 'b'], 
    'Charlie': ['a', 'b', 'd'], 
    'David': ['b', 'c', 'e'], 
    'Eve': ['a', 'b', 'c', 'd'], 
    'Frank': ['a', 'b', 'c', 'd'], 
    'Grace': ['d', 'b'], 
    'Heidi': ['d'], 
    'Ivan': ['a', 'c']
}

workers_availability = {
    'Alice': ['1/1/2025', '2/1/2025', '3/1/2025', '4/1/2025', '5/1/2025'], 
    'Bob': ['5/1/2025', '6/1/2025'], 
    'Charlie': ['1/1/2025',  '3/1/2025', '4/1/2025', '5/1/2025', '6/1/2025'], 
    'David': ['1/1/2025', '2/1/2025', '3/1/2025', '5/1/2025', '6/1/2025'], 
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
    'David': 4, 
    'Eve': 4, 
    'Frank': 1, 
    'Grace': 4, 
    'Heidi': 1, 
    'Ivan': 2
}

mandatory_experties = {'a': 1, 'b': 2, 'c': 1, 'd': 0, 'e': 1} # maybe should change according to the date
num_of_workers_per_day = 5

def schedual_workers():
    """ 
    sort the dates by the number of workers that can work on this date - we want to take first the dates with the least workers
    sort the workers by the max number of days they can work devide by the number of their available days
    """
    schedual = {}
    # sort the dates by the number of workers that can work on this date
    sorted_activity_dates = sorted(activity_dates, key=lambda date: len([worker for worker in workers if date in workers_availability[worker]]))
    for date in sorted_activity_dates:
        schedual[date] = {'workers': [], 'replacble_workers': []}
        # filter the workers that can work in this date
        available_workers = [worker for worker in workers if date in workers_availability[worker]]
        # sort workers by the max work days devided by the number of days they can work. pay attention to devided by zero
        available_workers_sorted = sorted(available_workers, key=lambda worker: len(workers_availability[worker]) / workers_max_work_days[worker] if workers_max_work_days[worker] > 0 else float('inf'))
        # for each experty in mandatory_experties, book the first worker that has this experty
        experties_to_book = mandatory_experties.copy()
        num_of_workers_booked = num_of_workers_per_day
        # sort the experties from the rearest experty to the most common
        # experties_sorted = sorted(experties_to_book, key=lambda experty: sum([1 for worker in available_workers_sorted if experty in workers_experties[worker]]))
        for experty in experties_to_book:
            workers_with_experty = [worker for worker in available_workers_sorted if experty in workers_experties[worker]]
            while experties_to_book[experty] > 0:
                if len(workers_with_experty) > 0:
                    worker = workers_with_experty[0]
                    available_workers_sorted.remove(worker)
                    workers_with_experty.remove(worker)
                    workers_max_work_days[worker] -= 1
                    # remove all the required experties on this date
                    for worker_experty in workers_experties[worker]:
                        experties_to_book[worker_experty] -= 1
                    num_of_workers_booked -= 1
                    schedual[date]['workers'].append(worker)
                    print(worker, date)
                else: 
                    print(f'no more workers with experty {experty} on date {date}')
                    break
        # count all experties that could not be booked
        experties_not_booked = sum([experties_to_book[experty] for experty in experties_to_book if experties_to_book[experty] > 0])
        # book the rest of the workers
        # todo: take workers with the least experties
        while num_of_workers_booked > experties_not_booked:
            for worker in available_workers_sorted:
                available_workers_sorted.remove(worker)
                workers_max_work_days[worker] -= 1
                # remove all the required experties on this date
                for worker_experty in workers_experties[worker]:
                    experties_to_book[worker_experty] -= 1
                print(worker, date)
                schedual[date]['workers'].append(worker)
                num_of_workers_booked -= 1

        # remove the date from the availability
        for worker in workers:
            if date in workers_availability[worker]:
                workers_availability[worker].remove(date)
        
        # find all the workers that could be replaced
        for worker in schedual[date]['workers']:
            is_replacable = True
            for worker_experty in workers_experties[worker]:
                # check if all the worker's experties are booked and have en extra worker with this experty
                if experties_to_book[worker_experty] >= 0:
                    is_replacable = False
                    break
            if is_replacable:
                schedual[date]['replacble_workers'].append(worker)
        schedual[date]['experties'] = experties_to_book
    return schedual

def replace_workers(worker1, date1, worker2, date2, schedual):
    """ replace worker1 with worker2 in the schedual """
    # check if the worker1 is in the schedual
    if worker1 in schedual[date1]['workers'] and worker2 in schedual[date2]['workers']:
        schedual[date1]['workers'].remove(worker1)
        schedual[date2]['workers'].append(worker2)
        # update the experties
        for experty in schedual[date1]['experties']:
            if experty in workers_experties[worker1]:
                schedual[date1]['experties'][experty] += 1
            if experty in workers_experties[worker2]:
                schedual[date1]['experties'][experty] -= 1
        for experty in schedual[date2]['experties']:
            if experty in workers_experties[worker2]:
                schedual[date2]['experties'][experty] += 1
            if experty in workers_experties[worker1]:
                schedual[date2]['experties'][experty] -= 1
    else:
        print(f'worker {worker1} is not in the schedual on date {date1} or worker {worker2} is not in the schedual on date {date2}')
        
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
