from API_config import API_CONFIG
from models.Example import Example

if __name__ == '__main__':
    CONFIG = API_CONFIG('http://localhost/api')

    example = Example(CONFIG)
    print(example.put(_id=1, mane='test'))
