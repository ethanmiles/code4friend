class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def add_friend(self, friend_person):
        try:
            self.friend_person.append(friend_person)
        except AttributeError:
            self.friend_person = [friend_person]
    
    def get_name(self):
        return  self.first_name + ' ' + self.last_name
    def get_friends(self):
        try:
            return self.friend_person
        except AttributeError:
            return []

def get_or_create_person(collection: dict, name:str):
    if name in collection:
        return collection[name]
    else:
        name_part = name.split(' ')
        new_person = Person(name_part[0], name_part[1])
        collection[name] = new_person
        return new_person

def load_people3():
    file_name = 'a2_sample_set.txt'
    person_list = []
    person_name_friend_name = {}
    person_name_person_index = {}
    with open(file_name) as file_handle:
        for content in file_handle:
            person_friend_group = content.replace('\n','').split(':')
            person_name = person_friend_group[0].strip()
            person_friends_name_list = [friend.strip() for friend in person_friend_group[1].split(',')]
            person_name_friend_name[person_name] = person_friends_name_list

        for person_name, friends_name in person_name_friend_name.items():
            new_person = get_or_create_person(person_name_person_index, person_name)
            for single_friend_name in friends_name:
                friend = get_or_create_person(person_name_person_index, single_friend_name)
                new_person.add_friend(friend)
            person_list.append(new_person)
    return person_list
