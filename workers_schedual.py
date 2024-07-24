import json

class WorkersSchedual:
    def __init__(self, workers_schedual):
        self.activity_dates = workers_schedual['activity_dates']
        self.workers = workers_schedual['workers']
        self.workers_availability = workers_schedual['workers_availability']
        self.workers_max_work_days = workers_schedual['workers_max_work_days']
        self.workers_experties = workers_schedual['workers_experties']
        self.mandatory_experties = workers_schedual['mandatory_experties']
        self.num_of_workers_per_day = workers_schedual['num_of_workers_per_day']

    # TODO:
    def add_worker_to_schedual(self, worker, date, experties_to_book, num_of_workers_booked, available_workers_sorted, workers_with_experty, schedual):
        available_workers_sorted.remove(worker)
        self.workers_max_work_days[worker] -= 1
        # remove all the required experties on this date
        for worker_experty in self.workers_experties[worker]:
            experties_to_book[worker_experty] -= 1
        num_of_workers_booked -= 1
        schedual[date]['workers'].append(worker)
        return num_of_workers_booked

    def create_schedual(self):
        """ 
        sort the dates by the number of workers that can work on this date - we want to take first the dates with the least workers
        sort the workers by the max number of days they can work devide by the number of their available days
        """
        schedual = {}
        # sort the dates by the number of workers that can work on this date
        sorted_activity_dates = sorted(self.activity_dates, key=lambda date: len([worker for worker in self.workers if date in self.workers_availability[worker]]))
        for date in sorted_activity_dates:
            schedual[date] = {'workers': [], 'replacble_workers': []}
            # filter the workers that can work in this date
            available_workers = [worker for worker in self.workers if date in self.workers_availability[worker]]
            # sort workers by the max work days devided by the number of days they can work. pay attention to devided by zero
            available_workers_sorted = sorted(available_workers, key=lambda worker: len(self.workers_availability[worker]) / self.workers_max_work_days[worker] if self.workers_max_work_days[worker] > 0 else float('inf'))
            # for each experty in mandatory_experties, book the first worker that has this experty
            experties_to_book = self.mandatory_experties.copy()
            num_of_workers_booked = self.num_of_workers_per_day
            for experty in experties_to_book:
                workers_with_experty = [worker for worker in available_workers_sorted if experty in self.workers_experties[worker]]
                while experties_to_book[experty] > 0:
                    if len(workers_with_experty) > 0:
                        worker = workers_with_experty[0]
                        num_of_workers_booked = self.add_worker_to_schedual(worker, date, experties_to_book, num_of_workers_booked, available_workers_sorted, workers_with_experty, schedual)
                        workers_with_experty.remove(worker)
                    else: 
                        print(f'no more workers with experty {experty} on date {date}')
                        break
            # count all experties that could not be booked
            experties_not_booked = sum([experties_to_book[experty] for experty in experties_to_book if experties_to_book[experty] > 0])
            # book the rest of the workers
            # todo: take workers with the least experties
            while num_of_workers_booked > experties_not_booked:
                for worker in available_workers_sorted:
                    num_of_workers_booked = self.add_worker_to_schedual(worker, date, experties_to_book, num_of_workers_booked, available_workers_sorted, workers_with_experty, schedual)

            # remove the date from the availability
            for worker in self.workers:
                if date in self.workers_availability[worker]:
                    self.workers_availability[worker].remove(date)
            
            # find all the workers that could be replaced
            for worker in schedual[date]['workers']:
                is_replacable = True
                for worker_experty in self.workers_experties[worker]:
                    # check if all the worker's experties are booked and have en extra worker with this experty
                    if experties_to_book[worker_experty] >= 0:
                        is_replacable = False
                        break
                if is_replacable:
                    schedual[date]['replacble_workers'].append(worker)
            schedual[date]['experties'] = experties_to_book
        return schedual

    def replace_workers(self, worker1, date1, worker2, date2, schedual):
        """ replace worker1 with worker2 in the schedual """
        # check if the worker1 is in the schedual
        if worker1 in schedual[date1]['workers'] and worker2 in schedual[date2]['workers']:
            print(f'replace worker {worker1} on date {date1} with worker {worker2} on date {date2}')
            schedual[date1]['workers'].remove(worker1)
            schedual[date2]['workers'].append(worker2)
            # update the experties
            for experty in schedual[date1]['experties']:
                if experty in self.workers_experties[worker1]:
                    schedual[date1]['experties'][experty] += 1
                if experty in self.workers_experties[worker2]:
                    schedual[date1]['experties'][experty] -= 1
            for experty in schedual[date2]['experties']:
                if experty in self.workers_experties[worker2]:
                    schedual[date2]['experties'][experty] += 1
                if experty in self.workers_experties[worker1]:
                    schedual[date2]['experties'][experty] -= 1
        else:
            print(f'worker {worker1} is not in the schedual on date {date1} or worker {worker2} is not in the schedual on date {date2}')
        return schedual
            
if __name__ == '__main__':
    # load workers schedual from workers_schedual.json
    with open('workers_schedual.json', 'r') as file:
        workers_schedual = json.load(file)
    workers_schedual = WorkersSchedual(workers_schedual)
    schedual = workers_schedual.create_schedual()
    print(schedual)
    # replace worker1 with worker2 in the schedual
    date1 = workers_schedual.activity_dates[0]
    worker1 = schedual[date1]['workers'][0]
    date2 = workers_schedual.activity_dates[1]
    worker2 = schedual[date2]['workers'][1]
    schedual = workers_schedual.replace_workers(worker1, date1, worker2, date2, schedual)
    print(schedual)