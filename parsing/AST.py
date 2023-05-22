class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def visualize(self, indent_level=0, is_last_child=True):
        indent = self.get_indentation(indent_level)
        connector = "└── " if is_last_child else "├── "

        print(indent + connector + self.value)

        if self.children:
            for i, child in enumerate(self.children):
                is_last = i == len(self.children) - 1
                child.visualize(indent_level + 1, is_last)

    def get_indentation(self, indent_level):
        spaces_per_indent = 4
        spaces = indent_level * spaces_per_indent
        return " " * spaces
