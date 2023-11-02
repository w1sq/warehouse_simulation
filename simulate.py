import json
import logging

import simpy


def read_scheme(filename="warehouse.json") -> dict:
    """Read warehouse scheme from file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.loads(file.read())


logging.basicConfig(
    filename="warehouse_simulation.log", level=logging.INFO, filemode="w"
)

NUM_ROBOTS = 3
SIM_TIME = 100
TASK_INTERVAL = 1
tasks_done = 0


class WareHouse:
    """Warehouse class for warehouse robot work simulation"""

    def __init__(self, simpy_env, num_robots=NUM_ROBOTS):
        self.env = simpy_env
        self.robots = simpy.Resource(simpy_env, num_robots)

    def pick_up(self, task):
        logging.info("Robot is picking up a cargo")
        yield self.env.timeout(1)

    def drop_off(self, task):
        logging.info("Robot is dropping off a cargo")
        yield self.env.timeout(1)


def task(simpy_env, task_number, warehouse):
    global tasks_done
    logging.info(f"Task %d starts at {simpy_env.now:.2f}", task_number)
    with warehouse.robots.request() as request:
        yield request
        yield simpy_env.process(warehouse.pick_up(task_number))
        logging.info(
            f"Cargo from task %d is picked up at {simpy_env.now:.2f}", task_number
        )
        yield simpy_env.process(warehouse.drop_off(task_number))
        logging.info(
            f"Cargo from task %d is dropped of at {simpy_env.now:.2f}", task_number
        )
        tasks_done += 1


def setup(simpy_env, num_robots=NUM_ROBOTS):
    """Setup of simulation"""
    warehouse = WareHouse(simpy_env, num_robots)

    for i in range(1, 11):
        simpy_env.process(task(simpy_env, i, warehouse))

    while True:
        yield simpy_env.timeout(TASK_INTERVAL)
        i += 1
        simpy_env.process(task(simpy_env, i, warehouse))


logging.info("Starting warehouse simulation")
env = simpy.Environment()
env.process(setup(env, NUM_ROBOTS))
env.run(until=SIM_TIME)
logging.info("Warehouse simulation finished")
logging.info("Tasks done: %d", tasks_done)
