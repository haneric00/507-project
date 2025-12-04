from draftsman.blueprintable import *
from draftsman.constants import Direction
from draftsman.entity import *

from factory import *

bp = '0eNqtl21zoyAQx78Lr7EjIEbzVW46GTSbljlFD7BzmYzf/VCTpmk0RS7vIg+/ZXf/G5YTKqoOWi2VRdsTkmWjDNr+OiEj35SohjElakBbJIyBuqikeotqUb5LBRFBPUZS7eEv2pIez2yyWijTNtpGBVT2y3Lav2IEykorYTI4fhx3qqsL0I6HFxgYtY1x2xo12HGoKH3hGB3dD8ZfeD+c4xuLhrCSeRb7ZEllQFs3dk/hNxSM9lJDOS0gdAaa4IdRvjfAvhlweNkO+8umbUFHpSgqQJfx3Z9OVM6em1eNrl2GZs7A/YMU3wT8xr1shpyGkBMf8sYnGWRlMrIQtbB5teQhLDrPInFIHJlPHAkJQVMvdFDxkYUQsBBYvABL1pUy8VIP4eG1TJ5VyySo5IhXPjch6NgLna0rZ8+EhNQgzRdukjgEli3AyCoBjpif/aU0WIBnC08QIGUBKhmD/qNKaBKCzrzQfJUAfROShmhms6CZTQgsXYBlIaHceIUyD0GnPmh2rUHTFcaKcekdllySNNvFeZXeNYBe3QgLueroQs/K1jWalHtpkT3sNOnDPwf+rD8Hdi2z3zo6CGOjqhH7WQfjBynAyB7bKUBtZ2cthdyD1KupZet6T9/8fL0CD1K5uah8B/NYQlOPd9mwM2CtS6sZFmqomw/YdW6uckeE/U5aqN3UQVQGMJqGpxfY2fA5sW0l7JDYsumGtyGJXdnVzX6UjksYiPFQn6+/11kR5/7uxP/ljtUd9MObcvh25q6vWow+nIOjIZ7SPMlznhGW53HS9/8AKoXg8w=='
bp = '0eNqtlt1urCAUhd+Fa2zEERVf5aQxyOy2JAgWsDnNxHfvdmyncyb2RCa9HH6+tdeGxXgivZlg9NpG0p6IVs4G0v45kaCfrTTLmJUDkJbIEGDojbbP2SDVi7aQMTJTou0R/pKWzXRjU/TShtH5mPVg4tXyYn6kBGzUUcMqeP7x3tlp6MEjj34xtA3gI45RMrqAG5xdFBCS8eKBU/JO2kPDHzjSj9qDWlewYqnohlpcUZ+0xalMvUCIW+zDDftrRxcgRmxDWFZ6GNwbdBPOGawRjp2OMODUkzQBKFmHV4efysqNI/hsNDIC6io3Lb1neU7J4I7nVsfMgDxXdenu47xh50B/aPSGHfZzq8oNdJmAztPQfM/RliLxaCv635u6oVDfKCBfj1cnpGRvlhNax7vXSRoUxHnr/IDXfKOIepc1fhGudllrkq193936X2tgUMk7q1WmtFeTjmkGRWIsxS6DLL8rl+JXc6mxLb+SSsbuiqXYkx1W3JXLfeyE56RsLuxmFzvhPbmK/j42v4u99GSLViXQqsRK6wR2nchuEt+eZiOa+Ke85AQZ358FlLxhUs4reFWIUgjesIMQeTnPH3TUsvw='
#bp = '0eNqV0dsKgzAMBuB3yXUVD9XZvsoYw0MYBY3S1jGRvvuqXowxhXmZ8OcLJDNU7YiDVmRBzqDqngzI6wxGPahslx6VHYIEq0syQ69tUGFrwTFQ1OALZOxuDJCssgq32bWY7jR2FWofYAcGg6E3fqynZY+nggsPMwYTyLQQYeYc+8GSE1jyhTFolMZ6S/AdOj1BR8d0sUPz/+m8OKbjZLm1sth56fM4Bk/UZk1keSK4EFkRp0JE3Lk3Z2ic9A=='
blueprint = Blueprint.from_string(bp)




UP      = 0
RIGHT   = 4
DOWN    = 8
LEFT    = 12

class SourcedEntity:
    def __init__(self, entity):
        self.entity = entity
        self.sources = []
    
    def add_source(self, source):
        self.sources.append(source)

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
        
        target = blueprint.find_entities_filtered(position = entity.position + target_pos)

        # These nodes "feed" into something, so add to their sources
        # Either: we are an inserter and feeding into something,
        # or we are a transport belt feeding into another transport belt
        if target and (type(entity) in [Inserter, Loader] or (type(entity) == TransportBelt and type(target[0]) == TransportBelt)):
            target[0].sources.add(entity)
            print(f'{type(entity)} {id(entity)} -> {type(target[0])} {id(target[0])} add feed target')
            #print(target[0].sources)

        # add source target
        if target and type(entity) in [Inserter, Loader]:
            source = blueprint.find_entities_filtered(position = entity.position - target_pos)
            if source:
                print(f'{type(source[0])} {id(source[0])} -> {type(entity)} {id(entity)} add source target')
                entity.sources.add(source[0])
                
        
    if type(entity) == AssemblingMachine:
        recipe = Recipe.from_str(entity.recipe)
        entity.factory_node = FactoryNode(entity.name, prod=recipe.result, recipe=recipe)
    
    elif type(entity) == InfinityContainer:
        prod = entity.filters
        if not prod:
            print(f'Infinity Chest does not produce any items! {entity}')
            entity.factory_node = FactoryNode(entity.name)
        else:
            entity.factory_node = FactoryNode(entity.name, prod={prod[0].name})
    else:
        entity.factory_node = FactoryNode(entity.name)

factory = Factory()

# add all nodes to factory with sources
for entity in blueprint.entities:
    node = entity.factory_node
    for source in entity.sources:
        node.sources.add(source.factory_node)
    factory.add_node(node)
    print(node, node.sources)

def find_source_assembler(node):
    #print(node)
    if node.name in ['infinity-chest', 'assembling-machine-1']:
        return node
    for source in node.sources:
        return find_source_assembler(source)
    
    print(f'no item producer for {node}')
    
# add prod types for inserters and belts
for entity in blueprint.entities:
    node = entity.factory_node
    if type(entity) in [TransportBelt, Inserter]:
        #print(node, [str(x) for x in node.sources])
        source = find_source_assembler(node)
        if source:
            node.add_prod(source.items_produced)

print(factory)

#print(blueprint)
