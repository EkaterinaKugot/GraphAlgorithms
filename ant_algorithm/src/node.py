
class Node:

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Неверный тип данных")
        
        self.name = name
        self.neighbours: dict = {}

    # Добавить соседа
    def add_neighbour(self, neighbour: 'Node', weight: float = 0.) -> None:
        if not isinstance(neighbour, Node):
                raise TypeError("Неверный тип данных")
        if not isinstance(weight, float):
                raise TypeError("Неверный тип данных")
        
        if neighbour not in self.neighbours.keys():
            self.neighbours[neighbour] = weight

    # Удалить соседа
    def remove_neighbour(self, neighbour: 'Node') -> None:
        if not isinstance(neighbour, Node):
                raise TypeError("Неверный тип данных")
        
        if neighbour in self.neighbours.keys(): 
            self.neighbours.pop(neighbour, None)

    def nb_begin(self):
        return iter(self.neighbours)
    
    def nb_end(self):
        return iter(())
    
    def __repr__(self):
        return f"Node({self.name})"

    