from draftsman.blueprintable import *
from draftsman.constants import Direction
from draftsman.entity import *

from factory import *

UP      = 0
RIGHT   = 4
DOWN    = 8
LEFT    = 12

def find_source_assembler(node):
    #print(node)
    if node.name in ['infinity-chest', 'assembling-machine-1']:
        return node
    for source in node.sources:
        return find_source_assembler(source)
    
    print(f'no item producer for {node}')


def synthesize_factory_graph(bp_string):

    blueprint = Blueprint.from_string(bp_string)

    for entity in blueprint.entities:
        entity.sources = set()
        entity.sinks = set()

    for entity in blueprint.entities:

        if type(entity) in [ElectricPole, Entity]:
            print(f'skipping entity {entity}')

        if type(entity) in [Inserter, TransportBelt, Loader]:
        
            if entity.direction == UP:
                target_pos = (0, 1)
            elif entity.direction == RIGHT:
                target_pos = (1, 0)
            elif entity.direction == DOWN:
                target_pos = (0, -1)
            elif entity.direction == LEFT:
                target_pos = (-1, 0)
            
            target = blueprint.find_entities_filtered(position = entity.position - target_pos)

            print(f'finding feed target for position {entity.position + target_pos}, {target[0].name}')

            # These nodes "feed" into something, so add to their sources
            # Either: we are an inserter and feeding into something,
            # or we are a transport belt feeding into another transport belt
            if target and (type(entity) in [Inserter, Loader] or (type(entity) == TransportBelt and type(target[0]) == TransportBelt)):
                target[0].sources.add(entity)
                entity.sinks.add(target[0])
                print(f'{type(entity)} {hex(id(entity))} -> {type(target[0])} {id(target[0])} add feed target')
                #print(target[0].sources)

            # add source target
            if target and type(entity) in [Inserter, Loader]:
                source = blueprint.find_entities_filtered(position = entity.position + target_pos)
                if source:
                    print(f'{type(source[0])} {id(source[0])} -> {type(entity)} {id(entity)} add source target')
                    entity.sources.add(source[0])
                    source[0].sinks.add(entity)
                    
            
        if type(entity) == AssemblingMachine:
            recipe = Recipe.from_str(entity.recipe)
            entity.factory_node = FactoryNode(entity.name, prod={recipe.result}, recipe=recipe, backer=entity)
        
        elif type(entity) == InfinityContainer:
            prod = entity.filters
            if not prod:
                print(f'Infinity Chest does not produce any items! {entity}')
                entity.factory_node = FactoryNode(entity.name, backer=entity)
            else:
                entity.factory_node = FactoryNode(entity.name, prod={prod[0].name}, backer=entity)
        else:
            entity.factory_node = FactoryNode(entity.name, backer=entity)

    factory = Factory()

    # add all nodes to factory with sources
    for entity in blueprint.entities:
        node = entity.factory_node
        for source in entity.sources:
            node.sources.add(source.factory_node)
        factory.add_node(node)
        print('NODE', node, node.sources, node.sinks)
        
    # add prod types for inserters and belts
    for entity in blueprint.entities:
        node = entity.factory_node
        if type(entity) in [TransportBelt, Inserter]:
            #print(node, [str(x) for x in node.sources])
            source = find_source_assembler(node)
            if source:
                node.add_prod(source.items_produced)
                node.add_cons(source.items_produced)

    #print(factory)
    return factory


