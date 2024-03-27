import asyncio, random, time

class Passenger:
    def __init__(self, start) -> None:
        self.start = start
        self.finish = random.choice(list(set(STATIONS) - set([self.start, ])))
        if STATIONS.index(self.start) < STATIONS.index(self.finish):
            self.dir = 1
        else:
            self.dir = 2


class Station:
    def __init__(self, name) -> None:
        self.name = name
        self.passengers = []
        self.capacity = 1000
    
    async def gen(self):
        await asyncio.sleep(wait_gen * 60 / scale)
        while True:
            if len(self.passengers) <= self.capacity:
                self.passengers.append(Passenger(self))
                await asyncio.sleep(interval_gen / scale)
            else:
                print(f'\nNot enough trains\n{self}\n')
                raise SystemExit
    
    def __str__(self) -> str:
        return f'{self.name}: {len(self.passengers)}'


class Train:
    def __init__(self, n) -> None:
        self.number = n
        self.previous = Station('Depo')
        self.next = STATIONS[0]
        self.dir = 1
        self.passengers = []
        self.capacity = 400
    
    async def go(self):
        i = 0
        start = True
        while True:
            if STATIONS[i] == STATIONS[0] and not start:
                self.dir = 1
                i = 0
            elif STATIONS[i] == STATIONS[-1] and not start:
                self.dir = 2
                i = -1
            if start:
                start = False
            if self.dir == 1:
                self.previous = STATIONS[i]
                self.next = STATIONS[i+1]
                i += 1
            else:
                self.previous = STATIONS[i]
                self.next = STATIONS[i-1]
                i -= 1
            station = self.previous
            for pas in self.passengers:
                if pas.finish == station:
                    self.get_off(pas)
            await asyncio.sleep(stop / scale)
            for pas in station.passengers:
                if self.dir == pas.dir and self.get_on(pas):
                        station.passengers.remove(pas)
            await asyncio.sleep(hauls[(self.previous, self.next)] * 60 / scale)

    def get_on(self, pas):
        if len(self.passengers) + 1 <= self.capacity:
            self.passengers.append(pas)
            return True
        else:
            return False
    
    def get_off(self, pas):
        self.passengers.remove(pas)
    
    def __str__(self) -> str:
        return f'{self.number} ({len(self.passengers)}): {self.previous.name} --> {self.next.name}'

    
n = int(input('Enter the amount of trains '))
start_time = None
trains = list(range(1, n+1))
scale = 200
interval_gen = 1
wait_gen = 18
interval_train = 38 / n
stop = 15
STATIONS =  ['Rokossovskaya', 'Sobornaya', 'Kristall', 'Zarechnaya', 'Biblioteka']
hauls = {(0, 1): 6,
         (1, 2): 3,
         (2, 3): 2,
         (3, 4): 7}

for st in STATIONS.copy():
    STATIONS.append(Station(st))
    STATIONS.remove(st)

for key, val in hauls.copy().items():
    del hauls[key]
    k1, k2 = key
    st1, st2 = STATIONS[k1], STATIONS[k2]
    hauls[st1, st2] = val
    hauls[st2, st1] = val

for n in trains.copy():
    trains.append(Train(n))
    trains.remove(n)


async def inform():
    start_time = time.monotonic()
    while True:
        sec = (time.monotonic() - start_time) * scale
        minutes = str(round(sec % 3600 // 60))
        if len(minutes) == 1:
            minutes = '0' + minutes
        hours = str(round(sec // 3600))
        if len(hours) == 1:
            hours = '0' + hours
        print(f'\nTIME: {hours}:{minutes}\n')
        for st in STATIONS:
            print(st)
        print()
        for tr in trains:
            print(tr)
        print('------------------------------------')
        if int(hours) >= 10:
            print()
            exit('SUCCESS\n')
        await asyncio.sleep(2)


async def start():
    loop.create_task(inform())
    for st in STATIONS:
        loop.create_task(st.gen())
    for train in trains:
        loop.create_task(train.go())
        await asyncio.sleep(interval_train * 60 / scale)


loop = asyncio.get_event_loop()
loop.create_task(start())
loop.run_forever()