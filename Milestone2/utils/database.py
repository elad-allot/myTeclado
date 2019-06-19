import csv
import os

MY_LIBRARY = 'books.csv'

def get_all():
    """
    csv file
    first line headers
    :return: list of dict [{name: str, author: str, read: bool},{},{}....] None if empty
    """
    try:
        with open(MY_LIBRARY, 'r') as f:
            return list_to_library(list(csv.reader(f))[1:])
    except FileNotFoundError:
        pass  # return None


def list_to_library(book_list):
    try:
        return [{'name': book[0], 'author': book[1], 'read': book[2]} for book in book_list]
    except IndexError:
        raise IndexError('Incorrect book_list Format')


def append(book):
    """

    :param book: (name, author, read)
    :return: None
    """
    with open(MY_LIBRARY, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'author', 'read'])
        if f.tell() == 0:
            writer.writeheader()
        try:
            writer.writerow({'name': book[0], 'author': book[1], 'read': book[2]})
        except IndexError:
            raise IndexError('Incorrect book Format')


def delete_book(att, att_value):
    """

    :param att: attribute in dict to look by
    :param att_value: value of attribute to compare too
    :return: boolean for is_deleted
    """
    my_library = get_all()
    is_deleted = False
    try:
        os.remove(MY_LIBRARY)
    except (FileExistsError, FileNotFoundError):
        raise FileExistsError
    else:
        for book in my_library:
            try:
                if book[att] != att_value:
                    b = (book['name'], book['author'], book['read'])
                    append(b)
                else:
                    is_deleted = True;
            except KeyError:
                raise KeyError('%s Is not a key' % att)
            finally:
                return is_deleted


def find_book(att, att_value):
    """

    :param att: attribute in dict to look by
    :param att_value: value of attribute to compare too
    :return: None
    """
    my_library = get_all()
    for book in my_library:
        try:
            if book[att] == att_value:
                return book
        except KeyError:
            raise KeyError('%s Is not a key' % att)
    pass


def mark_as_read(book):
    """

    :param book: dict {name: S, auther: S, read S}
    :return: True for update, False else
    """
    if delete_book('name', book['name']):
        append((book['name'], book['author'], True))
        return True
    return False