if __name__ == '__main__':
    bp = '0eNqtl21zoyAQx78Lr7EjIEbzVW46GTSbljlFD7BzmYzf/VCTpmk0RS7vIg+/ZXf/G5YTKqoOWi2VRdsTkmWjDNr+OiEj35SohjElakBbJIyBuqikeotqUb5LBRFBPUZS7eEv2pIez2yyWijTNtpGBVT2y3Lav2IEykorYTI4fhx3qqsL0I6HFxgYtY1x2xo12HGoKH3hGB3dD8ZfeD+c4xuLhrCSeRb7ZEllQFs3dk/hNxSM9lJDOS0gdAaa4IdRvjfAvhlweNkO+8umbUFHpSgqQJfx3Z9OVM6em1eNrl2GZs7A/YMU3wT8xr1shpyGkBMf8sYnGWRlMrIQtbB5teQhLDrPInFIHJlPHAkJQVMvdFDxkYUQsBBYvABL1pUy8VIP4eG1TJ5VyySo5IhXPjch6NgLna0rZ8+EhNQgzRdukjgEli3AyCoBjpif/aU0WIBnC08QIGUBKhmD/qNKaBKCzrzQfJUAfROShmhms6CZTQgsXYBlIaHceIUyD0GnPmh2rUHTFcaKcekdllySNNvFeZXeNYBe3QgLueroQs/K1jWalHtpkT3sNOnDPwf+rD8Hdi2z3zo6CGOjqhH7WQfjBynAyB7bKUBtZ2cthdyD1KupZet6T9/8fL0CD1K5uah8B/NYQlOPd9mwM2CtS6sZFmqomw/YdW6uckeE/U5aqN3UQVQGMJqGpxfY2fA5sW0l7JDYsumGtyGJXdnVzX6UjksYiPFQn6+/11kR5/7uxP/ljtUd9MObcvh25q6vWow+nIOjIZ7SPMlznhGW53HS9/8AKoXg8w=='
    #bp = '0eNqtlt1urCAUhd+Fa2zEERVf5aQxyOy2JAgWsDnNxHfvdmyncyb2RCa9HH6+tdeGxXgivZlg9NpG0p6IVs4G0v45kaCfrTTLmJUDkJbIEGDojbbP2SDVi7aQMTJTou0R/pKWzXRjU/TShtH5mPVg4tXyYn6kBGzUUcMqeP7x3tlp6MEjj34xtA3gI45RMrqAG5xdFBCS8eKBU/JO2kPDHzjSj9qDWlewYqnohlpcUZ+0xalMvUCIW+zDDftrRxcgRmxDWFZ6GNwbdBPOGawRjp2OMODUkzQBKFmHV4efysqNI/hsNDIC6io3Lb1neU7J4I7nVsfMgDxXdenu47xh50B/aPSGHfZzq8oNdJmAztPQfM/RliLxaCv635u6oVDfKCBfj1cnpGRvlhNax7vXSRoUxHnr/IDXfKOIepc1fhGudllrkq193936X2tgUMk7q1WmtFeTjmkGRWIsxS6DLL8rl+JXc6mxLb+SSsbuiqXYkx1W3JXLfeyE56RsLuxmFzvhPbmK/j42v4u99GSLViXQqsRK6wR2nchuEt+eZiOa+Ke85AQZ358FlLxhUs4reFWIUgjesIMQeTnPH3TUsvw='
    bp = '0eNqtVNtOwzAM/ZXKzylab7D2gR8BVKWpAUtpUpIUgab+O247tjHGtEm8JbZzjo8v2UCjB+wdmQDVBlr0ylEfyBqoQNm+RxfF99H2pGSjcbqjRhWcNaQiRU4NFPyjITZEvZYB/Z8xxkYN6uBBAClrPFQPG/D0YqSe+I3skIml99g1msxL3En1SgbjBEZ+Ylr8gCoZnwSgCRQIF4T58lmboWvQcYD4RiLzTIZdsXpFH5i1t54WeRtgqDgrbgoBn1Bld+lNMXMsL2qPIXAGfop02Nl3rAf26YAO25oCdux6ltqjgMW85LJlXkoWz/VgXmWHqcTJaiWgs+2sMsQa5ZzVXtg4il9y0gM5Hh0znRKSHwlpyXED5ogkPYGaibPlPsGQHjEwPvUHWufxgG97/TZIzYTsN9Z13OATSeQXSVvtiLOLpBVXohYXod5eMVXJEfZ/TdW0Y/8yU3fXdj9d7yTlP7u/X/R4u+jnZoBXd1LJlv3PI+Cddc5kxW1a5mVZrJOsLFf5OH4BYMmMqg=='
    #bp = '0eNp9kN1qBCEMRt8l107p/C3VVynL4rhhG9Bo1SldBt+9mV2WQlt6Zz7jOSYbLH7FlIkrmA3IRS5gXjcodGHr94xtQDBgS8GweOJLF6x7I8auh6aA+IyfYPp2VIBcqRLeCbfieuI1LJilQT1IxAVzlUxBikUeRN49AunG6WlWcAUzHuQk9DNldPeOfmjqF3VQ//7vD8PwwyB8SjvAxZQwd84uHuGRn95X60Uo9xxzkI3sc1LFIMn36hR8YC43zXwY9KT1/NKPWj9PrX0Bru90gQ=='
    #bp = '0eNqV0dsKgzAMBuB3yXUVD9XZvsoYw0MYBY3S1jGRvvuqXowxhXmZ8OcLJDNU7YiDVmRBzqDqngzI6wxGPahslx6VHYIEq0syQ69tUGFrwTFQ1OALZOxuDJCssgq32bWY7jR2FWofYAcGg6E3fqynZY+nggsPMwYTyLQQYeYc+8GSE1jyhTFolMZ6S/AdOj1BR8d0sUPz/+m8OKbjZLm1sth56fM4Bk/UZk1keSK4EFkRp0JE3Lk3Z2ic9A=='
    factory = synthesize_factory_graph(bp)

    print(factory)