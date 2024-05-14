from typing import Any, TypeVar
from enum import Enum
import inspect
import itertools

class RunOutcome(Enum):
    PASS       = 1
    FAIL       = 2
    UNRESOLVED = 3

ValuePool = list[Any]
ValuePools = dict[type, ValuePool]
RunResult = tuple[Any, RunOutcome]

class Runner(object):
    def __init__(self):
        raise NotImplementedError('You have to extend this class')

    def run(self, inp: Any) -> RunResult:
        raise NotImplementedError('You have to extend this class and implement \
                                  run')

class Fuzzer(object):
    def __init__(self):
        raise NotImplementedError('You have to extend this class')

    def fuzz(self, ftype: type=str):
        raise NotImplementedError('You have to extend this class and implement \
                                  fuzz')
    def run(self, runner: Runner) -> RunResult:
        fuzz_input: Any = self.fuzz()
        runner.run(inp=fuzz_input)

    def runs(self, runner: Runner, max_trials: int = 10) -> list[RunResult]:
        results: list[RunResult] = list()
        for i in range(max_trials):
            try:
                results.append(self.run(runner))
            except StopIteration:
                break
        return results

class PrintRunner(Runner):
    def __init__(self):
        self.name: str = 'PrintRunner'

    def run(self, inp: Any) -> RunResult:
        print(inp)
        return (None, RunOutcome.UNRESOLVED)

class FunctionRunner(Runner):
    def __init__(self, function):
        self.name: str = 'FunctionRunner'
        self.function = function

    def run(self, inp: Any) -> RunResult:
        self.function(*inp)
        # TODO(jso): return correct stuff
        return (None, RunOutcome.UNRESOLVED)

class ValuePoolFuzzer(Fuzzer):
    def __init__(self, vpools: ValuePools, argspec: inspect.FullArgSpec):
        self.name: str = 'ValuePoolFuzzer'
        assert(not vpools is None)
        self.vpools: ValuePools = vpools
        assert(not argspec is None)
        self.argspec = argspec
        self.__iter_init()

    def fuzz(self) -> str:
        return next(self.iter_values)

    def reset(self) -> None:
        self.__iter_init()

    def __iter_init(self) -> None:
        self.iter_values: Iterable[Any] = itertools.product(
                *[self.vpools.get(t) for t in self.argspec.annotations.values()])


def func_to_test(string: str, integer: int, fl: float=1337.0, arr: list=[]):
    pass

if __name__ == '__main__':
    prunner = PrintRunner()
    frunner = FunctionRunner(func_to_test)

    # TODO(jso): what to do with default values? -> also use them as value
    # candidates?
    argspec: inspect.FullArgSpec = inspect.getfullargspec(func_to_test)
    vpools: ValuePools = {
        int: [1, 2, 3, 4],
        str: ["lel", "lol", "lul"]
    }
    vpools[float] = vpools.get(int) + [133.7]
    vpools[list] = [[], vpools.get(int), vpools.get(str)]

    vp_fuzzer = ValuePoolFuzzer(vpools=vpools, argspec=argspec)
    results = vp_fuzzer.runs(prunner, max_trials=1000)
    vp_fuzzer.reset()
    vp_fuzzer.runs(frunner, max_trials=1000)

