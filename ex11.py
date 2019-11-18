import itertools

class Node:
    def __init__(self, data, pos=None, neg=None):
        self.data = data
        self.positive_child = pos
        self.negative_child = neg


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        self.root = root

    def diagnose(self, symptoms):
        """
        :return: illness that matches the symptoms
        """
        return self.__diagnose_helper(self.root, symptoms)

    def __diagnose_helper(self, node, symptoms):
        """
        recursively, checks if symptom is in symptoms' list.
        when leaf was reached, return illness.
        """
        # if node is a leaf, illness was found
        if not node.positive_child:
            return node.data

        # each iteration, checks if symptom is in list
        next_node = node.positive_child if node.data in symptoms else node.negative_child
        return self.__diagnose_helper(next_node, symptoms)

    def calculate_success_rate(self, records):
        """
        :param records: list of illnesses and symptoms
        :return: ratio of successful diagnosis / total records
        """
        if not records:
            return

        total_records = len(records)
        successful_diagnosis = 0
        diagnoser = Diagnoser(self.root)

        # if diagnosis matches illness, count as successful
        for record in records:
            if diagnoser.diagnose(record.symptoms) == record.illness:
                successful_diagnosis += 1

        return successful_diagnosis / total_records

    def all_illnesses(self):
        """
        :return: all illnesses in decision tree
        """
        visited_dict = self.__all_illnesses_helper(self.root, {})
        return sorted(visited_dict, key=lambda x: x[1])

    def __all_illnesses_helper(self, node, visited):
        """
        :return: a dictionary of illnesses, and count of appearances in tree
        """
        # if illness is already registered, add 1 to visit count
        if node.data in visited:
            visited[node.data] += 1

        # node not in list
        else:
            # if node ia a leaf, add node.data to list
            if not node.positive_child:
                visited[node.data] = 1

            # if node ia a parent, visit children
            else:
                self.__all_illnesses_helper(node.positive_child, visited)
                self.__all_illnesses_helper(node.negative_child, visited)

        return visited

    def most_rare_illness(self, records):
        """
        diagnose illness for every record's symptoms.
        :return: most rare illness among all records
        """
        illness_dict = {}
        for record in records:
            illness = self.diagnose(record.symptoms)
            if illness not in illness_dict:
                illness_dict[illness] = 1
            else:
                illness_dict[illness] += 1
        return min(illness_dict, key=lambda x: x[1])

    def paths_to_illness(self, illness):
        """
        :param illness: str
        :return: all paths leads to illness in decision tree
        """
        return self.__path_helper(self.root, illness, [], [])

    def __path_helper(self, start_node, illness, path, all_paths):
        """
        :return: all paths leads to illness
        """
        if not start_node.positive_child:
            # if path leads to illness, return value_path
            if start_node.data == illness:
                return path
            return None

        # positive path
        path.append(True)
        new_path = self.__path_helper(start_node.positive_child, illness, path, all_paths)
        if new_path:
            all_paths.append(new_path[:])
        path.pop()

        # negative path
        path.append(False)
        new_path = self.__path_helper(start_node.negative_child, illness, path, all_paths)
        if new_path:
            all_paths.append(new_path[:])
        path.pop()

        if start_node == self.root:
            return all_paths


def build_tree(records, symptoms):
    """
    :param records: lst of record obj
    :param symptoms: lst of str
    :return: root of new tree
    """
    return __build_helper(records, symptoms, 0, [])


def __build_helper(records, symptoms, cur_symp_idx, path):
    """
    build tree recursively based on symptoms list.
    :return: root node
    """
    if cur_symp_idx == len(symptoms):
        if __find_illness(records, path[:]):
            node = Node(__find_illness(records, path[:]), None, None)
        else:
            node = None
    else:
        symp = symptoms[cur_symp_idx]

        # create nodes in tree
        path.append((symp, True))
        positive_child = __build_helper(records, symptoms, cur_symp_idx + 1, path)
        path.pop()

        path.append((symp, False))
        negative_child = __build_helper(records, symptoms, cur_symp_idx + 1, path)
        path.pop()

        node = Node(symp, positive_child, negative_child)

    return node


def __find_illness(records, path_symptoms):
    """
    :param path_symptoms: list of tuples (symptom in path, True or False)
    :return: most common illness within records, where all path symptoms are met
    (and no other symptoms from all_symptoms).
    """
    matched_illnesses = {}
    for record in records:
        is_break = False
        for symp in path_symptoms:
            symptom, symp_status = symp

            # if True symptom not in illness symptoms, illness don't match.
            # move on to check next illness
            if symp_status:
                if symptom not in record.symptoms:
                    is_break = True
                    break

            # if False symptom in illness symptoms, illness don't match.
            # move on to check next illness
            if not symp_status:
                if symptom in record.symptoms:
                    is_break = True
                    break

        if not is_break:
            # illness match requirements
            if record.illness in matched_illnesses:
                matched_illnesses[record.illness] += 1
            else:
                matched_illnesses[record.illness] = 1

    return max(matched_illnesses, key=lambda key: matched_illnesses[key]) if matched_illnesses else None


def print_tree(root_tree, level=1, answer=''):
    print('    ' * (level - 1) + str(answer) + '+---' * (level > 0) + root_tree.data)
    if root_tree.positive_child:
        if root_tree.positive_child:
            print_tree(root_tree.positive_child, level + 1, 'P')
        if root_tree.negative_child:
            print_tree(root_tree.negative_child, level + 1, 'N')

def optimal_tree(records, symptoms, depth):
    """
    :return: root of tree with the highest success rate, with depth = num of symptoms
    """
    trees_success_rate = {}
    for combination in itertools.combinations(symptoms, depth):
        list(combination)
        root = build_tree(records, combination)
        diagnoser = Diagnoser(root)
        trees_success_rate[root] = diagnoser.calculate_success_rate(records)

    return max(trees_success_rate, key=lambda key: trees_success_rate[key])
