import json


class MediatorEvent():
    def __init__(self, type: str, val: str, intervalMs=0) -> None:
        self.__mType = type
        self.__mValue = val
        self.__mIntervalMs = intervalMs

    def type(self):
        return self.__mType

    def value(self):
        return self.__mValue

    def intervalMs(self):
        return self.__mIntervalMs

    __mType = str
    __mValue = str
    __mIntervalMs = int


class Mediator():
    def notify(self, sender: object, event: MediatorEvent) -> None:
        pass


class ConcreteMediator(Mediator):
    def __init__(self, component1: object, component2: object, component3: object) -> None:
        if not component1 == None:
            self._handler = component1
            self._handler.mediator = self
        if not component1 == None:
            self._reader = component2
            self._reader.mediator = self
        if not component1 == None:
            self._jproc = component3
            self._jproc.mediator = self

    def notify(self, sender: object, event: MediatorEvent) -> None:
        # print(event)

        if event.intervalMs() != 0:
            data = self._reader.readDataInInterval(event.intervalMs(), True)
        else:
            data = self._reader.getData()

        # self._reader.clearData()

        if event.type() == 'search_global':
            if len(data) > 0:
                # list records by last element
                metricsArray = self._jproc.listDataRecords(data[-1])
                sender.sendSearchResponce(metricsArray)
            else:
                print("Json reader has no read data!")

        if event.type() == 'search_target':
            print("Event search_target isn't supported!")
            # todo

        if event.type() == 'query_targets':
            responceData = self._jproc.getTagetData(data, event.value())
            try:
                sender.sendQueryResponce(json.loads(responceData))
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e.doc)
            except BrokenPipeError as e:
                print(e.errno, e.strerror, e.filename, e.filename2, e.args)


class BaseComponent:
    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator
