import inspect
import sys

import tabulate
import numpy

class ClassStats:
    def __init__(self):
        self.inheritance_depth = 0
        self.child_count = 0
        self.inherited_methods_count = 0
        self.overridden_methods_count = 0
        self.new_methods_count = 0
        self.visible_methods_count = 0
        self.private_methods_count = 0

class MetricCounter:
    def __init__(self):
        self.__cached_inheritance_depths: dict[type, int] = {}
        self.classes_stats: dict[type, ClassStats] = {}

    def count_class(self, clazz: type) -> ClassStats:
        class_metrics = ClassStats()
        class_metrics.child_count = len(clazz.__subclasses__())
        class_metrics.inheritance_depth = self.count_class_inheritance_depth(clazz)
        self.count_props(clazz, class_metrics)
        self.classes_stats[clazz] = class_metrics
        return class_metrics

    def count_class_inheritance_depth(self, clazz: type) -> int:
        if clazz in self.__cached_inheritance_depths:
            return self.__cached_inheritance_depths[clazz]
        if clazz.__base__ == object:
            inheritance_depth = 0
        else:
            inheritance_depth = self.count_class_inheritance_depth(clazz.__base__) + 1
        self.__cached_inheritance_depths[clazz] = inheritance_depth
        return inheritance_depth

    def count_props(self, clazz: type, out_stats: ClassStats):
        new_methods = 0
        inherited_methods = 0
        overridden_methods = 0
        visible_methods = 0
        private_methods = 0
        for name, obj in inspect.getmembers(clazz):
            if inspect.isroutine(obj):
                if name not in clazz.__dict__:
                    inherited_methods += 1
                elif any(name in super_class.__dict__ for super_class in clazz.mro()[1:]):
                    overridden_methods += 1
                else:
                    new_methods += 1
                if name.startswith(f'_{clazz.__name__}') and not name.endswith("__"):
                    private_methods += 1
                else:
                    visible_methods += 1
        out_stats.new_methods_count = new_methods
        out_stats.overridden_methods_count = overridden_methods
        out_stats.inherited_methods_count = inherited_methods
        out_stats.visible_methods_count = visible_methods
        out_stats.private_methods_count = private_methods

    def get_polymorphism_factor(self) -> float:
        overriden_methods = 0
        denom = 0
        for clazz, stats in self.classes_stats.items():
            overriden_methods += stats.overridden_methods_count
            denom += stats.new_methods_count * stats.child_count
        if overriden_methods == 0 or denom == 0:
            return 0.0
        return overriden_methods / denom

    def get_method_inheritance_factor(self) -> float:
        inherited_methods = 0
        all_methods = 0
        for clazz, stats in self.classes_stats.items():
            inherited_methods += stats.overridden_methods_count
            all_methods += stats.new_methods_count + stats.inherited_methods_count + stats.overridden_methods_count
        if inherited_methods == 0 or all_methods == 0:
            return 0.0
        return inherited_methods / all_methods

    def get_closed_methods_factor(self) -> float:
        private_methods = 0
        all_methods = 0
        for clazz, stats in self.classes_stats.items():
            private_methods += stats.private_methods_count
            all_methods += stats.visible_methods_count + stats.private_methods_count
        if private_methods == 0 or all_methods == 0:
            return 0.0
        return private_methods / all_methods


def class_stats_to_row(clazz: type, stats: ClassStats):
    return [clazz.__name__, stats.inheritance_depth, stats.child_count]


if __name__ == '__main__':
    counter = MetricCounter()
    for name, obj in inspect.getmembers(sys.modules['numpy']):
        if inspect.isclass(obj):
            counter.count_class(obj)
    table_headers = ["Class Name", "Inheritance Depth", "Children Count"]
    print(tabulate.tabulate([class_stats_to_row(clazz, stats) for clazz, stats in counter.classes_stats.items()],
                            headers=table_headers))

    lib_factors = {"Closed Methods Factor": [counter.get_closed_methods_factor()],
                   "Method Inheritance Factor": [counter.get_method_inheritance_factor()],
                   "Polymorphism Factor": [counter.get_polymorphism_factor()]}
    lib_factors_headers = ["Closed Methods Factor", "Method Inheritance Factor", "Polymorphism Factor"]
    print(tabulate.tabulate(lib_factors, headers="keys"))